DependencyGraph
===============
A tool to convert data into dependency graphs
--------------------------------------------------
DependencyGraph converts ``csv`` files into ``png`` graphs using ``pygraphviz``. The ``csv`` files must have a particular structure for each line:  
``Object ID, Object Text, Link to, Type``  
The ``csv`` should be saved with the columns separated by commas, and multiline strings surrounded by quotation marks.

* Object ID is the name which will be shown at the top of the node.
* Object Text is the text which will appear below the object ID
* Link to is the object ID of the objects that this node will be linked to. Multiple links can be separated with a newline character
* Type is the type of entry this node is. In future different colours will be able to be assigned to different types of node.

The program is called with the syntax:  
``dependency_graph.py [csv file] [Graph name]``  
The graph name is optional - if none is given, the ``csv`` file will be used without the ``.csv`` extension.

The output will be a ``png`` with the same name as the original ``csv``
