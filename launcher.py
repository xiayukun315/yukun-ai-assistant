"""
屿坤的 AI 助手 —— 极简桌面启动器（不依赖 pywebview）
双击桌面 .vbs 即静默运行本文件：
  1. 确保 Ollama 本地服务在跑（静默，不弹窗）
  2. 后台起 Flask 网站
  3. 自动用默认浏览器打开 http://127.0.0.1:5000
若任何步骤报错，会写到同目录 launcher_error.log 方便排查。
"""
import os
import sys
import time
import subprocess
import threading
import webbrowser

CREATE_NO_WINDOW = 0x08000000  # Windows：启动子进程但不显示窗口
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

OLLAMA_PATHS = [
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama\ollama.exe"),
    r"D:\Ollama\ollama.exe",
    r"C:\Users\XIAYULUN\AppData\Local\Programs\Ollama\ollama.exe",
]


def find_ollama():
    # 先试 PATH
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, timeout=6)
        if r.returncode == 0:
            return None  # 已在跑
    except Exception:
        pass
    # 再试常见安装路径
    for p in OLLAMA_PATHS:
        if os.path.exists(p):
            return p
    return None


def ensure_ollama():
    existing = find_ollama()
    if existing is None:
        # 已在运行
        return
    try:
        if existing:
            subprocess.Popen([existing, "serve"], creationflags=CREATE_NO_WINDOW)
        else:
            subprocess.Popen(["ollama", "serve"], creationflags=CREATE_NO_WINDOW)
    except Exception as e:
        log("未能自动启动 Ollama：" + str(e))
    time.sleep(4)


def run_flask():
    from app import app
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def log(msg):
    try:
        with open(os.path.join(PROJECT_DIR, "launcher_error.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")
    except Exception:
        pass


def open_browser(url):
    # Windows 上最稳：用系统 Shell 打开默认浏览器；失败再退回 webbrowser
    try:
        os.startfile(url)
    except Exception:
        try:
            webbrowser.open(url)
        except Exception as e:
            log("打开浏览器失败：" + str(e))


def main():
    log("启动中…")
    ensure_ollama()
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)
    open_browser("http://127.0.0.1:5000")
    log("已请求打开浏览器，进入保持运行状态。")
    # 保持进程存活（守护线程依赖主线程），直到手动结束
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
