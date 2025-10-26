"""
PDF 처리 및 이미지 변환 모듈
"""
import os
from pdf2image import convert_from_path
from PIL import Image


class PDFProcessor:
    """PDF를 이미지로 변환하는 클래스"""
    
    def __init__(self, pdf_path, output_dir='output'):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.images = []
        
    def convert_to_images(self, dpi=300):
        """
        PDF를 이미지로 변환
        
        Args:
            dpi: 해상도 (기본값: 300)
            
        Returns:
            list: PIL Image 객체 리스트
        """
        print(f"PDF 변환 중: {self.pdf_path}")
        
        # PDF를 이미지로 변환
        images = convert_from_path(
            self.pdf_path,
            dpi=dpi,
            fmt='png'
        )
        
        self.images = images
        print(f"총 {len(images)}페이지 변환 완료")
        
        return images
    
    def save_images(self, prefix='page'):
        """
        변환된 이미지를 파일로 저장
        
        Args:
            prefix: 파일명 접두사
            
        Returns:
            list: 저장된 파일 경로 리스트
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        saved_paths = []
        for i, image in enumerate(self.images):
            filename = f"{prefix}_{i+1}.png"
            filepath = os.path.join(self.output_dir, filename)
            image.save(filepath, 'PNG')
            saved_paths.append(filepath)
            print(f"저장됨: {filepath}")
            
        return saved_paths
