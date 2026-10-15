import io
import os
import struct
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

from PIL import ImageGrab


EMS_DIR = Path(r"D:\Auto\EMS\Pytest\EMSWebICAT")
PYTHON = Path(r"C:\Users\ZT02452\AppData\Local\Programs\Python\Python311\python.exe")
ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
INPUT_TEXT = "192.168.168.85\nProvision.py\n2\n2\n"


def fourcc(value):
    return value.encode("ascii")


class MjpegAviWriter:
    def __init__(self, path, width, height, fps):
        self.path = Path(path)
        self.width = width
        self.height = height
        self.fps = fps
        self.frames = 0
        self.index = []
        self.file = open(self.path, "wb")
        self._write_header()

    def _pack_chunk(self, chunk_id, data):
        self.file.write(fourcc(chunk_id))
        self.file.write(struct.pack("<I", len(data)))
        self.file.write(data)
        if len(data) % 2:
            self.file.write(b"\0")

    def _list(self, list_type, payload):
        return fourcc("LIST") + struct.pack("<I", len(payload) + 4) + fourcc(list_type) + payload

    def _write_header(self):
        avih = struct.pack(
            "<IIIIIIIIII4I",
            int(1_000_000 / self.fps),
            self.width * self.height * 3 * self.fps,
            0,
            0x10,
            0,
            0,
            1,
            self.width * self.height * 3,
            self.width,
            self.height,
            0,
            0,
            0,
            0,
        )

        strh = struct.pack(
            "<4s4sIHHIIIIIIIIHH",
            fourcc("vids"),
            fourcc("MJPG"),
            0,
            0,
            0,
            1,
            self.fps,
            0,
            0,
            self.width * self.height * 3,
            0xFFFFFFFF,
            0,
            self.width * self.height * 3,
            0,
            0,
        )
        strf = struct.pack(
            "<IiiHH4sIiiII",
            40,
            self.width,
            self.height,
            1,
            24,
            fourcc("MJPG"),
            self.width * self.height * 3,
            0,
            0,
            0,
            0,
        )

        hdrl_payload = b""
        hdrl_payload += fourcc("avih") + struct.pack("<I", len(avih)) + avih
        strl_payload = b""
        strl_payload += fourcc("strh") + struct.pack("<I", len(strh)) + strh
        strl_payload += fourcc("strf") + struct.pack("<I", len(strf)) + strf
        hdrl_payload += self._list("strl", strl_payload)
        hdrl = self._list("hdrl", hdrl_payload)

        self.file.write(fourcc("RIFF"))
        self.riff_size_pos = self.file.tell()
        self.file.write(struct.pack("<I", 0))
        self.file.write(fourcc("AVI "))
        self.file.write(hdrl)
        self.file.write(fourcc("LIST"))
        self.movi_size_pos = self.file.tell()
        self.file.write(struct.pack("<I", 0))
        self.file.write(fourcc("movi"))
        self.movi_data_start = self.file.tell()

    def add_frame(self, image):
        frame = image.convert("RGB").resize((self.width, self.height))
        data_io = io.BytesIO()
        frame.save(data_io, format="JPEG", quality=62, optimize=True)
        data = data_io.getvalue()
        offset = self.file.tell() - self.movi_data_start
        self._pack_chunk("00dc", data)
        self.index.append((offset, len(data)))
        self.frames += 1

    def close(self):
        idx_payload = b"".join(
            fourcc("00dc") + struct.pack("<III", 0x10, offset, size)
            for offset, size in self.index
        )
        idx_start = self.file.tell()
        self._pack_chunk("idx1", idx_payload)
        end = self.file.tell()

        self.file.seek(self.riff_size_pos)
        self.file.write(struct.pack("<I", end - 8))
        self.file.seek(self.movi_size_pos)
        self.file.write(struct.pack("<I", idx_start - self.movi_size_pos - 4))
        self.file.seek(0)
        data = self.file.read() if False else None
        self.file.close()


def record_screen(path, stop_event, fps=4, width=1280):
    first = ImageGrab.grab()
    ratio = width / first.width
    height = int(first.height * ratio)
    if height % 2:
        height -= 1
    writer = MjpegAviWriter(path, width, height, fps)
    interval = 1 / fps

    try:
        while not stop_event.is_set():
            started = time.perf_counter()
            writer.add_frame(ImageGrab.grab())
            elapsed = time.perf_counter() - started
            stop_event.wait(max(0, interval - elapsed))
    finally:
        writer.close()


def stream_output(pipe, log_file):
    for line in iter(pipe.readline, ""):
        print(line, end="")
        log_file.write(line)
        log_file.flush()


def main():
    ARTIFACT_DIR.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_path = ARTIFACT_DIR / f"EMSWebICAT_Provision_192.168.168.85_{stamp}.avi"
    log_path = ARTIFACT_DIR / f"EMSWebICAT_Provision_192.168.168.85_{stamp}.log"

    stop_event = threading.Event()
    recorder = threading.Thread(target=record_screen, args=(video_path, stop_event), daemon=True)
    recorder.start()
    time.sleep(1)

    proc = None
    return_code = 1
    with open(log_path, "w", encoding="utf-8", errors="replace") as log_file:
        log_file.write(f"Video: {video_path}\n")
        log_file.write(f"Inputs: 192.168.168.85 | Provision.py | 2 | 2\n\n")
        log_file.flush()
        try:
            proc = subprocess.Popen(
                [str(PYTHON), "RUN.py"],
                cwd=str(EMS_DIR),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            )
            reader = threading.Thread(target=stream_output, args=(proc.stdout, log_file), daemon=True)
            reader.start()
            proc.stdin.write(INPUT_TEXT)
            proc.stdin.flush()
            proc.stdin.close()
            return_code = proc.wait()
            reader.join(timeout=10)
        finally:
            stop_event.set()
            recorder.join(timeout=20)
            if proc and proc.poll() is None:
                proc.terminate()

    print(f"\nRETURN_CODE={return_code}")
    print(f"VIDEO={video_path}")
    print(f"LOG={log_path}")
    return return_code


if __name__ == "__main__":
    sys.exit(main())
