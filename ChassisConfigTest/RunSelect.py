import tkinter as tk
from tkinter import messagebox
import os
import json
import subprocess

PYTHON_SCRIPT_DIR = "."#/scripts"
SAVE_FILE = "selected_files.json"

class ScriptSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 執行器")
        self.window_width = 600
        self.window_height = 500
        self.center_window()

        self.running_processes = []
        self.check_vars = {}
        self.script_paths = self.get_python_files()
        self.load_selected()

        frame = tk.Frame(root)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        label = tk.Label(frame, text="請選擇要執行的 Python 檔案：", font=("Arial", 12, "bold"))
        label.pack(anchor="w")

        for script in self.script_paths:
            var = tk.BooleanVar(value=script in self.selected)
            cb = tk.Checkbutton(frame, text=script, variable=var, font=("Arial", 11))
            cb.pack(anchor="w")
            self.check_vars[script] = var

        self.parallel_var = tk.BooleanVar(value=False)
        tk.Checkbutton(frame, text="同時執行（非同步）", variable=self.parallel_var, font=("Arial", 11)).pack(anchor="w", pady=10)

        tk.Button(frame, text="執行選取的 Script", command=self.run_selected, font=("Arial", 11)).pack(pady=5)
        tk.Button(frame, text="停止執行", command=self.stop_execution, font=("Arial", 11)).pack(pady=5)
        tk.Button(frame, text="儲存選取", command=self.save_selected, font=("Arial", 11)).pack()

    def center_window(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - self.window_width) // 2
        y = (sh - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def get_python_files(self):
        # return [f for f in os.listdir(PYTHON_SCRIPT_DIR) if f.endswith(".py")]
        return [f for f in os.listdir(PYTHON_SCRIPT_DIR) if f.startswith("Run_") and f.endswith(".py")]

    def load_selected(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                self.selected = json.load(f)
        else:
            self.selected = []

    def save_selected(self):
        selected = [script for script, var in self.check_vars.items() if var.get()]
        with open(SAVE_FILE, "w") as f:
            json.dump(selected, f, indent=2)
        messagebox.showinfo("完成", "已儲存選取檔案。")

    def run_selected(self):
        selected = [script for script, var in self.check_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("沒有選取", "請至少選取一個檔案")
            return

        self.running_processes.clear()

        if self.parallel_var.get():
            for script in selected:
                script_path = os.path.join(PYTHON_SCRIPT_DIR, script)
                try:
                    proc = subprocess.Popen(["python", script_path])
                    self.running_processes.append(proc)
                except Exception as e:
                    messagebox.showerror("錯誤", f"{script} 執行失敗：\n{e}")
        else:
            try:
                for script in selected:
                    script_path = os.path.join(PYTHON_SCRIPT_DIR, script)
                    proc = subprocess.Popen(["python", script_path])
                    self.running_processes.append(proc)
                    proc.wait()
            except Exception as e:
                messagebox.showerror("錯誤", f"{script} 執行失敗：\n{e}")

    def stop_execution(self):
        if not self.running_processes:
            messagebox.showinfo("沒有進行中程式", "目前沒有執行中的 Python 腳本")
            return

        for proc in self.running_processes:
            if proc.poll() is None:  # 如果還在跑
                try:
                    proc.terminate()
                except Exception as e:
                    print(f"無法終止 process: {e}")

        self.running_processes.clear()
        messagebox.showinfo("已停止", "已嘗試停止所有正在執行的腳本")

if __name__ == "__main__":
    os.makedirs(PYTHON_SCRIPT_DIR, exist_ok=True)
    root = tk.Tk()
    app = ScriptSelectorApp(root)
    root.mainloop()
