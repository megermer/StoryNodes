import streamlit as st
import numpy as np
import pandas as pd
import graphviz as gv
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import logging
class App:

    # Initializes app
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    # Closes app
    def close(self):
        self.driver.close()

    # Helper method for finding NODE
    @staticmethod #NODE
    def _find_and_return_node(tx, node_name):
        query = (
            "MATCH (n) "
            "WHERE n.name = $node_name "
            "RETURN n.name AS name"
        )
        result = tx.run(query, node_name=node_name)
        return [row["name"] for row in result]
    
    # Helper method to create a PERSON
    @staticmethod
    def _create_character(tx, character_name):
        query = (
            "MERGE (p:Character { name: $character_name }) "
            "RETURN p "
        )
        result = tx.run(query, character_name=character_name)
        # return [row["name"] for row in result]
        return [row["p"]["name"] for row in result]
    
    # Helper method to create a PLACE
    @staticmethod 
    def _create_place(tx, place_name):
        query = (
            "MERGE (p:Place { name: $place_name }) "
            "RETURN p "
        )
        result = tx.run(query, place_name=place_name)
        return [row["p"]["name"] for row in result]
    
    # Helper method to create a THING
    @staticmethod
    def _create_thing(tx, thing_name):
        query = (
            "MERGE (p:Thing { name: $thing_name }) "
            "RETURN p "
        )
        result = tx.run(query, thing_name=thing_name)
        return [row["p"]["name"] for row in result]
    
    # Helper method for deleting nodes of types Character, Place, Thing
    @staticmethod
    def _delete_node(tx, node_name):
        query = (
            "MATCH (n) "
            "WHERE n.name = $node_name "
            "DETACH DELETE n "
        )
        result = tx.run(query, node_name=node_name)
        return node_name

    @staticmethod
    def _create_and_return_relationship(tx, name1, name2, relationship_type):
        query = (
            "MERGE (p1 { name: $name1 }) "
            "MERGE (p2 { name: $name2 }) "
            f"MERGE (p1)-[:{relationship_type}]-(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, name1=name1, name2=name2)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
        
    @staticmethod
    def _delete_relationship(tx, name1, name2, relationship_type):
        r_query = f"[r: {relationship_type}]"
        query = (
            "MATCH (p1 { name: $name1 })-" + r_query + "-(p2 { name: $name2 }) "
            "DELETE r "
            "RETURN p1, p2 "
        )
        result = tx.run(query, name1=name1, name2=name2, relationship_type=relationship_type)
    
    # General method for finding an element
    def find_node(self, node_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(
                self._find_and_return_node, node_name
            )
            for row in result:
                print("Found node : {row}".format(row=row))

    # General method for creating a node of type Character, Place, or Thing
    def create_node(self, node_type, node_name):
        with self.driver.session(database="neo4j") as session:
            if node_type == "Character":
                result = session.execute_write(self._create_character, node_name)
            if node_type == "Place":
                result = session.execute_write(self._create_place, node_name)
            if node_type == "Thing":
                result = session.execute_write(self._create_thing, node_name)
            for row in result: 
                print("Created {node_type} : {row}".format(row=row, node_type=node_type))

    # General method for deleting a node of type Character, Place, or Thing
    def delete_node(self, node_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._delete_node, node_name
            )
            print(f"Deleted node {node_name}")

    # Create a new relationship between existing nodes
    def create_relationship(self, name1, name2, relationship_type):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_and_return_relationship, name1, name2, relationship_type
            )
            for row in result:
                print("Created relationship {relationship_type} between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2'], relationship_type=relationship_type))

    # Delete a relationship
    def delete_relationship(self, name1, name2, relationship_type):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._delete_relationship, name1, name2, relationship_type
            )
            print(f"Deleted relationship {relationship_type} between: {name1}, {name2}")


    
if __name__ == "__main__":
    uri = "neo4j+s://0b4d88a8.databases.neo4j.io"
    user = "neo4j"
    password = "qE4ZrS-xtJ2QzwN_4OSXfXl3Gi9uwvGJqp4UI95xReE"
    app = App(uri, user, password)

    # app.find_node("Lucy")

    # node = input("Enter a node type to create: ")
    # name = input("Enter the name of the node: ")
    # app.create_node(node, name)

    node = input("Enter a node to delete: ")
    app.delete_node(node)

    # p1 = input("Enter the first person: ")
    # p2 = input("Enter the second person: ")
    # r = input("Enter the relationship type: ")
    # app.create_relationship(p1, p2, r)

    # p1 = input("Enter the first person: ")
    # p2 = input("Enter the second person: ")
    # r = input("Enter the relationship type: ")
    # app.delete_relationship(p1, p2, r)
    
    app.close()


# NEO4j Desktop application key eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Ii4rQC4rIiwibWl4cGFuZWxJZCI6ImF1dGgwfDYzZGQ4YTkxNWQ0ZmI4NTZkMmYxNWQ5NyIsIm1peHBhbmVsUHJvamVjdElkIjoiNGJmYjI0MTRhYjk3M2M3NDFiNmYwNjdiZjA2ZDU1NzUiLCJvcmciOiIuKiIsInB1YiI6Im5lbzRqLmNvbSIsInJlZyI6IiAiLCJzdWIiOiJuZW80ai1kZXNrdG9wIiwiZXhwIjoxNzA4NzMxNDE4LCJ2ZXIiOiIqIiwiaXNzIjoibmVvNGouY29tIiwibmJmIjoxNjc3MTk1NDE4LCJpYXQiOjE2NzcxOTU0MTgsImp0aSI6IjM3MGlLa1BXYyJ9.gs_iwai_YPNCoCMVsle-qnBFkNswAa6KlMrrCONnYYItOktMWsZBzQp7FYQA6tnbdvyt78Nfi8iI9Uk8g6INXZvxgpBy3O4pfeUIx4ee4xv5vmDssuTdgGHbmQoWBUvlfVi4CTHhE23Jm70pG5QMOG82H5Yty6AbgcO01HgCQ6AZg8JrBXCUETxOHbumi0NfYlNz2KdFMEEK0v6TMuQxQnu04KF0tsFrhgTuKVPp4S07wYX8YrASROcm_rrTDSwgruddBZPOCLkryQyeDl05xn3yEdfRmJwN8k33u2Fbo3FlH7Y6wcZ0et4OlPXY307lXYP1f8tZ8k5zSgL_aLOc8A