from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import openai
from dotenv import load_dotenv

app = FastAPI()

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise Exception("No OpenAI API key found. Please check your .env file.")

client = openai.OpenAI(api_key=openai.api_key)

# 정적 파일 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/answer/")
async def get_answer(question: str = Form(...)):
    # 예시 데이터 (실제 데이터는 로드하는 로직 필요)
    is_relevant = True  # 이 부분을 실제 로직으로 대체해야 함
    document_weight = "1.0"  # 문서 가중치 설정
    
    if is_relevant:
        # GPT 모델로부터 응답 받기 (여기서는 가상으로 설정)
        answer = "여기는 GPT로부터의 응답입니다."
        response = JSONResponse(content={"answer": answer}, status_code=200)
        response.headers['Document-Weight'] = document_weight
        return response
    else:
        response = JSONResponse(content={"answer": "관련 없는 질문에는 답변할 수 없습니다."}, status_code=400)
        response.headers['Document-Weight'] = document_weight
        return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("gptapi:app", host="0.0.0.0", port=8000)
