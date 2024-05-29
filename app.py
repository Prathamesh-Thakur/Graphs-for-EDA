import streamlit as st 
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

st.title("Graphs for Exploratory Data Analysis")

file = st.file_uploader("Upload a csv, excel, text or json file.", type = ['csv', 'xlsx'])
if file is not None:
    extension = Path(file.name).suffix
    if extension == '.csv':
        df = pd.read_csv(file)
    elif extension == '.xlsx':
        df = pd.read_excel(file)
    elif extension == '.txt':
        df = pd.read_table(file)
    elif extension == '.json':
        df = pd.read_json(file)
    else:
        st.write("File format not supported.")
    st.dataframe(df.head())

    numeric_columns = []
    categorical_columns = []

    for i in df.dtypes.index:
        if df.dtypes[i] == 'int64' or df.dtypes[i] == 'float64':
            numeric_columns.append(i)
        
        else:
            categorical_columns.append(i)
    
    st.write("Available numeric columns:")
    st.write(numeric_columns)

    st.write("Available categorical columns:")
    st.write(categorical_columns)

    option1 = st.selectbox(label = "Enter column on X axis:", options = df.columns, index = None)

    options2 = [i for i in df.columns if i != option1]
    option2 = st.selectbox(label = "Enter column on Y axis:", options = options2, index = None)
    if option2 is not None:
        html_str_1 = f"""<span>{option1}</span>"""
        html_str_2 = f"""<span>{option2}</span>"""
        subdf = df[[option1, option2]]
        st.subheader("Available charts:")
        
        st.caption("Line chart for " + html_str_1 + " against " + html_str_2, unsafe_allow_html = True)
        st.line_chart(subdf, x = option1, y = option2)
        st.text("Code for the graph")
        body1 = '''import matplotlib.pyplot as plt 
        plt.plot(X-axis column name, Y-axis column name)
        plt.show()'''
        st.code(body = body1, language = 'python')
        
        st.caption("Scatter chart for " + html_str_1 + " against " + html_str_2, unsafe_allow_html = True)
        st.scatter_chart(subdf, x = option1, y = option2)
        st.text("Code for the graph")
        body2 = '''import matplotlib.pyplot as plt 
        plt.scatter(X-axis column name, Y-axis column name)
        plt.show()'''
        st.code(body = body2, language = 'python')

        if option1 in categorical_columns:
            list1 = subdf[option1].value_counts().rename_axis('unique_values').to_frame('Frequency')
            st.caption("Bar chart for " + html_str_1 + " against frequencies of each " + html_str_1, unsafe_allow_html = True)
            st.bar_chart(list1, y = 'Frequency')
            st.text("Code for the graph")
            body3 = '''dataframe[column_name].value_counts().plot(kind = 'bar')'''
            st.code(body = body3, language = 'python')

            st.caption("Pie chart for " + html_str_1,  unsafe_allow_html = True)
            fig1, ax1 = plt.subplots()
            ax1.pie(subdf[option1].value_counts(), labels = subdf[option1].unique(), autopct='%1.1f%%')
            ax1.axis('equal')
            st.pyplot(fig1)
            st.text("Code for the graph")
            body4 = '''plt.pie(column.value_counts(), labels = column.unique(), autopct='%1.1f%%')
                    plt.show()'''
            st.code(body = body4, language = 'python')

        if option2 in categorical_columns:
            list2 = subdf[option2].value_counts().rename_axis('unique_values').to_frame('Frequency')
            st.caption("Bar chart for " + html_str_2 + " against frequencies of each " + html_str_2, unsafe_allow_html = True)
            st.bar_chart(list2, y = 'Frequency')
            st.text("Code for the graph")
            body3 = '''df[column_name].value_counts().plot(kind = 'bar')'''
            st.code(body = body3, language = 'python')

            st.caption("Pie chart for " + html_str_1,  unsafe_allow_html = True)
            fig1, ax1 = plt.subplots()
            ax1.pie(subdf[option2].value_counts(), labels = subdf[option2].unique(), autopct='%1.1f%%')
            ax1.axis('equal')
            st.pyplot(fig1)
            st.text("Code for the graph")
            body4 = '''plt.pie(column.value_counts(), labels = column.unique(), autopct='%1.1f%%')
                    plt.show()'''
            st.code(body = body4, language = 'python')
