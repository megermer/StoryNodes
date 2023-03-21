import streamlit as st
import numpy as np
# import pandas as pd
import graphviz as gv
from utils import back
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from pyvis.network import Network
import logging
import streamlit.components.v1 as components

# Placeholder for existing nodes so the order can select these to make connections
existing_node_names = back.retrieve_all_node_names()

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
    existing_node_names, 
)

# submit_args needs to replace 'connections' with a dictionary of connections and their relationship types
connections_and_relations = {}
for connection in connections:
    relation_type = st.text_input(f'Type of relationship to {connection} : ', key=connection)
    connections_and_relations[connection] = relation_type

st.write(connections_and_relations)

# Data to be sent to the back and used to create the node and its relationships
submit_args = (node_type, name, connections_and_relations)

# Submit button to send the data back 
submit = st.button(
                    label="Add Element", 
                    on_click=back.create_node, 
                    args=submit_args
                    )

# Test/checker for checking the arguments
st.write(submit_args)

###################
### Pyvis graph ###
###################

# Creates Network class of specified size and styling
net = Network(height='465px', bgcolor='#222222', font_color='white')

# Test code##############################
# net.add_node(1, label="Node 1") # node id = 1 and label = Node 1
# net.add_node(2) # node id and label = 2
# net.show("test.html")
############################################

# net.add_nodes(existing_node_names)

# Retrieves all of the three categories of nodes, needed for coloring issues
characters = back.retrieve_all_nodes_of_label("Character")
places = back.retrieve_all_nodes_of_label("Place")
things = back.retrieve_all_nodes_of_label("Thing")

for character in characters:
    net.add_node(character, color = "blue")

for place in places:
    net.add_node(place, color = "red")

for thing in things:
    net.add_node(thing, color = "yellow")

net.show("test.html")

# CRUCIAL for displaying graph on server (try) and locally (except)
try:
   path = './tmp'
   net.save_graph(f'{path}/pyvis_graph.html')
   HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')
except:
    path = './html_files'
    net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html','r',encoding='utf-8')

components.html(HtmlFile.read(), height=435)