#!/usr/bin/env python3
"""
시스템 환경 테스트 스크립트
"""
import sys
import os

def test_imports():
    """필수 모듈 임포트 테스트"""
    print("=" * 60)
    print("필수 모듈 임포트 테스트")
    print("=" * 60)
    
    modules = [
        ('Flask', 'flask'),
        ('pdf2image', 'pdf2image'),
        ('PIL', 'PIL'),
        ('cv2', 'cv2'),
        ('numpy', 'numpy'),
        ('pytesseract', 'pytesseract'),
        ('openai', 'openai'),
        ('dotenv', 'dotenv')
    ]
    
    success = True
    for display_name, module_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name}: OK")
        except ImportError as e:
            print(f"❌ {display_name}: FAILED - {e}")
            success = False
    
    return success

def test_tesseract():
    """Tesseract 설치 확인"""
    print("\n" + "=" * 60)
    print("Tesseract OCR 테스트")
    print("=" * 60)
    
    import pytesseract
    
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract 버전: {version}")
        return True
    except Exception as e:
        print(f"❌ Tesseract 오류: {e}")
        return False

def test_poppler():
    """Poppler 설치 확인"""
    print("\n" + "=" * 60)
    print("Poppler 테스트")
    print("=" * 60)
    
    import subprocess
    
    try:
        result = subprocess.run(
            ['pdftoppm', '-v'],
            capture_output=True,
            text=True
        )
        print("✅ Poppler 설치됨")
        print(result.stderr.strip())
        return True
    except FileNotFoundError:
        print("❌ Poppler가 설치되지 않았습니다")
        print("   설치 명령: sudo apt-get install poppler-utils")
        return False

def test_env_file():
    """환경 변수 설정 확인"""
    print("\n" + "=" * 60)
    print("환경 변수 설정 확인")
    print("=" * 60)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        masked_key = api_key[:8] + "..." + api_key[-4:]
        print(f"✅ OPENAI_API_KEY 설정됨: {masked_key}")
        return True
    else:
        print("❌ OPENAI_API_KEY가 설정되지 않았습니다")
        print("   .env 파일을 생성하고 다음 내용을 추가하세요:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False

def test_directories():
    """디렉토리 구조 확인"""
    print("\n" + "=" * 60)
    print("디렉토리 구조 확인")
    print("=" * 60)
    
    required_dirs = ['uploads', 'output', 'static', 'templates']
    success = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ 존재")
        else:
            print(f"❌ {dir_name}/ 없음")
            success = False
    
    return success

def main():
    print("\n🔍 PDF 수정/삭제 지시사항 자동 인식 서비스")
    print("시스템 환경 테스트를 시작합니다...\n")
    
    results = []
    
    results.append(("모듈 임포트", test_imports()))
    results.append(("Tesseract OCR", test_tesseract()))
    results.append(("Poppler", test_poppler()))
    results.append(("환경 변수", test_env_file()))
    results.append(("디렉토리 구조", test_directories()))
    
    # 요약
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    
    all_success = True
    for test_name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{test_name}: {status}")
        if not result:
            all_success = False
    
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 모든 테스트 통과! 서비스를 시작할 수 있습니다.")
        print("\n서비스 실행 명령:")
        print("  python app.py")
    else:
        print("⚠️  일부 테스트 실패. 위 오류를 해결한 후 다시 시도하세요.")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(main())
