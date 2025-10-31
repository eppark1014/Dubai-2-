#!/usr/bin/env python3
"""
간소화된 프롬프트 테스트
- 3가지 핵심 패턴만 인식
- 프롬프트 길이 확인
"""
import os
from ai_analyzer import AIAnalyzer
from image_analyzer import ImageAnalyzer
from few_shot_examples_simplified import get_simplified_prompt

def test_prompt_length():
    """프롬프트 길이 확인"""
    print("\n" + "="*70)
    print("프롬프트 길이 비교")
    print("="*70)
    
    # 간소화된 프롬프트
    simplified = get_simplified_prompt("Sample OCR text")
    print(f"\n✅ 간소화된 프롬프트:")
    print(f"   - 길이: {len(simplified)} 자")
    print(f"   - 토큰 추정: ~{len(simplified.split())} 단어")
    
    # 기존 프롬프트 (비교)
    try:
        from few_shot_examples import get_enhanced_prompt
        enhanced = get_enhanced_prompt("Sample OCR text")
        print(f"\n📊 기존 프롬프트:")
        print(f"   - 길이: {len(enhanced)} 자")
        print(f"   - 토큰 추정: ~{len(enhanced.split())} 단어")
        
        reduction = ((len(enhanced) - len(simplified)) / len(enhanced)) * 100
        print(f"\n🎯 감소율: {reduction:.1f}%")
    except:
        print("\n⚠️ 기존 프롬프트 비교 불가")

def test_with_real_image():
    """실제 이미지로 테스트"""
    print("\n" + "="*70)
    print("실제 이미지 분석 테스트")
    print("="*70)
    
    # 테스트 이미지 찾기
    test_images = [
        "output/0ae62426/page_1.png",
        "output/26003229/page_1.png",
        "output/ed734e5b/page_1.png"
    ]
    
    test_image = None
    for img_path in test_images:
        if os.path.exists(img_path):
            test_image = img_path
            break
    
    if not test_image:
        print("❌ 테스트 이미지를 찾을 수 없습니다.")
        return
    
    print(f"\n📄 테스트 이미지: {test_image}")
    
    # OCR 텍스트 추출
    img_analyzer = ImageAnalyzer(test_image)
    full_text = img_analyzer.get_full_page_text()
    print(f"📝 OCR 텍스트 길이: {len(full_text)} 자")
    
    # AI 분석
    print("\n🤖 간소화된 프롬프트로 AI 분석 시작...")
    ai_analyzer = AIAnalyzer(model="gpt-4o-mini")
    edits = ai_analyzer.analyze_handwritten_edits(test_image, full_text)
    
    print(f"\n✅ 분석 완료! {len(edits)}개 수정사항 발견")
    
    if edits:
        print("\n📋 분석 결과:")
        for i, edit in enumerate(edits, 1):
            print(f"\n  [{i}] {edit.get('action', 'N/A')}")
            print(f"      원본: {edit.get('original_text', 'N/A')[:80]}...")
            if edit.get('action') == "수정":
                print(f"      변환: {edit.get('new_text', 'N/A')[:80]}...")
            print(f"      위치: {edit.get('location', 'N/A')}")
            print(f"      신뢰도: {edit.get('confidence', 'N/A')}")
    else:
        print("\n⚠️ 수정사항이 발견되지 않았습니다.")

def main():
    """메인 테스트 함수"""
    print("\n" + "="*70)
    print("간소화된 프롬프트 테스트 시작")
    print("="*70)
    print("\n🎯 목표: 3가지 핵심 패턴만 인식")
    print("   - 패턴 A: 삭제 (박스 + 돼지꼬리)")
    print("   - 패턴 B: 수정 (박스 + 화살표 → 손글씨)")
    print("   - 패턴 C: 교체 대상 (동그라미/박스 단독 + 화살표)")
    
    try:
        # 테스트 1: 프롬프트 길이 확인
        test_prompt_length()
        
        # 테스트 2: 실제 이미지 분석
        test_with_real_image()
        
        print("\n" + "="*70)
        print("✅ 테스트 완료!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
