import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# ==============================================================================
# 1. ฟังก์ชันคำนวณทางคณิตศาสตร์ (Mathematical Functions)
# ==============================================================================
def f(t, y):
    """สมการเชิงอนุพันธ์ dy/dt = (y/t) - (y/t)^2"""
    return (y / t) - (y / t) ** 2


def exact_y(t):
    """Exact Solution: y(t) = t / (1 + ln(t))"""
    return t / (1 + np.log(t))


def solve_euler(t_start, t_end, h):
    """ฟังก์ชันคำนวณ Euler's Method และเปรียบเทียบกับ Exact Solution"""
    t_values = np.arange(t_start, t_end + h / 2, h)
    euler_values = [1.0]  # ค่าเริ่มต้น y(1) = 1

    for i in range(len(t_values) - 1):
        t_curr = t_values[i]
        y_curr = euler_values[-1]
        y_next = y_curr + h * f(t_curr, y_curr)
        euler_values.append(y_next)

    euler_values = np.array(euler_values)
    exact_values = exact_y(t_values)
    errors = np.abs(exact_values - euler_values)

    df = pd.DataFrame(
        {
            "t_i": t_values,
            "Euler's": euler_values,
            "Exact": exact_values,
            "Error": errors,
        }
    )

    return t_values, euler_values, exact_values, errors, df


# ==============================================================================
# 2. ส่วนการตั้งค่า Sidebar (Sidebar Configurations)
# ==============================================================================
st.set_page_config(page_title="Euler's Method", layout="wide")
st.title("Euler’s Method Approximate")

st.sidebar.header("การตั้งค่าพารามิเตอร์ (Input)")
h = st.sidebar.number_input(
    "1. กำหนดขนาดก้าว (Step size: h)",
    min_value=0.001,
    max_value=0.5,
    value=0.1,
    step=0.01,
    format="%.4f",
)
precision = st.sidebar.slider(
    "2. จำนวนตำแหน่งทศนิยมในตาราง (Precision)",
    min_value=2,
    max_value=8,
    value=7,
)
plt_style = st.sidebar.selectbox(
    "3. เลือกรูปแบบสไตล์กราฟ (Plot Style)",
    ["default", "ggplot", "bmh", "fivethirtyeight"],
)

# ==============================================================================
# 3. การประมวลผลและการแสดงผลบนหน้าเว็บ (Main App & Tabs)
# ==============================================================================
# กำหนดช่วงการคำนวณ 1 <= t <= 2
t_start, t_end = 1.0, 2.0
t_values, euler_values, exact_values, errors, df = solve_euler(
    t_start, t_end, h
)

tab1, tab2, tab3 = st.tabs(["โจทย์", "ตัวจำลองและกราฟ", "ตารางสรุปผล"])

# --- Tab 1: แสดงโจทย์ ---
with tab1:
    st.subheader(
        "Use Euler’s Method to approximate the solutions to the initial-value problems"
    )
    st.latex(
        r"y' = \frac{y}{t} - \left(\frac{y}{t}\right)^2 , \quad 1 \le t \le 2, \quad y(1) = 1"
    )
    st.subheader("Exact solution is :")
    st.latex(r"y(t) = \frac{t}{1 + \ln(t)}")

# --- Tab 2: ตัวจำลองและกราฟ ---
with tab2:
    st.subheader("เปรียบเทียบ Exact Solution และ Numerical Solution")

    m1, m2, m3 = st.columns(3)
    m1.metric("ค่า Step Size (h)", f"{h}")
    m2.metric("Error สูงสุด (Max Error)", f"{np.max(errors):.{precision}f}")
    m3.metric("Error เฉลี่ย (Mean Error)", f"{np.mean(errors):.{precision}f}")

    # วาดกราฟโดยใช้ Context Manager ของ Matplotlib สไตล์
    with plt.style.context(plt_style):
        fig, ax = plt.subplots(figsize=(10, 5))
        t_dense = np.linspace(t_start, t_end, 200)

        ax.plot(
            t_dense,
            exact_y(t_dense),
            label="Exact Solution",
            color="b",
            linewidth=2,
        )
        ax.plot(
            t_values,
            euler_values,
            "o--",
            label="Euler's Method",
            color="r",
            linewidth=1.5,
            markersize=5,
        )

        ax.set_title(f"Euler's Method Approximate (h = {h})", fontsize=14)
        ax.set_xlabel("t", fontsize=12)
        ax.set_ylabel("y(t)", fontsize=12)
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

        st.pyplot(fig)
        plt.close(fig)  # คืนหน่วยความจำ

# --- Tab 3: ตารางสรุปผล ---
with tab3:
    st.subheader(f"ตารางเปรียบเทียบค่าที่คำนวณได้ (h = {h})")
    df_display = df.copy()
    df_display["t_i"] = df_display["t_i"].map(lambda x: f"{x:.2f}")
    df_display["Euler's"] = df_display["Euler's"].map(
        lambda x: f"{x:.{precision}f}"
    )
    df_display["Exact"] = df_display["Exact"].map(
        lambda x: f"{x:.{precision}f}"
    )
    df_display["Error"] = df_display["Error"].map(
        lambda x: f"{x:.{precision}f}"
    )

    st.dataframe(df_display, use_container_width=True)
