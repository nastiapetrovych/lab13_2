# lab13_2
Discover the time of searhing words in list, binary tree(ordered, unordered and balanced)


My main task was to discover the difference in time using 2 data structures as list and binary tree. The results were obvious even before the program, that binary tree is much faster that simple list. For operations in list I used function list.index and for tree - method find().

Example of function call:
                                                       
                                                       tree = LinkedBST()
                                                       print(tree.demo_bst('empty.txt'))
 
 
**Results:** => they are rounded to two decimals places  after dot
 
Result of search in a list : 1.73 

Result of search in a sorted binary tree : 0.02 

Result of search in an unordered binary tree : 0.02 

Result of search in a balanced binary tree  : 0.01

As we see, the search in balanced binary tree is the fastest
