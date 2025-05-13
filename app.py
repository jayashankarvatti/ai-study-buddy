import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["api_keys"]["gemini"])

st.set_page_config(page_title="AI Study Buddy", page_icon="🧠")
st.title("🧠 AI Study Buddy")
st.write("Ask questions or start a quiz!")

mode = st.radio("Choose mode:", ["Explain a Topic", "Take a Quiz"])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

model = genai.GenerativeModel('gemini-1.5-flash-001-tuning')

def get_response(prompt):
    response = model.generate_content(prompt)
    return response.text

if mode == "Explain a Topic":
    topic = st.text_input("Enter a topic you'd like explained:")
    if st.button("Explain") and topic:
        with st.spinner("Thinking..."):
            answer = get_response(f"Explain the topic: {topic} in simple terms.")
            st.session_state.chat_history.append(("User", topic))
            st.session_state.chat_history.append(("AI", answer))
elif mode == "Take a Quiz":
    subject = st.text_input("Enter a subject for quiz questions:")
    if st.button("Start Quiz") and subject:
        with st.spinner("Generating question..."):
            question = get_response(f"Ask me a quiz question on {subject} with multiple choice answers. Wait for my answer before giving feedback.")
            st.session_state.chat_history.append(("AI", question))

    user_answer = st.text_input("Your answer (if a quiz is ongoing):")
    if st.button("Submit Answer") and user_answer:
        with st.spinner("Evaluating..."):
            feedback = get_response(f"This was my answer: {user_answer}. Tell me if it's correct based on the last question.")
            st.session_state.chat_history.append(("User", user_answer))
            st.session_state.chat_history.append(("AI", feedback))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "User":
        st.markdown(f"🧑 You:** {msg}")
    else:
        st.markdown(f"🤖 AI:** {msg}")

