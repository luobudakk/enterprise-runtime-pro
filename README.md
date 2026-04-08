# Enterprise Runtime Pro（企业级 AI 运行时）

`Enterprise Runtime Pro` 是一个面向企业场景的 AI Runtime 原型，核心目标是把「知识问答」「上下文编排」「可控执行」整合到统一工程中，而不是只做聊天界面。

---

## 项目定位

- 企业知识问答（RAG）：支持检索、重排、引用回答
- 结构化会话运行时：`Session / Turn / Command / Job`
- 可控动作执行：`预览 -> 确认 -> 执行`
- 多组件集成：FastAPI + Next.js + Milvus + Feishu + Temporal（可扩展）

---

## 主要功能

### 1) 企业知识问答（RAG）

- 文档上传与入库（txt/docx/pptx/xlsx/pdf）
- 文档解析、切块、向量索引
- 检索 + 重排 + 生成回答
- 输出带引用信息，提升可追溯性

### 2) Ask Runtime（会话编排）

- 意图路由（问答 / 动作 / 技能）
- 多轮上下文管理（工作上下文、会话记忆、待执行草案）
- 命令流转（确认、取消、选择目标等）
- 任务状态跟踪（jobs）

### 3) 可控动作执行

- 对发消息、创建会议等动作先生成预览
- 用户确认后才真正执行
- 降低误发消息、误操作风险

### 4) 企业集成能力

- Feishu（消息、群聊、日程能力）
- Milvus（向量检索）
- MinIO / 本地文件存储（自动回退）
- Temporal（流程编排扩展位）

---

## 技术栈

- 后端：`FastAPI` / `SQLAlchemy` / `pytest`
- 前端：`Next.js` / Node test runner
- 检索与知识：`Milvus` / 文档解析模块
- 工程化：Docker Compose、分层模块化结构

---

## 目录结构

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

### 启动后端

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\backend
py -3.11 -m pip install -r requirements-dev.txt
$env:EMATA_DATABASE_URL="sqlite:///./runtime-dev.db"
py -3.11 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 启动前端

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\frontend
npm install
npm run dev
```

访问地址：

- API：`http://127.0.0.1:8000`
- Ask 页面：`http://127.0.0.1:3000/ask`
- Knowledge 页面：`http://127.0.0.1:3000/knowledge`

---

## 测试

### 后端测试

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\backend
$env:EMATA_DATABASE_URL="sqlite:///./runtime-dev.db"
py -3.11 -m pytest -q
```

### 前端测试

```powershell
cd C:\Users\jinziqi\Desktop\2026\enterprise-runtime-pro\frontend
npm test -- --runInBand
```

---

## 环境变量说明

请参考根目录 `.env.example`。常用项：

- 运行时：`EMATA_API_HOST`、`EMATA_API_PORT`、`EMATA_DATABASE_URL`
- 模型与 RAG：`EMATA_MODEL_*`、`EMATA_RERANK_*`、`EMATA_EMBEDDING_*`
- 知识与存储：`EMATA_STORAGE_BACKEND`、`EMATA_UPLOAD_BASE_DIR`、`EMATA_MILVUS_URI`
- 飞书：`EMATA_FEISHU_APP_ID`、`EMATA_FEISHU_APP_SECRET`
- 兼容别名：`EMATA_LARK_APP_ID`、`EMATA_LARK_APP_SECRET`

---

## 面试演示建议

- 用知识库问题展示有引用回答
- 演示“把刚才结论发送到群聊”的预览与确认
- 解释为什么企业场景必须做可控执行链路
- 展示运行时分层设计（路由、上下文、技能、工具）

---

## 上传前检查

- 不提交真实 `.env`、密钥、凭据文件
- 仅保留 `.env.example` 作为模板
- 保证测试通过后再推送
- 可补充 `images/demo` 截图增强展示效果

---

## License

当前仓库未附带开源许可证。若计划公开开源，建议补充 `LICENSE` 文件。
