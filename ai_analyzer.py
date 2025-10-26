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
문서 위에 붉은색 손글씨로 수정/삭제 지시사항이 표시되어 있습니다.

**수정 지시사항 패턴:**
- 수정할 텍스트를 붉은색 박스로 표시
- 화살표(→)로 연결
- 화살표 끝에 새로운 텍스트를 손글씨로 작성

**삭제 지시사항 패턴:**
- 삭제할 텍스트를 붉은색 박스로 표시
- 돼지꼬리 표시 (물결표시, 취소선)로 삭제 의도 표시

다음 정보를 JSON 배열로 추출해주세요:

```json
[
  {{
    "order": 1,
    "action": "수정" or "삭제",
    "original_text": "원본 텍스트",
    "new_text": "변경될 텍스트 (삭제의 경우 (DELETE))",
    "location": "문서상의 위치 (예: Notify Party, Place of Receipt)",
    "confidence": "high/medium/low"
  }}
]
```

**중요:**
1. 붉은색 계열 유채색으로 표시된 모든 수정/삭제 사항을 찾으세요
2. 화살표가 있으면 '수정', 돼지꼬리/취소 표시가 있으면 '삭제'입니다
3. 손글씨를 꼼꼼히 읽고 정확한 텍스트를 추출하세요
4. location은 해당 텍스트가 위치한 문서의 필드명/컬럼명입니다
5. 순번(order)은 문서 위에서 아래로 순서대로 부여하세요

{f"참고: 전체 문서 텍스트: {full_page_text[:1000]}" if full_page_text else ""}

JSON 배열만 반환해주세요."""

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
