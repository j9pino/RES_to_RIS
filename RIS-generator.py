import streamlit as st
import tempfile
import pandas as pd

st.experimental_memo.clear()
st.set_page_config(page_title="RES to RIS")
st.title("RES to RIS")

#RES_df = pd.read_excel(r"C:\Users\9ex\OneDrive - Oak Ridge National Laboratory\Junk\report (2).xlsx")

# Declare object to open temporary file for writing
tmp = tempfile.NamedTemporaryFile('w+t', encoding = 'utf-8-sig')

# Declare the name of the temporary file
tmp.name="RES-to-RIS-Generator.RIS"

@st.experimental_memo(suppress_st_warning=True)
def RES_to_RIS(df):
    for line in range(len(df)):
        if df.iloc[line]['Communication Type'] == 'Journal':
            TY = 'JOUR' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Abstract':
            TY = 'UNPB' + '\n'
        elif df.iloc[line]['Communication Type'] == 'ORNL Report':
            TY = 'RPRT' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Presentation':
            TY = 'UNPB' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Conference Paper':
            TY = 'CPAPER' + '\n'
        elif df.iloc[line]['Communication Type'] == 'LDRD Report':
            TY = 'RPRT' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Other STI':
            TY = 'UNPB' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Book':
            TY = 'BOOK' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Book Chapter':
            TY = 'CHAP' + '\n'
        elif df.iloc[line]['Communication Type'] == 'Thesis / Dissertation':
            TY = 'UNPB' + '\n'
        TI = df.iloc[line]['Title'] + '\n'
        C1 = 'Report No.: ' + str(df.iloc[line]['Report Number']) + '\n'
        try:
            ID = 'RES Pub ID: ' + str(df.iloc[line]['\ufeffPub Id']) + '\n'
        except KeyError:
            ID = '\n'
        Authors = []
        Authors = df.iloc[line]['Authors'].split(', ')
        AUlength = len(Authors)
        AU = 'AU  - '
        AUlist = []
        for i in range(AUlength):
            name_surname = Authors[i].split(" ")
            to_output = name_surname[-1] + ", " + name_surname[0]   
            AUi = AU + to_output
            AUlist.append(AUi)
            spam = ('\n').join(AUlist)
    
        T2 = str(df.iloc[line]['Journal Name']) + '\n'
        AB = str(df.iloc[line]['Abstract']) + '\n'
        VL = str(df.iloc[line]['Volume']) + '\n'
        IS = str(df.iloc[line]['Issue']) + '\n'
        SP = str(df.iloc[line]['Page Start']) + '\n'
        EP = str(df.iloc[line]['Page End']) + '\n'
        PY = str(df.iloc[line]['Publication Year']) + '\n'
        DO = str(df.iloc[line]['DOI']) + '\n'
        ER = '' + '\n\n'
        
        tmp.write('TY  - ' + TY +
                      'TI  - ' + TI +
                      str(spam) + '\n' +
                      'T2  - ' + T2 +
                      'AB  - ' + AB +
                      'VL  - ' + VL +
                      'IS  - ' + IS +
                      'SP  - ' + SP +
                      'EP  - ' + EP +
                      'PY  - ' + PY +
                      'DO  - ' + DO +
                      'C1  - ' + C1 +
                      'ID  - ' + ID + 
                      'ER  - ' + ER)
    tmp.seek(0)
    st.download_button(
        label="Download RIS File",
        data=tmp.read(),
        file_name='RES-to-RIS.RIS')

data = st.file_uploader("Upload your RES export file",
                       key = '1')
if data is not None:
    RES_df = pd.read_excel(data, header=[0])
    RES_df = RES_df.fillna('')
    #display dataframe of uploaded DOIs     
    st.dataframe(RES_df)
    #introduce streamlit proress bar widget
    RES_to_RIS(RES_df)

