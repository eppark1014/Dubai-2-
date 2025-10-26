# 🚀 빠른 시작 가이드

## 1️⃣ OpenAI API 키 설정

서비스를 사용하려면 OpenAI API 키가 필요합니다.

### API 키 발급
1. https://platform.openai.com 접속
2. 계정 생성 및 로그인
3. API Keys 메뉴에서 새 키 생성
4. 생성된 키를 복사

### 환경 변수 설정
`.env` 파일을 생성하고 API 키를 입력합니다:

```bash
# .env 파일 생성
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-api-key-here
EOF
```

또는 직접 편집:
```bash
nano .env
```

## 2️⃣ 시스템 테스트

모든 환경이 제대로 설정되었는지 확인합니다:

```bash
python test_setup.py
```

예상 출력:
```
🎉 모든 테스트 통과! 서비스를 시작할 수 있습니다.
```

## 3️⃣ 서비스 실행

Flask 개발 서버를 시작합니다:

```bash
python app.py
```

서버가 시작되면 브라우저에서 다음 주소로 접속:
```
http://localhost:5000
```

## 4️⃣ 사용 방법

### PDF 업로드
1. 메인 페이지에서 "파일 선택" 버튼 클릭 또는 드래그 앤 드롭
2. PDF 파일 선택 (Bill of Lading 등)
3. "분석 시작" 버튼 클릭

### 분석 결과 확인
- **원본 페이지**: 변환된 이미지
- **붉은색 영역 감지**: 감지된 수정 영역 표시
- **수정사항 표**: 순번, 지시사항, 대상문구, 변환문구, 위치

### 결과 예시

| 순번 | 지시사항 | 대상문구 | 변환문구 | 위치 |
|------|----------|----------|----------|------|
| 1 | 삭제 | TEL:0574-87170623 | (DELETE) | Notify Party |
| 2 | 수정 | ABU DHABI, U.A.EMIRATES | ABU DHABI, U.A.E | Place of Receipt |

## 🔧 문제 해결

### "OPENAI_API_KEY가 설정되지 않았습니다"
- `.env` 파일이 존재하는지 확인
- API 키가 올바르게 입력되었는지 확인
- 파일을 저장했는지 확인

### "Tesseract가 설치되지 않았습니다"
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-kor
```

### "Poppler가 설치되지 않았습니다"
```bash
sudo apt-get install poppler-utils
```

### 포트가 이미 사용 중
다른 포트로 실행:
```python
# app.py 마지막 줄 수정
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📊 성능 최적화

### 고해상도 변환
`app.py`에서 DPI 조정:
```python
images = pdf_processor.convert_to_images(dpi=300)  # 기본값
# dpi=150  # 빠른 처리
# dpi=600  # 고품질 (느림)
```

### 붉은색 감지 감도 조절
`image_analyzer.py`에서 HSV 범위 조정:
```python
# 더 넓은 범위로 감지
lower_red1 = np.array([0, 80, 80])   # 낮은 채도도 인식
upper_red1 = np.array([15, 255, 255])
```

## 🎯 지원 문서 형식

- **Bill of Lading** (선하증권) ✅
- **Commercial Invoice** (상업송장) ✅
- **Packing List** (포장명세서) ✅
- 기타 붉은색 손글씨 수정이 포함된 PDF 문서

## 💡 팁

1. **고품질 스캔**: DPI 300 이상 권장
2. **명확한 손글씨**: 가독성 있는 손글씨 사용
3. **붉은색 펜**: 진한 빨간색 계열 사용 권장
4. **화살표 명확히**: 수정 지시 시 화살표를 명확히 표시
5. **영역 구분**: 수정/삭제 영역을 박스로 명확히 표시

## 📱 브라우저 지원

- Chrome / Edge: ✅ 완전 지원
- Firefox: ✅ 완전 지원
- Safari: ✅ 완전 지원
- Mobile: ✅ 반응형 지원

## 🔐 보안 주의사항

- `.env` 파일을 절대 Git에 커밋하지 마세요
- API 키를 공개 저장소에 업로드하지 마세요
- 업로드된 PDF는 서버에 임시 저장됩니다
- 민감한 문서는 사용 후 수동으로 삭제하세요

## 📞 지원

문제가 발생하면:
1. `test_setup.py`로 환경 확인
2. 로그 확인 (터미널 출력)
3. GitHub Issues에 문의

---

**즐거운 사용 되세요! 🎉**
