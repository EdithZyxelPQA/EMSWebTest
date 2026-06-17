import os
import sys


def split_report(src: str):
    out_dir = os.path.dirname(os.path.abspath(src))

    with open(src, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    print(f"Total lines: {total}")

    # Detect section boundaries
    system_end = None
    card_sections = {}  # {card_name: (start_line_idx, end_line_idx)}
    card_order = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('No Card Test') and 'Total time' in stripped:
            system_end = i + 1  # include this line
        if '>>>>' in stripped and '[' in stripped and ']' in stripped:
            card_name = stripped.split('[')[-1].split(']')[0].strip()
            card_order.append((card_name, i))

    # Assign end indices for each card section
    card_sections_list = []
    for idx, (card_name, start) in enumerate(card_order):
        end = card_order[idx + 1][1] if idx + 1 < len(card_order) else total
        card_sections_list.append((card_name, start, end))

    # Determine system end: up to (and including) "Card Test" separator
    # find the line index of "Card Test" header (just before first card)
    if card_sections_list:
        first_card_start = card_sections_list[0][1]
        # include lines from system_end up to first card start as part of system
        system_end_final = first_card_start
    else:
        system_end_final = system_end or total

    header = lines[0:18]
    base = os.path.splitext(os.path.basename(src))[0]

    # Write System file
    system_path = os.path.join(out_dir, f"{base}_System.log")
    with open(system_path, 'w', encoding='utf-8') as f:
        f.writelines(lines[0:system_end_final])
    print(f"Written: {os.path.basename(system_path)} ({system_end_final} lines)")

    # Write per-card files
    name_count = {}
    for card_name, start, end in card_sections_list:
        short = card_name[:3]
        name_count[short] = name_count.get(short, 0) + 1
        suffix = short if name_count[short] == 1 else f"{short}_{name_count[short]}"
        card_path = os.path.join(out_dir, f"{base}_{suffix}.log")
        content = header + lines[start:end]
        with open(card_path, 'w', encoding='utf-8') as f:
            f.writelines(content)
        print(f"Written: {os.path.basename(card_path)} ({len(content)} lines)")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_report(sys.argv[1])
    else:
        # default: same directory as this script, ask user to pass filename
        print("Usage: python split_report.py <report.log>")
        print("Example:")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        for f in os.listdir(script_dir):
            if f.endswith('.log') and '_System' not in f and '_NX' not in f:
                print(f"  python split_report.py \"{os.path.join(script_dir, f)}\"")
