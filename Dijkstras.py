from Graph import Graph


def dijkstras(graphDict,start,end):
    cost = {}
    parent= {}
    for key in graphDict:
        cost[key] = None
        parent[key] = None
    cost[start] = 0
    reached = set()
    candidates = set()
    candidates.add((start,cost[start]))
    while candidates:
        bestChoice = min(candidates, key = lambda t: t[1])
        reached.add(bestChoice)
        candidates.remove(bestChoice)
        reachedVertex = bestChoice[0]
        reachedCost = bestChoice[1]
        for neighbour in graphDict[reachedVertex]:
            neighbourCost = graphDict[reachedVertex][neighbour]
            pathCost=reachedCost+neighbourCost
            if not cost[neighbour]:
                candidates.add((neighbour,pathCost))
                cost[neighbour] = pathCost
                parent[neighbour] = reachedVertex
            elif pathCost < cost[neighbour]:
                cost[neighbour] = pathCost
                parent[neighbour] = reachedVertex
    return (cost,parent)


def buildGraph():
    graph = {}
    with open('flights.txt') as flights:
        for flight in flights:
            flight = flight.split('\t')
            
            comingFrom  = flight[0]
            goingTo     = flight[1] 
             
 
            flightInfo  = (int(flight[2]),int(flight[3]))
            if comingFrom in graph:
                graph[comingFrom][goingTo] = flightInfo
            else:
                graph[comingFrom] = {goingTo: flightInfo}
    return graph







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