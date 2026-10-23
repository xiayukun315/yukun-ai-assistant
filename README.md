# 屿坤的效率小站（Project A · v1）

> 第一项目 Demo（替代原漫剧方向）。个人效率小网站：课表 + 番茄钟 + 本地 AI 答疑。
> 技术栈：前端纯 HTML/JS，后端 Flask 代理本地 Ollama。零 API 成本、本地优先、立刻能跑。

## 功能
1. **课表**：把你这学期课表录入展示（数据在 `index.html` 的 `schedule` 变量，可自行改）。
2. **番茄钟**：25 分钟专注计时，完成才"奖励刷手机"——正好对应你"需外部监督/刷手机当奖励"的节奏。
3. **本地 AI 答疑**：调本地 `qwen2.5:7b`，流式输出，问学习规划、知识点都行。

## 本地运行（你自己的电脑）

### 方式一：一键脚本（推荐，适合新手）
直接**双击 `setup.bat`**，它会自动：检测/安装 Ollama → 拉 qwen2.5:7b 模型 → 建 venv 装依赖 → 启动网站。
全程需要联网（模型约 4.7GB）。装好后在浏览器开 `http://127.0.0.1:5000`。
> 脚本提示为英文，避免 Windows 批处理中文乱码；每步含义见下方"方式二"人工步骤。
> **磁盘位置**：Ollama 程序默认装到 `D:\Ollama`，模型（4.7GB）存到 `D:\OllamaModels`，不占 C 盘系统盘。若 D 盘不存在会自动回退到 C 盘默认位置。

### 方式二：手动命令
```bash
# 1. 装 Ollama 并拉模型（只需一次）
ollama pull qwen2.5:7b

# 2. 装依赖
pip install -r requirements.txt

# 3. 启动
python app.py

# 4. 浏览器打开
#    http://127.0.0.1:5000
```
> 若答疑报错"连接失败"，先确认 Ollama 在跑（终端 `ollama list` 能看到 qwen2.5:7b）。

## 部署到云学生机（可选，阶段3用）
1. 领腾讯云/阿里云学生机（~10 元/月），装好 Python。
2. 把整个文件夹传上去，`pip install -r requirements.txt`。
3. 把 `app.py` 里的 `host="127.0.0.1"` 改成 `host="0.0.0.0"`。
4. 用 `nohup python app.py &` 后台跑，或用 `gunicorn` 跑稳一点。
5. 浏览器用 `http://学生机公网IP:5000` 访问。
> 注意：学生机上也要装 Ollama 并拉模型；若学生机没显卡，7B 用 CPU 也能跑但较慢，可换更小模型如 `qwen2.5:3b`。

## 下一步可加（学习路线阶段1~2）
- 用 n8n 把"每日课表提醒"自动化（对应 Agent 方向"自动化工作流"）。
- 把站点做成作品集首页，放 GitHub Pages（练"想做网站"+ 实习敲门砖）。

## 桌面启动（推荐：bat + pythonw 静默版）
- 桌面用 `启动屿坤AI助手.bat`：双击即调用 `.venv\Scripts\pythonw.exe launcher.py`，**无控制台窗口**，Ollama/Flask 后台跑，浏览器自动弹出网站。（注：vbs 版在其机器上关联异常无法运行，已弃用，统一用 bat。）
- `launcher.py`：不依赖 pywebview；`ensure_ollama` 先查 PATH 再查常见安装路径（`%LOCALAPPDATA%\Programs\Ollama`、`D:\Ollama`），找不到则静默 `ollama serve`；报错写入 `launcher_error.log`。
- **若双击仍无反应**：看项目目录 `launcher_error.log`；或手动 `cd project && .venv\Scripts\python launcher.py` 在 cmd 里跑看报错。

## 桌面窗口版（原生窗口，可选）
- `desktop_app.py`：用 pywebview 套原生窗口，**需 Windows WebView2 运行时**，缺失时自动回退浏览器。

## 个性化：屿坤的私人 AI 助手（v3）
- 后端 `app.py` 新增 `SYSTEM_PROMPT`：把屿坤的个人背景（计算机大二、冲 AI 实习、拖延需监督、课表、四级等）注入 AI 答疑的 system 消息，模型"认识你"后再回答。
- 桌面一键启动器：`启动屿坤AI助手.bat`（自动起 Ollama + 开浏览器 + 起网站），已复制到桌面，双击即用。

## 已落地：专注打卡（v2）
- 番茄钟完整跑完 25 分钟 → 自动记一次打卡（localStorage 存储，刷新不丢）。
- 新增「手动打卡」按钮：用别的方式学了也能记。
- 底部 canvas 柱状图展示**本周一到周日专注分钟数** + 今日/本周累计 + 本周次数。
- 纯前端实现，改完刷新页面即生效（Flask debug 模式实时读盘）。

## 模型挪到 D 盘（释放 C 盘，可选）
若你手动装的 Ollama，模型默认在 `C:\Users\XIAYULUN\.ollama\models`（约 4.7GB）。想挪到 D：
```bash
# 1. 先彻底退出 Ollama（右下角托盘退出，或任务管理器结束 Ollama 进程）
# 2. 设置持久环境变量
setx OLLAMA_MODELS "D:\OllamaModels"
# 3. 移动模型目录
move C:\Users\XIAYULUN\.ollama\models D:\OllamaModels
# 4. 重新打开 Ollama，验证
ollama list
```

