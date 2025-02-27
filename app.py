import streamlit as st
import random
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📀 Data Sweeper", layout="wide")



st.markdown('<p style="text-align:center; font-weight:bold; font-size:60px; color:blue;">📀 Data Sweeper</p>', unsafe_allow_html=True)
st.write('<p style="text-align:center; margin-top:20px;">Transform your files between CSV and Excel formats with built-in data cleaning and visualization</p>', unsafe_allow_html=True)

upload_files = st.file_uploader("📂 Upload your CSV or EXCEL file:", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
        for file in upload_files:
            file_ext = os.path.splitext(file.name)[-1].lower()

            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue

            st.write(f"**📄 File Name:** {file.name}")
            st.write(f"**📏 File Size:** {file.size/1024:.2f} KB")

            st.subheader("👀 Data Preview")
            st.dataframe(df.head())

            st.subheader("🧹 Fill Missing Values")
            fill_method = st.radio("Choose method to fill missing values:", ["None", "Mean", "Median", "Mode"])

            if fill_method != "None":
                for column in df.columns:
                    if df[column].isnull().sum() > 0:
                        if fill_method == "Mean" and df[column].dtype in ['float64', 'int64']:
                            df[column].fillna(df[column].mean(), inplace=True)
                        elif fill_method == "Median" and df[column].dtype in ['float64', 'int64']:
                            df[column].fillna(df[column].median(), inplace=True)
                        elif fill_method == "Mode":
                            mode_value = df[column].mode()[0]
                            df[column].fillna(mode_value, inplace=True)

                st.write(f"Missing values filled using {fill_method}.")
                st.dataframe(df.head())

            st.subheader("❌ Remove Duplicates")
            remove_duplicates = st.checkbox("Remove duplicate rows")

            if remove_duplicates:
                before_remove = len(df)
                df.drop_duplicates(inplace=True)
                after_remove = len(df)
                st.write(f"Removed {before_remove - after_remove} duplicate rows.")
                st.dataframe(df.head())

            st.subheader("📊 Data Visualization")

            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

            if not numeric_columns:
                st.warning("⚠ No numeric columns available for visualization.")
                continue

            chart_options = ["Bar Chart", "Line Chart"]

            chart_type = st.selectbox(f"📌 Select Chart Type for {file.name}",
                                    chart_options, key=f"chart_{file.name}")

            selected_column = st.selectbox(f"📈 Select Column for Visualization in {file.name}", numeric_columns, key=f"col_{file.name}")

            custom_column_name = st.text_input("Enter custom column name (e.g., 'Total Test'):") 

            if custom_column_name and custom_column_name not in df.columns:
                df[custom_column_name] = df[selected_column]

            top_n = st.slider("Select top N categories to display in chart", min_value=1, max_value=20, value=10)

            if selected_column or custom_column_name:
                fig, ax = plt.subplots()

                if custom_column_name:
                    data_for_chart = df[custom_column_name]
                else:
                    data_for_chart = df[selected_column]

                if chart_type == "Bar Chart":
                    value_counts = data_for_chart.value_counts().nlargest(top_n)
                    value_counts.plot(kind='bar', ax=ax, color='skyblue')
                    ax.set_ylabel("Count")

                elif chart_type == "Line Chart":
                    data_for_chart.head(top_n).plot(kind='line', ax=ax, color='red', marker='o')
                    ax.set_ylabel("Value")

                ax.set_title(f"{chart_type} for {custom_column_name or selected_column}")
                st.pyplot(fig)

            st.subheader("⬇️ Download Cleaned Data")

            def convert_df_to_csv(df):
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df_to_csv(df)
            st.download_button(
                label="Download Cleaned Data as CSV",
                data=csv,
                file_name=f"cleaned_{file.name}",
                mime="text/csv"
            )

else:
        st.warning("⚠ No files uploaded yet.")



