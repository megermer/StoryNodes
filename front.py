import streamlit as st
import numpy as np
import pandas as pd
import graphviz as gv
from utils import back
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

def update_connections():
    for i in range(len(connection)):
        st.write(connection[i])

elements = pd.Series(['Placeholder1', 'Placeholder2', 'Placeholder3'])
connections = pd.Series([])

element = st.selectbox(
    'Add element',
    ('Character', 'Place', 'Thing'),
    key="element"
)

name = st.text_input('Name', key="name")
description = st.text_area('Description', key="description")

connection = st.multiselect(
    'Is connected with: ',
    elements, 
    on_change = update_connections
)

submit = st.button(
                    label="submit", 
                    on_click=back.create_node, 
                    # args=(st.session_state.name,),
                    args=(element, name)
                    )



