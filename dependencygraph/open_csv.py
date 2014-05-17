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
LINK_SPLIT_CHAR = "|"

def open_csv(csv_loc):
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
                node_text = line[1]
                link_to = line[2].split(LINK_SPLIT_CHAR) if line[2] != "" else None
                node_type = line[3]
                print(node_id, link_to)

            elif first_line == True:
                first_line = False

if __name__ == "__main__":
    open_csv("example_data.csv")
