#!/usr/bin/env python
"""
Dependency Graph - a tool to convert data into dependency graphs
Copyright (C) 2014 George Bryant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""

import pygraphviz as pgv
import open_csv

# Each entry stored as id, text, links, type, string
data = open_csv.parse_csv("example_data.csv")

nodes = []
edges = []

for entry in data:
    nodes.append(entry[-1])

def find_node(link):
    """Takes a node id and finds the node index"""
    for j in range(len(data)):
        entry = data[j]
        if entry[0] == link:
            break
    return j

for i in range(len(nodes)):
    links = data[i][2]

    if links is not None:
        for link in links:
            from_node = data[i][-1]
            to_node_index = find_node(link)
            to_node = data[to_node_index][-1]
            edges.append((from_node, to_node))

graph = pgv.AGraph(directed=True)

graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

graph.graph_attr["label"] = "Test Graph"
graph.node_attr["shape"] = "box"

graph.layout(prog="dot")
graph.draw("test.svg")
