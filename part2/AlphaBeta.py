from Tree import Tree, Node
import re

# def alpha_beta(root,alpha=-float('inf'),beta=float('inf')):
#   if root.isLeaf#     return root.data
#   bestValue = alpha
#   if root.isMax:
#     children = root.children
#     for child in children:
#       alpha = max(alpha,alpha_beta(child, alpha, beta))
#       if alpha > beta:
#         bestValue =
#     return alpha


class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    numLeavesExamined = 0
    score = 0

    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.get_root()  # GameNode
        return

    def alpha_beta_search(self, node=None):
        if not node:
            node = self.root
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print("AlphaBeta:  Utility Value of Root Node: = " + str(best_val))
        print("AlphaBeta:  Best State is: " + best_state.data)
        self.score = best_state.data
        print("{} leaf nodes examined".format(self.numLeavesExamined))
        return best_state

    def max_value(self, node, alpha, beta):
        print("AlphaBeta-->MAX: Visited Node :: " + node.data)
        if node.isLeaf:
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        print("AlphaBeta-->MIN: Visited Node :: " + str(node.data))
        if node.isLeaf:
            self.numLeavesExamined += 1
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    #                     #
    #   UTILITY METHODS   #
    #                     #

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    def getUtility(self, node):
        assert node is not None
        return node.data


def read_text(filepath):
    trees = []
    with open(filepath) as tree_file:
        for line in tree_file:
            line = line.split()
            nodes = format_line(line[0])
            possible_edges = format_line(line[1])
            edges = []
            nodes = [Node(data, True) if (val == 'MAX') else Node(
                data, False) for (data, val) in nodes]
            for parent, child in possible_edges:
                if child.isnumeric():  # The leaf nodes are the only ones that are numeric and aren't in the node list already
                    child = float(child)
                    nodes.append(Node(child, None, True))
                edges.append((parent, child))
            trees.append(create_tree(nodes, edges))
    return trees


def create_tree(nodes, edges):
    outTree = Tree()
    for node in nodes:
        outTree.add_node(node)
    for edge in edges:
        outTree.add_edge(edge)
    return outTree


def format_line(line):
    firstBracket, secondBracket = line.find("{"), line.find("}")
    reduced = line[firstBracket:secondBracket]
    regexPat = '\(\s?(.*?)\s?,\s?(.*?)\s?\)'
    toList = re.findall(regexPat, reduced)
    return toList


if __name__ == "__main__":
    trees = read_text('alphaBetaInput.txt')
    outfile = 'alphaceta_out.txt'

    with open(outfile, 'w') as f:  # clear text file
        pass
    for i, tree in enumerate(trees):
        test = AlphaBeta(tree)
        test.alpha_beta_search()
        # print(str(tree))
        with open(outfile, 'a') as f:
            f.write("Graph: {}, Score: {}, Leaf nodes examined: {}\n".format(
                i+1, test.score, test.numLeavesExamined))
