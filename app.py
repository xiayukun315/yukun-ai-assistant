"""
屿坤的个人效率小网站 —— 后端
技术栈：Flask（Web 服务） + Ollama（本地大模型）
功能：① 课表展示  ② 番茄钟  ③ 本地 LLM 答疑

运行前准备：
  1. 装好 Ollama（官网下载），终端执行  ollama pull qwen2.5:7b  拉取模型
  2. 安装依赖：  pip install -r requirements.txt
启动：  python app.py   →   浏览器打开 http://127.0.0.1:5000
说明：本地优先、零 API 成本；Ollama 没启动或没拉模型时，前端会友好提示。
"""
from flask import Flask, send_from_directory, request, Response, jsonify
import ollama
import json

app = Flask(__name__)

# 你本地的 Ollama 模型名；没拉模型会报错，前端会捕获并提示
MODEL_NAME = "qwen2.5:7b"

# ===== 屿坤的个人背景（喂给千问的系统提示，让它"认识你"）=====
# 内容来自知识库 knowledge_base.md 的【个人背景】条目，改这里即可更新。
SYSTEM_PROMPT = """你是屿坤的私人本地 AI 助手，运行在他的电脑上（本地大模型，不联网）。
关于屿坤，你需要记住这些背景，回答和给建议时主动贴合：
- 身份：计算机专业大二学生，网名/AI 名叫"浮熙"，由他命名。
- 目标：直接就业冲实习（AI 应用 / Agent 开发方向），考研暂缓不作为主线；想把 Java、Python、C 语言基本掌握，并学 AI 知识。
- 硬件：机械革命翼龙15，R7 8745H + RTX 4050，32GB 内存，本地优先跑模型（省钱）。
- 时间：工作日约 3h/天、周末约 7h/天可自学；高效时段是晚上+碎片时间；一般约 24:00 睡。
- 痛点：学习过程容易拖延（卡在刷手机/懒得动），需要外部监督/打卡才容易坚持——所以给他的计划要小步、可见反馈、带打卡机制。
- 学业：这学期在学 Java程序设计、数据结构A、线性代数、大学物理A2、大学英语III、体育专选I、形势与政策III；Java 和 数据结构A 之前没认真学，需要补；本学期考大学英语四级，要复习。
- 其他：solo 学习，暂无队友/社群；GitHub 有账号；漫剧暂不做（本地 ComfyUI 效果一般）；业余在写一部长篇修仙小说《铳灵：从一把灵能手枪开始》。
- 协作风格：交流偏简洁，直接给选项或结果比长篇解释更合适。
请像一个了解他情况的学长/搭子在回答，少说教，多给能立刻动手的具体步骤。"""


@app.route("/")
def index():
    # 返回同目录下的前端页面
    return send_from_directory(".", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    if not user_msg:
        return jsonify({"error": "消息为空"}), 400

    def generate():
        try:
            # 调用本地 Ollama，逐字流式返回（stream=True）
            stream = ollama.chat(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                stream=True,
            )
            for chunk in stream:
                token = chunk["message"]["content"]
                # 用 SSE 格式推给前端，前端边收边显示
                yield f"data: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    # 仅本机访问；若要部署到云学生机，把 host 改成 "0.0.0.0"
    app.run(host="127.0.0.1", port=5000, debug=True)
