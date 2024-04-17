from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain.chains import AnalyzeDocumentChain

load_dotenv()
# OpenAI 설정
openai_api_key = os.getenv('OPENAI_API_KEY')

app = FastAPI()

# 정적 파일 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# FastAPI에 모델 설정
model = ChatOpenAI(model='gpt-3.5-turbo')
qa_chain = load_qa_chain(model, chain_type='map_reduce')

# PDF 파일에서 텍스트 추출
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    raw_text = ''
    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text

# 텍스트 분할 함수
def split_text_into_parts(text, length=5000):
    return [text[i:i + length] for i in range(0, len(text), length)]

# 문서 분석 함수
def process_part(part_text, question):
    qa_document_chain = AnalyzeDocumentChain(combine_docs_chain=qa_chain)
    return qa_document_chain.run(input_document=part_text, question=question)

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...), question: str = Form(...)):
    try:
        contents = await file.read()
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        raw_text = extract_text_from_pdf("temp.pdf")
        split_texts = split_text_into_parts(raw_text)

        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(lambda part: process_part(part, question), split_texts))

        os.remove("temp.pdf")  # 임시 파일 삭제

        if results and any(results):
            return JSONResponse(content={"answer": results}, status_code=200)
        else:
            return JSONResponse(content={"answer": "No answer found"}, status_code=404)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
