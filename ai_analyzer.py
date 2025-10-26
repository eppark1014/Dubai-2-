"""
AI 기반 수정/삭제 지시사항 분석 모듈
Few-Shot Learning 적용
"""
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import json
from few_shot_examples import get_enhanced_prompt

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
        
        # Few-Shot Learning이 적용된 향상된 프롬프트 사용
        prompt = get_enhanced_prompt(full_page_text)

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
                max_tokens=3000,  # 더 자세한 분석을 위해 증가
                temperature=0.1   # 더 일관된 결과를 위해 감소
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
