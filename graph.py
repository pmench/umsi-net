import helper as utl


# Graph class from Runestone Academy
# https://runestone.academy/ns/books/published/pythonds/Graphs/Implementation.html
class Graph:
    """
    This class defines a graph object.

    Attributes:
        vert_list (dict): dictionary of vertices in the graph.
        num_vertices (int): total number of vertices in the graph.
    Methods:
        add_vertex: increases the number of vertices in the graph by one,
            adding the passed-in Vertex object to vert_list.
        get_vertex: given a vertex, it checks if the vertex exists in
            vert_list and, if so, returns the vertex object from vert_list.
        __contains__: defines the behavior of the "in" operator for the class.
            It checks if the given vertex n is in vert_list.
        add_edge: Adds edges to the graph, with optional weights. It checks
            whether the given vertices are present in the graph and, if not,
            adds them. It then calls the add_neighbor Vertex method to
            connect the vertices.
        get_vertices: returns a list of all the keys of vertices in the graph.
        __iter__: allows for iteration over the dictionary of vertex values.
    """

    def __init__(self):
        self.vert_list = {}
        self.num_vertices = 0

    def add_vertex(self, key):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(key)
        self.vert_list[key] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_list:
            return self.vert_list[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vert_list

    def add_edge(self, f, t, weight=0):
        if f not in self.vert_list:
            nv = self.add_vertex(f)
        if t not in self.vert_list:
            nv = self.add_vertex(t)
        self.vert_list[f].add_neighbor(self.vert_list[t], weight)

    def get_vertices(self):
        return self.vert_list.keys()

    def __iter__(self):
        return iter(self.vert_list.values())


# Vertex Class based on code from Runestone Academy
# https://runestone.academy/ns/books/published/pythonds/Graphs/Implementation.html
class Vertex:
    """
    TODO: Write Docstring
    """

    def __init__(self, key):
        self.id = key
        self.connected_to = {}
        self.color = 'white'
        self.dist = float('inf')
        self.pred = None
        self.affiliation = None
        self.affil_assets = None

    def add_neighbor(self, nbr, weight=0):
        self.connected_to[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connected_to: ' + str([x.id for x in self.connected_to])

    def set_color(self, color):
        self.color = color

    def set_distance(self, d):
        self.dist = d

    def set_pred(self, p):
        self.pred = p

    def set_movies(self, m):
        self.movies = m

    def get_connections(self):
        return self.connected_to.keys()

    def get_id(self):
        return self.id

    def get_weight(self, nbr):
        return self.connected_to[nbr]

    def get_pred(self):
        return self.pred

    def get_distance(self):
        return self.dist

    def get_color(self):
        return self.color

    def get_affiliation(self):
        return self.affiliation

    def get_affil_assets(self):
        return self.affil_assets


# Estimate number of entities in data
data = utl.read_json('cache.json')

faculty = len(data['auths-coauths'])
coauths = 0
institutions = len(data.get('institutions'))

for person in data['auths-coauths']:
    try:
        for coauth in person.get('coauthors'):
            coauths += 1
    except TypeError:
        continue

print(f"faculty = {faculty}, coauths = {coauths}, institutions = {institutions}")