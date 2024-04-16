import jsonpickle
import nltk
from nltk.tokenize import word_tokenize
from PyPDF2 import PdfReader

nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    raw_text = ''
    for page in reader.pages:
        text = page.extract_text()
        if text:
            raw_text += text
    return raw_text

def tokenize_text(text):
    tokens = word_tokenize(text)
    token_data = [{'token': token, 'lower_token': token.lower()} for token in tokens]  # 소문자 버전 추가
    return token_data

def save_tokens(tokens, file_path):
    with open(file_path, 'w') as file:
        serialized_data = jsonpickle.encode(tokens)
        file.write(serialized_data)

# 파일 경로 설정
pdf_path = "C:/Users/SSTLabs/Desktop/여형구/설명서.pdf"
tokens_file_path = "C:/Users/SSTLabs/Desktop/여형구/tokens.json"

# 텍스트 추출 및 토큰화
text = extract_text_from_pdf(pdf_path)
tokens = tokenize_text(text)

# 토큰 데이터 저장
save_tokens(tokens, tokens_file_path)
