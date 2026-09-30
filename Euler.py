import streamlit as st
import pandas as pd
import numpy as np

# --- ฟังก์ชันสำหรับผู้ใช้ปรับแก้ตามโจทย์จริง ---
def f(x, y):
    # ตัวอย่างสมการอนุพันธ์ y' = x + y
    return x + y 

def get_exact_solution(x):
    # ตัวอย่างสมการ Exact Solution
    return 2 * np.exp(x) - x - 1
# ----------------------------------------

# หัวข้อโปรเจกต์
st.title("Project1# Use the Euler’s to approximate the solutions to the initial-value problems")

# 1. Layout Organization: รับค่าพารามิเตอร์ใน Sidebar
st.sidebar.header("Input Parameters")
x0 = st.sidebar.number_input("Initial x (x0)", value=0.0)
y0 = st.sidebar.number_input("Initial y (y0)", value=1.0)
h = st.sidebar.number_input("Step size (h)", value=0.1)
n = st.sidebar.number_input("Number of steps (n)", value=10, step=1)

# แบ่งเนื้อหาด้วย st.tabs
tab_theory, tab_sim, tab_summary = st.tabs(["ทฤษฎี", "ตัวจำลอง", "สรุปผล"])

with tab_theory:
    st.header("ทฤษฎี (Theory)")
    st.write("ใส่เนื้อหาและสูตรทางคณิตศาสตร์ของวิธี Euler's Method ที่นี่")

with tab_sim:
    st.header("ตัวจำลอง (Simulator)")
    
    # คำนวณค่า Numerical Solution ด้วยวิธี Euler's Method
    x_vals = [x0]
    y_euler = [y0]
    y_exact_vals = [get_exact_solution(x0)]
    errors = [abs(y_exact_vals[0] - y_euler[0])]
    
    curr_x = x0
    curr_y = y0
    
    for _ in range(int(n)):
        curr_y = curr_y + h * f(curr_x, curr_y)
        curr_x = curr_x + h
        
        exact_val = get_exact_solution(curr_x)
        
        x_vals.append(curr_x)
        y_euler.append(curr_y)
        y_exact_vals.append(exact_val)
        errors.append(abs(exact_val - curr_y))
        
    # 2. แสดงกราฟเปรียบเทียบด้วย st.line_chart ของ Streamlit โดยตรง
    st.subheader("Graph Comparison")
    chart_data = pd.DataFrame({
        "Exact solution": y_exact_vals,
        "Numerical solution (Euler's)": y_euler
    }, index=x_vals)
    st.line_chart(chart_data)
    
    # 3. ตารางเปรียบเทียบผลลัพธ์
    st.subheader("Results Table")
    df_table = pd.DataFrame({
        "x": x_vals,
        "Euler's": [f"{val:.7f}" for val in y_euler],
        "Exact": [f"{val:.7f}" for val in y_exact_vals],
        "Error": [f"{val:.7f}" for val in errors]
    })
    
    df_table.set_index("x", inplace=True)
    st.dataframe(df_table, use_container_width=True)

with tab_summary:
    st.header("สรุปผล (Conclusion)")
    st.write("ใส่เนื้อหาสรุปผลการทดลองเปรียบเทียบค่า Error")
