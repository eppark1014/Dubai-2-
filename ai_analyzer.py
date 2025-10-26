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
    """OpenAI GPT-5 Nano를 사용하여 손글씨 수정 지시사항을 분석하는 클래스"""
    
    def __init__(self, model="gpt-5-nano-2025-08-07"):
        """
        Args:
            model: 사용할 모델 (기본값: gpt-5-nano-2025-08-07)
                   - gpt-5-nano-2025-08-07: 최신 GPT-5 Nano 모델 (400K context, $0.05/$0.40 per 1M tokens)
                   - gpt-4o: 더 강력하지만 비쌈 (이전 모델)
        """
        api_key = os.getenv('OPENAI_API_KEY')
        self.api_key = api_key
        self.model = model
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
        print("🤖 AI 분석 시작...")
        
        if not self.client:
            print("⚠️  OpenAI API 키가 없어 AI 분석을 건너뜁니다.")
            return []
        
        print("📷 이미지 인코딩 중...")
        base64_image = self.encode_image(image_path)
        print(f"✅ 이미지 인코딩 완료 (크기: {len(base64_image)} bytes)")
        
        # Few-Shot Learning이 적용된 향상된 프롬프트 사용
        print("📝 프롬프트 생성 중...")
        prompt = get_enhanced_prompt(full_page_text)
        print(f"✅ 프롬프트 생성 완료 (길이: {len(prompt)} 자)")

        try:
            print(f"🌐 OpenAI API 호출 중... (모델: {self.model}, 최대 120초 소요)")
            response = self.client.chat.completions.create(
                model=self.model,
                timeout=120.0,  # 2분 타임아웃 설정
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
            
            print("✅ OpenAI API 응답 받음")
            result_text = response.choices[0].message.content
            print(f"📄 응답 길이: {len(result_text)} 자")
            
            # JSON 추출 (코드 블록 제거)
            print("🔍 JSON 추출 중...")
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            # JSON 파싱
            print("📊 JSON 파싱 중...")
            edits = json.loads(result_text.strip())
            print(f"✅ AI 분석 완료! {len(edits)}개 항목 발견")
            
            return edits
            
        except Exception as e:
            print(f"❌ AI 분석 오류: {str(e)}")
            import traceback
            traceback.print_exc()
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
