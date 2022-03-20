from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
materials = {}

def add_material(material_id, container):
    with requests.Session() as session:
        get_url = 'https://glazy.org/api/recipes/{}'.format(material_id)
        r = session.get(get_url) #, headers=request_headers)
        j = json.loads(r.text)
    materials[material_id] = j

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
    
    col1, col2, col3 = st.columns([2,1,1])
    col1.header("Material")
    col2.header("Min %")
    col3.header("Max %")
    
    options = {}
    min_perc = {}
    
    for n in range(4):       
        col1, col2, col3 = st.columns([2,1,1])
        options[n] = col1.selectbox(
         '',
         ('Kaolin', 'Silica', 'Feldspar'),
         key = 'Material {}'.format(n),
         #on_change=add_material,
         #args=material_id
          )
        min_perc[n] = col2.number_input(
         '',
         min_value=0.0,
         max_value=100.0,
         step=0.1,
         key = 'Min {}'.format(n),
        max_perc[n] = col3.number_input(
         '',
         min_value=0.0,
         max_value=100.0,
         step=0.1,
         key = 'Max {}'.format(n),
         #on_change=add_material,
         #args=material_id
          )
