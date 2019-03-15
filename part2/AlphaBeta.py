from Tree import Tree, Node
import re
import time


class AlphaBeta:
    """
        Takes in a game tree and performs an alpha beta traversal to find the optimal value given an
        adversarial opponent. 
    """

    def __init__(self, game_tree, graphID=None):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.get_root()  # GameNode
        self.numLeavesExamined = 0
        self.score = 0
        print("Graph: {}".format(graphID))
        start = time.time()
        self.alpha_beta_search()
        print('Score: {:d}, Leaf Nodes Examined: {:d}, Total Time: {:f}s\n'.format(
            int(self.score), int(self.numLeavesExamined), time.time()-start))
        return

    def alpha_beta_search(self):
        node = self.root
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            if state.isMax:
                value = self.max_value(state, best_val, beta)
            else:
                value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        self.score = best_val
        return best_state

    def max_value(self, node, alpha, beta):
        if node.isLeaf:
            self.numLeavesExamined += 1
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:  # Cut off search below current node
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        if node.isLeaf:
            self.numLeavesExamined += 1
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:  # Cut off search below current node
                return value
            beta = min(beta, value)
        return value

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
    trees = read_text('alphabeta.txt')
    outfile = 'alphabeta_out.txt'

    with open(outfile, 'w') as f:  # clear text file
        pass
    for i, tree in enumerate(trees):
        alpha_beta = AlphaBeta(tree, i+1)
        with open(outfile, 'a') as f:
            f.write("Graph: {}, Score: {}, Leaf nodes examined: {}\n".format(
                i+1, alpha_beta.score, alpha_beta.numLeavesExamined))
