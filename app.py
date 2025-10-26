"""
PDF 수정/삭제 지시사항 자동 인식 서비스
Flask 웹 애플리케이션
"""
import os
import uuid
from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from pdf_processor import PDFProcessor
from image_analyzer import ImageAnalyzer
from ai_analyzer import AIAnalyzer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB 제한
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# 디렉토리 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """허용된 파일 확장자 체크"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """PDF 파일 업로드 및 처리"""
    if 'file' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '파일이 선택되지 않았습니다'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'PDF 파일만 업로드 가능합니다'}), 400
    
    try:
        # 고유 ID 생성
        unique_id = str(uuid.uuid4())[:8]
        
        # 파일 저장
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        file.save(file_path)
        
        # 출력 디렉토리 생성
        output_dir = os.path.join(app.config['OUTPUT_FOLDER'], unique_id)
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. PDF를 이미지로 변환
        pdf_processor = PDFProcessor(file_path, output_dir)
        images = pdf_processor.convert_to_images(dpi=300)
        image_paths = pdf_processor.save_images(prefix='page')
        
        # 2. 각 페이지 분석
        all_results = []
        
        for page_num, image_path in enumerate(image_paths, 1):
            print(f"\n=== 페이지 {page_num} 분석 중 ===")
            
            # 이미지 분석기 초기화
            analyzer = ImageAnalyzer(image_path)
            analyzer.load_image()
            
            # 붉은색 영역 감지
            red_mask = analyzer.detect_red_regions()
            bboxes = analyzer.find_red_contours()
            
            print(f"붉은색 영역 {len(bboxes)}개 발견")
            
            # 디버그 이미지 저장
            debug_path = os.path.join(output_dir, f'debug_page_{page_num}.png')
            analyzer.save_debug_image(debug_path)
            
            # 전체 페이지 텍스트 추출 (참고용)
            full_text = analyzer.get_full_page_text()
            
            # AI 분석
            if len(bboxes) > 0:
                ai_analyzer = AIAnalyzer()
                edits = ai_analyzer.analyze_handwritten_edits(
                    image_path,
                    full_text
                )
                
                result = {
                    'page': page_num,
                    'image_url': f'/output/{unique_id}/page_{page_num}.png',
                    'debug_url': f'/output/{unique_id}/debug_page_{page_num}.png',
                    'red_regions_count': len(bboxes),
                    'edits': edits,
                    'table': ai_analyzer.format_as_table(edits)
                }
            else:
                result = {
                    'page': page_num,
                    'image_url': f'/output/{unique_id}/page_{page_num}.png',
                    'debug_url': None,
                    'red_regions_count': 0,
                    'edits': [],
                    'table': {'headers': [], 'rows': []}
                }
            
            all_results.append(result)
        
        return jsonify({
            'success': True,
            'unique_id': unique_id,
            'filename': filename,
            'total_pages': len(image_paths),
            'results': all_results
        })
        
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'처리 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/output/<path:filename>')
def output_file(filename):
    """출력 파일 제공"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)


@app.route('/health')
def health():
    """헬스 체크"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("=" * 60)
    print("PDF 수정/삭제 지시사항 자동 인식 서비스")
    print("=" * 60)
    print("\n서버 시작 중...")
    print("브라우저에서 http://localhost:5000 접속\n")
    
    # 개발 서버 실행
    app.run(host='0.0.0.0', port=5000, debug=True)
