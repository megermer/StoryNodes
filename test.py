from pyvis.network import Network

net = Network(height='465px', bgcolor='#222222', font_color='white')

net.add_node(1, label="Node 1") # node id = 1 and label = Node 1
net.add_node(2) # node id and label = 2
net.show("test.html")