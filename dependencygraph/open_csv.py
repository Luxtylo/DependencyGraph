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


class Node:
    def __init__(self, node_dict, show_desc):
        self.node_id = node_dict["id"]
        self.links = node_dict["links"]
        self.node_type = node_dict["type"]
        self.desc = node_dict["description"]
        self.show_desc = show_desc

        self.visible = True
        self.linked = False

        self.text = self.make_text()

    def make_text(self):
        """Create node's self-description string"""
        node_string = ""
        node_string += self.node_id

        if (self.node_type is not None and
                self.desc is not "" and
                self.show_desc):
            node_string += "\\n" + self.node_type
            node_string += "\\r\\n" + self.desc
        elif self.node_type is not None:
            node_string += "\\n" + self.node_type
        elif self.desc is not "" and self.show_desc:
            node_string += "\\n\\n" + self.desc

        return node_string

    def __eq__(self, other):
        return self.node_id == other

    def __str__(self):
        return self.text

    def __repr__(self):
        return repr(self.text)

    def __len__(self):
        return len(self.text)


def parse_csv(csv_loc, columns, show_desc):
    """Parse CSV file and return data gathered"""
    columns = list(columns)

    try:
        with open(csv_loc, "r") as csv_file:
            csv_content = csv.reader(
                csv_file,
                delimiter=",",
                quotechar="\"")
            data = []

            first_line = True
            for line in csv_content:
                if not first_line and line[0] != "":
                    node_dict = {}

                    for n in range(4):
                        if columns[n] == "i":
                            node_dict["id"] = line[n]

                        elif columns[n] == "t":
                            node_text = line[n].replace("\n", "\\l")
                            node_text = node_text.replace("\r", "\\l") + "\l"
                            node_dict["description"] = node_text

                        elif columns[n] == "l":
                            try:
                                if line[n] != "":
                                    node_dict["links"] = line[n].split(
                                        LINK_SPLIT_CHAR)
                                else:
                                    node_dict["links"] = []
                            except IndexError:
                                node_dict["links"] = []

                        elif columns[n] == "y":
                            try:
                                if line[n] != "":
                                    node_dict["type"] = line[n]
                                else:
                                    node_dict["type"] = ""
                            except IndexError:
                                node_dict["type"] = ""

                    node = Node(node_dict, show_desc)
                    data.append(node)

                elif first_line:
                    first_line = False

            return data

    except IOError:
        raise SystemExit("The file " + csv_loc + " does not exist")

if __name__ == "__main__":
    data = parse_csv("test.csv")
