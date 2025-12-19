import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import zipfile
import PyPDF2


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Website Creation", page_icon="🤖")
st.title("AI Website Creation")


prompt = st.text_area(
    "Write your requirements for the website you want to create.",
    placeholder="Example: Create a professional portfolio website using the information from the uploaded resume."
)

uploaded_file = st.file_uploader(
    "Upload a reference file (optional – PDF / TXT)",
    type=["pdf", "txt"]
)

uploaded_content = ""


if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        uploaded_content = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        uploaded_content = "\n".join(
            page.extract_text()
            for page in reader.pages
            if page.extract_text()
        )

    st.success("File uploaded successfully!")


def extract_block(text, start, end):
    if start not in text or end not in text:
        return None
    return text.split(start)[1].split(end)[0].strip()


if st.button("Generate Website"):
    system_prompt = """
You are an expert frontend web developer.

STRICT RULES:
1. HTML must contain ONLY valid HTML.
2. DO NOT include CSS or JavaScript inside HTML.
3. CSS must be ONLY in the CSS section.
4. JavaScript must be ONLY in the JavaScript section.
5. DO NOT include the section markers inside the code.
6. DO NOT add explanations, comments, or markdown.

FORMAT (STRICT):

--html--
HTML code only.
Must include:
<link rel="stylesheet" href="style.css">
<script src="script.js"></script>
--html--

--CSS--
CSS code only.
--CSS--

--JavaScript--
JavaScript code only.
--JavaScript--
"""

    user_prompt = f"""
Website requirements:
{prompt}

Reference content (if any):
{uploaded_content}
"""

    messages = [
        ("system", system_prompt),
        ("user", user_prompt)
    ]

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0
    )

    try:
        response = model.invoke(messages)
    except Exception as e:
        st.error("AI request failed. Please check your API key or quota.")
        st.exception(e)
        st.stop()

    
    html_code = extract_block(response.content, "--html--", "--html--")
    css_code = extract_block(response.content, "--CSS--", "--CSS--")
    js_code = extract_block(response.content, "--JavaScript--", "--JavaScript--")

    
    if not html_code or not css_code or not js_code:
        st.error("AI response format was invalid. Please regenerate.")
        st.text_area("Raw AI Response", response.content, height=300)
        st.stop()

    if "--CSS--" in html_code or "--JavaScript--" in html_code:
        st.error("AI placed CSS or JavaScript inside HTML. Please regenerate.")
        st.text_area("Broken HTML", html_code, height=300)
        st.stop()

    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_code)

    with open("style.css", "w", encoding="utf-8") as f:
        f.write(css_code)

    with open("script.js", "w", encoding="utf-8") as f:
        f.write(js_code)

   
    with zipfile.ZipFile("website.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("index.html")
        zipf.write("style.css")
        zipf.write("script.js")

    st.download_button(
        "Download Website",
        data=open("website.zip", "rb"),
        file_name="website.zip",
        mime="application/zip"
    )

    st.success("Website generated successfully!")
