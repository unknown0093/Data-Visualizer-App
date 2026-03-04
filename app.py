import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & UI Settings
st.set_page_config(page_title="Pro Auto-Dashboard", page_icon="🚀", layout="wide")

# Custom CSS for UI Enhancement
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    h1, h2, h3 {color: #2c3e50;}
    .stMetric {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Pro Auto-Dashboard & Task Tracker")
st.write("Apna data analyze karein aur daily tasks ko track karein.")

# 2. Multi-Tab Layout
tab1, tab2 = st.tabs(["📊 Data Analytics Dashboard", "✅ Task Tracker & Productivity"])

# ==========================================
# TAB 1: DATA ANALYTICS DASHBOARD
# ==========================================
with tab1:
    st.markdown("### 🔗 Data Source")
    sheet_url = st.text_input("Google Sheet Link Paste Karein (Anyone with the link):", placeholder="https://docs.google.com/spreadsheets/d/...")

    if sheet_url:
        try:
            # Auto-convert link to CSV
            if "/d/" in sheet_url:
                sheet_id = sheet_url.split("/d/")[1].split("/")[0]
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            else:
                csv_url = sheet_url
                
            df = pd.read_csv(csv_url)
            
            # 3. Smart KPI Cards (Auto-Insights)
            st.markdown("### 💡 Quick Insights")
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            
            if len(numeric_cols) >= 2:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric(label=f"Total {numeric_cols[0]}", value=round(df[numeric_cols[0]].sum(), 2))
                col2.metric(label=f"Average {numeric_cols[0]}", value=round(df[numeric_cols[0]].mean(), 2))
                col3.metric(label=f"Max {numeric_cols[1]}", value=round(df[numeric_cols[1]].max(), 2))
                col4.metric(label=f"Total Records", value=len(df))
            
            st.divider()

            # Dashboard Builder
            st.markdown("### 📈 Custom Visualization")
            col_x, col_y = st.columns(2)
            with col_x:
                x_axis = st.selectbox("X-Axis (Bottom Line):", df.columns)
            with col_y:
                y_axis = st.selectbox("Y-Axis (Left Line):", df.columns)
                
            chart_type = st.radio("Chart Style:", ["Bar Chart", "Line Chart", "Scatter Plot"], horizontal=True)
            
            # Generate Chart with Export Functionality
            if st.button("Generate HD Chart", type="primary"):
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, template="plotly_white")
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, markers=True, template="plotly_white")
                else:
                    fig = px.scatter(df, x=x_axis, y=y_axis, size=y_axis, color=x_axis, template="plotly_white")
                
                # Update layout for better UI
                fig.update_layout(title=f"<b>{y_axis} by {x_axis}</b>", title_x=0.5, margin=dict(l=20, r=20, t=50, b=20))
                
                # Show chart (Includes native Plotly camera icon for PNG export)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
                
        except Exception as e:
            st.error("Error: Data load nahi ho saka. Link check karein.")

# ==========================================
# TAB 2: TASK TRACKER & PRODUCTIVITY
# ==========================================
with tab2:
    st.markdown("### 📝 Daily Task Notepad")
    
    # Initialize Session State for tasks so they don't disappear
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    # Add new task
    new_task = st.text_input("Naya Task Likhien:", placeholder="E.g., Complete UI design...")
    if st.button("Add Task"):
        if new_task:
            st.session_state.tasks.append({"task": new_task, "done": False})
            st.rerun()

    # Display Tasks and handle checkboxes
    st.markdown("#### Your Tasks:")
    completed_count = 0
    pending_count = 0
    
    for i, task_obj in enumerate(st.session_state.tasks):
        # Create a checkbox for each task
        is_done = st.checkbox(task_obj["task"], value=task_obj["done"], key=f"task_{i}")
        st.session_state.tasks[i]["done"] = is_done
        
        if is_done:
            completed_count += 1
        else:
            pending_count += 1

    # Task Analytics (Pie Chart)
    if len(st.session_state.tasks) > 0:
        st.divider()
        st.markdown("### 🎯 Productivity Analytics")
        
        task_data = pd.DataFrame({
            "Status": ["Completed", "Pending"],
            "Count": [completed_count, pending_count]
        })
        
        fig_pie = px.pie(task_data, names="Status", values="Count", 
                         color="Status", color_discrete_map={"Completed": "#2ecc71", "Pending": "#e74c3c"},
                         hole=0.4, template="plotly_white")
        
        fig_pie.update_layout(title="<b>Task Completion Ratio</b>", title_x=0.5)
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': True})
        
    # Clear Tasks Button
    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        st.rerun()

st.markdown("---")
st.caption("💡 Tip: Kisi bhi chart ko export karne ke liye chart ke top-right corner par 'Camera' 📷 icon par click karein (Download plot as png). Pure dashboard ko PDF banane ke liye `Ctrl+P` dabayen.")
