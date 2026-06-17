from __future__ import annotations

import html
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


def _case_status(case):
    failure = case.find("failure")
    error = case.find("error")
    skipped = case.find("skipped")
    if failure is not None:
        return "failed", failure.get("message", "failure")
    if error is not None:
        return "error", error.get("message", "error")
    if skipped is not None:
        return "skipped", skipped.get("message", "skipped")
    return "passed", ""


def parse_junit(path: Path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    rows = []
    for suite in suites:
        for case in suite.findall("testcase"):
            status, message = _case_status(case)
            rows.append(
                {
                    "classname": case.get("classname", ""),
                    "name": case.get("name", ""),
                    "time": float(case.get("time", "0") or 0),
                    "status": status,
                    "message": message,
                }
            )
    return rows


def build_markdown(rows):
    total = len(rows)
    counts = {status: sum(1 for row in rows if row["status"] == status) for status in ["passed", "failed", "error", "skipped"]}
    lines = [
        "# EMS Site Assessment Report",
        "",
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"- Total: {total}",
        f"- Passed: {counts['passed']}",
        f"- Failed: {counts['failed']}",
        f"- Errors: {counts['error']}",
        f"- Skipped: {counts['skipped']}",
        "",
        "## Results",
        "",
        "| Status | Test | Time (s) | Message |",
        "| --- | --- | ---: | --- |",
    ]
    for row in rows:
        test_name = f"{row['classname']}::{row['name']}"
        message = row["message"].replace("\n", " ")[:300]
        lines.append(f"| {row['status']} | `{test_name}` | {row['time']:.2f} | {message} |")
    lines.append("")
    return "\n".join(lines)


def build_html(markdown_text):
    escaped = html.escape(markdown_text)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>EMS Site Assessment Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; }}
    pre {{ white-space: pre-wrap; background: #f6f8fa; padding: 16px; border-radius: 6px; }}
  </style>
</head>
<body>
  <pre>{escaped}</pre>
</body>
</html>
"""


def main(argv):
    if len(argv) != 4:
        print("Usage: generate_report.py <junit.xml> <report.md> <report.html>")
        return 2

    junit_path = Path(argv[1])
    markdown_path = Path(argv[2])
    html_path = Path(argv[3])
    rows = parse_junit(junit_path)
    markdown_text = build_markdown(rows)
    markdown_path.write_text(markdown_text, encoding="utf-8")
    html_path.write_text(build_html(markdown_text), encoding="utf-8")
    print(f"Wrote {markdown_path}")
    print(f"Wrote {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

