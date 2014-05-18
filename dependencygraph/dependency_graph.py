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
import sys

help_string = """DependencyGraph converts csv files into png graphs using pygraphviz.

The csv files must have a particular structure for each line:  
  Object ID, Object Text, Link to, Type 

    Object ID is the name which will be shown at the top of the node.
    Object Text is the text which will appear below the object ID
    Link to is the object ID of the objects that this node will be linked to. Multiple links can be separated with a newline character
    Type is the type of entry this node is

Usage:
  ./dependency_graph.py [csv file] [graph title] [export format]

Options for export format are all those allowed by graphviz.
  Some common ones are:
    png, jpg, svg, pdf, eps
    svg currently acts oddly with fonts - the text extends outside the node boxes"""

def make_graph(file_loc, graph_name, export_format):
# Each entry stored as id, text, links, type, string
    data = open_csv.parse_csv(file_loc)

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
                #edges.append((from_node, to_node))
                edges.append((to_node, from_node))

    graph = pgv.AGraph(directed=True)

    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    graph.graph_attr["label"] = graph_name

    graph.graph_attr["labeljust"] = "l"
    graph.graph_attr["labelloc"] = "t"
    graph.graph_attr["labelfontsize"] = "16"

    graph.node_attr["fontsize"] = "12"
    graph.node_attr["labeljust"] = "l"
    graph.node_attr["shape"] = "box"

    graph.edge_attr["dir"] = "back"
    graph.edge_attr["concentrate"] = "true"

    graph.layout(prog="dot")
    png_name = "".join(file_loc.split(".")[:-1]) + "." + export_format
    graph.draw(png_name)

if len(sys.argv) > 1:
    filename = sys.argv[1]

    if len(sys.argv) == 2:
        if sys.argv[-1] == "--help" or sys.argv[-1] == "-h":
            print(help_string)
            sys.exit()
        graph_name = "".join(filename.split(".")[:-1])
        export_format = "png"
    elif len(sys.argv) == 3:
        graph_name = sys.argv[-1]
        export_format = "png"
    elif len(sys.argv) == 4:
        graph_name = sys.argv[2]
        export_format = sys.argv[3]
    else:
        sys.exit(0)

    try:
        make_graph(filename, graph_name, export_format)
    except IOError:
        print("Conversion failed - file " + filename + " does not exist")

else:
    print("Give a csv filename as an argument to convert it to a graph")
