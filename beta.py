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

def query_gpt(question, tokens):
    context = ' '.join([token['lower_token'] for token in tokens])  # 문맥을 토큰에서 생성
    start_time = time.time()  # 질문 처리 시작 시간
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "질문이 내용과 관련이 없다면 모른다고 해야합니다. 하지만 내용과 관련있는 정보에 대해서는 대답해도 좋습니다.:"},
                  {"role": "user", "content": f"질문: {question} based on the context: {context}"}]
    )
    end_time = time.time()  # 질문 처리 종료 시간
    processing_time = end_time - start_time  # 처리 시간 계산
    answer = response['choices'][0]['message']['content']
    return answer, processing_time

@app.post("/answer/")
async def get_answer(question: str = Form(...)):
    tokens_file_path = 'C:/Users/SSTLabs/Desktop/여형구/LLM_RAG/tokens.json'
    tokens = load_tokens(tokens_file_path)
    answer, processing_time = query_gpt(question, tokens)
    if processing_time == 0:  # 관련 없는 질문에 대한 특별 처리
        return JSONResponse(content={"answer": answer}, status_code=400)
    if answer:
        return JSONResponse(content={"answer": answer, "time": processing_time}, status_code=200)
    else:
        return JSONResponse(content={"answer": "그부분은 잘 모르겠어요", "time": processing_time}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("beta:app", host="0.0.0.0", port=8000)