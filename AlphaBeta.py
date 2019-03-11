from Graph import Graph
import re

def readText(filepath):
    graphs = []
    with open(filepath) as graphFile:
        for line in graphFile:
            line = line.split()
            nodes = formatLine(line[0])
            edges = formatLine(line[1])
            nodes = [(node,True) if (val == 'MAX') else (node, False) for (node, val) in nodes]
            edges = [(node,float(val)) if (val.isnumeric()) else (node, val) for (node, val) in edges]
            createGraph(nodes,edges)

def createGraph(nodes,edges):
  print(nodes,edges)
  
def formatLine(line):
  firstBracket, secondBracket = line.find("{"),line.find("}")
  reduced = line[firstBracket:secondBracket]
  regexPat = '\(\s?(.*?)\s?,\s?(.*?)\s?\)'
  toList = re.findall(regexPat, reduced)
  return toList

if __name__ == "__main__":
  readText('alphaBetaInput.txt')