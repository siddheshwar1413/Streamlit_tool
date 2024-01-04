import streamlit as st
import pandas as pd
import numpy as np

def load_data(file):
    try:
        if file is not None and file.readable() and file.seekable() and file.tell() != 0:
            data = pd.read_excel(file)
            if data.empty:
                raise pd.errors.EmptyDataError("No data in the file")
        else:
            raise ValueError("Invalid or empty file")
    except (UnicodeDecodeError, pd.errors.EmptyDataError, ValueError):
        data = pd.read_excel(file)
    return data

def calculate_difference(df1, df2, compare_column='PropertyValue'):
    try:
        compare_values = df1[compare_column] != df2[compare_column]
        both_not_null = df1[compare_column].notnull() | df2[compare_column].notnull()
        
        # Get the rows where differences occur and both columns are not null
        diff_rows = df2[compare_values & both_not_null]

        if not diff_rows.empty:
            # Annotate cells with differences in the result DataFrame
            diff_values = np.where(compare_values, df1[compare_column].astype(str) + ' --> ' + df2[compare_column].astype(str), '')

            # Create a new DataFrame with only the rows where differences occur and both columns are not null
            result_df = diff_rows.copy()
            
            # Ensure the length of 'Differences' matches the number of rows
            result_df['Differences'] = diff_values[compare_values][:len(result_df)]
        else:
            result_df = pd.DataFrame()
            
        return result_df
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return pd.DataFrame()

def main():
    try:
        st.title("File Comparison App")

        # Upload two files
        uploaded_file1 = st.file_uploader("Upload the first file", type=["csv", "xlsx"])
        uploaded_file2 = st.file_uploader("Upload the second file", type=["csv", "xlsx"])

        if uploaded_file1 is not None and uploaded_file2 is not None:
            df1 = load_data(uploaded_file1)
            df2 = load_data(uploaded_file2)

            compare_column_name = 'PropertyValue'
            diff_values = calculate_difference(df1, df2, compare_column_name)

            st.subheader(f"Differences in the column '{compare_column_name}' between the two files:")
            st.write(diff_values)
    except Exception as e:
        st.error(f"Error Column Name is not match: {str(e)}")

if __name__ == "__main__":
    main()
