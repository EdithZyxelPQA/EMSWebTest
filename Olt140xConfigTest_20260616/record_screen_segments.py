import argparse
import time
from datetime import datetime
from pathlib import Path

from PIL import ImageGrab

from run_emswebicat_with_recording import MjpegAviWriter


def record_segment(path, seconds, fps, width, stop_file):
    first = ImageGrab.grab()
    ratio = width / first.width
    height = int(first.height * ratio)
    if height % 2:
        height -= 1

    writer = MjpegAviWriter(path, width, height, fps)
    interval = 1 / fps
    end_at = time.monotonic() + seconds
    try:
        while time.monotonic() < end_at and not stop_file.exists():
            started = time.perf_counter()
            writer.add_frame(ImageGrab.grab())
            elapsed = time.perf_counter() - started
            time.sleep(max(0, interval - elapsed))
    finally:
        writer.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--prefix", default="EMSWebICAT_Provision_192.168.168.85")
    parser.add_argument("--segment-minutes", type=float, default=10)
    parser.add_argument("--fps", type=int, default=1)
    parser.add_argument("--width", type=int, default=960)
    parser.add_argument("--stop-file", required=True)
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(exist_ok=True)
    stop_file = Path(args.stop_file)
    segment_seconds = max(10, int(args.segment_minutes * 60))

    log_path = out_dir / f"{args.prefix}_segments.log"
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"\nStarted segmented recording at {datetime.now()}\n")
        log.write(f"fps={args.fps}, width={args.width}, segment_seconds={segment_seconds}\n")
        log.flush()

        index = 1
        while not stop_file.exists():
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = out_dir / f"{args.prefix}_segment_{index:03d}_{stamp}.avi"
            log.write(f"START {path}\n")
            log.flush()
            record_segment(path, segment_seconds, args.fps, args.width, stop_file)
            log.write(f"END {path}\n")
            log.flush()
            index += 1

        log.write(f"Stopped segmented recording at {datetime.now()}\n")


if __name__ == "__main__":
    main()
