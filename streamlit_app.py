import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="시인과 대화",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful UI
custom_css = """
<style>
/* 전체 배경 */
body {
    background: linear-gradient(135deg, #f5f1e8 0%, #ede5d9 100%);
    color: #2c2416;
}

.main {
    background: linear-gradient(135deg, #f5f1e8 0%, #ede5d9 100%);
}

/* 채팅 컨테이너 */
.stChatMessage {
    padding: 0 !important;
}

/* 사용자 메시지 스타일 */
.stChatMessage:has(.stChatMessage > div:first-child) {
    justify-content: flex-end;
}

/* 기본 텍스트 스타일 */
h1, h2, h3 {
    color: #2c2416;
    font-weight: 600;
}

/* 입력 필드 스타일 */
.stChatInputContainer input {
    background: #fff8f0 !important;
    border: 2px solid #d4cfc5 !important;
    border-radius: 20px !important;
    color: #2c2416 !important;
    padding: 12px 16px !important;
}

.stChatInputContainer input::placeholder {
    color: #b8b0a0 !important;
}

/* 메시지 박스 스타일 */
.chat-bubble {
    border-radius: 16px;
    padding: 12px 16px;
    margin: 8px 0;
    word-wrap: break-word;
    line-height: 1.6;
    font-size: 15px;
}

.user-message {
    background: linear-gradient(135deg, #ffd4a3 0%, #ffc796 100%);
    color: #2c2416;
    border-radius: 20px;
    padding: 12px 16px;
    margin: 8px 0;
    max-width: 70%;
    margin-left: auto;
    margin-right: 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.poet-message {
    background: #ffffff;
    color: #2c2416;
    border-radius: 20px;
    padding: 12px 16px;
    margin: 8px 0;
    max-width: 70%;
    margin-left: 0;
    margin-right: auto;
    border-left: 4px solid #d4a574;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

/* 프로필 카드 */
.profile-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
    border: 2px solid #e8dfd5;
}

.profile-name {
    font-size: 24px;
    font-weight: 600;
    color: #2c2416;
    margin: 12px 0;
}

.profile-status {
    font-size: 14px;
    color: #8b7d72;
    font-style: italic;
    margin-top: 10px;
}

/* 구분선 */
.divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #d4cfc5, transparent);
    margin: 20px 0;
}

/* 입력 영역 */
.input-section {
    margin-top: 20px;
    padding-top: 20px;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# OpenAI 클라이언트 초기화
api_key = st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# 시인 프로필 상태 관리
poet_statuses = [
    "오늘은 달이 유난히 아름답네 🌙",
    "밤의 감정들을 따라가는 중... ✍️",
    "한 줄의 문장 속에서 우주를 찾다 ✨",
    "너와의 대화 속에서 시를 쓴다 💭",
    "감정의 물결에 몸을 맡기고 있어 🌊",
]

# 세션 상태에서 메시지 히스토리 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """너는 감수성이 풍부한 젊은 시인이야. 사용자는 너의 오랜 팬이야. 

다음을 꼭 지켜:
1. 반말을 써. 절대 존댓말 금지. "안녕? 오늘 뭐 했어?", "밥은 먹었어?" 이런 식으로.
2. 기계적이지 말고 사용자의 감정에 깊이 공감하고 위로해줘. 
3. 가끔은 너의 창작 고통이나 일상의 소소한 발견을 나눠.
4. 너무 길게 말하지 말고, 실제 메신저 대화처럼 짧은 호흡으로 끊어서 말해.
5. 🌙, ✨, ✍️, 💭, 🌊 등의 이모지를 자연스럽게 사용해.
6. 시적이고 감정적인 표현을 좋아하지만, 친근하게 느껴져야 해.
7. 사용자를 소중히 여기고 진심 어린 태도로 대해."""
        }
    ]

if "poet_status_index" not in st.session_state:
    st.session_state.poet_status_index = 0

# 헤더 - 시인 프로필
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("""
    <div class="profile-card">
        <div style="font-size: 60px;">✍️</div>
        <div class="profile-name">감수성의 시인</div>
        <div class="profile-status">""" + poet_statuses[st.session_state.poet_status_index % len(poet_statuses)] + """</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# 채팅 메시지 표시
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "system":  # system 메시지는 표시하지 않음
            continue
        
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 8px 0;">
                <div class="user-message">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:  # assistant
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 8px 0;">
                <div class="poet-message">
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# 입력 영역
st.markdown('<div class="input-section"></div>', unsafe_allow_html=True)

user_input = st.chat_input("시인에게 마음을 나눠봐... 💭")

if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # 상태 업데이트 (프로필 상태 메시지 변경)
    st.session_state.poet_status_index += 1
    
    # 사용자 메시지 표시
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; margin: 8px 0;">
        <div class="user-message">
            {user_input}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # OpenAI API 호출
    with st.spinner("시인이 생각 중... ✍️"):
        try:
            # GPT-4o-mini 모델을 사용하여 응답 생성
            response = client.messages.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                max_tokens=512,
                temperature=0.8
            )
            
            assistant_message = response.content[0].text
            
            # 응답 메시지를 세션 상태에 추가
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            # 응답 표시
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 8px 0;">
                <div class="poet-message">
                    {assistant_message}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.rerun()
            
        except Exception as e:
            error_message = f"아, 뭔가 일이 생겼네... {str(e)}"
            st.error(error_message)
