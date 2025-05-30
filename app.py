import streamlit as st
import random  # 임시 데이터 생성용
from datetime import datetime
import pandas as pd  # 표 형태로 데이터를 표시하기 위해 추가
import json
import qrcode
from PIL import Image
import io

# 페이지 기본 설정
st.set_page_config(
    page_title="쓱쓱페이 - 소상공인과 함께하는 간편결제",
    page_icon="💸",
    layout="wide"
)

def generate_qr_code(data):
    """
    QR 코드를 생성하고 바이트 데이터로 반환합니다.
    
    Args:
        data (str): QR 코드에 담을 데이터
        
    Returns:
        bytes: QR 코드 이미지의 바이트 데이터
    """
    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # PIL Image로 변환
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # BytesIO를 사용하여 바이트로 변환
    byte_stream = io.BytesIO()
    qr_image.save(byte_stream, format='PNG')
    return byte_stream.getvalue()

# 세션 상태 초기화
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "balance" not in st.session_state:
    st.session_state.balance = 10000  # 초기 잔액
if "transactions" not in st.session_state:
    st.session_state.transactions = []  # 거래 내역

def logout():
    st.session_state.user_type = None
    st.session_state.user_name = None

def add_transaction(transaction_type, amount, description):
    transaction = {
        "type": transaction_type,
        "amount": amount,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.transactions.insert(0, transaction)  # 최신 거래를 앞에 추가

def get_today_points():
    today = datetime.now().strftime("%Y-%m-%d")
    today_transactions = [t for t in st.session_state.transactions if t["date"] == today and t["type"] == "적립"]
    return sum(t["amount"] for t in today_transactions)

# 메인 타이틀
st.title("💸 쓱쓱페이")
st.subheader("소상공인과 함께하는 간편결제")

# 로그인하지 않은 경우 로그인 인터페이스 표시
if not st.session_state.user_type:
    st.write("---")
    st.write("### 서비스 이용을 위해 로그인해주세요")
    
    # 사용자 유형 선택
    user_type = st.selectbox(
        "사용자 유형을 선택해주세요",
        options=["선택해주세요", "사용자", "소상공인"],
        index=0
    )
    
    # 이름 입력
    if user_type != "선택해주세요":
        name = st.text_input("이름 또는 닉네임을 입력해주세요")
        
        if st.button("로그인"):
            if name.strip():
                st.session_state.user_type = user_type
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("이름 또는 닉네임을 입력해주세요.")

# 로그인한 경우 사용자 유형에 따른 화면 표시
else:
    # 로그아웃 버튼
    st.sidebar.button("로그아웃", on_click=logout)
    
    # 환영 메시지
    st.write(f"안녕하세요, {st.session_state.user_name}님!")
    
    # 사용자 유형에 따른 다른 화면 표시
    if st.session_state.user_type == "사용자":
        # 잔액 표시
        st.write("## 현재 잔액")
        st.write(f"### 💰 {st.session_state.balance:,}원")
        
        # 기능 버튼들
        col1, col2 = st.columns(2)
        
        with col1:
            use_amount = st.number_input("사용할 금액", min_value=100, step=100)
            if st.button("💳 포인트 사용", use_container_width=True):
                if use_amount <= st.session_state.balance:
                    st.session_state.balance -= use_amount
                    add_transaction("사용", -use_amount, "포인트 사용")
                    st.success(f"{use_amount:,}원이 사용되었습니다!")
                else:
                    st.error("잔액이 부족합니다!")
        
        with col2:
            earn_amount = st.number_input("적립할 금액", min_value=100, step=100)
            if st.button("🎁 포인트 적립", use_container_width=True):
                st.session_state.balance += earn_amount
                add_transaction("적립", earn_amount, "포인트 적립")
                st.success(f"{earn_amount:,}원이 적립되었습니다!")
        
        # 거래 내역
        st.write("## 거래 내역")
        if st.session_state.transactions:
            for transaction in st.session_state.transactions:
                with st.expander(f"{transaction['date']} {transaction['time']} - {transaction['description']}"):
                    st.write(f"유형: {transaction['type']}")
                    amount_text = f"+{transaction['amount']:,}원" if transaction['amount'] > 0 else f"{transaction['amount']:,}원"
                    st.write(f"금액: {amount_text}")
        else:
            st.info("거래 내역이 없습니다.")
            
    else:  # 소상공인
        # 탭 생성
        tab1, tab2, tab3 = st.tabs(["포인트 적립", "적립 현황", "QR 코드 생성"])
        
        with tab1:
            # QR 스캔 시뮬레이션
            st.write("## QR 코드 스캔")
            st.info("현재는 테스트를 위해 사용자 이름 직접 입력으로 대체됩니다.")
            st.write("추후 QR 코드 스캐너 기능으로 업그레이드 예정입니다.")
            
            # 고객 정보 입력
            customer_name = st.text_input("고객 이름")
            amount = st.number_input("적립 금액", min_value=100, step=100)
            
            # 적립 처리
            if st.button("포인트 적립하기"):
                if customer_name and amount:
                    add_transaction("적립", amount, f"{customer_name}님 포인트 적립")
                    st.success(f"{customer_name}님에게 {amount:,}원이 적립되었습니다!")
                else:
                    st.error("고객 이름과 적립 금액을 모두 입력해주세요.")
            
            # 오늘의 적립 내역
            st.write("## 오늘의 적립 내역")
            today = datetime.now().strftime("%Y-%m-%d")
            today_transactions = [t for t in st.session_state.transactions if t["date"] == today and t["type"] == "적립"]
            
            if today_transactions:
                for transaction in today_transactions:
                    st.write(f"- {transaction['time']} | {transaction['description']}: +{transaction['amount']:,}원")
        
        with tab2:
            st.write("## 전체 적립 현황")
            
            # 적립 데이터만 필터링
            point_transactions = [t for t in st.session_state.transactions if t["type"] == "적립"]
            
            if point_transactions:
                # 데이터프레임으로 변환
                df = pd.DataFrame(point_transactions)
                
                # 사용자 이름 추출 (description에서 "님 포인트 적립" 제거)
                df['customer_name'] = df['description'].apply(lambda x: x.replace('님 포인트 적립', ''))
                
                # 표시할 열 선택 및 이름 변경
                display_df = df[['customer_name', 'amount', 'date', 'time']].rename(columns={
                    'customer_name': '고객명',
                    'amount': '적립금액',
                    'date': '날짜',
                    'time': '시간'
                })
                
                # 금액에 천 단위 구분자 추가
                display_df['적립금액'] = display_df['적립금액'].apply(lambda x: f"{x:,}원")
                
                # 정렬 (최신 순)
                display_df = display_df.sort_values(by=['날짜', '시간'], ascending=[False, False])
                
                # 테이블 표시
                st.dataframe(
                    display_df,
                    column_config={
                        "고객명": st.column_config.TextColumn("고객명", width=150),
                        "적립금액": st.column_config.TextColumn("적립금액", width=150),
                        "날짜": st.column_config.TextColumn("날짜", width=150),
                        "시간": st.column_config.TextColumn("시간", width=150),
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # 통계 정보
                total_points = sum(t['amount'] for t in point_transactions)
                unique_customers = len(display_df['고객명'].unique())
                
                # 통계 정보를 3열로 표시
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("총 적립금액", f"{total_points:,}원")
                with col2:
                    st.metric("총 적립 건수", f"{len(point_transactions):,}건")
                with col3:
                    st.metric("총 고객 수", f"{unique_customers:,}명")
                
            else:
                st.info("아직 적립 내역이 없습니다.")

        with tab3:
            st.write("## QR 코드 생성")
            st.write("매장 정보를 QR 코드로 생성합니다.")
            
            # 매장 정보 입력
            store_info = {
                "store_name": st.session_state.user_name,
                "type": "store",
                "timestamp": datetime.now().isoformat()
            }
            
            # 추가 정보 입력 (선택사항)
            with st.expander("추가 정보 입력"):
                store_info["address"] = st.text_input("매장 주소")
                store_info["phone"] = st.text_input("전화번호")
                store_info["business_hours"] = st.text_input("영업시간")
                store_info["description"] = st.text_area("매장 설명")
            
            # QR 코드 생성 버튼
            if st.button("매장 QR 코드 생성"):
                qr_bytes = generate_qr_code(json.dumps(store_info))
                st.image(qr_bytes, caption=f"{store_info['store_name']}의 QR 코드")
                
                # QR 코드 다운로드 버튼
                st.download_button(
                    label="QR 코드 다운로드",
                    data=qr_bytes,
                    file_name="store_qr_code.png",
                    mime="image/png"
                )
                
                # QR 코드 정보 표시
                st.write("### QR 코드 정보")
                st.json(store_info)