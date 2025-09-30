from ipyleaflet import Map, Marker, Polyline, Icon
from ipywidgets import VBox, HTML, Output
import heapq
# Linked List Node
class Node:
def __init__(self, name, coordinates):
self.name = name
self.coordinates = coordinates
self.neighbors = []
# Linked List Graph
class LinkedListGraph:
def __init__(self):
self.nodes = {}
def add_node(self, name, coordinates):
self.nodes[name] = Node(name, coordinates)
def add_edge(self, start, end):
self.nodes[start].neighbors.append(self.nodes[end])
def find_all_paths(self, start, end, path=[]):
path = path + [start]
if start == end:
return [path]
if start not in self.nodes:
return []
paths = []
for neighbor in self.nodes[start].neighbors:
if neighbor.name not in path:
new_paths = self.find_all_paths(neighbor.name, end, path)
for p in new_paths:
paths.append(p)
return paths
def calculate_distance(self, coord1, coord2): """Helper function to calculate Euclidean distance between two coordinates."""
return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5
def dijkstra(self, start, end): """Dijkstra's algorithm to find the shortest path.""" distances = {node: float('inf') for node in self.nodes}
distances[start] = 0
priority_queue = [(0, start)]

previous = {node: None for node in self.nodes}
while priority_queue:
current_distance, current_node = heapq.heappop(priority_queue)
if current_distance > distances[current_node]:
continue
for neighbor in self.nodes[current_node].neighbors:
distance = self.calculate_distance(
self.nodes[current_node].coordinates, neighbor.coordinates
)
new_distance = current_distance + distance
if new_distance < distances[neighbor.name]:
distances[neighbor.name] = new_distance
previous[neighbor.name] = current_node
heapq.heappush(priority_queue, (new_distance, neighbor.name))
# Reconstruct the shortest path
path = []
current = end
while current is not None:
path.insert(0, current)
current = previous[current]
return path, distances[end]
# Initialize LinkedListGraph
graph = LinkedListGraph()
# Add nodes and edges
intersection_data = {
'E-7': {'coordinates': (33.7296, 73.0514), 'neighbors': ['F-7', 'E-8']},
'E-8': {'coordinates': (33.7220, 73.0317), 'neighbors': ['F-7', 'F-8', 'E-9']},
'E-9': {'coordinates': (33.719153, 73.015382), 'neighbors': ['F-9', 'E-8']},
'E-11': {'coordinates': (33.697943, 72.973496), 'neighbors': ['F-11']},
'F-5': {'coordinates': (33.7368, 73.0892), 'neighbors': ['F-6', 'G-5']},
'F-6': {'coordinates': (33.729943, 73.076314), 'neighbors': ['F-7', 'G-6', 'F-5']},
'F-7': {'coordinates': (33.7220, 73.0570), 'neighbors': ['F-6', 'G-7', 'F-8', 'E-7']},
'F-8': {'coordinates': (33.711944, 73.037576), 'neighbors': ['E-8', 'F-9', 'G-8', 'F-7']},
'F-9': {'coordinates': (33.7017, 73.0228), 'neighbors': ['E-9', 'F-8', 'G-9', 'F-10']},
'F-10': {'coordinates': (33.6907, 73.0057), 'neighbors': ['G-10', 'F-9', 'F-11']},
'F-11': {'coordinates': (33.6824, 72.9909), 'neighbors': ['E-11', 'F-10', 'G-11']},
'G-5': {'coordinates': (33.7218, 73.0981), 'neighbors': ['G-6', 'F-5']},
'G-6': {'coordinates': (33.715168, 73.084973), 'neighbors': ['F-6', 'G-7', 'G-5']},
'G-7': {'coordinates': (33.7040, 73.0684), 'neighbors': ['F-7', 'G-6', 'G-8']},
'G-8': {'coordinates': (33.6973, 73.0515), 'neighbors': ['G-9', 'G-7', 'F-8', 'H-8']},
'G-9': {'coordinates': (33.6882, 73.0351), 'neighbors': ['G-8', 'F-9', 'G-10', 'H-9']},
'G-10': {'coordinates': (33.6769, 73.0149), 'neighbors': ['G-11', 'G-9', 'F-10', 'H-10']},
'G-11': {'coordinates': (33.6694, 72.9972), 'neighbors': ['F-11', 'G-10', 'H-11']},
'G-13': {'coordinates': (33.6517, 72.9667), 'neighbors': ['H-13']},
'H-8': {'coordinates': (33.6826, 73.0649), 'neighbors': ['G-8', 'I-8', 'H-9']},
'H-9': {'coordinates': (33.6680, 73.0448), 'neighbors': ['G-9', 'H-10', 'H-8', 'I-9']},
'H-10': {'coordinates': (33.6642, 73.0264), 'neighbors': ['H-9', 'H-11', 'I-10', 'G-10']},
'H-11': {'coordinates': (33.6548, 73.0111), 'neighbors': ['H-12', 'G-11', 'H-10', 'I-11']},

'H-12': {'coordinates': (33.646597, 72.987828), 'neighbors': ['H-11', 'H-13']},
'H-13': {'coordinates': (33.6361, 72.9789), 'neighbors': ['G-13']},
'I-8': {'coordinates': (33.670565, 73.071095), 'neighbors': ['H-8', 'I-9']},
'I-9': {'coordinates': (33.657535, 73.050507), 'neighbors': ['H-9', 'I-8', 'I-10']},
'I-10': {'coordinates': (33.643862, 73.038202), 'neighbors': ['H-10', 'I-9', 'I-11']},
'I-11': {'coordinates': (33.638321, 73.018431), 'neighbors': ['H-11', 'I-10']}
}
for name, data in intersection_data.items():
graph.add_node(name, data['coordinates'])
for name, data in intersection_data.items():
for neighbor in data['neighbors']:
graph.add_edge(name, neighbor)
# Initialize map
m = Map(center=(33.6844, 73.0479), zoom=12)
info_box = HTML()
output = Output()
# Markers
start_marker = Marker(location=(0, 0), visible=False, icon=Icon(color="green"))
end_marker = Marker(location=(0, 0), visible=False, icon=Icon(color="red"))
m.add_layer(start_marker)
m.add_layer(end_marker)
# Click handler for map
click_count = 0
start_node = None
end_node = None
polylines = []
def handle_map_click(**kwargs):
global click_count, start_node, end_node, polylines
if "type" in kwargs and kwargs["type"] == "click" and "coordinates" in kwargs:
lat, lon = kwargs["coordinates"]
# Set start marker
if click_count == 0:
start_marker.location = (lat, lon)
start_marker.visible = True
click_count += 1
start_node = min(graph.nodes, key=lambda node: (graph.nodes[node].coordinates[0] - lat) ** 2 +
(graph.nodes[node].coordinates[1] - lon) ** 2)
with output:
print(f"Start point set at: Latitude: {lat}, Longitude: {lon}, Node: {start_node}")
# Set end marker
elif click_count == 1:
end_marker.location = (lat, lon)
end_marker.visible = True
end_node = min(graph.nodes, key=lambda node: (graph.nodes[node].coordinates[0] - lat) ** 2 +
(graph.nodes[node].coordinates[1] - lon) ** 2)
with output:

print(f"End point set at: Latitude: {lat}, Longitude: {lon}, Node: {end_node}")
# Find all paths
if start_node and end_node:
all_paths = graph.find_all_paths(start_node, end_node)
shortest_path, shortest_distance = graph.dijkstra(start_node, end_node)
# Display the shortest path and its distance
info_box.value = f"<b>Total Paths Found:</b> {len(all_paths)}<br><b>Shortest Path:</b> {' ->
'.join(shortest_path)}<br><b>Distance:</b> {shortest_distance:.2f} km<br>" # Remove previous polylines
for polyline in polylines:
m.remove_layer(polyline)
polylines.clear()
# Visualize paths
path_colors = ['blue', 'darkgreen', 'purple', 'red', 'brown']
for i, path in enumerate(all_paths[:5]): # Show up to 5 paths
coords = [graph.nodes[node].coordinates for node in path]
color = path_colors[i % len(path_colors)]
line = Polyline(locations=coords, color=color, fill=False, weight=4)
polylines.append(line)
m.add_layer(line)
# Highlight the shortest path
shortest_coords = [graph.nodes[node].coordinates for node in shortest_path]
shortest_line = Polyline(locations=shortest_coords, color='gold', fill=False, weight=6)
polylines.append(shortest_line)
m.add_layer(shortest_line)
with output:
print(f"Shortest Path: {' -> '.join(shortest_path)}")
print(f"Distance: {shortest_distance:.2f} km")
click_count = 0 # Reset click counter for new selection
# Add handler to map
m.on_interaction(handle_map_click)
# Display map and info
info_box.value = "Click on the map