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

import csv

# Replace this with whatever DOORS uses in its CSV files
LINK_SPLIT_CHAR = "\n"

def make_node_string(entry):
    node_string = ""
    node_string += entry[0]

    if entry[3] is not None:
        node_string += "\\n" + entry[3]
    
    if entry[1] is not None:
        node_string += "\\n\\n" + entry[1]

    return node_string

def parse_csv(csv_loc):
    with open(csv_loc, "r") as csv_file:
        csv_content = csv.reader(
                csv_file,
                delimiter=",",
                quotechar="\""
                )
        data = []

        first_line = True
        for line in csv_content:
            if first_line != True and line[0] != "":
                node_id = line[0]
                node_text = line[1].replace("\n", "\\n\\l")
                link_to = line[2].split(LINK_SPLIT_CHAR) if line[2] != "" else None
                node_type = line[3] if line[3] != "" else None
                data.append([node_id, node_text, link_to, node_type])

            elif first_line == True:
                first_line = False

        for n in range(len(data)):
            node_string = make_node_string(data[n])
            data[n].append(node_string)

        return data

if __name__ == "__main__":
    parse_csv("example_data.csv")
