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
import argparser

def make_graph(file_loc, graph_name, export_formats, exclude, cut):
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

    if cut:
        print(str(len(nodes)) + " nodes")
        linked_nodes = []

        for j in range(len(data)):
            try:
                links = data[j][2]

                if links is not None:
                    for link in links:
                        link_index = find_node(link)
                        linked_nodes.append(data[link_index][-1])
                        linked_nodes.append(data[j][0])
            except TypeError:
                pass

        # remove duplicates
        linked_nodes = list(set(linked_nodes))

        nodes = list(linked_nodes)
        print(str(len(nodes)) + " nodes")

        new_data = list(data)
        for i in range(len(data)-1, -1, -1):
            if data[i][-1] not in linked_nodes:
                del new_data[i]

        data = new_data
        print(len(data))

    for i in range(len(nodes)):
        links = data[i][2]

        if links is not None:
            for link in links:
                from_node = data[i][-1]
                to_node_index = find_node(link)
                to_node = data[to_node_index][-1]
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

    #graph.layout(prog="dot")
    for ex_for in export_formats:
        try:
            export_file_name = "".join(file_loc.split(".")[:-1]) + "." + ex_for
            #graph.draw(export_file_name)
        except:
            print("Failed to export graph from " + file_loc + " as " + ex_for)

args = argparser.parser.parse_args()

if args.csv_help:
    print("""DependencyGraph converts csv files into png graphs using pygraphviz. The csv files must have a particular structure for each line:  
  Object ID, Object Text, Link to, Type  

    Object ID is the name which will be shown at the top of the node.
    Object Text is the text which will appear below the object ID
    Link to is the object ID of the objects that this node will be linked to
      Multiple links can be separated with a \\n
    Type is the type of entry this node is

  Link to and Type can be left blank

The csv should be saved with the columns separated by commas, and multiline strings surrounded by quotation marks.""")
    sys.exit(0)

else:
    if args.name is None:
        args.name = "".join(args.file_loc.split(".")[:-1])
    if args.ex_forms == []:
        args.ex_forms = ["png"]

    make_graph(args.file_loc, args.name, args.ex_forms, args.exclude, args.cut)
