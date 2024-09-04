import streamlit as st 
from audio_recorder_streamlit import audio_recorder 
import openai 
import base64 
import os 

api_key = "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"

api_key = os.getenv("api_key")

def setup_openai_client(api_key):
    return openai.OpenAI(api_key=api_key)

#function that can transcribe the audio into text
def transcribe_audio(client,audio_path):
    with open(audio_path,'rb') as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1",file=audio_file)
        return transcript.text 
    
#taking response from Openai
def fetch_ai_response(client,input_text):
    messages =[{"role":"user","content": input_text}]
    response = client.chat.completions.create(model = "gpt-3.5-turbo",messages= messages)
    return response.choices[0].message.content

#convert text to audio
def text_to_audio(client,text,audio_path):
    response = client.audio.speech.create(model="tts-1",voice="echo",input=text)
    response.stream_to_file(audio_path)
    

#auto-play audio function
def auto_play_audio(audio_file):
    with open(audio_file,"rb")as audio_file:
        audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
    audio_html = f'<audio src ="data:audio/mp3;base64,{base64_audio}" controls autoplay>'
    
def main():
    st.sidebar.title("API KEY CONFIGURATION")
    api_key = st.sidebar.text_input("Enter your API key",type="password")
    st.title("Audio to Text")
    st.write("Click here to interact with me")
    recorded_audio = audio_recorder()
    
    if api_key:
        client = setup_openai_client(api_key)
        recorded_audio = audio_recorder()
        
        if recorded_audio:
            audio_file = "audio.mp3"
            with open(audio_file,"wb") as f :
                f.write(recorded_audio)
                
            transcribe_text = fetch_ai_response(client,transcribe_text)
            st.write("Transcribed Text: ",transcribe_text)
            
            ai_response = fetch_ai_response(client,transcribe_text)
            response_audio_file = "audio_response.mp3"
            text_to_audio(client,ai_response,response_audio_file)
            # st.audio(response_audio_file)
            # st.write("AI Response: ",ai_response)
            auto_play_audio(response_audio_file)
            st.write(ai_response,"AI Response")
            
if __name__ == "__main__":
    main()
    
