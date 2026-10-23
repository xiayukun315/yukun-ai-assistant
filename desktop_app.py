"""
屿坤的 AI 助手 —— 桌面端启动程序
用 pywebview 把现有网站（课表/番茄钟/打卡/个性化千问）套进原生桌面窗口。
双击「启动屿坤AI助手.bat」即调用本文件。

做了什么：
  1. 静默启动 Ollama 本地服务（不弹黑窗）
  2. 后台起 Flask 网站
  3. 用原生窗口打开 http://127.0.0.1:5000（不是浏览器标签页）
若 pywebview 不可用，自动回退为用浏览器打开。
"""
import subprocess
import sys
import time
import threading

CREATE_NO_WINDOW = 0x08000000  # Windows：启动子进程但不显示窗口


def ensure_ollama():
    """确保本地 Ollama 服务在跑（静默启动，不弹窗）。"""
    try:
        r = subprocess.run(["ollama", "list"], capture_output=True, timeout=6)
        if r.returncode == 0:
            return
    except Exception:
        pass
    try:
        subprocess.Popen(["ollama", "serve"], creationflags=CREATE_NO_WINDOW)
    except Exception as e:
        print("未能自动启动 Ollama：", e, "（若聊天失败，请先手动打开 Ollama 桌面端）")
    time.sleep(4)


def run_flask():
    # 延迟导入，避免启动 Ollama 之前就加载 Flask
    from app import app
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def main():
    ensure_ollama()
    # 后台线程跑网站
    threading.Thread(target=run_flask, daemon=True).start()
    time.sleep(2)

    try:
        import webview
        webview.create_window(
            "屿坤的 AI 助手",
            "http://127.0.0.1:5000",
            width=1000,
            height=740,
            text_select=True,
        )
        webview.start()
    except Exception as e:
        print("pywebview 不可用，回退到浏览器：", e)
        import webbrowser
        webbrowser.open("http://127.0.0.1:5000")
        # 浏览器模式下保持进程存活，否则网站线程会随程序退出
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
