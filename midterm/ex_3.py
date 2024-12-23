import sys
import random
from collections import defaultdict
from heapq import heappop, heappush

'''
7 11
1 2 1
1 4 3
1 5 7
2 3 6
2 4 10
3 4 5
3 7 2
4 5 6
4 7 4
5 6 15
6 7 9
2
2
5 6
'''

def parse_input():
    input = sys.stdin.read()
    lines = input.strip().split('\n')
    n, m = map(int, lines[0].split())
    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, lines[i].split())
        edges.append((u - 1, v - 1, w))  
    source = int(lines[m + 1]) - 1 
    k = int(lines[m + 2])
    terminals = list(map(lambda x: int(x) - 1, lines[m + 3].split()))  
    return n, edges, source, terminals

class LocalSearch:
    def __init__(self, n, edges, source, terminals):
        self.n = n
        self.edges = edges
        self.graph = self.create_graph(edges)
        self.source = source
        self.terminals = set(terminals)

    def create_graph(self,edges):
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))
        return graph

    def generate_initial_solution(self):
        mst_edges = set()
        total_weight = 0
        visited = set()
        min_heap = [(0, self.source, -1)]
        
        while min_heap and len(visited) < self.n:
            weight, u, parent = heappop(min_heap)
            if u in visited:
                continue
            visited.add(u)
            if parent != -1:
                mst_edges.add((u, parent) if u < parent else (parent, u))
                total_weight += weight
            for v, w in self.graph[u]:
                if v not in visited:
                    heappush(min_heap, (w, v, u))
                    
        return mst_edges, total_weight
    
    def is_valid(self, solution_edges):
        connected = set()
        adj_list = defaultdict(list)
        for u, v in solution_edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        
        stack = [self.source]
        while stack:
            node = stack.pop()
            if node in connected:
                continue
            connected.add(node)
            for v in adj_list[node]:
                if v not in connected:
                    stack.append(v)
                
        return self.terminals.issubset(connected)
    
    def calculate_cost(self, solution_edges):
        total_cost = 0
        edge_set = set(solution_edges)
        for u, v, w in self.edges:
            if (u, v) in edge_set or (v, u) in edge_set:
                total_cost += w
        return total_cost
    
    def solve(self):
        current_edges, current_cost = self.generate_initial_solution()
        best_edges, best_cost = current_edges, current_cost
        
        for _ in range(1000):
            neighbor_edges = set(best_edges)
            action = random.choice(['add', 'del', 'replace'])
            
            if action == 'add':
                candidate_edges = [e for e in self.edges if (e[0], e[1]) not in neighbor_edges and (e[1], e[0]) not in neighbor_edges]
                if candidate_edges:
                    edge = random.choice(candidate_edges)
                    neighbor_edges.add((edge[0], edge[1]) if edge[0] < edge[1] else (edge[1], edge[0]))
            
            elif action == 'del':
                if neighbor_edges:
                    edge = random.choice(list(neighbor_edges))
                    neighbor_edges.remove(edge)
                    
            elif action == 'replace':
                 if neighbor_edges:
                    edge_to_remove = random.choice(list(neighbor_edges))
                    neighbor_edges.remove(edge_to_remove)
                    candidate_edges = [e for e in self.edges if (e[0], e[1]) not in neighbor_edges and (e[1], e[0]) not in neighbor_edges]
                    if candidate_edges:
                        edge_to_add = random.choice(candidate_edges)
                        neighbor_edges.add((edge_to_add[0], edge_to_add[1]) if edge_to_add[0] < edge_to_add[1] else (edge_to_add[1], edge_to_add[0]))
                        
            if self.is_valid(neighbor_edges):
                neighbor_cost = self.calculate_cost(neighbor_edges)
                if neighbor_cost < best_cost:
                    best_edges, best_cost = neighbor_edges, neighbor_cost
                
        return best_edges, best_cost
        
        
n, edges, source, terminals = parse_input()

solver = LocalSearch(n, edges, source, terminals)
best_edges, best_cost = solver.solve()

print(len(best_edges))  
for u, v in best_edges:
    print(u + 1, v + 1)