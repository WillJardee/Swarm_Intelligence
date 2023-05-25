import random

class Ant:
    def __init__(self, **kwargs) -> None:
        pass

class DefaultAnt(Ant):
    def __init__(self, colony, **kwargs) -> None:
        super().__init__(**kwargs)
        self.colony = colony
        self.path = []
        self.max_path_length = round(kwargs.get("max_path_length", self.colony.graph.number_of_edges()**(1/2)))
        self.current_node = self.colony.start
        self.path_weight = 0
        self.tabu_list = []

    def find_path(self, max_path_length = None) -> None:
        if max_path_length is not None:
            self.max_path_length = max_path_length
        
        for _ in range(self.max_path_length):
            probs = self.find_probabilities()
            rand = random.random()
            for edge in probs:
                if edge[0] > rand:
                    select_edge = edge[1]
                    break
                else:
                    rand -= edge[0]
            if self.make_step(select_edge):
                break
            
    def lay_pheromone(self):
        for edge in self.path:
            self.colony.graph.edges[edge]['pheromone'] += 0 if self.current_node == self.colony.end else 1/self.path_weight

    def find_probabilities(self) -> list:
        u = self.current_node
        g = self.colony.graph
        candi_list = [v for v in list(g[u]) if v not in self.tabu_list]
        pheromones = [(g[u][v]['pheromone']**self.colony.alpha) * (1/g[u][v]['weight'])**self.colony.beta for v in (candi_list if len(candi_list) > 0 else list(g[u]))]
        pheromones = [p/sum(pheromones) for p in pheromones]
        pheromones = [(pheromones[i], (u, list(g[u])[i])) for i in range(len(pheromones))]
        return pheromones
    
    def make_step(self, edge) -> bool:
        self.path.append(edge)
        self.current_node = edge[1]
        self.path_weight += self.colony.graph.edges[edge]['weight']
        self.tabu_list.append(self.current_node)
        if len(self.tabu_list) > 0:
            self.tabu_list.pop(0) 
        return self.current_node == self.colony.end
