#!/usr/bin/env python3
"""
GPT-5 Nano 마이그레이션 간단 테스트 (비대화형)
"""
import os
import time
from ai_analyzer import AIAnalyzer
from image_analyzer import ImageAnalyzer

def main():
    print("\n" + "="*70)
    print("GPT-5 Nano 마이그레이션 테스트")
    print("="*70)
    
    # 테스트 1: 모델 초기화
    print("\n[1] 모델 초기화 테스트")
    print("-" * 70)
    
    analyzer_default = AIAnalyzer()
    print(f"✅ 기본 모델: {analyzer_default.model}")
    assert analyzer_default.model == "gpt-5-nano", "기본 모델이 gpt-5-nano가 아닙니다!"
    
    analyzer_gpt4 = AIAnalyzer(model="gpt-4o")
    print(f"✅ GPT-4o 모델: {analyzer_gpt4.model}")
    assert analyzer_gpt4.model == "gpt-4o", "모델 파라미터가 전달되지 않았습니다!"
    
    print("✅ 초기화 테스트 통과!")
    
    # 테스트 2: 실제 이미지로 API 호출
    print("\n[2] GPT-5 Nano API 호출 테스트")
    print("-" * 70)
    
    # 사용 가능한 첫 번째 이미지 찾기
    test_image = None
    possible_paths = [
        "./output/0ae62426/page_1.png",
        "./output/26003229/page_1.png",
        "./output/ed734e5b/page_1.png"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            test_image = path
            break
    
    if not test_image:
        print("⚠️  테스트 이미지를 찾을 수 없습니다.")
        print("⚠️  실제 API 호출 테스트는 건너뜁니다.")
        print("\n✅ 기본 테스트 완료! (API 키 확인 필요)")
        return
    
    print(f"📄 테스트 이미지: {test_image}")
    
    # OCR
    img_analyzer = ImageAnalyzer(test_image)
    full_text = img_analyzer.get_full_page_text()
    print(f"📝 OCR 텍스트 길이: {len(full_text)} 자")
    
    # GPT-5 Nano 분석
    print("\n🚀 GPT-5 Nano 분석 시작...")
    start_time = time.time()
    
    ai_analyzer = AIAnalyzer(model="gpt-5-nano")
    edits = ai_analyzer.analyze_handwritten_edits(test_image, full_text)
    
    elapsed = time.time() - start_time
    
    print(f"\n✅ 분석 완료!")
    print(f"⏱️  소요 시간: {elapsed:.2f}초")
    print(f"📊 결과: {len(edits)}개 수정사항 발견")
    
    if edits:
        print("\n📋 첫 3개 결과:")
        for i, edit in enumerate(edits[:3], 1):
            action = edit.get('action', 'N/A')
            original = edit.get('original_text', 'N/A')
            new = edit.get('new_text', 'N/A')
            confidence = edit.get('confidence', 'N/A')
            
            print(f"\n  [{i}] {action}")
            print(f"      원본: {original[:60]}{'...' if len(original) > 60 else ''}")
            if action == "수정":
                print(f"      변환: {new[:60]}{'...' if len(new) > 60 else ''}")
            print(f"      신뢰도: {confidence}")
    
    print("\n" + "="*70)
    print("✅ 모든 테스트 통과!")
    print("="*70)
    print(f"\n📊 요약:")
    print(f"   - 기본 모델: gpt-5-nano")
    print(f"   - API 호출: 성공")
    print(f"   - 응답 시간: {elapsed:.2f}초")
    print(f"   - 결과 개수: {len(edits)}개")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
