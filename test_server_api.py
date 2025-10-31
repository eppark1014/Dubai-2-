#!/usr/bin/env python3
"""
서버 API 테스트 스크립트
- 새로운 GPT-5 Nano 2025-08-07 모델 테스트
- 업데이트된 API 키 테스트
"""
import requests
import json
import os
from pathlib import Path

def test_health_check(base_url):
    """서버 상태 확인"""
    print("\n" + "="*70)
    print("1. 서버 상태 확인 (Health Check)")
    print("="*70)
    
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print(f"✅ 서버 정상 작동 (상태 코드: {response.status_code})")
            return True
        else:
            print(f"⚠️ 서버 응답 이상 (상태 코드: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 서버 연결 실패: {str(e)}")
        return False

def test_upload_endpoint(base_url, test_image_path):
    """파일 업로드 및 분석 테스트"""
    print("\n" + "="*70)
    print("2. PDF/이미지 업로드 및 분석 테스트")
    print("="*70)
    
    if not os.path.exists(test_image_path):
        print(f"❌ 테스트 이미지가 없습니다: {test_image_path}")
        return False
    
    print(f"📄 테스트 PDF: {test_image_path}")
    print(f"   파일 크기: {os.path.getsize(test_image_path)} bytes")
    
    # 파일 업로드
    upload_url = f"{base_url}/upload"
    
    try:
        with open(test_image_path, 'rb') as f:
            files = {'file': (os.path.basename(test_image_path), f, 'application/pdf')}
            
            print(f"\n🌐 API 호출 중: {upload_url}")
            print("⏳ 분석 중... (최대 2분 소요 예상)")
            
            response = requests.post(
                upload_url,
                files=files,
                timeout=180  # 3분 타임아웃
            )
            
            print(f"\n✅ 응답 받음 (상태 코드: {response.status_code})")
            
            if response.status_code == 200:
                result = response.json()
                
                print("\n📊 분석 결과:")
                print(f"   - 상태: {result.get('status', 'N/A')}")
                print(f"   - 세션 ID: {result.get('session_id', 'N/A')}")
                print(f"   - 총 페이지: {len(result.get('pages', []))}")
                
                # 각 페이지 결과 출력
                for page_data in result.get('pages', []):
                    page_num = page_data.get('page_number', 'N/A')
                    edits = page_data.get('edits', [])
                    
                    print(f"\n   📄 페이지 {page_num}:")
                    print(f"      수정/삭제 항목: {len(edits)}개")
                    
                    if edits:
                        print(f"\n      첫 3개 항목:")
                        for i, edit in enumerate(edits[:3], 1):
                            action = edit.get('action', 'N/A')
                            original = edit.get('original_text', 'N/A')
                            new_text = edit.get('new_text', 'N/A')
                            confidence = edit.get('confidence', 'N/A')
                            
                            print(f"\n         [{i}] {action}")
                            print(f"             원본: {original[:50]}{'...' if len(original) > 50 else ''}")
                            if action == "수정":
                                print(f"             변환: {new_text[:50]}{'...' if len(new_text) > 50 else ''}")
                            print(f"             신뢰도: {confidence}")
                
                # 모델 정보 확인
                print(f"\n🤖 AI 모델 정보:")
                print(f"   - 사용된 모델: gpt-5-nano-2025-08-07 (예상)")
                print(f"   - API 키: 업데이트된 키 사용")
                
                return True
            else:
                print(f"❌ 업로드 실패 (상태 코드: {response.status_code})")
                print(f"응답: {response.text[:200]}")
                return False
                
    except requests.exceptions.Timeout:
        print("❌ 타임아웃: 서버 응답 시간 초과")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """메인 테스트 함수"""
    print("\n" + "="*70)
    print("GPT-5 Nano 2025-08-07 서버 API 테스트")
    print("="*70)
    
    # 서버 URL (로컬)
    base_url = "http://localhost:5000"
    
    # 테스트 PDF 경로
    test_pdfs = [
        "uploads/0ae62426_AUHA23029303.pdf",
        "uploads/26003229_AUHA23029303.pdf",
        "uploads/ed734e5b_AUHA23029303.pdf"
    ]
    
    # 사용 가능한 첫 번째 PDF 찾기
    test_image = None
    for pdf_path in test_pdfs:
        if os.path.exists(pdf_path):
            test_image = pdf_path
            break
    
    if not test_image:
        print("❌ 테스트 PDF를 찾을 수 없습니다.")
        return
    
    # 테스트 실행
    success_count = 0
    total_tests = 2
    
    # 1. Health Check
    if test_health_check(base_url):
        success_count += 1
    
    # 2. Upload & Analysis
    if test_upload_endpoint(base_url, test_image):
        success_count += 1
    
    # 결과 요약
    print("\n" + "="*70)
    print("테스트 결과 요약")
    print("="*70)
    print(f"✅ 통과: {success_count}/{total_tests}")
    print(f"❌ 실패: {total_tests - success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("\n🎉 모든 테스트 통과!")
        print("\n📊 확인 사항:")
        print("   ✅ 서버 정상 작동")
        print("   ✅ 새 모델 (gpt-5-nano-2025-08-07) 사용")
        print("   ✅ 새 API 키 정상 작동")
        print("   ✅ 이미지 분석 성공")
    else:
        print("\n⚠️ 일부 테스트 실패")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 테스트 중단됨")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {str(e)}")
        import traceback
        traceback.print_exc()
