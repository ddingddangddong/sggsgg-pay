import requests
import json
from config import get_api_key, NAVER_OCR_API_URL, KAKAO_LOCAL_API_URL

def call_naver_ocr_api(image_file):
    """
    네이버 OCR API를 호출하여 영수증 이미지에서 텍스트를 추출합니다.
    
    Args:
        image_file (bytes): 이미지 파일 데이터
        
    Returns:
        dict: OCR 결과
    """
    api_info = get_api_key('naver')
    
    if not api_info:
        raise ValueError("네이버 API 설정이 필요합니다.")
    
    headers = {
        'X-Naver-Client-Id': api_info['client_id'],
        'X-Naver-Client-Secret': api_info['client_secret']
    }
    
    files = {
        'image': image_file
    }
    
    response = requests.post(NAVER_OCR_API_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")

def search_address(query):
    """
    카카오 로컬 API를 사용하여 주소를 검색합니다.
    
    Args:
        query (str): 검색할 주소
        
    Returns:
        list: 검색된 주소 목록
    """
    api_key = get_api_key('kakao')
    
    if not api_key:
        raise ValueError("카카오 API 설정이 필요합니다.")
    
    headers = {
        'Authorization': f'KakaoAK {api_key}'
    }
    
    params = {
        'query': query
    }
    
    response = requests.get(KAKAO_LOCAL_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get('documents', [])
    else:
        raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")

def analyze_receipt(image_file):
    """
    영수증 이미지를 분석하여 정보를 추출합니다.
    
    Args:
        image_file (bytes): 영수증 이미지 파일 데이터
        
    Returns:
        dict: 추출된 영수증 정보
    """
    ocr_result = call_naver_ocr_api(image_file)
    
    # OCR 결과에서 필요한 정보 추출
    receipt_info = {
        'total_amount': 0,
        'store_name': '',
        'date': '',
        'items': []
    }
    
    # OCR 결과 파싱 로직 구현
    if 'images' in ocr_result and ocr_result['images']:
        fields = ocr_result['images'][0].get('fields', [])
        for field in fields:
            text = field.get('inferText', '').strip()
            # 여기에 영수증 정보 파싱 로직 추가
    
    return receipt_info

def get_store_location(store_name):
    """
    상점 이름으로 위치 정보를 검색합니다.
    
    Args:
        store_name (str): 상점 이름
        
    Returns:
        dict: 위치 정보 (위도, 경도 등)
    """
    search_results = search_address(store_name)
    
    if search_results:
        location = search_results[0]
        return {
            'address': location.get('address_name', ''),
            'road_address': location.get('road_address_name', ''),
            'lat': location.get('y', ''),
            'lng': location.get('x', '')
        }
    
    return None 