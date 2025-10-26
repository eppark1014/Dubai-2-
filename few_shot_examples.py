"""
Few-Shot Learning을 위한 샘플 데이터
실제 Bill of Lading 수정사항 예시
"""

# 샘플 수정사항 패턴
SAMPLE_EXAMPLES = """
### 학습 예시 1: 수정 패턴
이미지 설명: "ABU DHABI, U.A.EMIRATES" 텍스트가 붉은색 박스로 표시되고, 화살표(→)가 "ABU DHABI, U.A.E"로 연결됨
분석 결과:
{
  "order": 1,
  "action": "수정",
  "original_text": "ABU DHABI, U.A.EMIRATES",
  "new_text": "ABU DHABI, U.A.E",
  "location": "Place of Receipt",
  "confidence": "high"
}

### 학습 예시 2: 삭제 패턴
이미지 설명: "TEL:0574-87170623" 텍스트가 붉은색으로 동그라미 쳐지고, 물결표시(~~~) 또는 X 표시가 있음
분석 결과:
{
  "order": 2,
  "action": "삭제",
  "original_text": "TEL:0574-87170623",
  "new_text": "(DELETE)",
  "location": "Notify Party",
  "confidence": "high"
}

### 학습 예시 3: 복합 수정 패턴
이미지 설명: "LDPE FT4119" 텍스트 옆에 손글씨로 "COMMODITY : LDPE FT4119 QUANTITY : 24.75MT"라고 작성되고 화살표로 연결
분석 결과:
{
  "order": 3,
  "action": "수정",
  "original_text": "LDPE FT4119 QUANTITY. 24.75MT",
  "new_text": "COMMODITY : LDPE FT4119 QUANTITY : 24.75MT",
  "location": "Description of Goods",
  "confidence": "high"
}

### 학습 예시 4: 위치 변경 패턴
이미지 설명: Final Destination 필드의 "NEW YORK, USA" 텍스트가 박스로 표시되고, 화살표가 "ABU DHABI, U.A.E"를 가리킴
분석 결과:
{
  "order": 4,
  "action": "수정",
  "original_text": "NEW YORK, USA",
  "new_text": "ABU DHABI, U.A.E",
  "location": "Final Destination",
  "confidence": "high"
}

### 학습 예시 5: HS CODE 삭제 패턴
이미지 설명: "HS CODE : 39011000" 텍스트가 붉은색 박스로 쳐지고 취소선(~~~ 또는 ---)이 그어짐
분석 결과:
{
  "order": 5,
  "action": "삭제",
  "original_text": "HS CODE : 39011000",
  "new_text": "(DELETE)",
  "location": "No of Containers or Other Pkgs",
  "confidence": "high"
}
"""

# 패턴 인식 가이드
PATTERN_GUIDE = """
## 수정/삭제 패턴 인식 가이드

### 1. 수정(Modification) 패턴의 특징:
✓ 화살표 존재: →, ➔, ⇒, -->, =>
✓ 원본 텍스트 + 화살표 + 새 텍스트 구조
✓ "변경", "수정", "change" 등의 단어
✓ 두 개의 텍스트가 연결됨

### 2. 삭제(Deletion) 패턴의 특징:
✓ 물결표시: ~~~, ≈≈≈
✓ 취소선: ---, ━━━
✓ X 표시: ✕, ✗, ×
✓ "삭제", "delete", "remove" 등의 단어
✓ 박스/동그라미만 있고 화살표 없음

### 3. 손글씨 읽기 팁:
- 대문자와 소문자 구분 주의
- 쉼표(,)와 마침표(.) 구분
- 콜론(:)과 세미콜론(;) 구분
- 숫자 0과 알파벳 O 구분
- 숫자 1과 알파벳 I/l 구분

### 4. 위치(Location) 파악:
- 텍스트가 있는 문서의 섹션/필드명 정확히 파악
- 일반적인 Bill of Lading 필드:
  * Shipper (화주)
  * Consignee (수하인)
  * Notify Party (통지처)
  * Place of Receipt (수령지)
  * Port of Loading (선적항)
  * Port of Discharge (양하항)
  * Final Destination (최종 목적지)
  * Description of Goods (화물 명세)
  * Container Number (컨테이너 번호)
  * Gross Weight (총 중량)
"""

# 정확도 향상을 위한 체크리스트
ACCURACY_CHECKLIST = """
## 분석 정확도 체크리스트

### 반드시 확인해야 할 사항:
1. ✓ 화살표가 있나요? → 수정
2. ✓ 취소선/물결/X표시가 있나요? → 삭제
3. ✓ 손글씨를 정확히 읽었나요?
4. ✓ 대소문자를 구분했나요?
5. ✓ 문장부호를 정확히 인식했나요?
6. ✓ 숫자와 알파벳을 구분했나요?
7. ✓ 원본 텍스트 위치(필드명)를 확인했나요?
8. ✓ 모든 붉은색 마킹을 빠짐없이 찾았나요?

### 흔한 실수 방지:
❌ 화살표가 있는데 삭제로 분류
❌ 손글씨의 일부만 읽음
❌ U.A.E를 U.A.EMIRATES로 잘못 읽음
❌ 쉼표(,)를 빠뜨림
❌ 콜론(:)을 빠뜨림
❌ 위치를 잘못 파악
"""


def get_enhanced_prompt(full_page_text=""):
    """Few-Shot Learning이 적용된 향상된 프롬프트 생성"""
    
    prompt = f"""당신은 Bill of Lading 문서의 수정/삭제 지시사항을 분석하는 전문가입니다.
이미지에 표시된 붉은색 계열의 모든 수정사항을 정확하게 인식해야 합니다.

{SAMPLE_EXAMPLES}

{PATTERN_GUIDE}

{ACCURACY_CHECKLIST}

## 현재 분석 대상 문서:
이 Bill of Lading 문서를 위의 학습 예시를 참고하여 분석하세요.

### 분석 절차:
1. 이미지 전체를 스캔하여 붉은/분홍/주황 계열 마킹을 모두 찾기
2. 각 마킹에 화살표가 있는지 확인 (있으면 수정, 없고 취소선이면 삭제)
3. 박스로 표시된 원본 텍스트를 정확히 읽기
4. 화살표가 가리키는 손글씨를 정확히 읽기 (대소문자, 문장부호 주의)
5. 해당 텍스트가 위치한 문서 필드명 파악
6. 신뢰도 평가 (high/medium/low)

### JSON 출력 형식:
```json
[
  {{
    "order": 1,
    "action": "수정" or "삭제",
    "original_text": "박스로 표시된 원본 텍스트 (정확히)",
    "new_text": "화살표가 가리키는 새 텍스트 (정확히) 또는 (DELETE)",
    "location": "문서 필드명 (정확히)",
    "confidence": "high/medium/low"
  }}
]
```

{f"### 문서 전체 텍스트 (참고):\\n{full_page_text[:1500]}" if full_page_text else ""}

⚠️ 중요: 
- 화살표(→)가 보이면 반드시 "수정"
- 취소선/물결/X표시만 있으면 "삭제"
- 손글씨를 한 글자도 빠뜨리지 말고 정확히 읽기
- 대소문자, 문장부호 정확히 인식
- 모든 붉은색 마킹을 빠짐없이 분석

JSON 배열만 반환하세요."""
    
    return prompt
