"""
AI 기반 수정/삭제 지시사항 분석 모듈
Few-Shot Learning 적용
"""
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
import json
from few_shot_examples_simplified import get_simplified_prompt

load_dotenv()


class AIAnalyzer:
    """OpenAI GPT-5 Nano를 사용하여 손글씨 수정 지시사항을 분석하는 클래스"""
    
    def __init__(self, model="gpt-4o-mini"):
        """
        Args:
            model: 사용할 모델 (기본값: gpt-4o-mini)
                   - gpt-4o-mini: 빠르고 저렴한 모델 (128K context, $0.15/$0.60 per 1M tokens)
                   - gpt-4o: 더 강력한 모델 (128K context, 더 비쌈)
                   - gpt-5-nano-2025-08-07: GPT-5 Nano (현재 사용 불가 - 빈 응답 반환)
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
        
        # 간소화된 Few-Shot Learning 프롬프트 사용 (3가지 핵심 패턴만)
        print("📝 프롬프트 생성 중... (간소화된 버전)")
        prompt = get_simplified_prompt(full_page_text)
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
            if result_text is None:
                result_text = ""
                print("⚠️ 응답이 None입니다! 빈 문자열로 처리합니다.")
            print(f"📄 응답 길이: {len(result_text)} 자")
            if len(result_text) > 0:
                print(f"📝 응답 미리보기: {result_text[:200]}...")
            
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
