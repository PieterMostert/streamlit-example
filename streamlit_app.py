from collections import namedtuple
import altair as alt
import math
import pandas as pd
import requests
import streamlit as st
import json

st.set_page_config(layout = 'wide')
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""

st.session_state.selected_materials = {}
st.session_state.selected_oxides = {}
st.session_state.user_id = ''
st.session_state.inventory = []

def get_inventory():
    with requests.Session() as session:
        get_url = 'https://glazy.org/api/usermaterials?u={}'.format(st.session_state.user_id)
        r = session.get(get_url)
        j = json.loads(r.text)
        st.session_state.inventory = [x['materialName'] for x in j['data']]

def add_material(n):
    material_id = st.session_state['Material {}'.format(n)]
    with requests.Session() as session:
        get_url = 'https://glazy.org/api/recipes/{}'.format(material_id)
        r = session.get(get_url) #, headers=request_headers)
        #j = json.loads(r.text)
    #st.session_state['Material {} analysis'.format(material_id)] = j
    
def add_oxides():
    for ox in st.session_state.selected_oxides:       
        col1, col2, col3 = st.columns([2,1,1])
        oxide_labels[ox] = col1.text(ox)
        min_perc[ox] = col2.number_input(
         '',
         min_value=0.0,
         max_value=100.0,
         step=0.1,
         key = 'Min {}'.format(ox)
         )
        max_perc[ox] = col3.number_input(
         '',
         min_value=0.0,
         max_value=100.0,
         value=100,
         step=0.1,
         key = 'Max {}'.format(ox),
         #on_change=add_material,
         #args=material_id
         )


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    alpha = st.slider("Alpha", 0.0, 10.0, 0.5, 0.001)

    Point = namedtuple('Point', 'x y')
    data = []

    for curr_point_num in range(total_points):
        radius = math.sqrt(curr_point_num)
        angle = radius * 2 * math.pi * math.sqrt(alpha)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
    
    user = st.container()
    material_input = st.container()
    oxide_input = st.container()
    
    with user:
        st.text_input('Glazy user ID', on_change=get_inventory)
                                   
    with material_input:
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        col1.subheader("Material")
        col2.subheader("Min constraint")
        col3.subheader("Max constraint")
        col4.subheader("Min possible")
        col5.subheader("Max possible")

        options = {}
        min_constraint = {}
        max_constraint = {}
        min_possible = {}
        max_possible = {}

        for n in range(4):       
            col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
            options[n] = col1.selectbox(
             '',
             [''] + st.session_state.inventory,
             key = 'Material {}'.format(n),
             #on_change=add_material,
             #args=material_id
              )
            min_constraint[n] = col2.number_input(
             '',
             min_value=0.0,
             max_value=100.0,
             step=0.1,
             key = 'Min {}'.format(n)
             )
            max_constraint[n] = col3.number_input(
             '',
             min_value=0.0,
             max_value=100.0,
             value=100.0,
             step=0.1,
             key = 'Max {}'.format(n),
             #on_change=add_material,
             #args=material_id
             )
            min_possible[n] = col4.text('')
            max_possible[n] = col5.text('')
                                   
    with oxide_input:
        col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
        col1.subheader("Oxide")
        col2.subheader("Min constraint")
        col3.subheader("Max constraint")
        col4.subheader("Min possible")
        col5.subheader("Max possible")
