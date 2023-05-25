import antcolony
import networkx as nx


if __name__ == "__main__":
    g = nx.read_edgelist("small_toy_graph.txt")
    g = g.to_directed()
    for i in range(1, 10):
        AC = antcolony.AntColony(g, s = '1', t = '7', max_iterations=10*i, num_ants=5)
        AC.run()
        AC.complete_print(pheromones=False)
        print()
    pass