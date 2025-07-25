import streamlit as st

st.set_page_config(page_title="작업장 위험 평가", page_icon="⚠️", layout="centered")
st.title("작업장 위험 가중치 평가 시스템 (3.1~3.4)")

# ----------- 3.1 근속년수 -----------
st.header("3.1 근속년수")
ratio = st.number_input("6개월 미만 사원 비율 (%)", min_value=0.0, max_value=100.0, step=0.1)
if ratio < 5:
    score_31, level_31 = 0.125, "매우 양호"
elif ratio < 10:
    score_31, level_31 = 0.25, "양호"
elif ratio <= 15:
    score_31, level_31 = 0.375, "미흡"
else:
    score_31, level_31 = 0.5, "불량"
st.write(f"➡️ 등급: **{level_31}**, 점수: `{score_31}`")

# ----------- 3.2 휴식시간 -----------
st.header("3.2 휴식시간")
rest = st.number_input("1시간당 평균 휴식시간 (분)", min_value=0.0, max_value=60.0, step=1.0)
if rest >= 15:
    score_32, level_32 = 0.125, "매우 양호"
elif rest >= 10:
    score_32, level_32 = 0.25, "양호"
elif rest > 1:
    score_32, level_32 = 0.375, "미흡"
else:
    score_32, level_32 = 0.5, "불량"
st.write(f"➡️ 등급: **{level_32}**, 점수: `{score_32}`")

# ----------- 3.3 통로 장해물과 사각지대 -----------
st.header("3.3 통로 장해물과 사각지대")
grade_opts = ["매우 양호", "양호", "미흡", "불량"]
score_map = {"매우 양호": 0.025, "양호": 0.05, "미흡": 0.075, "불량": 0.1}

g1 = st.radio("3.3.1 정리정돈 상태", grade_opts, horizontal=True)
g2 = st.radio("3.3.2 조명 밝기", grade_opts, horizontal=True)
sharp = st.number_input("3.3.3 날카로운 장애물 개수", min_value=0, step=1)
others = st.number_input("        그 밖의 장애물 개수", min_value=0, step=1)

if sharp == 0 and others == 0:
    s3 = 0.025
elif sharp == 0 and others <= 2:
    s3 = 0.05
elif sharp <= 2 and others <= 4:
    s3 = 0.075
else:
    s3 = 0.1

width = st.number_input("3.3.4 통로 폭 (cm)", min_value=0, step=1)
if width >= 250:
    s4 = 0.025
elif width >= 100:
    s4 = 0.05
elif width > 60:
    s4 = 0.075
else:
    s4 = 0.1

g5 = st.radio("3.3.5 사각지대 상태", grade_opts, horizontal=True)

s1 = score_map[g1]
s2 = score_map[g2]
s5 = score_map[g5]

score_33 = round(s1 + s2 + s3 + s4 + s5, 3)
if score_33 <= 0.125:
    level_33 = "매우 양호"
elif score_33 <= 0.25:
    level_33 = "양호"
elif score_33 <= 0.375:
    level_33 = "미흡"
else:
    level_33 = "불량"

st.write(f"➡️ 등급: **{level_33}**, 점수: `{score_33}`")

# ----------- 3.4 작업장 자재 및 물품 상태 -----------
st.header("3.4 작업장 자재 및 물품 상태")

expected = {
    "3.4.1 기반침하가능성": "x",
    "3.4.2 벽면과의 거리": "x",
    "3.4.3 높이 / 폭 비율": "o",
    "3.4.4 경사각": "x",
    "3.4.5 정리정돈 상태": "o",
    "3.4.6 기인물 적재유무": "x"
}

x_count = 0
inputs_34 = {}

for q, correct in expected.items():
    val = st.radio(f"{q}", ["o", "x"], index=0 if correct == "o" else 1, horizontal=True)
    inputs_34[q] = val
    if val != correct:
        x_count += 1

if x_count == 0:
    score_34, level_34 = 0.125, "매우 양호"
elif x_count == 1:
    score_34, level_34 = 0.25, "양호"
elif x_count <= 4:
    score_34, level_34 = 0.375, "미흡"
else:
    score_34, level_34 = 0.5, "불량"

st.write(f"➡️ 등급: **{level_34}**, 점수: `{score_34}`")

# ----------- 총합 -----------
st.markdown("---")
total = round(score_31 + score_32 + score_33 + score_34, 3)
st.subheader(f"📊 총합 점수: **{total}** (범위: 0.5 ~ 2.0)")
