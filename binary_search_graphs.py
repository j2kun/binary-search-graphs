from collections import defaultdict
from collections import namedtuple

import dijkstra


Edge = namedtuple('Edge', ('source', 'target', 'weight'))


class Graph:
    # A bare-bones implementation of a weighted, undirected graph
    def __init__(self, vertices, edges=tuple()):
        self.vertices = vertices
        self.incident_edges = defaultdict(list)

        for edge in edges:
            self.add_edge(
                edge[0],
                edge[1],
                1 if len(edge) == 2 else edge[2]  # optional weight
            )

    def add_edge(self, u, v, weight=1):
        self.incident_edges[u].append(Edge(u, v, weight))
        self.incident_edges[v].append(Edge(v, u, weight))

    def edge(self, u, v):
        return [e for e in self.incident_edges[u] if e.target == v][0]


def possible_targets(graph, start, edge):
    '''
    Given an undirected graph G = (V,E), an input vertex v in V, and an edge e
    incident to v, compute the set of nodes w such that e is on a shortest path from
    v to w.
    '''
    dijkstra_output = dijkstra.single_source_shortest_paths(graph, start)
    return set(v for v in graph.vertices
               if dijkstra_output.path_to_destination_contains_edge(v, edge))
        

def find_median(graph, vertices):
    '''
    Compute as output a vertex in the input graph which minimizes the sum of distances
    to the input set of vertices
    '''
    dijkstra_outputs = [dijkstra.single_source_shortest_paths(graph, v)
                        for v in graph.vertices]
    # for x in dijkstra_outputs:
    #     print(x.start, x.distance_from_start)
        
    return min(dijkstra_outputs, key=lambda x: x.sum_of_distances(vertices)).start


QueryResult = namedtuple('QueryResult', ('found_target', 'feedback_edge'))


def binary_search(graph, query):
    '''
    Find a target node in a graph, with queries of the form "Is x the target?"
    and responses either "You found the target!" or "Here is an edge on a shortest
    path to the target."
    '''
    candidate_nodes = set(x for x in graph.vertices)  # copy

    while len(candidate_nodes) > 1:
        median = find_median(graph, candidate_nodes)
        query_result = query(median)

        if query_result.found_target:
            return median
        else:
            edge = query_result.feedback_edge
            legal_targets = possible_targets(graph, median, edge)
            candidate_nodes = candidate_nodes.intersection(legal_targets)

    return candidate_nodes.pop()


if __name__ == "__main__":
    '''
    Graph looks like this tree, with uniform weights
    
        a       k
         b     j
          cfghi
         d     l
        e       m 
    '''
    G = Graph(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
               'j', 'k', 'l', 'm'],
              [
                   ('a', 'b'),
                   ('b', 'c'),
                   ('c', 'd'),
                   ('d', 'e'),
                   ('c', 'f'),
                   ('f', 'g'),
                   ('g', 'h'),
                   ('h', 'i'),
                   ('i', 'j'),
                   ('j', 'k'),
                   ('i', 'l'),
                   ('l', 'm'),
              ])

    def simple_query(v):
        ans = input("is '%s' the target? [y/N] " % v)
        if ans and ans.lower()[0] == 'y':
            return QueryResult(True, None)
        else:
            print("Please input a vertex on the shortest path between"
                  " '%s' and the target. The graph is: " % v)
            for w in G.incident_edges:
                print("%s: %s" % (w, G.incident_edges[w]))

            target = None
            while target not in G.vertices:
                target = input("Input neighboring vertex of '%s': " % v)

        return QueryResult(
            False,
            G.edge(v, target)
        )

    output = binary_search(G, simple_query)
    print("Found target: %s" % output)
