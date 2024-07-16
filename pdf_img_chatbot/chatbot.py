from pdf_img_chatbot.models.olllama import OllamaModel
from pdf_img_chatbot.prompts.rag import RAG_PROMPT_1
from pdf_img_chatbot.vector_db.qdrant import QdrantDB
from pdf_img_chatbot.documents_loader.unstructured import UnstructuredDocumentLoader, PyPdfDocumentLoader
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydub import AudioSegment
from langchain_community.document_loaders import TextLoader
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chains.question_answering import load_qa_chain
import os
import base64
from io import BytesIO
from PIL import Image


import speech_recognition as sr

def convert_to_base64(pil_image):
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

class ChatBot:
    def __init__(self):
        self.db = None
        self.prompt = PromptTemplate.from_template(RAG_PROMPT_1)
        self.model = OllamaModel()
        self.chatbot = self.prompt | self.model.chat_model
        self.llm = self.model.chat_model
        self.rag_prompt = ChatPromptTemplate(
            input_variables=['context', 'question'], 
            messages=[
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=['context', 'question'], 
                        template="""You answer questions about the contents of a transcribed audio file. 
                        Use only the provided audio file transcription as context to answer the question. 
                        Do not use any additional information.
                        If you don't know the answer, just say that you don't know. Do not use external knowledge. 
                        Use three sentences maximum and keep the answer concise. 
                        Make sure to reference your sources with quotes of the provided context as citations.
                        \nQuestion: {question} \nContext: {context} \nAnswer:"""
                    )
                )
            ]
        )
        self.chain = load_qa_chain(self.llm, chain_type="stuff", prompt=self.rag_prompt)

    def upload_file(self, file):
        print(f'file: {file}')
        self.file = file
        self.docs = PyPdfDocumentLoader(file).loader.load_and_split()
        print("Docs:",self.docs)
        self.embeddings = self.model.embeddings_model
        self.db = QdrantDB(
            collection_name="pdf_img_chatbot",
            embeddings=self.embeddings,
            docs=self.docs
        ).db
        print("File uploaded successfully")
        print(f"number of documents: {len(self.docs)}")
    
    def upload_web_content(self, url):
        print(f'url: {url}')
        web_loader = WebBaseLoader(url)
        
        web_docs = web_loader.load_and_split()
        print("WEB:",web_docs)
        self.embeddings = self.model.embeddings_model
        self.db = QdrantDB(
            collection_name="web_content_chatbot",
            embeddings=self.embeddings,
            docs=web_docs
        ).db
        print("Web content loaded successfully")
        print(f"number of documents: {len(web_docs)}")

    def upload_audio_file(self, audio_file_path):
        print(f'audio file: {audio_file_path}')
        
        # Convert audio file to WAV format using pydub
        audio = AudioSegment.from_file(audio_file_path)
        print("AUDIO:_______", audio)
        wav_audio_path = "converted_audio.wav"
        print("________________________")
        audio.export(wav_audio_path, format="wav")
        print("________________________")
        # Initialize recognizer
        r = sr.Recognizer()
        r.energy_threshold = 300
        # Load the converted WAV audio file
        with sr.AudioFile(wav_audio_path) as source:
            audio = r.listen(source)
        transcription = r.recognize_google(audio)
        from langchain.docstore.document import Document


        # Split the transcription into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = splitter.split_text(transcription)
        from langchain_text_splitters import CharacterTextSplitter
        from langchain_community.document_loaders import TextLoader


        file_path = "tts_maker.txt"
        with open(file_path, "w") as file:
            file.write(texts[0])

        # Load the text file
        loader = TextLoader(file_path)
        documents = loader.load()

        # Split the documents with specified parameters
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        doc= text_splitter.split_documents(documents)

        print("TEXT:",texts)
        # Wrap each chunk in a dictionary with a 'page_content' key
        #doc = [{'page_content': text} for text in texts]
        #print("TEXT:", doc)
        
        # Initialize embeddings and create the QdrantDB instance
        self.embeddings = self.model.embeddings_model
        self.db = QdrantDB(
            collection_name="audio_transcribe",
            embeddings=self.embeddings,
            docs=doc
        ).db

        print("Audio file transcribed and processed successfully")

    def get_content(self, user_input):
        if self.db is None:
            return "Please upload a file first"

        content = self.db.similarity_search(
            user_input,
            k=2
        )
        print(f"content used for this chat: {content}\n-------------------")
        return content
    
    def get_image_description(self, image_path , image_question = "Describe the image in a very detailed way"):
        pil_image = Image.open(image_path)
        img_base64 = convert_to_base64(pil_image)
        image_model = self.model.img_model.bind(images = [img_base64])
        return image_model.invoke(image_question)

    def chat(self, user_input , chat_history , content):
        response = self.chatbot.invoke(
            input = {
                "content": content,
                "chat_history": chat_history,
                "question": user_input
            }
        )
        return response

    def chat_with_audio(self, user_input, chat_history, query):
        if self.db is None:
            return "Please upload an audio file first"

        docs = self.db.similarity_search(query)
        response = self.chain({"input_documents": docs, "question": user_input}, return_only_outputs=True)
        return response["output_text"]

#chat=ChatBot()
#chat.upload_audio_file(r'20230607_me_canadian_wildfires.mp3')

