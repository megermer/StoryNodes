import streamlit as st
import numpy as np
import pandas as pd
import graphviz as gv
from utils import back
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

# Placeholder for existing nodes so the order can select these to make connections
# existing_nodes = ['Thing1', 'Thing2']
existing_nodes = back.retrieve_all_nodes()

# Select the type of node being added
node_type = st.selectbox(
    'Select element type: ',
    ('Character', 'Place', 'Thing'),
    key="new_element"
)

# Type the name of the node being added
name = st.text_input('Name', key="name")

# Type the description of the onde being added
description = st.text_area('Description', key="description")

# Choose what *existing* nodes the new node is connected to
connections = st.multiselect(
    'Is connected with: ',
    existing_nodes, 
)

for connection in connections:
    st.text_input(f'Type of relationship to {connection} : ', key=connection)

# submit_args needs to replace 'connections' with a dictionary of connections and their relationship types


# Data to be sent to the back and used to create the node and its relationships
submit_args = (node_type, name, connections)

# Submit button to send the data back 
submit = st.button(
                    label="Add Element", 
                    on_click=back.create_node, 
                    args=submit_args
                    )

# Test/checker for checking the arguments
st.write(submit_args)


