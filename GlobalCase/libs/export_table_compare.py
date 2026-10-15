from html.parser import HTMLParser


def _normalize(value):
    # EMS exports may prepend an invisible zero-width character to values such
    # as "null".  Remove formatting characters before applying the existing
    # empty-value equivalence rules.
    value = (value or "").translate(
        str.maketrans("", "", "\u200b\u200c\u200d\ufeff")
    )
    value = " ".join(value.split())
    return "" if value.casefold() in {"", "--", "null"} else value


def _normalize_for_column(header, value):
    value = _normalize(value)
    header_key = "".join(header.casefold().split())
    if header_key in {"slot", "slotid", "port", "portid", "ont", "ontid"} and value in {"", "0"}:
        return ""
    return value


def _is_live_optical_value(header, key):
    column_key = "".join(f"{header} {key}".casefold().split())
    return any(name in column_key for name in ("txpower", "rxpower", "opticalpower"))


def _values_match(header, key, table_value, export_value):
    table_value = _normalize_for_column(header, table_value)
    export_value = _normalize_for_column(header, export_value)
    if table_value == export_value:
        return True
    if not _is_live_optical_value(header, key):
        return False
    try:
        # Optical power can move slightly while the export is being generated.
        return abs(float(table_value) - float(export_value)) <= 0.3
    except (TypeError, ValueError):
        return False


class _ExportParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "tr":
            self.row = []
        elif tag.lower() in {"td", "th"} and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag.lower() in {"td", "th"} and self.cell is not None:
            self.row.append(_normalize("".join(self.cell)))
            self.cell = None
        elif tag.lower() == "tr" and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None


def capture_table_and_export(driver, table_id):
    snapshot = driver.execute_script(
        r"""
        const id = arguments[0];
        const headers = Array.from(document.querySelectorAll(`#${id}_head thead tr th`));
        const excluded = new Set(["Index", "DevID"]);
        const columns = headers.map((header, index) => ({
            index, name: header.innerText.replace(/\s+/g, " ").trim(),
            key: header.getAttribute("name") || ""
        })).filter(column => column.name && !excluded.has(column.name));
        const rows = Array.from(document.querySelectorAll(`#${id}_body tbody tr`)).map(row => {
            const cells = Array.from(row.querySelectorAll(":scope > td"));
            return columns.map(column => {
                const cell = cells[column.index];
                if (column.key === "Severity") {
                    const match = (cell.className || "").match(/td_(critical|major|minor|warning|info)/i);
                    return match ? match[1][0].toUpperCase() + match[1].slice(1).toLowerCase() : cell.innerText;
                }
                if (column.key === "Ack") {
                    const cls = (cell.querySelector("a") || {}).className || "";
                    if (cls.split(/\s+/).includes("ackRead")) return "Acknowledged";
                    if (cls.split(/\s+/).includes("ackNotRead")) return "Not Acknowledged";
                }
                return cell.innerText;
            });
        });
        document.querySelector("#i_action_export > a").click();
        return {headers: columns.map(column => column.name), keys: columns.map(column => column.key), rows};
        """,
        table_id,
    )
    snapshot["headers"] = [_normalize(value) for value in snapshot["headers"]]
    snapshot["rows"] = [tuple(_normalize(value) for value in row) for row in snapshot["rows"]]
    return snapshot


def assert_export_matches(path, snapshot, label):
    # An empty table has no row content that can be compared.  The caller still
    # verifies that the export file was downloaded and is not an empty file.
    if not snapshot.get("rows"):
        return

    parser = _ExportParser()
    with open(path, encoding="utf-8-sig") as export_file:
        parser.feed(export_file.read())
    assert parser.rows, f"No table data found in {path}"
    export_header = parser.rows[0]
    lookup = {header.casefold(): index for index, header in enumerate(export_header)}
    selected = []
    for index, header in enumerate(snapshot["headers"]):
        export_name = "" if snapshot["keys"][index] == "Severity" and "" in export_header else header
        if export_name.casefold() in lookup:
            selected.append((index, lookup[export_name.casefold()]))
    assert selected, f"No comparable columns for {label}. Header: {export_header}"
    table_rows = [tuple(row[left] for left, _ in selected) for row in snapshot["rows"]]
    export_rows = [
        tuple(row[right] for _, right in selected)
        for row in parser.rows[1:]
        if len(row) > max(right for _, right in selected)
    ]
    remaining_export_rows = list(export_rows)
    missing = []
    for table_row in table_rows:
        match_index = next(
            (
                index
                for index, export_row in enumerate(remaining_export_rows)
                if all(
                    _values_match(
                        snapshot["headers"][left],
                        snapshot["keys"][left],
                        table_row[column_index],
                        export_row[column_index],
                    )
                    for column_index, (left, _) in enumerate(selected)
                )
            ),
            None,
        )
        if match_index is None:
            missing.append(
                tuple(
                    _normalize_for_column(snapshot["headers"][left], value)
                    for value, (left, _) in zip(table_row, selected)
                )
            )
        else:
            remaining_export_rows.pop(match_index)
    assert not missing, f"{label} table and export file differ. Missing rows: {missing[:5]}"
