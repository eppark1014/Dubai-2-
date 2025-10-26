#!/usr/bin/env python3
"""
GPT-5 Nano API 직접 테스트
- 실제 API 호출 테스트
- 응답 확인
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_simple_call():
    """간단한 텍스트 응답 테스트"""
    print("\n" + "="*70)
    print("GPT-5 Nano 2025-08-07 직접 API 테스트")
    print("="*70)
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ API 키가 설정되지 않았습니다!")
        return
    
    print(f"\n✅ API 키: {api_key[:20]}...{api_key[-10:]}")
    
    client = OpenAI(api_key=api_key)
    
    # 테스트 1: 간단한 텍스트 응답
    print("\n[테스트 1] 간단한 텍스트 응답")
    print("-" * 70)
    
    try:
        print("🌐 API 호출 중...")
        response = client.chat.completions.create(
            model="gpt-5-nano-2025-08-07",
            messages=[
                {"role": "user", "content": "Say 'Hello, GPT-5 Nano!' and nothing else."}
            ],
            max_completion_tokens=50
        )
        
        print("✅ 응답 받음!")
        message = response.choices[0].message
        content = message.content
        
        print(f"\n📋 Message 객체 전체:")
        print(f"   - content: {content}")
        print(f"   - role: {message.role}")
        print(f"   - refusal: {getattr(message, 'refusal', 'N/A')}")
        print(f"   - tool_calls: {getattr(message, 'tool_calls', 'N/A')}")
        
        if content:
            print(f"\n📄 응답: {content}")
            print(f"📊 응답 길이: {len(content)} 자")
        else:
            print("\n⚠️ 응답이 None 또는 빈 문자열입니다!")
            
        print(f"\n📋 전체 응답 객체:")
        print(f"   - Model: {response.model}")
        print(f"   - Finish Reason: {response.choices[0].finish_reason}")
        print(f"   - Usage: {response.usage}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # 테스트 2: JSON 응답
    print("\n[테스트 2] JSON 형식 응답")
    print("-" * 70)
    
    try:
        print("🌐 API 호출 중...")
        response = client.chat.completions.create(
            model="gpt-5-nano-2025-08-07",
            messages=[
                {"role": "user", "content": 'Return a JSON object: {"status": "ok", "message": "test"}'}
            ],
            max_completion_tokens=100
        )
        
        print("✅ 응답 받음!")
        content = response.choices[0].message.content
        
        if content:
            print(f"📄 응답: {content}")
            print(f"📊 응답 길이: {len(content)} 자")
        else:
            print("⚠️ 응답이 None 또는 빈 문자열입니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "="*70)
    print("✅ 모든 테스트 완료!")
    print("="*70)
    return True

if __name__ == "__main__":
    test_simple_call()
