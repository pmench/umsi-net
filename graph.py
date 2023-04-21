import re
from collections import deque

import numpy as np
from tqdm import tqdm

import helper as utl


# Graph class based on code from Runestone Academy
# https://runestone.academy/ns/books/published/pythonds/Graphs/Implementation.html
class Graph:
    """
    This class defines a graph object.

    Attributes:
        vert_list (dict): dictionary of vertices in the graph.
        num_vertices (int): total number of vertices in the graph.
    Methods:
        add_vertex: increases the number of vertices in the graph by one,
            adding the passed-in Vertex object to vert_list if it is not
            already in the graph. If the optional "warn" is set to True,
            it prints the names of vertices already in the graph as it
            encounters them.
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

    def add_vertex(self, key, warn=False):
        if key not in self.vert_list:
            self.num_vertices = self.num_vertices + 1
            new_vertex = Vertex(key)
            self.vert_list[key] = new_vertex
            return new_vertex
        elif warn is True:
            print(f'{key} already in graph')

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
    This class defines a Vertex object representing a person or institution.

    Attributes:
        id (str): identifier for vertex object (e.g. name)
        connected_to (dict): dictionary of vertices connected to vertex
            by an edge.
        color (str): indicator used to track traversal during search.
        dist (float | int): counter for distance traversed between vertices
            during search.
        pred (vertex obj): vertex traversed just before vertex during search.
        affiliation (str): affiliated institution and job position for vertex.
        affil_endow (str): size of endowment of affiliated institution.
        degree (int): number of vertices connected to vertex.
        type (str): indicates whether the vertex is a person or an institution.
    Methods:
        add_neighbor: updates the connected_to attribute with nbr vertex
            as key and weight as value.
            When called by the Graph() class method add_edge, it obtains
            information for the connected vertices from the graph's
            vert_list.
        __str__: defines behavior for returning a string with vertex
            information.
        set_color: sets the color attribute of a vertex, used for tracking
            whether the vertex has been traversed during search.
        set_distance: sets the distance attribute of the vertex, reflecting
            the distance traveled from a starting vertex during a search.
        set_pred: sets the pred attribute of a vertex, which tracks the
            vertex traversed immediately before the vertex during search.
        set_affiliation: sets the affiliation attribute of the vertex.
        set_affil_endow: sets the affil_endow attribute of the vertex.
        set_type: sets the type attribute of the vertex.
        get_connections: returns keys from the connected_to attribute,
            listing all vertices set as the vertex's neighbor.
        get_connection_ids: returns the keys for each vertex object in the
            connected_to dictionary.
        get_id: returns the vertex's key, or the name given to the vertex.
        get_weight: returns the weight of the edge between vertex and nbr
            from the connected_to dictionary.
        get_pred: returns the pred attribute of the vertex.
        get_distance: returns the distance attribute of the vertex.
        get_color: returns the color attribute of the vertex.
        get_affiliation: returns affiliation attribute of the vertex.
        get_affil_endow: returns the affil_endow attribute of the vertex.
        get_degree: returns the degree attribute of the vertex.
        calc_degree: determines the number of vertices connected to the vertex
            and assigns the value to the vertex's degree attribute.
        get_type: returns the type attribute of the vertex.
    """

    def __init__(self, key):
        self.id = key
        self.connected_to = {}
        self.color = 'white'
        self.dist = float('inf')
        self.pred = None
        self.affiliation = None
        self.affil_endow = None
        self.degree = 0
        self.type = None

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

    def set_affiliation(self, a):
        self.affiliation = a

    def set_affil_endow(self, e):
        self.affil_endow = e

    def set_type(self, t):
        self.type = t

    def get_connections(self):
        return self.connected_to.keys()

    def get_connection_ids(self):
        connects = self.connected_to.keys()
        return [[vert.get_id()] for vert in connects]

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

    def get_affil_endow(self):
        return self.affil_endow

    def get_degree(self):
        return self.degree

    def calc_degree(self):
        self.degree = len(self.connected_to.keys())

    def get_type(self):
        return self.type


def build_graph(data):
    """
    Constructs a graph object of UMSI faculty and their co-authors and affiliations.

    :param data: (dict) faculty and institution data.
    :return: graph object.
    """
    g = Graph()

    # Add UMSI faculty to graph
    for faculty in tqdm(data.get('auths-coauths'), 'Adding UMSI faculty'):
        g.add_vertex(faculty.get('name'))
        g.get_vertex(faculty.get('name')).set_type('person')
        g.get_vertex(faculty.get('name')).set_affiliation('University of Michigan')

    # Add institutions with endowment data to graph
    for org in tqdm(data.get('enrich_institutions'), 'Adding institutions'):
        if org.get('endowment') is not None:
            g.add_vertex(org.get('org'))
            g.get_vertex(org.get('org')).set_affil_endow(org.get('endowment'))
            g.get_vertex(org.get('org')).set_type('institution')

    # Add coauthors to graph and connect people
    for faculty in tqdm(data.get('auths-coauths'), 'Connecting people'):
        if faculty.get('coauthors') is not None:
            for person in faculty.get('coauthors'):
                g.add_vertex(person.get('name'))
                g.get_vertex(person.get('name')).set_type('person')
                g.add_edge(faculty.get('name'), person.get('name'))
                g.add_edge(person.get('name'), faculty.get('name'))
                if g.get_vertex(person.get('name')).get_affiliation() is None:
                    g.get_vertex(person.get('name')).set_affiliation(person.get('affiliation'))

    # Connect institutions and people
    verts = g.vert_list.keys()
    for vert in tqdm(verts, 'Connecting people and institutions'):
        current_vert = [g.get_vertex(vert).get_affiliation()]
        for affil in current_vert:
            if affil is not None:
                for entity in verts:
                    if entity in affil:
                        g.add_edge(vert, entity)
                        g.add_edge(entity, vert)
                        g.get_vertex(vert).set_affil_endow(g.get_vertex(entity).get_affil_endow())
    return g


def bfs(graph, start, end):
    """
    Using breadth-first search, finds the shortest path between the start and end vertices.
    :param graph: (graph obj) graph object containing data.
    :param start: (vertex obj) vertex at which to begin the search.
    :param end: (vertex obj) vertex at which to end the search.
    :return: (tuple) integer representing distance between start and end
        and a list of vertices traversed between start and end.
    """
    reset_graph(graph)
    try:
        q = deque()
        q.appendleft(start)
        preds = []
        while q:
            current_vert = q.pop()
            if current_vert == end:
                x = current_vert
                while x.get_pred():
                    preds.append(x.get_id())
                    x = x.get_pred()
                preds.append(x.get_id())
                return current_vert.get_distance(), preds
            else:
                for nbr in current_vert.get_connections():
                    if nbr.get_color() == 'white':
                        nbr.set_color('gray')
                        nbr.set_distance(current_vert.get_distance() + 1)
                        nbr.set_pred(current_vert)
                        q.appendleft(nbr)
                current_vert.set_color('black')
    except KeyError as e:
        print(f"Entity not found: {e}")
        return None
    except AttributeError as e:
        print(f"Entity not found: {e}")
        return None


def reset_graph(graph):
    """
    This function allows for successive searches of the graph by resetting
    vertex attributes that are used to track visited vertices during search.
    :param graph: object of the Graph class.
    :return: none.
    """
    for vert in graph:
        vert.set_color('white')
        vert.set_distance(0)
        vert.set_pred(None)


def get_degrees(graph):
    """
    Assembles a list of all vertices in the graph with the total number
    of vertices connected to each vertex.
    :param graph: object of the Graph class.
    :return: list of tuples
    """
    authors = []
    for key in graph.vert_list.keys():
        graph.vert_list[key].calc_degree()
        authors.append((key, graph.vert_list[key].get_degree()))
    return sorted(authors, key=lambda item: item[1], reverse=True)


def get_avg_degree(graph):
    """
    For the entire graph, calculates the average number of connections
    each vertex has.
    :param graph: object of the Graph class.
    :return: float
    """
    degrees = []
    for key in graph.vert_list.keys():
        graph.vert_list[key].calc_degree()
        degrees.append((graph.vert_list[key].get_degree()))
    return sum(degrees) / len(graph.vert_list.keys())


def get_endow_summary(graph, show_all=False):
    """
    Calculates the mean and median of endowments in the graph data or, optionally,
    the endowments of all institutions in graph. It delegates parsing endowment data to the
    parse_endow function.
    :param graph: object of the Graph class.
    :param show_all: (bool) if True, returns a list of all endowments rather than the mean and median.
    :return: (list | tuple) list of all endowments or a tuple of the mean and median of all endowments.
    """
    endowments = []
    for vert in graph.vert_list:
        if graph.get_vertex(vert).get_affil_endow() is not None and graph.get_vertex(vert).get_type() == 'institution':
            endow = graph.get_vertex(vert).get_affil_endow()
            endowments.append(parse_endow(endow))
    if show_all:
        return endowments
    else:
        return np.mean(endowments), np.median(endowments)


def parse_endow(endowment):
    """
    Converts a string with information about the size of an institution's endowment
    to a float, using exchange rates current as of 2023-04-19 to convert currencies
    to USD.
    :param endowment: (str) size of an institution's endowment.
    :return: float
    """
    units = {'billion': 1_000_000_000, 'million': 1_000_000}
    xchg = {'euro': 1.0973118055, 'gbp': 1.2450927781}
    regex = r'((£|\$|€)s*.*?)\s'
    match = re.search(regex, endowment)
    if match:
        clean_endow = float(match.group(1).strip(match.group(2)).replace(',', '.'))
        if match.group(2) == '£':
            clean_endow = clean_endow * xchg.get('gbp')
        elif match.group(2) == '€':
            clean_endow = clean_endow * xchg.get('euro')
        if 'billion' in endowment:
            factor_endow = clean_endow * units.get('billion')
            return factor_endow
        elif 'million' in endowment:
            factor_endow = clean_endow * units.get('million')
            return factor_endow
        else:
            raise ValueError
    else:
        clean_endow = float(endowment.strip('£$€¥').replace(',', ''))
        if '£' in endowment:
            endow = clean_endow * xchg.get('gbp')
            return endow
        if '€' in endowment:
            endow = clean_endow * xchg.get('euro')
            return endow
        else:
            return clean_endow


def graph_to_json(graph):
    """
    Constructs a dictionary of vertices in the graph object and exports to
    JSON format, delegating JSON serialization to the write_json function
    in the helper module.
    :param graph: object of the Graph class.
    :return: none.
    """
    graph_json = {}
    vertices = graph.vert_list
    for vert in vertices:
        graph_json.update({vertices[vert].get_id(): {
            'connected_to': [entity.get_id() for entity in vertices[vert].get_connections()],
            'color': vertices[vert].get_color(),
            'dist': 'infinity',
            'pred': vertices[vert].get_pred(),
            'affiliation': vertices[vert].get_affiliation(),
            'affil_endow': vertices[vert].get_affil_endow(),
            'degree': vertices[vert].get_degree(),
            'type': vertices[vert].get_type()}})
    utl.write_json('graph_structure.json', graph_json)


def orgs_to_csv(graph):
    """
    Writes a list of institutions, the size of their endowments, and the number of vertices
    each is connected to in the graph to a CSV file. It delegates creation of the CSV file
    to the write_csv function in the helper module.
    :param graph: object of the Graph class.
    :return: none.
    """
    orgs = []
    headers = ['institution', 'endowment', 'num_connections']
    vertices = graph.vert_list
    for vert in vertices:
        if vertices[vert].get_type() == 'institution':
            info = [vertices[vert].get_id(), vertices[vert].get_affil_endow(), len(vertices[vert].connected_to.keys())]
            orgs.append(info)
    utl.write_csv('institutions.csv', orgs, headers=headers)


def main():
    """
    Entry point for program.

    :params: none.
    :return: none.
    """
    # Check properties of graph
    umsi_net = build_graph(utl.read_json('cache.json'))
    print(len(umsi_net.vert_list))
    utl.print_pretty(umsi_net.get_vertices())
    print((umsi_net.get_vertex('Ixchel Faniel').get_id(), umsi_net.get_vertex('Ixchel Faniel').get_affiliation()))
    print((umsi_net.get_vertex('Stanford University').get_id(),
           umsi_net.get_vertex('Stanford University').get_affil_endow()))
    print(umsi_net.get_vertex('Michael S. Bernstein'))
    print(len(umsi_net.get_vertex('Michael S. Bernstein').get_connections()))
    print(bfs(umsi_net, umsi_net.get_vertex('Dan Jurafsky'), umsi_net.get_vertex('Ixchel Faniel')))
    utl.print_pretty(get_degrees(umsi_net)[:10])


if __name__ == '__main__':
    main()
