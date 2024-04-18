from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import openai
import os
from dotenv import load_dotenv
import logging
from langchain.chains import OpenAIChain
from langchain.schema import KnowledgeBase, Document
from langchain.retrievers import EmbeddingRetriever
import pdfplumber

app = FastAPI()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    logger.error("No OpenAI API key found. Please check your .env file.")
    raise Exception("No OpenAI API key found. Please check your .env file.")

app.mount("/static", StaticFiles(directory="static"), name="static")

# PDF 내용을 로드하는 함수
def load_pdf_content(file_path):
    with pdfplumber.open(file_path) as pdf:
        full_text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    return full_text

# LangChain 설정
document = Document(content=load_pdf_content("C:/Users/SSTLabs/Desktop/여형구/설명서.pdf"))
knowledge_base = KnowledgeBase(documents=[document])
retriever = EmbeddingRetriever(knowledge_base)
chain = OpenAIChain(
    model_name="gpt-3.5-turbo",
    retriever=retriever,
    api_key=openai_api_key
)

@app.post("/answer/")
async def get_answer(question: str = Form(...)):
    retrieval = chain.retriever.retrieve(question)

    if not retrieval:
        return JSONResponse(content={"message": "No relevant document content found."}, status_code=404)

    answer = chain.answer(question, retrieval[0])
    return JSONResponse(content={"answer": answer}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app", host="0.0.0.0", port=8000)
