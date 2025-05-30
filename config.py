import os
from dotenv import load_dotenv

# .env 파일이 있으면 로드
load_dotenv()

# API 키 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID', '')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET', '')
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY', '')

# 데이터베이스 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'ssgssg_pay_db'),
    'user': os.getenv('DB_USER', ''),
    'password': os.getenv('DB_PASSWORD', '')
}

# 앱 설정
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# API 엔드포인트
NAVER_OCR_API_URL = "https://openapi.naver.com/v1/vision/receipt"
KAKAO_LOCAL_API_URL = "https://dapi.kakao.com/v2/local/search/address.json"

def get_api_key(api_name):
    """
    API 키를 안전하게 가져오는 함수
    
    Args:
        api_name (str): API 이름 ('openai', 'naver', 'kakao' 등)
        
    Returns:
        str: API 키
    """
    api_keys = {
        'openai': OPENAI_API_KEY,
        'naver': {
            'client_id': NAVER_CLIENT_ID,
            'client_secret': NAVER_CLIENT_SECRET
        },
        'kakao': KAKAO_API_KEY
    }
    
    return api_keys.get(api_name.lower(), None)

def is_api_configured(api_name):
    """
    특정 API의 설정이 완료되었는지 확인하는 함수
    
    Args:
        api_name (str): API 이름 ('openai', 'naver', 'kakao' 등)
        
    Returns:
        bool: API 설정 완료 여부
    """
    api_key = get_api_key(api_name)
    
    if isinstance(api_key, dict):
        return all(api_key.values())
    
    return bool(api_key) 