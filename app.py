import streamlit as st
from parallel import chat, transcription  
import time
from pydub import AudioSegment
import tempfile
import base64
import time


def autoplay_audio(audio_bytes):
    audio = AudioSegment.from_file(audio_bytes, format="mp3")
    audio_length = len(audio) / 1000.0
    b64 = base64.b64encode(audio_bytes.getvalue()).decode()
    audio_html = f"""
    <audio autoplay="true">
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    sound = st.empty()
    sound.markdown(audio_html, unsafe_allow_html=True)

    time.sleep(audio_length + 2)
    sound.empty()


def handle_text_input(user_input):
    start_time = time.time()
    response_data = chat(user_input,"testuser_streamlit","session4")
    end_time = time.time()
    execution_time = end_time - start_time
    print("Time taken: ", execution_time)
    if response_data[0]:
        st.write(f"{response_data[1]} : {response_data[0]}")
        audio_1,_=response_data[2]
        autoplay_audio(audio_1)
    if len(response_data)>3:
        st.write(f"{response_data[4]} : {response_data[3]}")
        audio_2, _ = response_data[5]
        autoplay_audio(audio_2)   




def main():
    st.title("Prespectives")
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("You: ", placeholder="Type your message here...")

    uploaded_file = st.file_uploader("Or upload an audio message", type=['wav', 'mp3', 'ogg'])

    if st.button('Send Text') and user_input:
        handle_text_input(user_input)
        st.session_state.chat_history.append(user_input)

    if uploaded_file is not None and st.button('Process Audio'):
        with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
            transcribed_text = transcription(tmp_path)
        handle_text_input(transcribed_text)

if __name__ == "__main__":
    main()
