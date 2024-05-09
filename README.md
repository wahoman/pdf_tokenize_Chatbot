# GitHub README: 문서 기반 지능형 챗봇 프로젝트 📘🤖

## 프로젝트 개요 🌟
이 프로젝트는 특정 메뉴얼이나 문서를 기반으로 정확한 답변을 제공하는 지능형 챗봇을 개발하는 것입니다. 사용자는 PDF 형태의 문서를 업로드하면 자동으로 내용이 임베딩되어 데이터베이스에 저장되며, 이를 통해 필요한 정보를 효율적으로 제공받을 수 있습니다. 초기 단계에서는 비용 효율성을 고려하여 Llama3, Phi, Solar 등의 오픈소스 모델을 사용해 보았습니다. 그러나 이러한 모델들은 품질 면에서 만족스럽지 못했고, 다수 사용자 접속 시 GPU 부족 문제 및 긴 추론 시간 등의 기술적 한계가 있었습니다. 이에 따라, 고품질의 답변을 보장하기 위해 GPT-3.5 Turbo 모델로 전환하여 프로젝트를 완성하게 되었습니다.

## 기술 스택 🛠️
- **FastAPI** 🚀: 웹 서버 및 API 관리
- **OpenAI** 🧠: GPT-3.5 Turbo 모델을 통한 문서 기반 질의응답 처리
- **Langchain** 🔗: 문서를 임베딩하고 검색 가능한 벡터로 변환
- **Chroma** 📊: 임베딩된 문서를 저장 및 관리하는 벡터 데이터베이스
- **PyPDFLoader** 📄: PDF 문서의 텍스트 추출 및 처리

## 주요 기능 📌
1. **문서 기반 질의응답** 📖: 사용자가 업로드한 PDF 문서를 기반으로, 문서의 내용에 관련된 질문에 대해 정확하고 구체적인 답변을 제공합니다.
2. **고품질의 임베딩 처리** 🔍: OpenAI의 임베딩 기술을 활용하여 문서의 내용을 높은 품질의 벡터로 변환하고, 이를 바탕으로 효율적인 정보 검색을 수행합니다.
3. **스마트한 정보 필터링** ⚠️: 메뉴얼과 관련 없는 질문에는 "제가 답해드릴 수 없는 질문이에요"라고 응답하여 정보의 오용 가능성을 최소화합니다.

## 사용 방법 📑
- **서버 구동** 🔌: 프로젝트 폴더 내에서 FastAPI 서버를 구동시켜 웹 서비스를 시작합니다.
- **문서 업로드 및 질의응답** 💬: 사용자는 웹 인터페이스를 통해 PDF 문서를 업로드하고, 업로드된 문서 기반으로 질문을 할 수 있습니다. 시스템은 문서 내용을 분석하여 필요한 정보를 추출하고, 질문에 대한 답변을 반환합니다.

## 프로젝트의 장점 ✨
- **정보 접근성 향상** 🚀: 복잡하고 긴 문서를 일일이 읽지 않고도 필요한 정보를 빠르게 얻을 수 있습니다.
- **비용 효율성** 💸: 초기 비용을 절감하면서도 품질을 유지할 수 있는 최적의 기술 선택.
- **사용자 경험 개선**

 🙌: 직관적인 웹 인터페이스를 통해 사용자가 쉽게 문서를 업로드하고 질문할 수 있도록 설계되었습니다.

## 미래 전망 🔮
이 챗봇은 기업 또는 교육 기관에서 매뉴얼이나 교재와 같은 특정 문서들을 더욱 효과적으로 활용할 수 있게 만들어 줍니다. 추가적인 기능 개발과 모델 최적화를 통해 더욱 다양한 형태의 문서 처리 및 더 나은 사용자 경험을 제공할 계획입니다.
