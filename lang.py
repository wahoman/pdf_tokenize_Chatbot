import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
import openai
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# .env 파일에서 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 문서 로딩 및 처리 준비
loader = PyPDFLoader("C:/Users/SSTLabs/Desktop/여형구/20. 장민섭_YOLOv5를 이용한 2D X-Ray 이미지 상의 폭발물 탐지_Rev3.0.pdf")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(texts, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 프롬프트 및 체인 설정
system_template="""Use the following pieces of context to answer the users question shortly.
Given the following summaries of a long document and a question, create a final answer with references ("SOURCES"), use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "제가 답해드릴 수 없는 질문이에요", don't try to make up an answer.
----------------
{summaries}

You MUST answer in Korean:"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)
llm = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=openai_api_key)
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

# 루트 경로
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse('static/lang.html')

# 질문 처리 경로
@app.post("/answer/")
async def answer(question: str = Form(...)):
    result = chain.invoke({"question": question})
    answer = result['answer'] if 'answer' in result else "No answer found."
    return {"answer": answer}
