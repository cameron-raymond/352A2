class Tree(object):

    def __init__(self,root=None):
        """ 
        initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        self.__tree_dict = {}
        self.__root = None
        if root:
            self.__root = root
            self.__tree_dict[root.data] = root

    def tree_dict(self):
        return self.__tree_dict
        
    def get_root(self):
        return self.__root

    def nodes(self):
        """ returns the nodes of a graph """
        return [c for c in self.__tree_dict]

    # def edges(self):
    #     """ returns the edges of a graph """
    #     return self.__generate_edges()

    def add_node(self, node):
        """ If the node "node" is not in 
            self.__graph_dict, a key "node" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if not self.__root:
            self.__root = node
        if node.data not in self.__tree_dict:
            self.__tree_dict[node.data] = node

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two nodes.
            Both nodes must already be in the tree!!
        """
        edge = set(edge)
        (parent, child) = tuple(edge)
        if parent in self.__tree_dict and child in self.__tree_dict:
            childNode =  self.__tree_dict[child]
            self.__tree_dict[parent].add_child(childNode)
        else:
           raise ValueError('Nodes must already be in the tree lookup table before you can add an edge between them.')
    def inorderTraversal(self,root):
        res = ""
        if root:
            for child in root.chilren:
                res += self.inorderTraversal(child) 
            res+=(root.data)
        return res




#     def __str__(self):
#         res = "nodes
# : "
#         for k in self.__tree_list:
#             res += str(k) + " "
#         res += "\nedges: "
#         for edge in self.__generate_edges():
#             res += str(edge) + " "
#         return res


class Node(object):
    def __init__(self, data,isMax=False, isLeaf = False):
        self.data = data
        self.isMax = isMax
        self.isLeaf = isLeaf
        self.children = set()

    def add_child(self, obj):
        self.children.add(obj)
    
    def __str__(self):
        string = "Data (ID): "+str(self.data)
        if self.isLeaf:
            return string+",\tLeaf: "+str(self.isLeaf)
        return string+",\tMinOrMax: "+str(self.isMax)+", NumChildren: "+str(len(self.children))
