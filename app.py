import streamlit as st

st.set_page_config(page_title="작업장 위험 평가", page_icon="⚠️", layout="centered")
st.title("작업장 위험 가중치 평가 시스템 (3.1~3.4)")

# 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = 1
if "score_31" not in st.session_state:
    st.session_state.score_31 = 0
if "score_32" not in st.session_state:
    st.session_state.score_32 = 0
if "score_33" not in st.session_state:
    st.session_state.score_33 = 0
if "score_34" not in st.session_state:
    st.session_state.score_34 = 0

# ---------------- STEP 1: 3.1 ----------------
if st.session_state.step == 1:
    st.subheader("3.1 근속년수")
    ratio = st.number_input("6개월 미만 사원 비율 (%)", min_value=0.0, max_value=100.0, step=0.1)
    col1, col2 = st.columns(2)
    with col2:
        if st.button("다음 →", key="next1"):
            if ratio < 5:
                st.session_state.score_31 = 0.125
            elif ratio < 10:
                st.session_state.score_31 = 0.25
            elif ratio <= 15:
                st.session_state.score_31 = 0.375
            else:
                st.session_state.score_31 = 0.5
            st.session_state.step = 2

# ---------------- STEP 2: 3.2 ----------------
elif st.session_state.step == 2:
    st.subheader("3.2 휴식시간")
    rest = st.number_input("1시간당 평균 휴식시간 (분)", min_value=0.0, max_value=60.0, step=1.0)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전", key="prev2"):
            st.session_state.step = 1
    with col2:
        if st.button("다음 →", key="next2"):
            if rest >= 15:
                st.session_state.score_32 = 0.125
            elif rest >= 10:
                st.session_state.score_32 = 0.25
            elif rest > 1:
                st.session_state.score_32 = 0.375
            else:
                st.session_state.score_32 = 0.5
            st.session_state.step = 3

# ---------------- STEP 3: 3.3 ----------------
elif st.session_state.step == 3:
    st.subheader("3.3 통로 장해물과 사각지대")
    grade_opts = ["매우 양호", "양호", "미흡", "불량"]
    score_map = {"매우 양호": 0.025, "양호": 0.05, "미흡": 0.075, "불량": 0.1}

    g1 = st.radio("3.3.1 정리정돈 상태", grade_opts, horizontal=True)
    g2 = st.radio("3.3.2 조명 밝기", grade_opts, horizontal=True)
    sharp = st.number_input("3.3.3 날카로운 장애물 개수", min_value=0, step=1)
    others = st.number_input("그 밖의 장애물 개수", min_value=0, step=1)
    width = st.number_input("3.3.4 통로 폭 (cm)", min_value=0, step=1)
    g5 = st.radio("3.3.5 사각지대 상태", grade_opts, horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전", key="prev3"):
            st.session_state.step = 2
    with col2:
        if st.button("다음 →", key="next3"):
            s1 = score_map[g1]
            s2 = score_map[g2]
            s5 = score_map[g5]

            if sharp == 0 and others == 0:
                s3 = 0.025
            elif sharp == 0 and others <= 2:
                s3 = 0.05
            elif sharp <= 2 and others <= 4:
                s3 = 0.075
            else:
                s3 = 0.1

            if width >= 250:
                s4 = 0.025
            elif width >= 100:
                s4 = 0.05
            elif width > 60:
                s4 = 0.075
            else:
                s4 = 0.1

            st.session_state.score_33 = round(s1 + s2 + s3 + s4 + s5, 3)
            st.session_state.step = 4

# ---------------- STEP 4: 3.4 ----------------
elif st.session_state.step == 4:
    st.subheader("3.4 작업장 자재 및 물품 상태")
    questions = [
        "3.4.1 기반 안정성",
        "3.4.2 벽면과의 거리 상태",
        "3.4.3 높이 / 폭 비율",
        "3.4.4 경사각 상태",
        "3.4.5 정리정돈 상태",
        "3.4.6 기인물 보관상태"
    ]

    x_count = 0
    for q in questions:
        val = st.radio(q, ["o", "x"], index=0, horizontal=True, key=q)
        if val != "o":
            x_count += 1

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전", key="prev4"):
            st.session_state.step = 3
    with col2:
        if st.button("최종 결과 보기", key="next4"):
            if x_count == 0:
                st.session_state.score_34 = 0.125
            elif x_count == 1:
                st.session_state.score_34 = 0.25
            elif x_count <= 4:
                st.session_state.score_34 = 0.375
            else:
                st.session_state.score_34 = 0.5
            st.session_state.step = 5

# ---------------- STEP 5: 결과 ----------------
elif st.session_state.step == 5:
    st.success("✅ 모든 항목 평가 완료!")
    st.subheader("📊 최종 총합 점수")
    total = round(
        st.session_state.score_31 + st.session_state.score_32 + st.session_state.score_33 + st.session_state.score_34, 3
    )
    st.metric("총합 점수 (0.5 ~ 2.0)", total)
    st.write("3.1 점수:", st.session_state.score_31)
    st.write("3.2 점수:", st.session_state.score_32)
    st.write("3.3 점수:", st.session_state.score_33)
    st.write("3.4 점수:", st.session_state.score_34)

    if st.button("처음부터 다시 평가하기"):
        st.session_state.step = 1
