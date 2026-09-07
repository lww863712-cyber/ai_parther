`markdown
# 智能机器人（AI Partner）项目说明文档

## 一、项目概述

**项目名称：** PythonProject3（AI Partner / 智能机器人）
**作者：** lww863712-cyber
**Python 版本：** >= 3.13
**构建工具：** uv (uv_build)
**远程仓库：** https://github.com/lww863712-cyber/ai_parther.git

这是一个基于 Streamlit + DeepSeek 大模型 API 构建的 AI 聊天伴侣 Web 应用，项目以学习教程的形式组织，从基础入门逐步演进到一个功能完整的 AI 聊天机器人。

## 二、项目结构

    PythonProject3/
    ├── .env                          # 环境变量（存储 DEEPSEEK_API_KEY）
    ├── pyproject.toml                # 项目配置与依赖管理
    ├── src/pythonproject3/           # 标准包目录（目前为空）
    └── 第三章/                        # 核心代码目录
        ├── resual/                   # 资源文件目录
        │   ├── 2025.3.16.jpg         # 图片资源
        │   └── user.json             # JSON 示例数据
        ├── session/                  # 会话持久化存储目录
        │   ├── 2026-09-04_15-14-43.json
        │   └── 2026-09-04_17-41-38.json
        ├── 02json入门.py              # JSON 读写入门示例
        ├── 02streamlit入门.py         # Streamlit UI 入门示例
        ├── deepSeek.py               # DeepSeek API 基础调用示例
        ├── 03.ai_parther.1.py        # AI 聊天机器人 V1（流式输出）
        ├── 04.ai_parther.2.py        # AI 聊天机器人 V2（非流式输出）
        ├── 05.ai_parther.3.py        # AI 聊天机器人 V3（+侧边栏角色定制）
        └── 06.ai_parther.4.py        # AI 聊天机器人 V4（+会话管理/持久化）【最终版】

## 三、各文件功能说明

### 3.1 基础入门模块

| 文件 | 功能 |
|------|------|
| 02json入门.py | 演示 Python JSON 基础操作：将字典（中文姓名、年龄、爱好）写入 user.json，再读取打印，学习 json.dump() 和 ensure_ascii=False |
| 02streamlit入门.py | Streamlit UI 入门：演示 st.title、st.header、st.subheader、st.write、st.image 等基本组件 |
| deepSeek.py | DeepSeek API 基础调用：使用 OpenAI SDK 连接 DeepSeek，配置系统提示词，发起单次对话请求，开启深度思考模式 |

### 3.2 AI Partner 迭代演进

| 版本 | 文件 | 新增特性 |
|------|------|----------|
| V1 | 03.ai_parther.1.py | 基础聊天界面 + 流式输出（stream=True），逐字显示 AI 回复，支持上下文多轮对话 |
| V2 | 04.ai_parther.2.py | 改为非流式输出（stream=False），等待完整回复后一次性显示 |
| V3 | 05.ai_parther.3.py | 新增侧边栏控制面板：可自定义 AI 昵称和性格；系统提示词升级为"陪伴知心大姐姐"角色模板 |
| V4（最终版） | 06.ai_parther.4.py | 新增完整会话管理系统：新建/保存/加载/删除会话；代码重构，抽取工具函数，增加异常处理 |

## 四、技术栈

| 技术 | 版本/来源 | 用途 |
|------|-----------|------|
| Python | >= 3.13 | 开发语言 |
| Streamlit | 第三方库 | Web UI 框架 |
| OpenAI SDK | 第三方库 | 调用 DeepSeek API（兼容 OpenAI 接口协议） |
| DeepSeek API | 远程服务 | AI 大语言模型推理服务 |
| python-dotenv | 第三方库 | 从 .env 文件加载环境变量 |
| JSON | Python 内置 | 会话数据持久化存储 |
| uv | 构建工具 | 项目构建与依赖管理 |

## 五、系统架构

    用户浏览器
        ↓
    Streamlit Web UI（页面配置 / 标题 / 历史消息 / 侧边栏 / 聊天输入框）
        ↓
    session_state 状态管理（messages / nick_name / nature / current_session）
        ↓
    OpenAI SDK Client ← .env（DEEPSEEK_API_KEY）
        ↓
    DeepSeek API 服务（模型: deepseek-chat，流式输出: stream=True）
        ↓
    session/ JSON 持久化存储

## 六、模块划分

    06.ai_parther.4.py
    ├── 工具函数层
    │   ├── generate_session_name()    # 生成会话名称（时间戳）
    │   ├── save_session()             # 保存会话到 JSON 文件
    │   ├── load_sessions()            # 获取所有会话列表
    │   └── load_session(name)         # 加载指定会话到 session_state
    ├── 配置初始化层
    │   ├── 页面配置 (set_page_config)
    │   ├── 环境变量加载 (dotenv)
    │   ├── session_state 初始化
    │   └── OpenAI 客户端创建
    ├── UI 展示层
    │   ├── 标题与当前会话名称显示
    │   ├── 历史消息渲染
    │   ├── 侧边栏（AI控制面板 + 陪伴信息）
    │   └── 聊天输入框
    └── 业务逻辑层
        ├── 新建会话流程
        ├── 加载/删除历史会话
        ├── 调用 DeepSeek API（流式）
        └── 消息追加与状态更新

## 七、功能详细说明

### 7.1 页面配置

| 参数 | 值 | 说明 |
|------|----|------|
| page_title | "智能机器人" | 浏览器标签页标题 |
| page_icon | 🤖 | 浏览器标签页图标 |
| layout | "wide" | 宽屏布局 |
| initial_sidebar_state | "expanded" | 侧边栏默认展开 |

### 7.2 AI 角色定制

| 配置项 | 状态键 | 默认值 | 说明 |
|--------|--------|--------|------|
| 昵称 | nick_name | "空" | AI 的名字，注入到系统提示词 |
| 性格 | nature | "活泼开朗的南方姑娘" | AI 的性格描述，注入到系统提示词 |

### 7.3 系统提示词模板

使用 %s 占位符，运行时动态注入昵称和性格，定义"陪伴知心大姐姐"角色，要求完全带入角色、使用中文回答。

### 7.4 多轮对话

使用 session_state.messages 列表存储完整对话历史，每次调用 API 时将系统提示词和全部历史消息一并发送，实现上下文关联。

消息发送顺序：system提示词 → user → assistant → user → assistant → ...

### 7.5 流式输出

调用 API 时 stream=True，逐 chunk 拼接内容，通过 st.empty() 占位容器实时更新显示，实现逐字输出效果。

### 7.6 会话管理

| 操作 | 触发方式 | 说明 |
|------|----------|------|
| 新建会话 | 点击「🚀 新建会话」 | 保存当前 → 清空消息 → 新时间戳 → 刷新 |
| 加载会话 | 点击会话名称按钮 | 读取 JSON → 恢复状态 → 刷新 |
| 删除会话 | 点击 ❌ 按钮 | 删除 JSON → 刷新 |

会话命名格式：YYYY-MM-DD_HH-MM-SS（避免冒号，确保可用作文件名）

会话 JSON 结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| current_session | str | 会话唯一标识（时间戳） |
| messages | list[dict] | 完整对话消息列表 |
| nick_name | str | AI 昵称 |
| nature | str | AI 性格描述 |

## 八、状态管理

| 键名 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| messages | list[dict] | [] | 当前对话的完整消息列表 |
| nick_name | str | "空" | AI 角色昵称 |
| nature | str | "活泼开朗的南方姑娘" | AI 角色性格描述 |
| current_session | str | 当前时间戳 | 当前会话的唯一标识 |

## 九、API 调用配置

| 参数 | 值 | 说明 |
|------|----|------|
| model | "deepseek-chat" | 模型名称 |
| messages | 系统提示词 + 全部历史消息 | 完整对话上下文 |
| stream | True | 启用流式输出 |
| api_key | 来自 .env 的 DEEPSEEK_API_KEY | 认证密钥 |
| base_url | https://api.deepseek.com | API 服务地址 |

## 十、核心业务流程

### 10.1 启动流程

启动应用 → 加载 .env → 页面配置 → 判断 session_state 是否已初始化 → 未初始化则初始化（messages / nick_name / nature / current_session）→ 渲染标题 + 历史消息 → 创建 OpenAI 客户端 → 渲染侧边栏 → 等待用户输入

### 10.2 消息发送流程

用户输入 → 显示消息 + 追加到 messages → 组装系统提示词（注入昵称+性格）→ 调用 DeepSeek API（stream=True）→ 成功则逐 chunk 流式拼接并实时更新显示 → 追加完整回复到 messages → 等待下次输入。失败则 st.error 提示 + st.stop 终止。

### 10.3 新建会话流程

点击新建会话 → save_session 保存当前会话到 JSON → 清空 messages 列表 → 生成新时间戳作为 current_session → st.rerun 刷新页面

## 十一、函数说明

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| generate_session_name() | 无 | str | 时间戳，格式 YYYY-MM-DD_HH-MM-SS |
| save_session() | 无 | 无 | 保存当前会话到 session/{name}.json，自动创建目录 |
| load_sessions() | 无 | list[str] | 扫描 session/ 目录，返回所有会话名称（不含 .json） |
| load_session(name) | session_name: str | bool | 加载指定会话到 session_state，失败返回 False |

## 十二、UI 布局

    ┌─────────────────────────────────────────────────────┐
    │  🤖 智能机器人                                       │
    │  会话名称: 2026-09-07_14-30-00                       │
    ├────────────────────────────┬────────────────────────┤
    │      主聊天区域              │    侧边栏              │
    │  - 历史消息气泡              │  [🚀 新建会话]        │
    │  - 用户消息 / AI回复         │  会话历史列表          │
    │                            │  [📄 会话1] [❌]      │
    │                            │  [📄 会话2] [❌]      │
    │                            │  陪伴信息              │
    │                            │  昵称: [输入框]        │
    │                            │  性格: [文本域]        │
    ├────────────────────────────┴────────────────────────┤
    │  [💬 请输入您的要求问题________________________]      │
    └─────────────────────────────────────────────────────┘

## 十三、数据流

用户输入 → st.chat_input → 显示用户消息 + 追加到 session_state.messages → 组装请求（系统提示词 + 全部历史）→ DeepSeek API → 流式响应 chunk → 拼接 full_response + st.empty 实时更新 UI → 追加 AI 回复到 messages → 等待下次输入

## 十四、启动与运行

环境准备：pip install streamlit openai python-dotenv

配置 .env 文件：DEEPSEEK_API_KEY=你的API密钥

启动命令：cd 第三章 && streamlit run 06.ai_parther.4.py

启动后浏览器自动打开 http://localhost:8501

## 十五、注意事项

1. API 密钥安全：.env 文件不应提交到版本控制系统
2. 会话文件管理：session/ 目录会持续增长，建议定期清理
3. 模型名称：当前使用 deepseek-chat，可更换为其他可用模型
4. 上下文长度：每次请求发送全部历史消息，轮次过多可能超出上下文窗口
5. 错误处理：API 调用失败时 st.error() 提示并 st.stop() 终止执行
