import streamlit as st
import dotenv
import langchain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
import zipfile


API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Website Creation", page_icon=":robot_face:")

st.title("AI WebSite Creation")

prompt = st.text_area("Write your requirements for the website you want to create.")

if st.button("Generate Website"):
    message=[("system","""You are a expert in web development mainly in frontend. so create a HTML , CSS and JAVA script for the frontend based website as per the user requirements.
              the output should be in the below format only :
              
              --html--
              [html code]
              --html--
              
              --CSS--
              [css code]
              --CSS--
              
              --JavaScript--
              [JavaScript code]
              --JavaScript--
              """)]
    

    message.append(("user",prompt))

    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    response= model.invoke(message)

    with open("index.html","w",encoding="utf-8") as file:
        file.write(response.content.split("--html--")[1])

    with open("style.css","w",encoding="utf-8") as file:
        file.write(response.content.split("--CSS--")[1])

    with open("script.js","w",encoding="utf-8") as file:
        file.write(response.content.split("--JavaScript--")[1])

    with zipfile.ZipFile("website.zip","w") as zipf:
        zipf.write("index.html")
        zipf.write("style.css")
        zipf.write("script.js")

    st.download_button("Download Website",data=open("website.zip","rb"),file_name="website.zip")    
    st.write("success")



