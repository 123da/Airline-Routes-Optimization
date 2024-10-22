from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)  # Adjacency list for the graph
        self.vertices = vertices  # Number of vertices

    def add_edge(self, u, v):
        """Function to add an edge to the graph."""
        self.graph[u].append(v)

    def dfs(self, v, visited, stack=None, scc=None):
        """Depth-First Search (DFS) for graph traversal."""
        visited[v] = True
        if scc is not None:
            scc.append(v)
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited, stack, scc)
        if stack is not None:
            stack.append(v)

    def get_transpose(self):
        """Transpose the graph by reversing all edges."""
        g = Graph(self.vertices)
        for node in self.graph:
            for neighbor in self.graph[node]:
                g.add_edge(neighbor, node)
        return g

    def kosaraju_scc(self):
        """Step 1: Kosaraju's Algorithm to find all SCCs."""
        # Step 1: Fill the stack with vertices in the order of their finishing times
        stack = []
        visited = [False] * self.vertices
        for i in range(self.vertices):
            if not visited[i]:
                self.dfs(i, visited, stack)

        # Step 2: Get the transposed graph
        gr = self.get_transpose()

        # Step 3: Do DFS on the transposed graph in the order of the stack
        visited = [False] * self.vertices
        sccs = []
        while stack:
            node = stack.pop()
            if not visited[node]:
                scc = []
                gr.dfs(node, visited, scc=scc)
                sccs.append(scc)
        return sccs

    def compress_graph(self, sccs):
        """Step 2: Compress the graph based on SCCs."""
        # Create a mapping from each node to its SCC index
        scc_map = {}
        for idx, scc in enumerate(sccs):
            for node in scc:
                scc_map[node] = idx

        # Create the compressed graph and calculate in-degrees
        compressed_graph = defaultdict(set)
        in_degree = [0] * len(sccs)
        
        for u in self.graph:
            for v in self.graph[u]:
                if scc_map[u] != scc_map[v]:
                    if scc_map[v] not in compressed_graph[scc_map[u]]:
                        compressed_graph[scc_map[u]].add(scc_map[v])
                        in_degree[scc_map[v]] += 1

        return compressed_graph, in_degree

    def calculate_additional_routes(self, start_node):
        """Calculate the minimum number of additional routes needed."""
        # Step 1: Find all SCCs
        sccs = self.kosaraju_scc()

        # Step 2: Compress the graph based on SCCs
        compressed_graph, in_degree = self.compress_graph(sccs)

        # Step 3: Find the starting node's SCC
        start_scc = None
        for idx, scc in enumerate(sccs):
            if start_node in scc:
                start_scc = idx
                break

        # Step 4: Count the number of SCCs with in_degree = 0 that are not the start SCC
        additional_routes = 0
        for i in range(len(in_degree)):
            if in_degree[i] == 0 and i != start_scc:
                additional_routes += 1

        return additional_routes

# Sample usage
airports = ["DSM", "ORD", "BGI", "LGA", "JFK", "TLV", "DEL", "CDG", "DOH", "LHR", "SFO", "SAN", "EYW", "EWR", "HND", "ICN", "SIN", "BUD"]
g = Graph(len(airports))

# Adding the edges as per the diagram
g.add_edge(0, 1)  # DSM -> ORD
g.add_edge(1, 2)  # ORD -> BGI
g.add_edge(2, 3)  # BGI -> LGA
g.add_edge(3, 4)  # LGA -> JFK
g.add_edge(4, 15) # JFK -> HND
g.add_edge(15, 16) # HND -> ICN
g.add_edge(16, 14) # ICN -> EWR
g.add_edge(11, 9)  # SAN -> LHR
g.add_edge(9, 10)  # LHR -> SFO
g.add_edge(10, 11) # SFO -> SAN
g.add_edge(10, 12) # SFO -> EYW
g.add_edge(5, 6)   # TLV -> DEL
g.add_edge(6, 7)   # DEL -> CDG
g.add_edge(7, 17)  # CDG -> BUD
g.add_edge(17, 7)  # BUD -> CDG
g.add_edge(8, 6)   # DOH -> DEL

# Set starting airport
starting_airport = airports.index("JFK")

# Calculate additional routes
routes_needed = g.calculate_additional_routes(starting_airport)
print(f"Minimum additional routes needed: {routes_needed}")
