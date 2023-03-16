Striking similarities exist between the fields of literature
and data science. Both require strong competencies in reading
comprehension and writing fluency, as well as the ability to
summarize and draw conclusions from an abundance of infor-
mation. Within data science, the data visualization discipline
enables data analysts to quickly see trends and summarize
findings through bar graphs, scatter plots, histograms, and
many other graphical representations. However, no such sector
exists within the field of literature, leaving literary scholars
with almost no way to draw their own conclusions except
with their own interpretation of information directly from the
text. While some tools exist to help visualize certain aspects
of narratives, they are either very advanced tools that must be
adapted to fit the narrative storyline [1], or they rely almost
exclusively on the timeline approach with no way to represent
relationships between different characters and events [2].

Thus, our contribution is a web application that allows the
user to add different characters, relationships, and events from
a narrative into a graph database. The user can then interact
with the user-interface to run queries on this data, returning
the corresponding nodes and edges in an easy-to-read manner.
This enables the user to visualize the general trajectory of
a narrative as whole rather than having to draw conclusions
straight from the raw text.

Dependencies needed: 
- Streamlit
- PyVis