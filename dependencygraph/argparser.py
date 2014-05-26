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

import argparse

parser = argparse.ArgumentParser(
        description="Convert csv files into dependency graphs",
        formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("file_loc", metavar="file", type=str,
        help="location of the csv file to be converted")

parser.add_argument("-c", "--column-order", type=str, action="store",
        default="itly", dest="cols",
        help="""Specify csv's column order.
  Default order: itly
    i: Node ID
    t: Node text
    l: Node links
    y: Node type""")

parser.add_argument("-t", "--title", type=str, action="store",
        default="",
        help="give the graph a custom title")

parser.add_argument("-o", "--output", type=str, action="store",
        metavar="NAME", default="", dest="output_loc",
        help="specify output filename. Do not include extension")

parser.add_argument("-f", "--format", action="append", default=[], dest="ex_forms",
        choices=["png", "jpg", "pdf", "eps", "svg"],
        help="choose output filetype(s)")

parser.add_argument("-e", "--exclude", action="append",
        default=[], metavar="TYPE",
        help="add node types to exclude")

parser.add_argument("-x", "--cut", action="store_true",
        help="remove unlinked nodes")

parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
        help="print verbose messages")

