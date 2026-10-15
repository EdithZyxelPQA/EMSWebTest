"""Sequential reruns; update only passed sections and stop after two failed attempts."""
from pathlib import Path
from datetime import datetime
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'Output/Web_EMS_OLT1408A-C_03.00.11 (AAVV.221) b12_2026-09-14 1729_.84.txt'


def update_report(case, log):
    result = log.read_text(encoding='utf-8')
    if 'Runner: COMPLETED' not in result or re.search(r'\b(fail|failed|error|exception)\b', result, re.I):
        raise ValueError('Refusing to replace report with unsuccessful rerun')
    text = REPORT.read_text(encoding='utf-8')
    failure = re.search(r'^' + re.escape(case) + r' failed after .*$', text, re.M)
    if failure is None:
        raise ValueError('Original failure section not found')
    header = re.search(r'^(.+ Test Start)\s*$', result, re.M).group(1).strip()
    start = text.index(header)
    end_line = text.find('\n', failure.end())
    # Keep surrounding historical timing and subsequent sections unchanged.
    end = len(text) if end_line < 0 else end_line + 1
    replacement = f'[PASS RERUN {datetime.now().isoformat(timespec="seconds")}; source: {log.name}]\n' + result + '\n'
    updated = text[:start] + replacement + text[end:]
    assert case + ' failed after' not in updated
    temp = REPORT.with_suffix('.tmp')
    temp.write_text(updated, encoding='utf-8')
    temp.replace(REPORT)


def main():
    text = REPORT.read_text(encoding='utf-8')
    pending = re.findall(r'^(\w+) failed after 2 attempts\. Skipping\.\.\.', text, re.M)
    shutil.copy2(REPORT, str(REPORT) + '.before_batch_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.bak')
    print('Pending: ' + ', '.join(pending), flush=True)
    for case in pending:
        for attempt in (1, 2):
            print(f'START {case} attempt {attempt}/2', flush=True)
            before = set((ROOT / 'Output').glob(f'{case}_rerun_*.txt'))
            proc = subprocess.run([sys.executable, str(ROOT / 'run_basic_ip.py'), '--case', case], cwd=ROOT)
            new = set((ROOT / 'Output').glob(f'{case}_rerun_*.txt')) - before
            if proc.returncode == 0 and len(new) == 1:
                log = new.pop()
                update_report(case, log)
                print(f'PASS UPDATED {case}: {log.name}', flush=True)
                break
            print(f'FAILED {case} attempt {attempt}/2', flush=True)
        else:
            print(f'STOP: {case} failed twice. Remaining cases not run; report failure retained.', flush=True)
            return 1
    print('ALL REMAINING CASES PASSED AND UPDATED', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
