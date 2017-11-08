import math
import heapq


'''
Dijkstra's algorithm with associated metadata to compute
all shortest paths
'''
class DijkstraOutput:
    def __init__(self, graph, start):
        self.start = start
        self.graph = graph
        
        # the smallest distance from the start to the destination v
        self.distance_from_start = {v: math.inf for v in graph.vertices}
        self.distance_from_start[start] = 0

        # a list of predecessor edges for each destination
        # to track a list of possibly many shortest paths
        self.predecessor_edges = {v: [] for v in graph.vertices}

    def found_shorter_path(self, vertex, edge, new_distance):
        # update the solution with a newly found shorter path
        self.distance_from_start[vertex] = new_distance

        if new_distance < self.distance_from_start[vertex]:
            self.predecessor_edges[vertex] = [edge]
        else:  # tie for multiple shortest paths
            self.predecessor_edges[vertex].append(edge)

    def path_to_destination_contains_edge(self, destination, edge):
        predecessors = self.predecessor_edges[destination]
        if edge in predecessors:
            return True
        return any(self.path_to_destination_contains_edge(e.source, edge)
                   for e in predecessors)

    def sum_of_distances(self, subset=None):
        subset = subset or self.graph.vertices
        return sum(self.distance_from_start[x] for x in subset)   


def single_source_shortest_paths(graph, start):
    '''
    Compute the shortest paths and distances from the start vertex to all
    possible destination vertices. Return an instance of DijkstraOutput.
    '''
    output = DijkstraOutput(graph, start)
    visit_queue = [(0, start)]

    while len(visit_queue) > 0:
        priority, current = heapq.heappop(visit_queue)
        
        for incident_edge in graph.incident_edges[current]:
            v = incident_edge.target
            weight = incident_edge.weight
            distance_from_current = output.distance_from_start[current] + weight

            if distance_from_current <= output.distance_from_start[v]:
                output.found_shorter_path(v, incident_edge, distance_from_current)
                heapq.heappush(visit_queue, (distance_from_current, v))

    return output
