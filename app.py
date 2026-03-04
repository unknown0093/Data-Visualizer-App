import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auto Dashboard Generator", layout="wide")

st.title("📊 Google Sheets Auto-Dashboard")
st.write("Apni Google Sheet ka link niche paste karein. (Note: Sheet ka access 'Anyone with the link' hona chahiye)")

# User se normal link lena
sheet_url = st.text_input("Google Sheet Link Paste Karein:", placeholder="https://docs.google.com/spreadsheets/d/...")

if sheet_url:
    try:
        # MAGIC TRICK: Normal link ko automatically CSV format mein convert karna
        if "/d/" in sheet_url:
            # Link se sheet ka ID nikalna
            sheet_id = sheet_url.split("/d/")[1].split("/")[0]
            # Naya CSV link banana
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        else:
            csv_url = sheet_url # Agar pehle se CSV link ho
            
        # Data load karna
        df = pd.read_csv(csv_url)
        st.success("Data successfully load ho gaya! 🎉")
        
        st.subheader("Data Preview")
        st.dataframe(df.head())
        
        # Dashboard Builder
        st.subheader("Dashboard Options")
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("X-Axis (Bottom Line):", df.columns)
        with col2:
            y_axis = st.selectbox("Y-Axis (Left Line):", df.columns)
            
        if st.button("Generate Chart"):
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}", template="plotly_white", color=x_axis)
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error("Error: Data load nahi ho saka. Make sure sheet ka link theek hai aur access 'Anyone with the link' par set hai.")
