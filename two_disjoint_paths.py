from ortools.sat.python import cp_model
import sys


def read_input():
    lines = sys.stdin.readlines()
    no_nodes, no_edges = map(int, lines[0].split())
    
    edges = []
    for i in range(1, no_edges + 1):
        u, v, w = map(int, lines[i].split())
        edges.append(u, v, w)
        
    return no_nodes, edges
    