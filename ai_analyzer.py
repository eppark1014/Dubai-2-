"""
AI 기반 수정/삭제 지시사항 분석 모듈
"""
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()


class AIAnalyzer:
    """OpenAI GPT-4 Vision을 사용하여 손글씨 수정 지시사항을 분석하는 클래스"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.api_key = api_key
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
            print("⚠️  OPENAI_API_KEY가 설정되지 않았습니다. AI 분석 기능이 비활성화됩니다.")
    
    def encode_image(self, image_path):
        """이미지를 base64로 인코딩"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_handwritten_edits(self, image_path, full_page_text=""):
        """
        이미지에서 손글씨 수정/삭제 지시사항 분석
        
        Args:
            image_path: 분석할 이미지 경로
            full_page_text: 전체 페이지 OCR 텍스트 (참고용)
            
        Returns:
            list: 수정/삭제 지시사항 리스트
        """
        if not self.client:
            print("⚠️  OpenAI API 키가 없어 AI 분석을 건너뜁니다.")
            return []
        
        base64_image = self.encode_image(image_path)
        
        prompt = f"""이 이미지는 Bill of Lading (선하증권) 문서입니다.
문서에 붉은색/분홍색/주황색 계열의 손글씨로 수정/삭제 지시사항이 표시되어 있습니다.

⚠️ 중요: 이미지를 매우 자세히 살펴보고 붉은 계열 색상으로 표시된 모든 수정사항을 찾아야 합니다!

**수정 지시사항 패턴:**
- 원본 텍스트 주변에 붉은색 박스/밑줄/동그라미로 표시
- 화살표(→, ➔, ⇒)로 연결하여 새로운 텍스트로 안내
- 화살표 끝에 손글씨로 새로운 텍스트 작성
- 예: [ABU DHABI, U.A.EMIRATES] → ABU DHABI, U.A.E

**삭제 지시사항 패턴:**
- 삭제할 텍스트를 붉은색 박스/취소선으로 표시
- 돼지꼬리(~~~), X표시, 취소선으로 삭제 의도 표시
- 예: [TEL:0574-87170623] ~~~

**분석 단계:**
1. 전체 문서를 스캔하여 붉은/분홍/주황 계열 마킹을 모두 찾기
2. 각 마킹의 종류 파악 (화살표 있음 = 수정, 취소표시 = 삭제)
3. 박스/밑줄로 표시된 원본 텍스트 정확히 읽기
4. 화살표가 가리키는 손글씨 텍스트 읽기 (수정인 경우)
5. 해당 영역이 위치한 문서 필드명 파악

다음 형식의 JSON 배열로 반환:

```json
[
  {{
    "order": 1,
    "action": "수정" or "삭제",
    "original_text": "박스로 표시된 원본 텍스트",
    "new_text": "화살표가 가리키는 새 텍스트 (삭제의 경우 (DELETE))",
    "location": "문서 필드명 (예: Notify Party, Place of Receipt, Port of Loading, Final Destination, Shipper, Description of Goods 등)",
    "confidence": "high/medium/low"
  }}
]
```

**반드시 확인할 영역:**
- Shipper (화주) 정보 영역
- Consignee (수하인) 정보 영역  
- Notify Party (통지처) 영역
- Place of Receipt (수령지) 영역
- Port of Loading (선적항) 영역
- Port of Discharge (양하항) 영역
- Final Destination (최종 목적지) 영역
- Description of Goods (화물 명세) 영역
- Container Number 영역
- 기타 텍스트 영역

{f"참고: 전체 문서 텍스트: {full_page_text[:1000]}" if full_page_text else ""}

⚠️ 이미지에서 붉은 계열 색상의 마킹이 하나라도 보이면 반드시 분석하여 결과에 포함시켜야 합니다!
빈 배열 []을 반환하지 말고, 보이는 모든 수정사항을 JSON 배열로 반환하세요."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2000,
                temperature=0.2
            )
            
            result_text = response.choices[0].message.content
            
            # JSON 추출 (코드 블록 제거)
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            # JSON 파싱
            edits = json.loads(result_text.strip())
            
            return edits
            
        except Exception as e:
            print(f"AI 분석 오류: {str(e)}")
            return []
    
    def format_as_table(self, edits):
        """
        분석 결과를 표 형식으로 변환
        
        Args:
            edits: 수정/삭제 지시사항 리스트
            
        Returns:
            dict: 표 형식 데이터
        """
        return {
            "headers": ["순번", "지시사항", "대상문구", "변환문구", "위치"],
            "rows": [
                {
                    "order": edit.get("order", i + 1),
                    "action": edit.get("action", ""),
                    "original_text": edit.get("original_text", ""),
                    "new_text": edit.get("new_text", ""),
                    "location": edit.get("location", ""),
                    "confidence": edit.get("confidence", "medium")
                }
                for i, edit in enumerate(edits)
            ]
        }
