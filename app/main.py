import streamlit as st
from pdf_img_chatbot.chatbot import ChatBot
import os
import tempfile
import base64

# title and page config
st.set_page_config(page_title="KnowledgeLink ChatBot", page_icon="🤖", layout="wide")

# Custom CSS
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_custom_css(background_image):
    bin_str = get_base64_of_bin_file(background_image)
    css = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

            body {{
                font-family: 'Roboto', sans-serif;
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: white;
            }}
            .stApp {{
                background-color: rgba(0, 0, 0, 0.8);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                color: white;
            }}
            .stButton>button {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                margin: 10px 0;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }}
            .stButton>button:hover {{
                background-color: #45a049;
            }}
            .stTextInput>div>input {{
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 16px;
                color: black;
            }}
            .stFileUploader>div>div>button {{
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .stFileUploader>div>div>button:hover {{
                background-color: #0056b3;
            }}
            .stImage {{
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .css-1cpxqw2 {{
                background-color: #ffffff;
                border: 1px solid #e0e0e0;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                color: black;
            }}
            .css-1vq4p4l {{
                margin: 15px;
                color: white;
            }}
            .css-1d391kg {{
                margin-top: -60px;
                color: white;
            }}
            .css-qri22k {{
                margin-top: 10px;
                color: white;
            }}
            .css-1siy2j7 {{
                color: #333333;
            }}
            .css-1v3fvcr {{
                color: #007bff;
            }}
            .css-1v3fvcr:hover {{
                color: #0056b3;
            }}
            .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
                color: white;
            }}
            .custom-title {{
                color: #FFD700;
                font-size: 2em;
                font-weight: bold;
            }}
            .css-1d391kg {{
                background-color: rgba(0, 0, 0, 0.8);
            }}
        </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply custom CSS with the local background image
apply_custom_css("pexels-felixmittermeier-956999.jpg")

def init():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "qdrant_db" not in st.session_state:
        st.session_state.qdrant_db = None
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = ChatBot()
    if "file" not in st.session_state:
        st.session_state.file = None
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = None
    if "img_file" not in st.session_state:
        st.session_state.img_file = None
    if "image_description" not in st.session_state:
        st.session_state.image_description = None
    if "url" not in st.session_state:
        st.session_state.url = None
    if "audio_file" not in st.session_state:
        st.session_state.audio_file = None

# sidebar
def upload_file():
    st.subheader("Upload File, Image, Audio or Provide URL")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
    if st.button("Upload and chat", key="upload_chat"):
        if uploaded_file is not None:
            # save file
            st.session_state.file = uploaded_file
            st.session_state.temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(st.session_state.temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.session_state.chatbot.upload_file(file_path)
            st.success("File uploaded successfully")
        else:
            st.warning("Please upload a file")

    url = st.text_input("Enter a URL")
    if st.button("Upload and chat from URL", key="upload_url_chat"):
        if url:
            st.session_state.url = url
            st.session_state.chatbot.upload_web_content(url)
            st.success("Web content loaded successfully")
        else:
            st.warning("Please enter a valid URL")

    if st.button("Clear chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.img_file = None
        st.session_state.image_description = None
        st.session_state.file = None
        st.session_state.url = None
        st.session_state.audio_file = None
        st.success("Chat cleared")

    image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], key="image_uploader")
    if image_file is not None:
        st.session_state.img_file = image_file
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
        image_description = st.session_state.chatbot.get_image_description(image_file)
        st.session_state.image_description = image_description
        st.session_state.chat_history.append({"role": "bot", "message": f"Image description: {image_description}"})
        st.success("Image uploaded successfully")

    audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "opus"], key="audio_uploader")
    if st.button("Upload and transcribe audio", key="upload_audio"):
        if audio_file is not None:
            st.session_state.audio_file = audio_file
            st.session_state.temp_dir = tempfile.mkdtemp()
            audio_file_path = os.path.join(st.session_state.temp_dir, audio_file.name)
            with open(audio_file_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            st.session_state.chatbot.upload_audio_file(audio_file_path)
            st.success("Audio file uploaded and transcribed successfully")
        else:
            st.warning("Please upload an audio file")

def chatbot():
    st.markdown('<h1 class="custom-title">KnowledgeLink ChatBot</h1>', unsafe_allow_html=True)

    chat_container = st.container()
    for chat in st.session_state.chat_history:
        with chat_container:
            st.chat_message(chat["role"]).markdown(chat["message"])
    
    user_input = st.chat_input("Ask anything about your file, image, audio, or web content")
    if user_input:
        if st.session_state.file is None and st.session_state.url is None and st.session_state.audio_file is None:
            st.warning("Please upload a file, provide a URL, or upload an audio file first")
            return
        with chat_container:
            st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        with st.spinner("Thinking..."):
            chat_history_str = "\n".join([chat["message"] for chat in st.session_state.chat_history[-5:]])
            content = st.session_state.chatbot.get_content(user_input)
            
            if st.session_state.img_file is not None:
                content += f"\nImage description: {st.session_state.image_description}"
            if st.session_state.audio_file is not None:
                response = st.session_state.chatbot.chat_with_audio(user_input, chat_history_str, content)
            else:
                response = st.session_state.chatbot.chat(user_input, chat_history_str, content)
            with chat_container:
                st.chat_message("bot").markdown(response)
            st.session_state.chat_history.append({"role": "bot", "message": response})

def main():
    init()
    with st.sidebar:
        upload_file()
    chatbot()

if __name__ == "__main__":
    main()
