"""
간소화된 Few-Shot Learning 예시
3가지 핵심 패턴만 학습
"""

SIMPLIFIED_PATTERN_GUIDE = """
## 🎯 **핵심 규칙: 3가지 패턴만 인식하세요!**

### ✅ **패턴 A: 삭제 (박스/동그라미 + 돼지꼬리)**
**시각적 특징:**
- 텍스트가 박스 또는 동그라미로 둘러싸여 있음
- 취소선, 물결선, 또는 돼지꼬리 표시가 있음
- 색상: 빨강, 주황, 분홍 등

**JSON 형식:**
```json
{
  "order": 1,
  "action": "삭제",
  "original_text": "삭제할 텍스트",
  "new_text": "(DELETE)",
  "location": "위치",
  "confidence": "high"
}
```

---

### ✅ **패턴 B: 수정 (박스 + 화살표 → 손글씨/박스)**
**시각적 특징:**
- 기존 텍스트가 박스로 표시됨
- 화살표(→, ⇒, ➡️)가 있음
- 화살표 끝에 손글씨 또는 다른 박스가 있음

**JSON 형식:**
```json
{
  "order": 2,
  "action": "수정",
  "original_text": "원본 텍스트",
  "new_text": "변경할 텍스트",
  "location": "위치",
  "confidence": "high"
}
```

---

### ✅ **패턴 C: 교체 대상 (동그라미/박스 단독 + 다른 곳 화살표)**
**시각적 특징:**
- 동그라미 또는 박스만 단독으로 있음
- 이것이 대체 텍스트(목표값)임
- 다른 곳에서 이쪽으로 오는 화살표가 있음

**JSON 형식:**
```json
{
  "order": 3,
  "action": "수정",
  "original_text": "화살표 출발점의 텍스트",
  "new_text": "이 박스 안의 텍스트",
  "location": "위치",
  "confidence": "medium"
}
```

---

## ⚠️ **중요: 무시해야 하는 경우**

### ❌ **강조 표시 (아무 것도 하지 마세요!)**
- 박스나 동그라미만 있고
- 화살표 없음
- 취소선/물결선 없음
- 손글씨 없음
→ **이것은 강조일 뿐! JSON에 포함하지 마세요!**

예시: "FREIGHT PREPAID", "AS ARRANGED" 등이 박스로만 둘러싸여 있으면 무시!

---

## 📝 **병렬 텍스트 처리 규칙**

### **여러 줄이 하나의 박스 안에 있으면:**
→ **순번 1개에 모든 내용을 넣으세요!**
→ 줄바꿈은 `\\n`으로 구분

**예시:**
```
박스 안:
TEL: 123-456
FAX: 789-012
EMAIL: test@example.com
```

**JSON 결과:**
```json
{
  "order": 1,
  "action": "삭제",
  "original_text": "TEL: 123-456\\nFAX: 789-012\\nEMAIL: test@example.com",
  "new_text": "(DELETE)",
  "location": "Contact Info",
  "confidence": "high"
}
```

---
"""

SIMPLIFIED_EXAMPLES = """
## 📚 **학습 예시**

### 예시 1: 패턴 A - 삭제 (박스 + 취소선)
**이미지:**
- "YANGPU, HAINAN, CHINA"가 빨간 박스로 둘러싸여 있음
- 텍스트에 물결선(~~~~~) 또는 취소선이 그어져 있음

**결과:**
```json
{
  "order": 1,
  "action": "삭제",
  "original_text": "YANGPU, HAINAN, CHINA",
  "new_text": "(DELETE)",
  "location": "Port of Loading",
  "confidence": "high"
}
```

---

### 예시 2: 패턴 B - 수정 (박스 + 화살표)
**이미지:**
- "JEBEL ALI"가 빨간 박스로 둘러싸여 있음
- 화살표(→)가 "DUBAI"로 연결됨

**결과:**
```json
{
  "order": 1,
  "action": "수정",
  "original_text": "JEBEL ALI",
  "new_text": "DUBAI",
  "location": "Port of Discharge",
  "confidence": "high"
}
```

---

### 예시 3: 패턴 A - 여러 줄 삭제 (병렬 텍스트)
**이미지:**
- 하나의 큰 빨간 박스 안에 4줄이 있음:
  ```
  USCI: 91330000MA28BUPEXXX
  CONTACT PERSON NAME: MIKE
  CONTACT PERSON TEL: +86-12345678
  EMAIL: test@example.com
  ```
- 취소선 또는 물결선이 있음

**결과:**
```json
{
  "order": 1,
  "action": "삭제",
  "original_text": "USCI: 91330000MA28BUPEXXX\\nCONTACT PERSON NAME: MIKE\\nCONTACT PERSON TEL: +86-12345678\\nEMAIL: test@example.com",
  "new_text": "(DELETE)",
  "location": "Shipper Info",
  "confidence": "high"
}
```

⚠️ **중요**: 여러 줄이 하나의 박스에 있으면 → 1개의 JSON 항목으로!

---

### 예시 4: 패턴 C - 대체 텍스트 (화살표 목표)
**이미지:**
- "ABU DHABI"가 빨간 박스로 표시됨 (화살표 출발점)
- 화살표(→)가 있음
- 화살표 끝에 "DUBAI"가 동그라미로 표시됨

**결과:**
```json
{
  "order": 1,
  "action": "수정",
  "original_text": "ABU DHABI",
  "new_text": "DUBAI",
  "location": "Destination",
  "confidence": "high"
}
```

---

### 예시 5: ❌ 무시 - 강조 표시
**이미지:**
- "FREIGHT PREPAID"가 빨간 박스로만 둘러싸여 있음
- 화살표 없음
- 취소선 없음
- 손글씨 없음

**결과:**
```json
[]
```

⚠️ 이것은 강조일 뿐! 아무것도 반환하지 마세요!

---
"""

def get_simplified_prompt(full_page_text=""):
    """간소화된 프롬프트 생성"""
    
    base_instruction = f"""
당신은 Bill of Lading 문서의 손글씨 수정 지시사항을 분석하는 전문가입니다.

## 🎯 **당신의 임무**
이미지에서 **붉은색 계열 손글씨 수정 지시사항**을 찾아 JSON 배열로 반환하세요.

## ✅ **인식해야 하는 3가지 패턴**

### 패턴 A: 삭제 (박스/동그라미 + 돼지꼏리)
- 박스 또는 동그라미로 둘러싸인 텍스트
- 취소선, 물결선, 또는 돼지꼬리 표시
- action: "삭제", new_text: "(DELETE)"

### 패턴 B: 수정 (박스 + 화살표 → 손글씨/박스)
- 박스로 표시된 기존 텍스트
- 화살표가 새로운 텍스트로 연결
- action: "수정", new_text: 화살표 끝의 텍스트

### 패턴 C: 교체 대상 (동그라미/박스 단독 + 다른 곳 화살표)
- 동그라미나 박스만 단독으로 있음
- 다른 곳에서 이쪽으로 화살표가 옴
- 이것이 대체 텍스트(목표값)
- action: "수정", original_text: 화살표 출발점, new_text: 이 박스 내용

## ❌ **무시해야 하는 경우**
- 박스/동그라미만 있고 화살표, 취소선, 손글씨가 전혀 없으면 → 강조 표시! 무시!

## 📝 **병렬 텍스트 규칙**
- 하나의 박스 안에 여러 줄이 있으면 → 1개의 JSON 항목에 모두 포함
- 줄바꿈은 \\n으로 구분
- 예: "Line1\\nLine2\\nLine3"

{SIMPLIFIED_PATTERN_GUIDE}

{SIMPLIFIED_EXAMPLES}

## 📄 **OCR 추출 텍스트 (참고용)**
```
{full_page_text[:2000] if full_page_text else "N/A"}
```

## 📤 **출력 형식**
반드시 다음 형식의 JSON 배열만 반환하세요:

```json
[
  {{
    "order": 1,
    "action": "삭제" 또는 "수정",
    "original_text": "원본 텍스트",
    "new_text": "새 텍스트 또는 (DELETE)",
    "location": "문서 내 위치",
    "confidence": "high/medium/low"
  }}
]
```

**중요:**
- 패턴 A, B, C에 해당하는 것만 반환
- 강조 표시는 무시 (JSON에 포함하지 마세요)
- 여러 줄은 하나의 항목으로 병합
- 확실하지 않으면 confidence를 "medium" 또는 "low"로 설정

이제 이미지를 분석하고 JSON 배열만 반환하세요.
"""
    
    return base_instruction.strip()
