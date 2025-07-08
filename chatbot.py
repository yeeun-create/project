
import streamlit as st
import openai
import os
from dotenv import load_dotenv
import gpts_prompt

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="오늘의 기분처방전", page_icon="💊")
st.title("오늘의 기분처방전")

SYSTEM_PROMPT = gpts_prompt.SYSTEM_PROMPT


# 세션 상태 초기화 (최초 1회만)
if "messages" not in st.session_state or not isinstance(st.session_state["messages"], list):
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]



# 첫 인사 메시지(대화 기록에도 남김)
if len(st.session_state["messages"]) == 1:
    greeting = "안녕하세요! 저는 감정 기반 콘텐츠 큐레이션 챗봇이에요. 오늘의 기분은 어떤가요?"
    st.session_state["messages"].append({"role": "assistant", "content": greeting})

# 대화 내용 출력
for msg in st.session_state["messages"]:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 입력창
user_input = st.chat_input("메시지를 입력하세요...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner("콘텐츠 큐레이터가 답변을 작성 중입니다..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state["messages"],
                stream=False
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"오류 발생: {e}"
    st.session_state["messages"].append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

