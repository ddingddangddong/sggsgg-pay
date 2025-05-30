import streamlit as st
import qrcode
from PIL import Image
import io

def generate_qr_code(data):
    """
    데이터를 받아서 QR 코드 이미지를 생성합니다.
    
    Args:
        data (str): QR 코드에 담을 데이터
        
    Returns:
        bytes: QR 코드 이미지 바이트 데이터
    """
    # 1. QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # 2. PIL Image 객체로 변환
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # 3. BytesIO를 사용하여 이미지를 바이트로 변환
    byte_stream = io.BytesIO()
    qr_image.save(byte_stream, format='PNG')
    qr_bytes = byte_stream.getvalue()
    
    return qr_bytes

# Streamlit 앱 설정
st.set_page_config(
    page_title="QR 코드 생성기",
    page_icon="🔲",
    layout="centered"
)

# 메인 타이틀
st.title("🔲 QR 코드 생성기")
st.write("텍스트를 입력하면 QR 코드로 변환해드립니다!")

# 사용자 입력 받기
user_input = st.text_input(
    "QR 코드로 변환할 텍스트를 입력하세요",
    placeholder="예: https://www.example.com"
)

# QR 코드 생성 버튼
if st.button("QR 코드 생성"):
    if user_input:
        # QR 코드 생성 및 표시
        qr_bytes = generate_qr_code(user_input)
        
        # 4. Streamlit으로 QR 코드 표시
        st.image(
            qr_bytes,
            caption=f"QR 코드: {user_input}",
            use_column_width=False
        )
        
        # QR 코드 다운로드 버튼 추가
        st.download_button(
            label="QR 코드 다운로드",
            data=qr_bytes,
            file_name="qr_code.png",
            mime="image/png"
        )
    else:
        st.error("텍스트를 입력해주세요!") 