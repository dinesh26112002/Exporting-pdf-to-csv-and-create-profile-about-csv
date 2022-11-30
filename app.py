import streamlit as st # data app development
import subprocess
from subprocess import STDOUT
import os 
import base64 
import camelot as cam 
import numpy as np
import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.sidebar.header('''
                   **How TO USE**
#**`Step 1` Upload you'r pdf file you want to extract**

#**`Step 2` Now select the page number which you want to extract as csv.**

#**`Step 3` Download the csv file you extract.**

#**`Step 4`   If you want to see your profile of the downloaded csv.**

#**`Step 5` Upload your csv file by draging or using browse option below**

#**`Step 6` The profile is displayed on the right side**

#**`Step 7` If you want to check how profiling works on csv press example dataset button.**

#**`Step 8` By this you can verify how it is working.**

**`Thank you for visiting`**
''')

# to run this only once and it's cached

st.title("PDF Table Extractor")
st.subheader("with `Camelot` Python library")

st.image("https://raw.githubusercontent.com/camelot-dev/camelot/master/docs/_static/camelot.png", width=200)


# file uploader on streamlit 

input_pdf = st.file_uploader(label = "upload your pdf here", type = 'pdf')

st.markdown("### Page Number")

page_number = st.text_input("Enter the page # from where you want to extract the PDF eg: 3", value = 1)

# run this only when a PDF is uploaded

if input_pdf is not None:
    # byte object into a PDF file 
    with open("input.pdf", "wb") as f:
        base64_pdf = base64.b64encode(input_pdf.read()).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))
    f.close()

    # read the pdf and parse it using stream
    table = cam.read_pdf("input.pdf", pages = page_number, flavor = 'stream')

    st.markdown("### Number of Tables")

    # display the output after parsing 
    st.write(table)

    # display the table

    if len(table) > 0:

        # extract the index value of the table
        
        option = st.selectbox(label = "Select the Table to be displayed", options = range(len(table) + 1))

        st.markdown('### Output Table')

        # display the dataframe
        
        op_df = table[int(option)-1].df

        st.dataframe(op_df)

        st.download_button("Download csv",op_df.to_csv(),mime='text/csv')

        
        

# Web App Title
st.markdown('''
# **See the profile of the csv you have `Downloaded` above**
This is the **EDA App** created in Streamlit using the **pandas-profiling** library.
**Credit:** App built in `Python` + `Streamlit` by [Dinesh]
''')

# Upload CSV data
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")

# Pandas Profiling Report
if uploaded_file is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    df = load_csv()
    pr = ProfileReport(df, explorative=True)
    st.header('**Input DataFrame**')
    st.write(df)
    st.write('---')
    st.header('**Pandas Profiling Report**')
    st_profile_report(pr)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        # Example data
        @st.cache
        def load_data():
            a = pd.DataFrame(
                np.random.rand(100, 5),
                columns=['a', 'b', 'c', 'd', 'e']
            )
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)