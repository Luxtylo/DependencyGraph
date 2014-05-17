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

graph = pgv.AGraph(
        directed=True,
        label="Test Graph",
        shape="square")

nodes = ["a", "b", "c", "d"]
graph.add_nodes_from(nodes)

graph.add_edge("a", "b")
graph.add_edge("b", "c")
graph.add_edge("b", "d")
graph.add_edge("a", "d")

graph.graph_attr["label"] = "Test Graph"
graph.node_attr["shape"] = "square"

graph.layout(prog="dot")
graph.draw("test.png")
