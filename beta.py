import os
import time
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import jsonpickle
import openai
from dotenv import load_dotenv

app = FastAPI()

# .env 파일에서 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise Exception("No OpenAI API key found. Please check your .env file.")

# 정적 파일 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

def load_tokens(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            tokens = jsonpickle.decode(data)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while reading the file: {e}")

def check_relevance(question, tokens):
    # 단순히 토큰 중 일부가 질문에 포함되어 있는지 확인 (더 복잡한 로직으로 대체 가능)
    context = ' '.join([token['lower_token'] for token in tokens])
    return any(token in question.lower() for token in context.split())

def query_gpt(question, tokens):
    context = ' '.join([token['lower_token'] for token in tokens])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "pdf 내용을 기반으로 대답해야 합니다."},
                  {"role": "user", "content": f"질문: {question} based on the context: {context}"}]
    )
    return response['choices'][0]['message']['content']

@app.post("/answer/")
async def get_answer(question: str = Form(...)):
    tokens_file_path = 'C:/Users/SSTLabs/Desktop/여형구/LLM_RAG/tokens.json'
    tokens = load_tokens(tokens_file_path)
    if check_relevance(question, tokens):
        answer = query_gpt(question, tokens)
        return JSONResponse(content={"answer": answer}, status_code=200)
    else:
        return JSONResponse(content={"answer": "관련 없는 질문에는 답변할 수 없습니다."}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("beta:app", host="0.0.0.0", port=8000)
