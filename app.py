import streamlit as st
import pandas as pd
import plotly.express as px

# App ki basic settings
st.set_page_config(page_title="Auto Dashboard Generator", layout="wide")

st.title("📊 Google Sheets Auto-Dashboard")
st.write("Apni Google Sheet ka link niche paste karein aur jadoo dekhein!")

# User se link lena
sheet_url = st.text_input("Google Sheet (CSV) Link:", placeholder="Yahan link paste karein...")

if sheet_url:
    try:
        # Data ko read karna
        df = pd.read_csv(sheet_url)
        st.success("Data successfully load ho gaya!")
        
        # Data ka preview dikhana
        st.subheader("Tumhara Data")
        st.dataframe(df.head())
        
        # Dashboard ke options (e.g., Dates vs Earnings/Views)
        st.subheader("Banao Apna Chart")
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("X-Axis select karo (e.g., Dates, Names):", df.columns)
        with col2:
            y_axis = st.selectbox("Y-Axis select karo (e.g., Earnings, Views):", df.columns)
            
        # Chart generate karna
        if st.button("Generate Chart"):
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}", template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Error: Link theek nahi hai ya sheet public nahi hai. Pura link check karo.")
else:
    st.info("👆 Upar link paste karein tool ko test karne ke liye.")
