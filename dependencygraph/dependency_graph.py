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
import argparse

parser = argparse.ArgumentParser(description="Convert csv files into graphs")

parser.add_argument("file_loc", metavar="file", type=str,
        help="location of the csv file to be converted")

parser.add_argument("-c", "--csv-help", action="store_true",
        help="show help about csv formatting")
parser.add_argument("-n", "--name", type=str, action="store",
        help="give the graph a custom title")
parser.add_argument("-f", "--format", action="append", default=[], dest="ex_forms",
        choices=["png", "jpg", "pdf", "eps", "svg"],
        help="choose output filetype(s)")
parser.add_argument("-e", "--exclude", action="append", metavar="TYPE",
        help="add node types to exclude")
parser.add_argument("-x", "--cut", action="store_true",
        help="remove unlinked nodes")

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
    for ex_for in export_formats:
        try:
            export_file_name = "".join(file_loc.split(".")[:-1]) + "." + ex_for
            graph.draw(export_file_name)
        except:
            print("Failed to export graph from " + file_loc + " as " + ex_for)

args = parser.parse_args()

#def make_graph(file_loc, graph_name, export_formats, exclude, cut):
#Namespace(csv_help=False, cut=False, exclude=None, file_loc='test.csv', format=[], name=None)

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
