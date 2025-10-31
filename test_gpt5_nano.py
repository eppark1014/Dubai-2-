#!/usr/bin/env python3
"""
GPT-5 Nano 마이그레이션 테스트
- 모델 파라미터 확인
- API 호출 검증
- 성능 비교 (GPT-4o vs GPT-5 Nano)
"""
import os
import sys
import time
from ai_analyzer import AIAnalyzer
from image_analyzer import ImageAnalyzer

def test_model_initialization():
    """모델 초기화 테스트"""
    print("\n" + "="*70)
    print("테스트 1: 모델 초기화 확인")
    print("="*70)
    
    # 기본값 (gpt-5-nano)
    analyzer1 = AIAnalyzer()
    print(f"✅ 기본 모델: {analyzer1.model}")
    assert analyzer1.model == "gpt-5-nano", "기본 모델이 gpt-5-nano가 아닙니다!"
    
    # 명시적으로 gpt-4o 지정
    analyzer2 = AIAnalyzer(model="gpt-4o")
    print(f"✅ 지정 모델: {analyzer2.model}")
    assert analyzer2.model == "gpt-4o", "모델 파라미터가 제대로 전달되지 않았습니다!"
    
    # 커스텀 모델명
    analyzer3 = AIAnalyzer(model="gpt-4o-mini")
    print(f"✅ 커스텀 모델: {analyzer3.model}")
    assert analyzer3.model == "gpt-4o-mini", "커스텀 모델명이 전달되지 않았습니다!"
    
    print("\n✅ 모든 초기화 테스트 통과!")

def test_api_call_with_gpt5_nano():
    """GPT-5 Nano API 호출 테스트"""
    print("\n" + "="*70)
    print("테스트 2: GPT-5 Nano API 호출")
    print("="*70)
    
    # 테스트 이미지 경로
    test_image = "/home/user/webapp/test_images/single_box_arrow_simple.png"
    
    if not os.path.exists(test_image):
        print(f"⚠️  테스트 이미지가 없습니다: {test_image}")
        print("⚠️  다른 이미지로 테스트하려면 경로를 수정하세요.")
        return
    
    # OCR로 전체 텍스트 추출
    print(f"📄 이미지: {test_image}")
    img_analyzer = ImageAnalyzer(test_image)
    full_text = img_analyzer.get_full_page_text()
    print(f"📝 OCR 텍스트 길이: {len(full_text)} 자")
    
    # GPT-5 Nano로 분석
    print("\n🚀 GPT-5 Nano 분석 시작...")
    start_time = time.time()
    
    ai_analyzer = AIAnalyzer(model="gpt-5-nano")
    edits = ai_analyzer.analyze_handwritten_edits(test_image, full_text)
    
    elapsed = time.time() - start_time
    
    print(f"\n✅ 분석 완료!")
    print(f"⏱️  소요 시간: {elapsed:.2f}초")
    print(f"📊 결과: {len(edits)}개 수정사항 발견")
    
    if edits:
        print("\n📋 분석 결과:")
        for i, edit in enumerate(edits, 1):
            print(f"\n  [{i}] {edit.get('action', 'N/A')}")
            print(f"      원본: {edit.get('original_text', 'N/A')[:50]}...")
            print(f"      변환: {edit.get('new_text', 'N/A')[:50]}...")
            print(f"      신뢰도: {edit.get('confidence', 'N/A')}")
    
    return elapsed, len(edits)

def compare_models():
    """GPT-4o vs GPT-5 Nano 성능 비교"""
    print("\n" + "="*70)
    print("테스트 3: 모델 성능 비교 (GPT-4o vs GPT-5 Nano)")
    print("="*70)
    
    test_image = "/home/user/webapp/test_images/single_box_arrow_simple.png"
    
    if not os.path.exists(test_image):
        print(f"⚠️  테스트 이미지가 없습니다: {test_image}")
        print("⚠️  성능 비교를 건너뜁니다.")
        return
    
    # OCR
    img_analyzer = ImageAnalyzer(test_image)
    full_text = img_analyzer.get_full_page_text()
    
    results = {}
    
    # 각 모델 테스트
    for model_name in ["gpt-4o", "gpt-5-nano"]:
        print(f"\n📊 {model_name} 테스트...")
        start_time = time.time()
        
        analyzer = AIAnalyzer(model=model_name)
        edits = analyzer.analyze_handwritten_edits(test_image, full_text)
        
        elapsed = time.time() - start_time
        results[model_name] = {
            "time": elapsed,
            "count": len(edits),
            "edits": edits
        }
        
        print(f"   ⏱️  소요 시간: {elapsed:.2f}초")
        print(f"   📊 결과 개수: {len(edits)}개")
    
    # 결과 비교
    print("\n" + "="*70)
    print("비교 결과:")
    print("="*70)
    
    gpt4_time = results["gpt-4o"]["time"]
    gpt5_time = results["gpt-5-nano"]["time"]
    speedup = gpt4_time / gpt5_time if gpt5_time > 0 else 0
    
    print(f"⏱️  GPT-4o 속도:      {gpt4_time:.2f}초")
    print(f"⏱️  GPT-5 Nano 속도:  {gpt5_time:.2f}초")
    print(f"🚀 속도 향상:         {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")
    
    print(f"\n📊 GPT-4o 결과:      {results['gpt-4o']['count']}개")
    print(f"📊 GPT-5 Nano 결과:  {results['gpt-5-nano']['count']}개")
    
    # 결과 일치 여부 확인
    if results["gpt-4o"]["count"] == results["gpt-5-nano"]["count"]:
        print("✅ 결과 개수 일치!")
    else:
        print("⚠️  결과 개수 불일치 (품질 차이 가능)")

def main():
    """메인 테스트 실행"""
    print("\n" + "="*70)
    print("GPT-5 Nano 마이그레이션 테스트 시작")
    print("="*70)
    
    try:
        # 테스트 1: 초기화
        test_model_initialization()
        
        # 테스트 2: API 호출
        test_api_call_with_gpt5_nano()
        
        # 테스트 3: 성능 비교 (선택적)
        user_input = input("\n❓ GPT-4o와 성능 비교를 진행하시겠습니까? (y/N): ").strip().lower()
        if user_input == 'y':
            compare_models()
        else:
            print("⏩ 성능 비교 건너뜀")
        
        print("\n" + "="*70)
        print("✅ 모든 테스트 완료!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
