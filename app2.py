import streamlit as st
import google.generativeai as genai

# ------------- Configure Gemini API -------------
genai.configure(api_key="AIzaSyDtxBhFPE0jkb_Jab9ThC362WPA5922pqE")
model = genai.GenerativeModel('gemini-2.5-flash')

if "sessions" not in st.session_state:
    st.session_state.sessions = {"Chat 1": []}
    st.session_state.current_chat = "Chat 1"

# Sidebar
st.sidebar.title("📂 AI Story Generator Sessions")
if st.sidebar.button("➕ New Chat"):
    chat_name = f"Chat {len(st.session_state.sessions) + 1}"
    st.session_state.sessions[chat_name] = []
    st.session_state.current_chat = chat_name
    st.rerun()

for chat in list(st.session_state.sessions.keys()):
    col1, col2 = st.sidebar.columns([4, 1])
    if col1.button(chat, use_container_width=True):
        st.session_state.current_chat = chat
        st.rerun()
    if col2.button("🗑️", use_container_width=True, key=chat):
        del st.session_state.sessions[chat]
        if st.session_state.sessions:
            st.session_state.current_chat = list(st.session_state.sessions.keys())[0]
        else:
            st.session_state.sessions = {"Chat 1": []}
            st.session_state.current_chat = "Chat 1"
        st.rerun()

if st.sidebar.button("🗑️ Clear All Chats"):
    st.session_state.sessions = {"Chat 1": []}
    st.session_state.current_chat = "Chat 1"
    st.rerun()

# Story options
st.title("📖 AI Story Generator")
with st.expander("⚙️ Story Options"):
    length = st.selectbox("Select Story Length", ["Short", "Medium", "Long"])
    theme = st.selectbox("Select Story Theme", ["Adventure", "Fantasy", "Sci-Fi", "Mystery"])

chat = st.session_state.sessions[st.session_state.current_chat]

# Display messages
for msg in chat:
    align = "user" if msg["role"] == "user" else "assistant"
    if align == "user":
        st.markdown(f"<div style='text-align:right; background-color:#3E3E3E; padding:10px; border-radius:8px; max-width:75%; margin-left:auto; margin-bottom:10px;'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:left; padding:10px; max-width:75%; margin-right:auto; margin-bottom:10px;'>{msg['content']}</div>", unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Write your story prompt here..."):
    chat.append({"role": "user", "content": prompt})
    st.rerun()

if chat and chat[-1]["role"] == "user":
    with st.spinner("AI is generating..."):
        length_mod = {"Short": "about 100 words", "Medium": "about 200 words", "Long": "about 300 words"}
        prompt = f"Write a {theme} story, {length_mod[length]}, based on: {chat[-1]['content']}"
        response = model.generate_content(prompt)
        chat.append({"role": "assistant", "content": response.text})
        st.rerun()