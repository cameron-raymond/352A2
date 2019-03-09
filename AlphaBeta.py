from Graph import Graph

def alpha_beta(current,alpha,beta):
    if current.isRootNode:
        alpha = -float("inf")
        beta = float("inf")
    

if __name__ == "__main__":

    graph = { "a" : {"d":1},
          "b" : {"c":3},
          "c" : {"b":3, "d":10, "e":3},
          "d" : {"a":1, "c":10},
          "e" : {"c":3},
          "f" : {}
        }
    

    print(buildGraph())
    # print("Vertices of graph:")
    # print(graph.vertices())

    # print('Adding an edge {"x","y"} with new vertices:')
    # graph.add_edge({"x","y"})
    # print(dijkstras(graph,"c","f"))