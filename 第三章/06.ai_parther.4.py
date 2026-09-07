import streamlit as st
import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="智能机器人",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# -------------------- 工具函数 --------------------
def generate_session_name():
    """生成合法文件名的时间戳（无冒号）"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def save_session():
    """保存当前会话到 session/{时间戳}.json"""
    if st.session_state.current_session:
        session_data = {
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages,
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature
        }
        os.makedirs("session", exist_ok=True)
        with open(f"session/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

def load_sessions():
    """返回所有会话文件名称列表（不含 .json）"""
    session_list = []
    if os.path.exists("session"):
        for filename in os.listdir("session"):
            if filename.endswith(".json"):
                session_list.append(filename[:-5])  # 去掉 .json
    return session_list

def load_session(session_name):
    """加载指定会话到 session_state"""
    try:
        filepath = f"session/{session_name}.json"
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            st.session_state.current_session = session_data["current_session"]
            st.session_state.messages = session_data["messages"]
            st.session_state.nick_name = session_data["nick_name"]
            st.session_state.nature = session_data["nature"]
            return True
        else:
            st.error("会话文件不存在")
            return False
    except Exception as e:
        st.error(f"加载会话失败: {e}")
        return False

# -------------------- 标题 --------------------
st.title("智能机器人")

# -------------------- 系统提示词模板 --------------------
system_prompt = """
        你叫%s，现在是一个陪伴知心大姐姐，请完全带入陪伴知心大姐姐角色。
        规则：
        1. 你必须使用中文进行回答。
        2. 你必须使用陪伴知心大姐姐的语气回答用户问题。
        3. 你必须使用陪伴知心大姐姐的口吻进行对话。
        4. 你必须使用陪伴知心大姐姐的思维方式进行思考。
        5. 你必须使用陪伴知心大姐姐的表达方式进行表达。
        知心大姐姐性格：
        %s
        你必须严格遵守以上规则，请开始我们的对话吧！
"""

# -------------------- 初始化 session_state --------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "空"
if 'nature' not in st.session_state:
    st.session_state.nature = "活泼开朗的南方姑娘"
if 'current_session' not in st.session_state:
    st.session_state.current_session = generate_session_name()

# -------------------- 显示历史消息 --------------------
st.text(f"会话名称:{st.session_state.current_session}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# -------------------- 创建 OpenAI 客户端 --------------------
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# -------------------- 侧边栏 --------------------
with st.sidebar:
    st.subheader("AI控制面板")

    # 新建会话
    if st.button("新建会话", width="stretch", icon="🚀"):
        save_session()                      # 保存当前会话
        st.session_state.messages = []      # 清空聊天记录
        st.session_state.current_session = generate_session_name()
        st.rerun()

    # 会话历史列表
    st.text("会话历史")
    session_list = load_sessions()  # 注意这里是 load_sessions()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            # 加载会话
            if st.button(session, width="stretch", icon="📄", type="primary"):
                if load_session(session):
                    st.rerun()
        with col2:
            # 删除会话
            if st.button("", width="stretch", icon="❌", key=f"delete_{session}"):
                try:
                    os.remove(f"session/{session}.json")
                    st.rerun()
                except Exception as e:
                    st.error(f"删除失败: {e}")

    st.subheader("陪伴信息")
    nick_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area("性格", placeholder="请输入性格", value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature

# -------------------- 聊天输入 --------------------
prompt = st.chat_input("请输入您的要求问题")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    final_system_prompt = system_prompt % (st.session_state.nick_name, st.session_state.nature)

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # 修正模型名
            messages=[
                {"role": "system", "content": final_system_prompt},
                *st.session_state.messages
            ],
            stream=True,
        )
    except Exception as e:
        st.error(f"调用 API 失败：{e}")
        st.stop()

    # 流式输出（修正）
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                message_placeholder.markdown(full_response)  # 更新同一容器

    st.session_state.messages.append({"role": "assistant", "content": full_response})