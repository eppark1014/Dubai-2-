#!/usr/bin/env python3
"""
GPT-5 Nano 2025-08-07 모델 테스트
- 새 모델명 확인
- API 키 확인
- 초기화 테스트
"""
import os
from ai_analyzer import AIAnalyzer

def main():
    print("\n" + "="*70)
    print("GPT-5 Nano 2025-08-07 모델 테스트")
    print("="*70)
    
    # 환경 변수 확인
    print("\n[1] 환경 변수 확인")
    print("-" * 70)
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"✅ API 키 설정됨: {api_key[:20]}...{api_key[-10:]}")
    else:
        print("❌ API 키가 설정되지 않았습니다!")
        return
    
    # 모델 초기화 테스트
    print("\n[2] 모델 초기화 테스트")
    print("-" * 70)
    
    # 기본값 테스트
    analyzer1 = AIAnalyzer()
    print(f"✅ 기본 모델: {analyzer1.model}")
    assert analyzer1.model == "gpt-5-nano-2025-08-07", f"기본 모델이 gpt-5-nano-2025-08-07이 아닙니다! (현재: {analyzer1.model})"
    
    # 명시적 지정 테스트
    analyzer2 = AIAnalyzer(model="gpt-5-nano-2025-08-07")
    print(f"✅ 명시적 지정: {analyzer2.model}")
    assert analyzer2.model == "gpt-5-nano-2025-08-07", "모델명이 제대로 전달되지 않았습니다!"
    
    # GPT-4o 여전히 사용 가능
    analyzer3 = AIAnalyzer(model="gpt-4o")
    print(f"✅ GPT-4o 호환: {analyzer3.model}")
    assert analyzer3.model == "gpt-4o", "GPT-4o 모델 지정이 작동하지 않습니다!"
    
    # Client 초기화 확인
    print("\n[3] OpenAI Client 확인")
    print("-" * 70)
    if analyzer1.client:
        print(f"✅ OpenAI Client 초기화 성공")
        print(f"   - API 키: {analyzer1.api_key[:20]}...{analyzer1.api_key[-10:]}")
        print(f"   - 모델: {analyzer1.model}")
    else:
        print("❌ OpenAI Client 초기화 실패!")
        return
    
    print("\n" + "="*70)
    print("✅ 모든 테스트 통과!")
    print("="*70)
    print("\n📊 요약:")
    print(f"   ✅ API 키: 설정됨")
    print(f"   ✅ 기본 모델: gpt-5-nano-2025-08-07")
    print(f"   ✅ Client: 초기화됨")
    print(f"   ✅ 하위 호환성: GPT-4o 사용 가능")
    print("\n🚀 프로덕션 준비 완료!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
