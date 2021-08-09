import streamlit as st 
import pandas as pd
import numpy as np

from PIL import Image

st.write("""
## NEXT BEST ACTION: HEALTHCARE
	""")
expander_bar = st.expander("About")
expander_bar.markdown("""
This app takes HCP parameters as inputs along with a rules configuration file, and predicts the Next Best Action for each individual HCP.

The NBA prediction can also be done in batch format by uploading a file with HCP details
""")


st.subheader("")

st.sidebar.header("HCP input parameters")

#st.sidebar.markdown("""
#[Example CSV input file](https://www.csv_hosting_site.com/example_data.csv)
#	""")


st.sidebar.write("Upload rules file or use the default rules file")
rules_file = st.sidebar.file_uploader("Upload your rules config CSV file", type=["csv"])




if rules_file is not None:
    st.write("Rules Config file uploaded, using config rules provided by user")
else:
    st.write('Awaiting Rules config to be uploaded, Currently using default rules')





#Collect User Input Features into the Dataframe





hcp_score = st.sidebar.slider("HCP Score", 0,100,30,step=10)

lifestage= st.sidebar.selectbox('Select HCP lifestage as per Journey',('Access/Support','General Brand Info','Efficacy & Safety','Diagnosis', 'Disease Information'))


specialty = st.sidebar.selectbox('Select HCP Specialty',('Anesthesiology','Cardiology', 'Ophthalmology','Pediatrics','Psychiatry'))


gender=st.sidebar.radio(
    "Gender",
    ("Male", "Female", "Others"))

st.sidebar.write("Additional Rules can be configured here based on data, or this data can be sent to a model API for prediction")


image_lifestage = Image.open('hcp_campaign_lifestage.png')
image_hcp_score = Image.open('hcp_scoring.png')
if st.button('View Details on Lifestage'):
	st.image(image_lifestage, width = 50, use_column_width=True)
if st.button('View Details on HCP Scoring'):
	st.image(image_hcp_score, width = 50, use_column_width=True)


data = {'HCP_Score':hcp_score,'Lifestage':lifestage,'Specialty':specialty,'Gender':gender}

df = pd.DataFrame(data,index=[0])
st.subheader("Data Snapshot")
st.write(df.head())




## Content Config

@cache
def read_data(filepath):
	df = pd.read_csv(filepath)
	return df

if rules_file is not None:
	rules_df = pd.read_csv(rules_file)
else:
	filepath = "rules_config.csv"
	rules_df = read_data(filepath)


filtered = rules_df.loc[(rules_df['Specialty']==specialty) & (rules_df['ContentGroup']==lifestage) & (rules_df['HCP_Score_min']<hcp_score) & (rules_df['HCP_Score_max']>=hcp_score)]

result = filtered['ContentDetails'].values


st.subheader("Next Best Content Recommendation: ")
st.subheader(result[0])


