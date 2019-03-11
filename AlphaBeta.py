from Tree import Tree,Node
import re

def readText(filepath):
    Trees = []
    with open(filepath) as TreeFile:
        for line in TreeFile:
            line = line.split()
            nodes = formatLine(line[0])
            possibleEdges = formatLine(line[1])
            edges = []
            nodes = [Node(data,True) if (val == 'MAX') else Node(data, False) for (data, val) in nodes]
            for parent,child in possibleEdges:
              if child.isnumeric(): #The leaf nodes are the only ones that are numeric and aren't in the node list already
                child = float(child)
                nodes.append(Node(child,None,True))
              edges.append((parent,child))
            createTree(nodes,edges)

def createTree(nodes,edges):
  outTree = Tree()
  for node in nodes:
    outTree.add_node(node)
  for edge in edges:
    outTree.add_edge(edge)
    print(edge)
  root = outTree.get_root()
  for child in root.children:
    print(child)
  
def formatLine(line):
  firstBracket, secondBracket = line.find("{"),line.find("}")
  reduced = line[firstBracket:secondBracket]
  regexPat = '\(\s?(.*?)\s?,\s?(.*?)\s?\)'
  toList = re.findall(regexPat, reduced)
  return toList

if __name__ == "__main__":
  readText('alphaBetaInput.txt')