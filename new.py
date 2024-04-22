import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import openai
import json

app = FastAPI()

# 환경 변수 로드
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("No OPENAI_API_KEY found. Please check your .env file.")

# API 클라이언트 초기화
client = openai.OpenAI(api_key=openai_api_key)

# 정적 파일 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 토큰 파일에서 데이터 로드 및 처리
def load_and_process_tokens(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        token_data = json.load(file)
        # 'token' 값으로부터 문자열을 생성
        processed_text = " ".join([item['token'] for item in token_data])
    return processed_text

# 질문이 문서의 내용과 관련 있는지 확인
def is_relevant(question, processed_text):
    # 문서의 모든 토큰을 소문자로 변환하여 검사
    tokens = processed_text.lower().split()
    return any(token in question.lower() for token in tokens)

# GPT-3로 질문 응답
def query_gpt(question, context):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 사용자에게 pdf내용으로 답변을 해주는 챗봇입니다. pdf에 있는 내용만으로 가독성있게 대답해야 합니다. 질문이 pdf에 없는 내용이라면 답변하지 말아야 합니다."},
                {"role": "user", "content": f"Question: {question} based on the context: {context}"}
            ]
        )
        # response 객체에서 메시지 내용 추출
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        # 오류 처리를 위한 로그 출력
        print(f"An error occurred: {str(e)}")
        return "Error processing your request."


@app.post("/answer/")
async def get_answer(question: str = Form(...)):
    tokens_file_path = 'C:/Users/SSTLabs/Desktop/여형구/LLM_RAG/tokens.json'
    processed_text = load_and_process_tokens(tokens_file_path)
    
    if is_relevant(question, processed_text):
        answer = query_gpt(question, processed_text)
        return JSONResponse(content={"answer": answer}, status_code=200)
    else:
        return JSONResponse(content={"answer": "This question is not relevant to the document contents."}, status_code=400)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)