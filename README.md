DependencyGraph
===============
A tool to convert data into dependency graphs
--------------------------------------------------
DependencyGraph converts ``csv`` files into ``png`` graphs using ``pygraphviz``. The ``csv`` files must have a particular structure for each line:  
``Object ID, Object Text, Link to, Type``  

* Object ID is the name which will be shown at the top of the node.
* Object Text is the text which will appear below the object ID
* Link to is the object ID of the objects that this node will be linked to. Multiple links can be separated with a newline character
* Type is the type of entry this node is. In future different colours will be able to be assigned to different types of node.

The only compulsory column is the "Object ID" column. The ``csv`` should be saved with the columns separated by commas, and multiline strings surrounded by quotation marks.

The program's help message (Obtained with ``./dependency_graph.py -h``):
```
usage: dependency_graph.py [-h] [-c] [-n NAME] [-f {png,jpg,pdf,eps,svg}]
                           [-e TYPE] [-x]
                           file

Convert csv files into graphs

positional arguments:
  file                  location of the csv file to be converted

optional arguments:
  -h, --help            show this help message and exit
  -c, --csv-help        show help about csv formatting
  -n NAME, --name NAME  give the graph a custom title
  -f {png,jpg,pdf,eps,svg}, --format {png,jpg,pdf,eps,svg}
                        choose output filetype(s)
  -e TYPE, --exclude TYPE
                        add node types to exclude
  -x, --cut             remove unlinked nodes
```

If, in the ``csv`` given to the program, there are nodes which depend on nodes outside the dataset, the program will generate these nodes with the type "Unknown". These can be ignored by simply using the flag "-e Unknown".

Dependencies
============
* Python 2.7
* [PyGraphviz](pygraphviz.github.io/index.html)
