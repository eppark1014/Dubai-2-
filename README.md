# PDF 수정/삭제 지시사항 자동 인식 서비스

AI 기반으로 PDF 문서의 붉은색 손글씨 수정/삭제 지시사항을 자동으로 인식하고 정리하는 웹 서비스입니다.

## 🎯 주요 기능

- **PDF 자동 변환**: PDF 파일을 고해상도 이미지로 자동 변환
- **붉은색 영역 감지**: OpenCV를 사용하여 붉은색 계열 손글씨 영역 자동 감지
- **OCR 텍스트 추출**: Tesseract를 통한 정확한 텍스트 인식
- **AI 분석**: GPT-4 Vision API로 수정/삭제 지시사항 자동 분석
- **표 형식 정리**: 분석 결과를 보기 쉬운 표로 자동 정리
- **직관적인 UI**: 드래그 앤 드롭 지원, 실시간 결과 표시

## 📋 지시사항 인식 패턴

### 수정 지시사항
- 수정할 텍스트를 붉은색 박스로 표시
- 화살표(→)로 연결
- 화살표 끝에 새로운 텍스트 작성

### 삭제 지시사항
- 삭제할 텍스트를 붉은색 박스로 표시
- 돼지꼬리 표시(물결, 취소선)로 삭제 의도 표시

## 🚀 설치 및 실행

### 1. 필수 요구사항

- Python 3.8 이상
- Tesseract OCR
- Poppler (pdf2image 사용)
- OpenAI API Key

### 2. 시스템 의존성 설치

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-kor poppler-utils
```

#### macOS
```bash
brew install tesseract tesseract-lang poppler
```

### 3. Python 패키지 설치

```bash
cd /home/user/webapp
pip install -r requirements.txt
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정합니다:

```bash
cp .env.example .env
# .env 파일을 열어서 API 키 입력
nano .env
```

`.env` 파일 내용:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 5. 서버 실행

```bash
python app.py
```

서버가 시작되면 브라우저에서 `http://localhost:5000`으로 접속합니다.

## 📁 프로젝트 구조

```
/home/user/webapp/
├── app.py                 # Flask 웹 애플리케이션
├── pdf_processor.py       # PDF → 이미지 변환 모듈
├── image_analyzer.py      # 이미지 분석 및 OCR 모듈
├── ai_analyzer.py         # AI 기반 분석 모듈
├── requirements.txt       # Python 의존성
├── .env.example          # 환경 변수 예시
├── .gitignore            # Git 제외 파일
├── README.md             # 프로젝트 문서
├── static/               # 정적 파일
│   ├── style.css        # CSS 스타일시트
│   └── script.js        # JavaScript
├── templates/            # HTML 템플릿
│   └── index.html       # 메인 페이지
├── uploads/              # 업로드된 PDF 저장
└── output/               # 변환된 이미지 저장
```

## 🔧 기술 스택

### Backend
- **Flask**: 웹 프레임워크
- **pdf2image**: PDF → 이미지 변환
- **OpenCV**: 이미지 처리 및 붉은색 영역 감지
- **Tesseract OCR**: 텍스트 추출
- **OpenAI GPT-4 Vision**: AI 기반 손글씨 분석

### Frontend
- **HTML5/CSS3**: 반응형 웹 UI
- **JavaScript (Vanilla)**: 파일 업로드 및 결과 표시

## 📊 분석 결과 형식

분석 결과는 다음과 같은 표 형식으로 제공됩니다:

| 순번 | 지시사항 | 대상문구 | 변환문구 | 위치 |
|------|----------|----------|----------|------|
| 1 | 삭제 | TEL:0574-87170623 | (DELETE) | Notify Party |
| 2 | 수정 | ABU DHABI, U.A.EMIRATES | ABU DHABI, U.A.E | Place of Receipt |
| 3 | 수정 | ABU DHABI, U.A.EMIRATES | ABU DHABI, U.A.E | Port of Loading |
| 4 | 삭제 | HS CODE : 39011000 | (DELETE) | No of Containers |
| 5 | 수정 | LDPE FT4119 QUANTITY. 24.75MT | COMMODITY : LDPE FT4119 QUANTITY : 24.75MT | Description |

## 🎨 UI 특징

- **드래그 앤 드롭**: 파일을 드래그하여 간편하게 업로드
- **실시간 피드백**: 분석 진행 상황 표시
- **이미지 미리보기**: 원본 + 붉은색 영역 감지 결과 비교
- **반응형 디자인**: 모바일/태블릿/데스크톱 지원
- **사용자 친화적**: 직관적인 인터페이스

## 🔒 보안 고려사항

- 파일 크기 제한: 최대 50MB
- 허용 파일 형식: PDF만 허용
- 업로드 파일명 보안 처리 (secure_filename)
- 고유 ID 기반 파일 관리

## 📝 사용 예시

1. 웹 브라우저에서 서비스 접속
2. PDF 파일 업로드 (드래그 또는 클릭)
3. "분석 시작" 버튼 클릭
4. AI가 자동으로 분석 진행
5. 페이지별 분석 결과 확인
6. 표 형식으로 정리된 수정/삭제 지시사항 확인

## 🐛 문제 해결

### Tesseract 오류
```bash
# Tesseract가 설치되어 있는지 확인
tesseract --version

# 없다면 설치
sudo apt-get install tesseract-ocr
```

### Poppler 오류
```bash
# Poppler가 설치되어 있는지 확인
pdftoppm -v

# 없다면 설치
sudo apt-get install poppler-utils
```

### OpenAI API 오류
- `.env` 파일에 올바른 API 키가 설정되어 있는지 확인
- API 사용량 한도를 확인

## 📄 라이선스

MIT License

## 👨‍💻 개발자

AI 기반 문서 처리 서비스

---

**문의사항이나 버그 리포트는 이슈로 등록해주세요.**
