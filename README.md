Required dependencies:
- Streamlit `pip install streamlit`
- PyVis `pip install pyvis`
- Neo4J `pip install neo4j`

To run the app:
- Once you've installed the required dependencies or accessed them with a virtual environment, open the application and open a new terminal.
- Type `streamlit run front.py` 
- The application should open in your default browser

Limitations:
- You CANNOT update an existing node after it is submitted. Re-entering the same node name and attempting to update the information will duplicate the existing relationships associated with the node.
- The functionality to delete a node does not exist.
- You MUST specify a relationship type if you are adding a relationship. Failure to do so may result in the app crashing.
- Due to the nature of Streamlit's input fields, you MUST either click 'Enter' after specifying a relation type or click out of the input field before hitting the 'Submit' button. Failure to do so will result in the app crashing. 
- There is a chance that every time the app and graph refresh, Microsoft's Edge browser may open. The only way this issue was resolved was to delete Edge, and my hypothesis is that is is a bug somewhere in the Streamlit library.

URI and AUTH credentials:
URI = "neo4j+s://0b4d88a8.databases.neo4j.io"
AUTH = ("neo4j", "qE4ZrS-xtJ2QzwN_4OSXfXl3Gi9uwvGJqp4UI95xReE")


