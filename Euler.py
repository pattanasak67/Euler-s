import streamlit as st
import pandas as pd
import numpy as np

# =========================================================
# 📌 ปรับแก้สมการและค่าเริ่มต้นตามโจทย์จริงได้ที่ส่วนนี้
# =========================================================
def f(x, y):
    # สมการอนุพันธ์ y' = f(x, y)
    return (y/x) - ((y/x)**2)   

def exact_sol(x):
    # สมการ Exact Solution
    return x/(1+np.log(x))   

X0 = 1.0       # ค่า x เริ่มต้น
Y0 = 2.1272295  # ค่า y เริ่มต้น (y0)
X_END = 2.0    # ค่า x ปลายทาง
# =========================================================

# หัวข้อโปรเจกต์
st.title("Project1# Use the Euler’s to approximate the solutions to the initial-value problems")
st.markdown("**Exact solution is:** $y(x) = 2e^x - x - 1$")

# 1. st.sidebar รับเฉพาะค่า h (Step size) ตามคำสั่งโจทย์
st.sidebar.header("Input Parameter")
h = st.sidebar.number_input(
    "Step size (h)", 
    value=0.1, 
    min_value=0.0001, 
    max_value=1.0, 
    step=0.01, 
    format="%.4f"
)

# แบ่งเนื้อหาออกเป็น 3 ส่วนด้วย st.tabs
tab_theory, tab_sim, tab_summary = st.tabs(["ทฤษฎี", "ตัวจำลอง", "สรุปผล"])

# --- Tab 1: ทฤษฎี ---
with tab_theory:
    st.header("ทฤษฎี (Theory)")
    st.write("ระบุเนื้อหาและสูตร Euler's Method:")
    st.latex(r"y_{i+1} = y_i + h \cdot f(x_i, y_i)")

# --- Tab 2: ตัวจำลอง ---
with tab_sim:
    st.header("ตัวจำลอง (Simulator)")
    st.info(f"ค่า Step size (h) ที่ระบุ: **{h}**")
    
    # คำนวณหาคำตอบด้วยวิธี Euler's Method
    x_vals = []
    y_euler = []
    
    curr_x = X0
    curr_y = Y0
    
    # วนลูปคำนวณตามช่วง x0 ถึง x_end
    while curr_x <= X_END + 1e-9:
        x_vals.append(round(curr_x, 6))
        y_euler.append(curr_y)
        curr_y = curr_y + h * f(curr_x, curr_y)
        curr_x += h
        
    # คำนวณ Exact Solution และค่า Error
    y_exact = [exact_sol(x) for x in x_vals]
    errors = [abs(ex - eu) for ex, eu in zip(y_exact, y_euler)]
    
    # 2. แสดงกราฟเปรียบเทียบระหว่าง Exact Solution และ Numerical Solution
    st.subheader("Graph Comparison")
    chart_data = pd.DataFrame({
        "Exact solution": y_exact,
        "Numerical solution (Euler's)": y_euler
    }, index=x_vals)
    st.line_chart(chart_data)
    
    # 3. ตารางเปรียบเทียบผลลัพธ์ตาม Format ในโจทย์
    st.subheader("Results Table")
    df_table = pd.DataFrame({
        "Euler's": [f"{v:.7f}" for v in y_euler],
        "Exact": [f"{v:.7f}" for v in y_exact],
        "Error": [f"{v:.7f}" for v in errors]
    }, index=[f"{x:.1f}" for x in x_vals])
    
    st.dataframe(df_table, use_container_width=True)

# --- Tab 3: สรุปผล ---
with tab_summary:
    st.header("สรุปผล (Conclusion)")
    st.write("ระบุข้อสรุปเกี่ยวกับการเปรียบเทียบค่า Error เมื่อปรับเปลี่ยนค่า h")
