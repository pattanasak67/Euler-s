import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- ฟังก์ชันสำหรับผู้ใช้ปรับแก้ตามโจทย์จริง ---
def f(x, y):
    # แก้ไขสมการอนุพันธ์ที่นี่ (ตัวอย่าง: y' = x + y)
    return x + y 

def get_exact_solution(x):
    # แก้ไขสมการ Exact Solution ที่นี่
    return 2 * np.exp(x) - x - 1
# ----------------------------------------

# หัวข้อโปรเจกต์
st.title("Project1# Use the Euler’s to approximate the solutions to the initial-value problems")

# 1. Layout Organization: จัดวางหน้าตาแอปพลิเคชันและรับค่าพารามิเตอร์
st.sidebar.header("Input Parameters")
x0 = st.sidebar.number_input("Initial x (x0)", value=0.0)
y0 = st.sidebar.number_input("Initial y (y0)", value=1.0)
h = st.sidebar.number_input("Step size (h)", value=0.1)
n = st.sidebar.number_input("Number of steps (n)", value=10, step=1)

# แบ่งเนื้อหาออกเป็นส่วนๆ ด้วย st.tabs
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
        
    # 2. แสดงกราฟเปรียบเทียบระหว่าง exact solution และ numerical solution
    st.subheader("Graph Comparison")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_vals, y_exact_vals, label="Exact Solution", color='blue', marker='o')
    ax.plot(x_vals, y_euler, label="Numerical (Euler's)", color='red', linestyle='--', marker='x')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    
    # 3. ตารางเปรียบเทียบผลลัพธ์
    st.subheader("Results Table")
    # สร้าง DataFrame โดยกำหนด Format ทศนิยมตามตัวอย่างในภาพ
    df = pd.DataFrame({
        "x": x_vals,
        "Euler's": [f"{val:.7f}" for val in y_euler],
        "Exact": [f"{val:.7f}" for val in y_exact_vals],
        "Error": [f"{val:.7f}" for val in errors]
    })
    
    # ซ่อนชื่อคอลัมน์แรกด้วยการเซ็ต index เป็น x เพื่อให้รูปแบบตรงตามภาพอ้างอิง
    df.set_index("x", inplace=True)
    st.dataframe(df, use_container_width=True)

with tab_summary:
    st.header("สรุปผล (Conclusion)")
    st.write("ใส่เนื้อหาสรุปผลการทดลองเปรียบเทียบค่า Error ที่ได้จากการเปลี่ยน step size (h)")
