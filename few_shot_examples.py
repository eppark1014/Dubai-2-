"""
Few-Shot Learning을 위한 최적화된 샘플 데이터
핵심 패턴만 포함하여 성능 향상
"""

# 핵심 샘플 예시 (간결화)
CORE_EXAMPLES = """
### 예시 1: 박스 + 화살표 = 수정 (핵심!)
- 박스 안 텍스트 = original_text
- 화살표 끝 텍스트 = new_text (손글씨 또는 타이핑)
- 박스 형태: 직사각형/타원/원형/불규칙 (모두 OK)
- 화살표 방향: 상/하/좌/우/곡선 (모두 OK)
- 색상: 붉은색 계열 (모두 OK)

예: "KHALIFA PORT, ABU DHABI, UAE" 박스 → 화살표 → "KHALIFA PORT, U.A.E" 손글씨
→ action="수정", original="KHALIFA PORT, ABU DHABI, UAE", new="KHALIFA PORT, U.A.E"

### 예시 2: 취소선/물결선 = 삭제 (최우선!)
- 취소선(---, ━━━) 또는 물결선(~~~) = 100% 삭제
- 화살표 있어도 취소선 있으면 = 삭제

예: "14 DAYS CONTAINER FREE..." 위에 ~~~
→ action="삭제", new_text="(DELETE)"

### 예시 3: NOTIFY PARTY 연락처 삭제 (자주 누락!)
각 줄마다 별도 박스 + 물결선 = 각각 독립 삭제 항목
- USCI: 91330212MA28840CY4D
- CONTACT PERSON NAME: MS. JOY SHAO
- CONTACT PERSON TEL: 86-574-88291892
- EMAIL: JOYSHAO@CHISAGE.COM
→ 4개의 별도 JSON 객체

### 예시 4: 여러 줄 텍스트
박스 안 여러 줄 = 모두 읽고 \\n으로 구분
예: "TEL:0574-87170623\\nFAX:0574-87026831"
"""

# 핵심 규칙 (간결화)
CORE_RULES = """
## 우선순위 (순서대로 확인!)

### 1순위: 취소선/물결선 = 삭제
- 텍스트 위에 ---, ~~~, ━━━ → 무조건 "삭제"
- 여러 개 있으면 각각 별도 항목

### 2순위: 박스 + 화살표 = 수정
- 형태/방향/색상 무관
- 박스 안 = original_text
- 화살표 끝 = new_text

### 3순위: 번호 표시 = 수정
- #1, #2, #20 등 → 주변 텍스트 읽기

## 필수 확인 항목
1. NOTIFY PARTY 하단: USCI, CONTACT PERSON NAME, TEL, EMAIL (4개)
2. "14 DAYS CONTAINER FREE..." 텍스트
3. 모든 박스 + 화살표 패턴
"""


def get_enhanced_prompt(full_page_text=""):
    """최적화된 프롬프트 생성"""
    
    prompt = f"""Bill of Lading 문서의 수정/삭제 지시사항을 분석하세요.

{CORE_EXAMPLES}

{CORE_RULES}

## 분석 절차
1. 취소선/물결선 찾기 → 삭제
2. 박스 + 화살표 찾기 → 수정
3. 번호 표시 찾기 → 수정
4. NOTIFY PARTY 하단 4개 연락처 확인 (자주 누락!)

## JSON 출력 형식
```json
[
  {{
    "order": 1,
    "action": "수정" or "삭제",
    "original_text": "박스 안 텍스트",
    "new_text": "화살표 끝 텍스트 or (DELETE)",
    "location": "필드명",
    "confidence": "high/medium/low"
  }}
]
```

핵심:
- 취소선/물결선 = 100% 삭제
- 박스 + 화살표 = 100% 수정
- NOTIFY PARTY 연락처 4개 = 각각 별도 항목
- 여러 줄 = \\n으로 구분

{f"참고 텍스트:\\n{full_page_text[:500]}" if full_page_text else ""}

JSON 배열만 반환하세요."""
    
    return prompt
