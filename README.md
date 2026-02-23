# Printable Doc Studio（前后端一体示例）

一个使用 **Python + FastAPI** 的网站原型，支持将文字和图片组合成可打印文档，并提供即时预览：

- 支持纸张尺寸：A4 / A5
- 支持背景预设：纯白 / 米白 / 网格 / 横线
- 支持视觉风格：简洁 / 商务 / 柔和
- 支持浏览器打印（`window.print()`）

## 启动方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

打开：`http://localhost:8000`

## 项目结构

```text
app/
  main.py            # FastAPI 后端
  templates/
    index.html       # 前端页面模板
  static/
    style.css        # 样式
    app.js           # 交互逻辑与即时预览
```
