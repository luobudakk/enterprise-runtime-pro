# Enterprise Runtime Pro（企业级 AI 运行时）

`Enterprise Runtime Pro` 是一个面向企业场景的 AI Runtime 项目，聚焦三件事：

- 企业知识问答（RAG）要“有依据、可追溯”
- AI 动作执行要“可控、可确认”
- 对话系统要“可扩展、可工程化”

---

## 项目简介

这是一个企业级 AI 系统原型：  
基于 `FastAPI + Next.js`，实现从知识入库、检索问答到动作预览确认执行的完整闭环，强调真实工程落地而非单纯聊天 Demo。

---

## 业务价值

- **降低知识查找成本**：员工可直接用自然语言询问制度/流程，系统返回带引用答案
- **减少误操作风险**：消息发送、会议创建等动作必须先预览再确认
- **提升系统可维护性**：通过 Runtime 分层管理上下文、技能、工具和策略

---

## 主要能力

### 1) 企业知识问答（RAG）

- 支持文件上传：`txt / docx / pptx / xlsx / pdf`
- 支持文档解析、切块、向量检索、重排、生成回答
- 回答支持引用信息（citation），增强可信度

### 2) Ask Runtime 编排

- 会话实体化：`Session / Turn / Command / Job`
- 意图路由：问答 / 动作 / 技能
- 上下文管理：工作上下文、会话记忆、待执行草案

### 3) 可控动作执行

- 执行链路：`预览 -> 确认 -> 执行`
- 适用于发消息、建会议等有风险动作
- 防止错误目标、错误正文被直接执行

### 4) 集成与扩展

- 飞书能力（消息、群聊、日程）
- Milvus 向量检索
- MinIO / 本地存储（不可达时自动回退）
- Temporal 工作流扩展位

---

## 核心实现

- 设计并实现 Ask Runtime 主链路（路由、上下文、命令、任务状态）
- 打通 RAG 全流程（上传、解析、切块、检索、重排、回答）
- 实现动作可控执行模型（预览确认机制）
- 修复跨平台与依赖问题（Windows 环境、存储回退、解析异常处理）
- 完成后端与前端测试闭环，保障可回归

---

## 技术栈

- 后端：`FastAPI`、`SQLAlchemy`、`pytest`
- 前端：`Next.js`、Node test runner
- 知识检索：`Milvus`
- 工程化：`Docker Compose`、模块化分层架构

---

## 项目结构

```text
enterprise-runtime-pro/
├─ backend/
│  ├─ app/
│  ├─ tests/
│  ├─ requirements.txt
│  ├─ requirements-optional.txt
│  └─ requirements-dev.txt
├─ frontend/
│  ├─ app/
│  ├─ components/
│  ├─ lib/
│  └─ tests/
├─ infra/
├─ scripts/
├─ images/demo/
├─ docker-compose.yml
└─ .env.example
```

---

## 本地运行（Windows）

### 后端

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\backend
py -3.11 -m pip install -r requirements-dev.txt
$env:EMATA_DATABASE_URL="sqlite:///./runtime-dev.db"
py -3.11 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 前端

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\frontend
npm install
npm run dev
```

访问地址：

- API：`http://127.0.0.1:8000`
- Ask：`http://127.0.0.1:3000/ask`
- Knowledge：`http://127.0.0.1:3000/knowledge`

---

## 测试

### 后端

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\backend
$env:EMATA_DATABASE_URL="sqlite:///./runtime-dev.db"
py -3.11 -m pytest -q
```

### 前端

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\frontend
npm test -- --runInBand
```

---

## 环境变量

详细配置见 `.env.example`，常用项：

- 运行时：`EMATA_API_HOST`、`EMATA_API_PORT`、`EMATA_DATABASE_URL`
- 模型/RAG：`EMATA_MODEL_*`、`EMATA_RERANK_*`、`EMATA_EMBEDDING_*`
- 存储/检索：`EMATA_STORAGE_BACKEND`、`EMATA_UPLOAD_BASE_DIR`、`EMATA_MILVUS_URI`
- 飞书：`EMATA_FEISHU_APP_ID`、`EMATA_FEISHU_APP_SECRET`

---

## License

当前仓库未附带开源许可证。
