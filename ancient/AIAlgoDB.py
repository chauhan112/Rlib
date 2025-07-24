class AIAlgoDB:
    def geneticAlgo(gene, target, populationSize = 100):
        import random
        class GeneticAlgorithm:
            def mutate_genes():
                return random.choice(GeneticAlgorithm.gene)

            def create_gnome():
                return [GeneticAlgorithm.mutate_genes() for i in range(len(GeneticAlgorithm.target))]

            def cal_fitness(chromosome): 
                ''' 
                Calculate fittness score, it is the number of 
                characters in string which differ from target 
                string. 
                '''
                fitness = 0
                for gs, gt in zip(chromosome, GeneticAlgorithm.target): 
                    if gs != gt: fitness+= 1
                return fitness 
        class Individual:
            def __init__(self, chromosome):
                self.chromosome = chromosome
                self.fitness = GeneticAlgorithm.cal_fitness(chromosome) 

            def mate(self, par2):
                child_chromosome = [] 
                for gp1, gp2 in zip(self.chromosome, par2.chromosome):     
                    prob = random.random() 
                    if prob < 0.45: 
                        child_chromosome.append(gp1) 
                    elif prob < 0.90: 
                        child_chromosome.append(gp2) 
                    else: 
                        child_chromosome.append(GeneticAlgorithm.mutate_genes()) 
                return Individual(child_chromosome)

        GeneticAlgorithm.gene = gene
        GeneticAlgorithm.target = target

        generation = 1
        found = False
        population = [] 
        for _ in range(populationSize): 
            gnome = GeneticAlgorithm.create_gnome() 
            population.append(Individual(gnome)) 
        while not found: 
            population = sorted(population, key = lambda x:x.fitness) 
            if population[0].fitness <= 0: 
                found = True
                break
            new_generation = [] 
            s = int((10 * populationSize)/100) 
            new_generation.extend(population[:s]) 
            s = int((90 * populationSize)/100) 
            for _ in range(s): 
                parent1 = random.choice(population[:50]) 
                parent2 = random.choice(population[:50]) 
                child = parent1.mate(parent2) 
                new_generation.append(child) 
            population = new_generation 
            print("Generation: {}\tString: {}\tFitness: {}".format(generation, 
                "".join(population[0].chromosome), 
                population[0].fitness)) 
            generation += 1
        print("Generation: {}\tString: {}\tFitness: {}".format(generation, 
            "".join(population[0].chromosome), 
            population[0].fitness)) 
    
    def incrementalSearch(wordBags = [], resultSize = 1, cost = 3):
        # Auto Complete
        from fast_autocomplete import AutoComplete
        from useful.ListDB import ListDB
        class _AutoComplete:
            def __init__(self, container, cost = 3, size = 1, synonyms = None):
                self.container = {k:{} for k in container}
                self.engine = AutoComplete(words = self.container, synonyms= synonyms)
                self.cost = cost
                self.size = size
            def search(self, word):
                if(word == ""):
                    return list(self.container.keys())
                return ListDB.flatten(self.engine.search(word, max_cost = self.cost, size = self.size))
        return _AutoComplete(wordBags, cost=cost, size=resultSize)


class Perceptron:
    def _perceptron(X, w):
        return np.sign(np.dot(X, w))

    def _pla(X, y, w_t):
        for i in range(len(X)):
            x_t = np.hstack((np.array([1]), X[i]))
            y_t = y[i]
            if y_t != Perceptron._perceptron(x_t, w_t):
                return Perceptron._pla(X, y, w_t + y_t*x_t)
        return w_t

    def fit(X, y):
        d = len(X[0])
        Perceptron.w = np.ones((d+1,1)).flatten()
        Perceptron.w = Perceptron._pla(X,y, w)
        return Perceptron.w
    
    def predict(X):
        x_t = np.hstack((np.ones((len(X),1)), X))
        return np.array([Perceptron._perceptron(x1, Perceptron.w) for x1 in x_t])
    
    def error(X, y):
        out = Perceptron.predict(X)
        n = 0
        for i, val in enumerate(y):
            if(val != out[i]):
                n += 1
        return n/len(out)
        
class Dijkstra:
    def __init__(self, vertices, graph):
        self.vertices = vertices  # ("A", "B", "C" ...)
        self.graph = graph  # {"A": {"B": 1}, "B": {"A": 3, "C": 5} ...}

    def find_route(self, start, end):
        unvisited = {n: float("inf") for n in self.vertices}
        unvisited[start] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex = min(unvisited, key=unvisited.get)  # get smallest distance
            for neighbour, _ in self.graph.get(min_vertex, {}).items():
                if neighbour in visited:
                    continue
                new_distance = unvisited[min_vertex] + self.graph[min_vertex].get(neighbour, float("inf"))
                if new_distance < unvisited[neighbour]:
                    unvisited[neighbour] = new_distance
                    parents[neighbour] = min_vertex
            visited[min_vertex] = unvisited[min_vertex]
            unvisited.pop(min_vertex)
            if min_vertex == end:
                break
        return parents, visited

    @staticmethod
    def generate_path(parents, start, end):
        path = [end]
        while True:
            key = parents[path[0]]
            path.insert(0, key)
            if key == start:
                break
        return path


class IGraph:
    def get_vertices(self):
        raise NotImplementedError("abstract method")
    def has_ended(self):
        raise NotImplementedError("abstract method")
    def get_nebors(self, pos):
        raise NotImplementedError("abstract method")
class INode:
    def get_uuid(self):
        raise NotImplementedError("abstract method")
    def get_value(self):
        raise NotImplementedError("abstract method")
    def is_less(self, anotherNode):
        raise NotImplementedError("abstract method")
class IBreakingCondition:
    def target_reached(self, *params) -> bool:
        pass
class ModularDijkstra:
    def set_graph(self, grp: IGraph):
        self._graph = grp
    def find_route(self, start: INode):
        unvisited = {n.get_uuid(): float("inf") for n in self._graph.get_vertices()}
        unvisited[start.get_uuid()] = 0  # set start vertex to 0
        visited = {}  # list of all visited nodes
        parents = {}  # predecessors
        while unvisited:
            min_vertex_id = min(unvisited, key=lambda x: unvisited.get(x.get_uuid()))  # get smallest distance
            for neighbour in self._graph.get_nebors(self._graph.get_node_from_uuid(min_vertex_id)):
                if neighbour.get_uuid() in visited:
                    continue
                new_distance = unvisited[min_vertex_id] + self._graph.get_value_from_to(self._graph.get_node_from_uuid(min_vertex_id), neighbour)
                if new_distance < unvisited[neighbour.get_uuid()]:
                    unvisited[neighbour.get_uuid()] = new_distance
                    parents[neighbour.get_uuid()] = min_vertex_id
            visited[min_vertex_id] = unvisited[min_vertex_id]
            unvisited.pop(min_vertex_id)
            if self._condition.target_reached(min_vertex_id):
                break
        return parents, visited
    def set_breaking_condition(self, condition: IBreakingCondition):
        self._condition = condition