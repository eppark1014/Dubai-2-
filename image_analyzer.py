"""
이미지 분석 및 붉은색 영역 감지 모듈
"""
import cv2
import numpy as np
from PIL import Image
import pytesseract


class ImageAnalyzer:
    """이미지에서 붉은색 손글씨 영역을 감지하고 분석하는 클래스"""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None
        self.hsv_image = None
        self.red_mask = None
        
    def load_image(self):
        """이미지 로드"""
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"이미지를 로드할 수 없습니다: {self.image_path}")
        return self.image
    
    def detect_red_regions(self):
        """
        붉은색 영역 감지
        
        Returns:
            numpy.ndarray: 붉은색 마스크 이미지
        """
        # BGR을 HSV로 변환
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        
        # 붉은색 범위 정의 (HSV)
        # 붉은색은 0도와 360도 근처에 있어서 두 범위로 나눔
        # 채도와 명도를 낮춰서 더 넓은 범위의 붉은색 감지
        lower_red1 = np.array([0, 50, 50])    # 채도 50, 명도 50으로 낮춤
        upper_red1 = np.array([15, 255, 255])  # 색상 범위 확장 (10→15)
        lower_red2 = np.array([155, 50, 50])   # 채도 50, 명도 50으로 낮춤
        upper_red2 = np.array([180, 255, 255])
        
        # 두 범위의 마스크 생성
        mask1 = cv2.inRange(self.hsv_image, lower_red1, upper_red1)
        mask2 = cv2.inRange(self.hsv_image, lower_red2, upper_red2)
        
        # 두 마스크 합치기
        self.red_mask = cv2.bitwise_or(mask1, mask2)
        
        # 노이즈 제거
        kernel = np.ones((3, 3), np.uint8)
        self.red_mask = cv2.morphologyEx(self.red_mask, cv2.MORPH_CLOSE, kernel)
        self.red_mask = cv2.morphologyEx(self.red_mask, cv2.MORPH_OPEN, kernel)
        
        return self.red_mask
    
    def find_red_contours(self):
        """
        붉은색 영역의 윤곽선 찾기
        
        Returns:
            list: 윤곽선 리스트 (x, y, w, h)
        """
        if self.red_mask is None:
            self.detect_red_regions()
        
        # 윤곽선 찾기
        contours, _ = cv2.findContours(
            self.red_mask, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # 바운딩 박스 정보 추출 (최소 면적 필터링)
        bounding_boxes = []
        min_area = 200  # 최소 면적 (픽셀) - 더 작은 수정사항도 감지
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(contour)
                bounding_boxes.append({
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'area': area
                })
        
        # Y 좌표로 정렬 (위에서 아래로)
        bounding_boxes.sort(key=lambda box: box['y'])
        
        return bounding_boxes
    
    def extract_region_image(self, bbox, padding=20):
        """
        특정 영역 이미지 추출
        
        Args:
            bbox: 바운딩 박스 정보 (dict)
            padding: 여백 (픽셀)
            
        Returns:
            numpy.ndarray: 추출된 이미지
        """
        x = max(0, bbox['x'] - padding)
        y = max(0, bbox['y'] - padding)
        w = bbox['width'] + padding * 2
        h = bbox['height'] + padding * 2
        
        # 이미지 경계 체크
        h_img, w_img = self.image.shape[:2]
        x_end = min(w_img, x + w)
        y_end = min(h_img, y + h)
        
        return self.image[y:y_end, x:x_end]
    
    def preprocess_for_ocr(self, image):
        """
        OCR 정확도 향상을 위한 이미지 전처리
        
        Args:
            image: 원본 이미지
            
        Returns:
            numpy.ndarray: 전처리된 이미지
        """
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 노이즈 제거 (Gaussian Blur)
        denoised = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # 대비 향상 (CLAHE - Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)
        
        # 이진화 (Adaptive Thresholding)
        binary = cv2.adaptiveThreshold(
            enhanced, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 
            11, 2
        )
        
        return binary
    
    def ocr_region(self, region_image):
        """
        영역 이미지에서 텍스트 추출 (OCR) - 개선된 버전
        
        Args:
            region_image: 이미지 영역
            
        Returns:
            str: 추출된 텍스트
        """
        # 이미지 전처리
        processed = self.preprocess_for_ocr(region_image)
        
        # OpenCV 이미지를 PIL 이미지로 변환
        pil_image = Image.fromarray(processed)
        
        # OCR 실행 (한국어 + 영어)
        # PSM 모드:
        # 6 = 단일 텍스트 블록
        # 7 = 단일 텍스트 라인
        # 11 = 가능한 한 많은 텍스트 찾기
        text = pytesseract.image_to_string(
            pil_image,
            lang='eng+kor',
            config='--psm 6 --oem 3'  # OEM 3 = Default (LSTM + Legacy)
        )
        
        return text.strip()
    
    def get_full_page_text(self):
        """
        전체 페이지 텍스트 추출 - 개선된 버전
        
        Returns:
            str: 전체 페이지 텍스트
        """
        # 이미지 전처리
        processed = self.preprocess_for_ocr(self.image)
        pil_image = Image.fromarray(processed)
        
        # OCR 실행 (영어)
        text = pytesseract.image_to_string(
            pil_image, 
            lang='eng',
            config='--psm 1 --oem 3'  # PSM 1 = Automatic page segmentation with OSD
        )
        return text
    
    def save_debug_image(self, output_path):
        """
        디버깅용 이미지 저장 (붉은색 영역 표시)
        
        Args:
            output_path: 저장 경로
        """
        if self.red_mask is None:
            self.detect_red_regions()
        
        # 원본 이미지 복사
        debug_image = self.image.copy()
        
        # 붉은색 마스크 영역을 초록색으로 표시
        debug_image[self.red_mask > 0] = [0, 255, 0]
        
        # 윤곽선 그리기
        bboxes = self.find_red_contours()
        for i, bbox in enumerate(bboxes):
            x, y, w, h = bbox['x'], bbox['y'], bbox['width'], bbox['height']
            cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(
                debug_image, 
                f"#{i+1}", 
                (x, y - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (0, 0, 255), 
                2
            )
        
        cv2.imwrite(output_path, debug_image)
        print(f"디버그 이미지 저장: {output_path}")
