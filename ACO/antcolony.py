import networkx as nx
import random

from decorators import *

import ants


class Colony:
    """
    A blueprint for colonies for the Ant metaheuristic.
    

    Attributes
    ----------
    num_ants : int
        number of ants intialized
        default: 10
    max_iterations : int
        number of iterations to quit after if other termination criteria not met
        defult: 1000
    evap_rate : float
        number between 0 and such that pheromones betweeen iterations is decreased by a factor of evap_rate
        default: 0.1

    Methods
    -------
    build_graph(graph: nx.graph):
        readable graph structure to read
    """

    def __init__(self, **kwargs) -> None:
        self.num_ants = kwargs.get("num_ants", 10)
        self.max_iterations = kwargs.get("max_iterations", 100)
        self.evap_rate = kwargs.get("evap_rate", 0.1)
        self.alpha = kwargs.get("alpha", 1)
        self.beta = kwargs.get("beta", 1)
        # self.ant_type = kwargs.get("ant_type")

        self.graph_original = nx.Graph()
        self.ants = [ants.Ant() for _ in range(self.num_ants)]
    
    @undefined_func_decorator
    def __str__(self, *args) -> str:
        """
        
        """
        pass

    @undefined_func_decorator
    def build_graph(self, *args) -> None:
        pass

    @undefined_func_decorator
    def update_pheromones(self, graph: nx.graph, *args) -> None:
        pass

    @undefined_func_decorator
    def ant_steps(self, *args) -> bool:
        pass

    @undefined_func_decorator
    def run(self, *args):
        pass


class AntColony(Colony):
    def __init__(self, graph, s, t, **kwargs) -> None:
        super().__init__(**kwargs)
        self.graph_original = graph.copy
        self.graph = graph.copy()
        for edge in self.graph.edges():
            self.graph.edges[edge]['pheromone'] = random.random()
        self.start = s
        self.end = t

        self.ants = [ants.DefaultAnt(self, max_path_length = 10) for _ in range(self.num_ants)]

    def __str__(self) -> str:
        return "Ant Colony with %i ants. We are ready to march Sir!" % (self.num_ants)
    
    # TODO: 
    def greedy_path(self):
            try:
                path = []
                path.append(self.start)
                while True:
                    lis = [(p, dict(self.graph[path[-1]])[p]['pheromone']) for p in dict(self.graph[path[-1]]).keys()]
                    lis.sort(reverse= True, key=lambda x: x[1])
                    lis = [l for l in lis if l[0] not in path]
                    path.append(lis[0][0])
                    if path[-1] == self.end: break
                return path
            except IndexError:
                return "Greedy path did not find finish."

    def complete_print(self, pheromones=True):
        print("%" + "-"*45 + "%")
        if pheromones:
            e = dict(self.graph.edges())
            print("edge pheromones:")
            for edge in e.keys():
                print(str(edge) + "; p =  " + str(round(e[edge]['pheromone'], 2)))
            print()


        print("% Shortest path:")
        print("% " + str(self.greedy_path()))
        print("%" + "-"*45 + "%")


    def update_pheromones(self) -> None:
        for edge in self.graph.edges:
            self.graph.edges[edge]['pheromone'] *= (1-self.evap_rate)
        for ant in self.ants:
            ant.lay_pheromone()

    @func_timer_decorator
    def run(self, max_iterations = None) -> None:
        if max_iterations is None:
            max_iterations = self.max_iterations
        
        for _ in range(max_iterations):
            for ant in self.ants:
                ant.find_path()
            self.update_pheromones()



if __name__ == "__main__":
    pass