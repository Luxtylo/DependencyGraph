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
import argparser
import time


def prepare_data(file_loc, exclude, cut, columns, show_desc):
    """Prepare data from csv for graphing.

    Add nodes to list, add edges to second list.
    Remove unlinked or hide types if necessary.
    Return lists of node strings and edges"""
    nodes = open_csv.parse_csv(file_loc, columns, show_desc)
    edges = []

    def find_node(target):
        """When given a node ID, find the matching node's index"""
        found = False
        i = 0
        for node in nodes:
            if node == target:
                found = True
                break
            else:
                i += 1

        if found:
            return i
        else:
            node_dict = {"id": target,
                         "links": [],
                         "type": "Unknown",
                         "description": ""}
            nodes.append(open_csv.Node(node_dict))

            return len(nodes) - 1

    def remove_unlinked(nodes):
        """Hide all nodes not linked to"""
        for node in nodes:
            if node.links != []:
                node.linked = True

                for link in node.links:
                    linked_node = find_node(link)
                    nodes[linked_node].linked = True

        for node in nodes:
            if not node.linked:
                node.visible = False

    if cut:
        remove_unlinked(nodes)

    if exclude != []:
        for node in nodes:
            if node.node_type in exclude:
                node.visible = False

    for node in nodes:
        if node.visible:
            for link in node.links:
                start_node_index = find_node(link)
                start_node = nodes[start_node_index]

                if start_node.visible:
                    edges.append((str(start_node), str(node)))

    node_strings = []
    nodes_drawn = 0
    for node in nodes:
        if node.visible:
            nodes_drawn += 1
            node_strings.append(str(node))

    return (node_strings, edges)


def draw_graph(output_loc, graph_name, export_formats, nodes, edges):
    """Output graph in given formats from node and edge lists"""
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
            export_file_name = output_loc + "." + ex_for
            graph.draw(export_file_name)
        except:
            print("Failed to export graph from " +
                  output_loc + " as " + ex_for)

    return len(graph.nodes())

args = argparser.parser.parse_args()

if args.ex_forms == []:
    args.ex_forms = ["png"]
if args.output_loc == "":
    args.output_loc = "".join(args.file_loc.split(".")[:-1])

args.cols = args.cols.lower()
if args.cols != "itly":
    if len(args.cols) != 4:
        raise SystemExit("Column order string should be 4 characters long")
    elif set(list(args.cols)) != set(["i", "t", "l", "y"]):
            raise SystemExit(
                """Column order string should be constructed of chars:
  i: Node ID
  t: Node text
  l: Node links
  y: Node type""")

start_time = time.time()

(nodes, edges) = prepare_data(args.file_loc, args.exclude, args.cut,
                              args.cols, args.desc)
nodes_drawn = draw_graph(args.output_loc, args.title, args.ex_forms,
                         nodes, edges)

end_time = time.time()
time_taken = round(end_time - start_time, 2)

print(str(nodes_drawn)+" nodes drawn in "+str(time_taken)+" seconds.")
