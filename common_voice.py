import os
# os.environ['TRANSFORMERS_CACHE'] = '/mnt/hf_cache'
from datasets import load_dataset

import streamlit as st
import pandas as pd
import numpy as np

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import plotly.express as px

# pd.options.plotting.backend = "plotly" 


# TODO show average sentence length
# TODO show audio stats
# TODO speed better caching

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

@st.cache(suppress_st_warning=True)
def cache_graph(dat,y,x,color=None):
    #I feel like this doesn't work correctly 
    return px.bar(dat,y=y,x=x,color=color)

@st.cache(suppress_st_warning=True)
def cache_dataset(language,split=None):
    dat=load_dataset("common_voice",language,split=split)
    if split:
        return pd.DataFrame(dat)
    else:
        return dat


language_codes=['ab', 'ar', 'as', 'br', 'ca', 'cnh', 'cs', 'cv', 'cy', 'de', 'dv', 'el', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'fy-NL', 'ga-IE', 'hi', 'hsb', 'hu', 'ia', 'id', 'it', 'ja', 'ka', 'kab', 'ky', 'lg', 'lt', 'lv', 'mn', 'mt', 'nl', 'or', 'pa-IN', 'pl', 'pt', 'rm-sursilv', 'rm-vallader', 'ro', 'ru', 'rw', 'sah', 'sl', 'sv-SE', 'ta', 'th', 'tr', 'tt', 'uk', 'vi', 'vot', 'zh-CN', 'zh-HK', 'zh-TW']


return_mode_value = DataReturnMode.AS_INPUT 
update_mode_value = GridUpdateMode.SELECTION_CHANGED

def configure_grid_stat(df):

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=False)
    # gb.configure_side_bar()

    gb.configure_selection("multiple", use_checkbox=False,rowMultiSelectWithClick=True, suppressRowDeselection=False)

#     gb.configure_grid_options(domLayout='autoHeight')
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()
    return gridOptions

def configure_grid_detail(df):

    gb = GridOptionsBuilder.from_dataframe(df)

    # gb.configure_default_column(groupable=False, value=True, enableRowGroup=False, editable=False)
    # gb.configure_side_bar()
    gb.configure_default_column(editable=False)
    gb.configure_column("sentence",initialPinned="left")
#     gb.configure_column("client_id",hide=True)
    gb.configure_selection("single", use_checkbox=False)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal')

    gridOptions = gb.build()
    return gridOptions

st.sidebar.markdown("# Common Voice Explorer")
st.sidebar.markdown('[Common Voice](https://commonvoice.mozilla.org/en/datasets) dataset by Mozilla')

language=st.sidebar.selectbox("Language code:",language_codes)
placeholder = st.sidebar.empty()
placeholder.markdown('Loading for the first time may take a while...downloading dataset :hourglass_flowing_sand:')
dat = cache_dataset(language, split=None)
split=placeholder.multiselect("Split:",list(dat.keys()),default="train")
if len(split)>1:
    split="+".join(split)
elif split:
    split=split[0]
    
split_stat=pd.DataFrame(dat.num_rows.items(), columns=['split', 'num_rows'])
fig =  cache_graph(split_stat,y='split',x='num_rows')
st.sidebar.plotly_chart(fig, use_container_width=True,config=dict(displayModeBar=False))
st.sidebar.markdown("Dataset Explorer by [Ceyda Cinarel](https://github.com/cceyda/common-voice-explorer)")

chart_data = cache_dataset(language, split=split)
 

cols=["accent", "age", "down_votes", "gender", "locale", "segment", "up_votes"]
cols_other=["sentence","path","client_id"]


st.markdown("# Stats")
st.markdown("## Distribution")
# st.markdown("x axis:first selection  color:second selection ")

attributes=st.multiselect("Colums:",cols)

if attributes:

    # chart_data = chart_data.replace(r'^\s+$', "UNK", regex=True)
    stats=chart_data.groupby(attributes).size().reset_index(name='counts')

    col1, col2 = st.columns(2)

    if len(attributes)>1:
        color=attributes[1]
    else:
        color=None
    fig = cache_graph(stats, x=attributes[0], y='counts',color=color)

    col1.plotly_chart(fig, use_container_width=True)

    gridOptions=configure_grid_stat(stats)
    with col2:
        selection=AgGrid(stats,
                        data_return_mode=return_mode_value,
                          update_mode=update_mode_value,
                        fit_columns_on_grid_load=True,
        #                  allow_unsafe_jscode=True,
                         gridOptions=gridOptions
                            )
        st.write(":point_up: Click on the table to see details")
        
    condition=False
    if selection['selected_rows']:
        for r in selection['selected_rows']:
        
            del r["counts"]
#             st.write(r)
            sub_cond=True
            for a in r.keys():
                sub_cond&=(chart_data[a]==r[a])

            condition|=sub_cond

        detail_frame=chart_data[condition]
        gridOptions=configure_grid_detail(detail_frame)

        detail_selection=AgGrid(detail_frame,
                            data_return_mode=return_mode_value,
                              update_mode=update_mode_value,
            #                  allow_unsafe_jscode=True,
                             gridOptions=gridOptions
                                )
        if detail_selection['selected_rows']:
            
            example=detail_selection['selected_rows'][0]
            st.audio(example["path"])
            st.write(example["sentence"])
        else:
            st.write(":point_up: Click on the table to listen")
            
else:
    st.write(":point_up: Select a column or two")


