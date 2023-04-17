import streamlit as st
import pandas as pd
import requests, json

st.set_page_config(
  # page_title="PDF-Uploader",
  # page_icon=":computer:",
  layout="wide",  # sets page to wide mode as default. 
  # initial_sidebar_state="expanded"
)

# Formats text.
def change_name_format(name):
  return name.replace("_", " ").title()

# Returns list of keys of a dictonary.
def get_column_name(keys):
  return [change_name_format(key) for key in keys.keys()]

# Displays response from the API.
def show_response(res):
  st.header("Response")
  if isinstance(res["result"], dict):
    for k, v in res["result"].items():
      st.subheader(k)
      st.write(v)
  else:
    st.write(res["result"])

title = st.text_input('Enter json')
if title:
  title = json.loads(title)
  df = pd.DataFrame(
    [list(title["data"].values())],
    columns = get_column_name(title["data"])
  )
  hide_table_row_index = """
    <style>
      thead tr th:first-child {display:none}
      tbody th {display:none}
    </style>
    """
  st.markdown(hide_table_row_index, unsafe_allow_html=True)
  st.header(change_name_format(title["topic"]))
  st.table(df)

  url = "http://216.48.187.220:5001/api/v1/SummaryGeneration"
  headers = {'Content-Type': 'application/x-www-form-urlencoded', 'x-access-token': st.secrets["auth_key"]}

  #Post API call.
  response = requests.post(url, json=title, headers=headers)

  if response:
    show_response(response.json())

