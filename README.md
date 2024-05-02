### PDF 임베딩 후 Langchain을 이용한 챗봇
### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pdf에 관련된 내용은 답변을 하고, &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;관련되지 않은 내용은 답변을 하지 않는다.
<img src="https://github.com/wahoman/pdf_tokenize_Chatbot/assets/93651467/a35c9193-2550-4c5e-8c13-388a15c9a8bf" width="40%" height="40%">


<img src="https://github.com/wahoman/pdf_tokenize_Chatbot/assets/93651467/85190197-9ecc-4ee9-807a-025d57439752" width="40%" height="40%">






### 테스트 목록:

### 1. 정확성 테스트 (Accuracy Testing)
- **올바른 응답 검증**: 챗봇이 주어진 질문에 대해 정확하고 관련성 있는 답변을 제공하는지 테스트합니다.
- **오답 검출**: 잘못된 정보를 제공하는 경우가 있는지 확인합니다.

### 2. 응답 거부 테스트 (Rejection Testing)
- **불필요한 질문 거부**: 챗봇이 회사 기밀과 관련 없거나 민감한 질문에 대해 응답을 거부하는지 테스트합니다.
- **범위 외 질문에 대한 처리**: 챗봇이 지원하지 않는 주제나 범위 외의 질문에 적절히 대응하는지 확인합니다.

### 3. 보안 테스트 (Security Testing)
- **정보 유출 검사**: 기밀 정보가 유출되지 않도록 챗봇의 응답을 체계적으로 검사합니다.
- **인증 및 접근 제어**: 적절한 사용자만이 챗봇을 이용할 수 있도록 인증과 접근 제어 기능을 검토합니다.

### 4. 성능 및 부하 테스트 (Performance and Load Testing)
- **응답 시간**: 질문에 대한 응답 시간을 측정하여 성능 이슈를 식별합니다.
- **동시 사용자 처리**: 여러 사용자가 동시에 접속했을 때 챗봇의 안정성 및 처리 능력을 평가합니다.

### 5. 사용자 경험 테스트 (User Experience Testing)
- **이용자 피드백**: 실제 사용자들의 피드백을 수집하여 챗봇의 사용성을 평가합니다.
- **질문 이해 능력**: 다양한 유형의 질문(예: 비유, 추상적 질문 등)에 대한 챗봇의 이해력과 대응력을 검증합니다.

### 6. 로깅 및 모니터링 (Logging and Monitoring)
- **로그 기록**: 모든 사용자 질문과 챗봇의 응답을 기록하여 후속 검토가 가능하도록 합니다.
- **오류 추적**: 오류가 발생했을 때 이를 신속하게 발견하고 대응할 수 있는 시스템을 구축합니다.
