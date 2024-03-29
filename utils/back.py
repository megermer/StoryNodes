import streamlit as st
import numpy as np
import pandas as pd
import graphviz as gv
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging

URI = "neo4j+s://0b4d88a8.databases.neo4j.io"
AUTH = ("neo4j", "qE4ZrS-xtJ2QzwN_4OSXfXl3Gi9uwvGJqp4UI95xReE")
driver = GraphDatabase.driver(URI, auth=AUTH)
session = driver.session()

# Helper method for finding NODE
def _find_and_return_node(tx, node_name):
    query = (
        "MATCH (n) "
        "WHERE n.name = $node_name "
        "RETURN n.name AS name"
    )
    result = tx.run(query, node_name=node_name)
    return [row["name"] for row in result]

# Helper method for retrieving all node names
def _find_and_retrieve_all_node_names(tx):
    query = (
        "MATCH (n) "
        "RETURN n.name AS name"
    )
    result = tx.run(query)
    return [row["name"] for row in result]

# Helper method for retrieving all node names of specific label with their descriptions (dict format)
def _find_and_retrieve_all_nodes_of_label(tx, label):
    nodes = {}
    query = (
        f"MATCH (n: {label}) "
        "RETURN n "
    ) 
    result = tx.run(query)
    # return [row["name"] for row in result]
    for row in result:
        name = row["n"]["name"]
        description = row["n"]["description"]
        nodes[name] = description 
    return nodes


# Helper method for retrieving all node descriptions (for future on-hover feature)
def _find_and_retrieve_all_node_descriptions(tx, node_name):
    query = (
        "MATCH (n) "
        "WHERE n.name = $node_name "
        "RETURN n.name AS name "
    )
    result = tx.run(query)
    return [row["name"] for row in result]

def _find_and_retrieve_all_relationships(tx, nodes : list):
    relationships = []
    for node_name in nodes:
        query = (
            "MATCH (n { name: $node_name})-[r]->(m) "
            "RETURN type(r) AS relationship, m.name AS endpoint "
        )
        result = tx.run(query, node_name=node_name)
        for row in result:
            if len(row["relationship"]) > 0:
                relationships.append([node_name, row["relationship"], row["endpoint"]])
    return relationships

# Helper method to create a CHARACTER
def _create_character(tx, character_name, description):
    query = (
        "MERGE (p:Character { name: $character_name, description: $description }) "
        "RETURN p "
    )
    result = tx.run(query, character_name=character_name, description=description)
    return [row["p"]["name"] for row in result]

# Helper method to create a PLACE
def _create_place(tx, place_name, description):
    query = (
        "MERGE (p:Place { name: $place_name, description: $description }) "
        "RETURN p "
    )
    result = tx.run(query, place_name=place_name, description=description)
    return [row["p"]["name"] for row in result]

# Helper method to create a THING
def _create_thing(tx, thing_name, description):
    query = (
        "MERGE (p:Thing { name: $thing_name, description: $description }) "
        "RETURN p "
    )
    result = tx.run(query, thing_name=thing_name, description=description)
    return [row["p"]["name"] for row in result]

# Helper method for deleting nodes of types Character, Place, Thing
def _delete_node(tx, node_name):
    query = (
        "MATCH (n) "
        "WHERE n.name = $node_name "
        "DETACH DELETE n "
    )
    result = tx.run(query, node_name=node_name)
    return node_name

# Helper method for creating a relationship
def _create_and_return_relationship(tx, name1, name2, relationship_type):
    query = (
        "MERGE (p1 { name: $name1 }) "
        "MERGE (p2 { name: $name2 }) "
        f"MERGE (p1)-[:{relationship_type}]-(p2) "
        "RETURN p1, p2 "
    )
    result = tx.run(query, name1=name1, name2=name2)
    try:
        return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]} for row in result]
    except ServiceUnavailable as exception:
        logging.error("{query} raised an error: \n {exception}".format(
            query=query, exception=exception))
        raise
    
# Helper method for deleting a relationship
def _delete_relationship(tx, name1, name2, relationship_type):
    r_query = f"[r: {relationship_type}]"
    query = (
        "MATCH (p1 { name: $name1 })-" + r_query + "-(p2 { name: $name2 }) "
        "DELETE r "
        "RETURN p1, p2 "
    )
    result = tx.run(query, name1=name1, name2=name2, relationship_type=relationship_type)

# General method for finding an element
def find_node(node_name):
    with session:
        result = session.execute_read(
            _find_and_return_node, node_name
        )
        for row in result:
            print("Found node : {row}".format(row=row))

# General method for retrieving all nodes
def retrieve_all_node_names():
    node_names = []
    # Have to create new session because the original one closes after state refreshes
    with GraphDatabase.driver(URI, auth=AUTH).session() as session2:
        result = session2.execute_read(
            _find_and_retrieve_all_node_names
        )
        for row in result:
            node_names.append(row)
            print(" Found node : {row}".format(row=row))
        session2.close()
        return node_names

def retrieve_all_nodes_of_label(label):
    # node_names = []
    node_names = {}
    with GraphDatabase.driver(URI, auth=AUTH).session() as session2:
        result = session2.execute_read(
            _find_and_retrieve_all_nodes_of_label, label
        )
        # for row in result:
        #     node_names.append(row)
            # print("Found node : {row}".format(row=row))
        for key, value in result.items():
            node_names[key] = value
        session2.close()
        return node_names

# General method for retrieving all nodes (will need 3 helper methods for getting names, types, and descriptions)
# MIGHT NOT NEED THIS
def retrieve_all_nodes():
    pass

def retrieve_all_relationships():
    nodes = retrieve_all_node_names()
    relationships = []
    with GraphDatabase.driver(URI, auth=AUTH).session() as session2:
        result = session2.execute_read(
            _find_and_retrieve_all_relationships, nodes
        )
        for row in result:
            relationships.append(row)
            print(f"Found relationship : {row}")
        session2.close()
        return relationships

# General method for creating a node of type Character, Place, or Thing
def create_node(node_type, node_name, description, relationships : dict):
    with GraphDatabase.driver(URI, auth=AUTH).session() as session2:
        if node_type == "Character":
            result = session.execute_write(_create_character, node_name, description)
        elif node_type == "Place":
            result = session.execute_write(_create_place, node_name, description)
        elif node_type == "Thing":
            result = session.execute_write(_create_thing, node_name, description)
        for row in result: 
            print("Created {node_type} : {row}".format(row=row, node_type=node_type))
        if len(relationships) > 0:
            for relation, relation_type in relationships.items():
                create_relationship(node_name, relation, relation_type)
        session2.close()

# General method for deleting a node of type Character, Place, or Thing
def delete_node(node_name):
    # with GraphDatabase.driver(URI, auth=AUTH).session() as session: 
    with session: 
        result = session.execute_write(_delete_node, node_name)
    print(f"Deleted node {node_name}")

# Create a new relationship between existing nodes
def create_relationship(name1, name2, relationship_type):
    with GraphDatabase.driver(URI, auth=AUTH).session() as session2:
        result = session.execute_write(
            _create_and_return_relationship, name1, name2, relationship_type
        )
        for row in result:
            print("Created relationship {relationship_type} between: {p1}, {p2}"
                  .format(p1=row['p1'], p2=row['p2'], relationship_type=relationship_type))
        session2.close()

# Delete a relationship
def delete_relationship(name1, name2, relationship_type):
    with session:
        result = session.execute_write(
            _delete_relationship, name1, name2, relationship_type
        )
        print(f"Deleted relationship {relationship_type} between: {name1}, {name2}")


    
if __name__ == "__main__":
    # uri = "neo4j+s://0b4d88a8.databases.neo4j.io"
    # user = "neo4j"
    # password = "qE4ZrS-xtJ2QzwN_4OSXfXl3Gi9uwvGJqp4UI95xReE"
    # app = App(uri, user, password)

    # find_node("Lucy")

    create_node("Character", "John Doe", "lorem ipsum", {})

    # node = input("Enter a node type to create: ")
    # name = input("Enter the name of the node: ")
    # create_node(node, name)
    
    # node = input("Enter a node to delete: ")
    # try:
    #     delete_node(node)
    # finally:
    #     session.close()

    # p1 = input("Enter the first person: ")
    # p2 = input("Enter the second person: ")
    # r = input("Enter the relationship type: ")
    # create_relationship(p1, p2, r)

    # p1 = input("Enter the first person: ")
    # p2 = input("Enter the second person: ")
    # r = input("Enter the relationship type: ")
    # delete_relationship(p1, p2, r)

    # nodes = retrieve_all_nodes()
    # for node in nodes:
    #     print(node['name'])
    
    # retrieve_all_nodes_of_label("Character")

    # retrieve_all_node_names()
    # retrieve_all_relationships()

    driver.close()


# NEO4j Desktop application key eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ii4rQC4rIiwibWl4cGFuZWxJZCI6ImF1dGgwfDYzZGQ4YTkxNWQ0ZmI4NTZkMmYxNWQ5NyIsIm1peHBhbmVsUHJvamVjdElkIjoiNGJmYjI0MTRhYjk3M2M3NDFiNmYwNjdiZjA2ZDU1NzUiLCJvcmciOiIuKiIsInB1YiI6Im5lbzRqLmNvbSIsInJlZyI6IiAiLCJzdWIiOiJuZW80ai1kZXNrdG9wIiwiZXhwIjoxNzA4NzMxNDE4LCJ2ZXIiOiIqIiwiaXNzIjoibmVvNGouY29tIiwibmJmIjoxNjc3MTk1NDE4LCJpYXQiOjE2NzcxOTU0MTgsImp0aSI6IjM3MGlLa1BXYyJ9.gs_iwai_YPNCoCMVsle-qnBFkNswAa6KlMrrCONnYYItOktMWsZBzQp7FYQA6tnbdvyt78Nfi8iI9Uk8g6INXZvxgpBy3O4pfeUIx4ee4xv5vmDssuTdgGHbmQoWBUvlfVi4CTHhE23Jm70pG5QMOG82H5Yty6AbgcO01HgCQ6AZg8JrBXCUETxOHbumi0NfYlNz2KdFMEEK0v6TMuQxQnu04KF0tsFrhgTuKVPp4S07wYX8YrASROcm_rrTDSwgruddBZPOCLkryQyeDl05xn3yEdfRmJwN8k33u2Fbo3FlH7Y6wcZ0et4OlPXY307lXYP1f8tZ8k5zSgL_aLOc8A