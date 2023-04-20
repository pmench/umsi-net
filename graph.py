import re
from collections import deque

import numpy as np
from tqdm import tqdm

import helper as utl


# Graph class from Runestone Academy
# https://runestone.academy/ns/books/published/pythonds/Graphs/Implementation.html
class Graph:
    """
    TODO: Update docstring
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
    TODO: Write Docstring
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
    TODO: Update docstring
    This function uses breadth-first search to find the shortest path
    between the start and end.

    Parameters:
        graph (object): object of Graph() class containing data.
        start (object): vertex where search should begin.
        end (object): vertex where search should end.
    Returns:
        integer representing distance between start and end.
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
                    print(x.get_id())
                    preds.append(x.get_id())
                    x = x.get_pred()
                preds.append(x.get_id())
                print(x.get_id())
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

    Parameters:
        graph (object): object of the Graph() class containing vertices.
    Returns:
        None
    """
    for vert in graph:
        vert.set_color('white')
        vert.set_distance(0)
        vert.set_pred(None)


def get_degrees(graph):
    """
    TODO: write docstring
    :param graph:
    :return:
    """
    authors = []
    for key in graph.vert_list.keys():
        graph.vert_list[key].calc_degree()
        authors.append((key, graph.vert_list[key].get_degree()))
    return sorted(authors, key=lambda item: item[1], reverse=True)


def get_avg_degree(graph):
    """
    TODO: Write docstring
    :param graph:
    :return:
    """
    degrees = []
    for key in graph.vert_list.keys():
        graph.vert_list[key].calc_degree()
        degrees.append((graph.vert_list[key].get_degree()))
    return sum(degrees) / len(graph.vert_list.keys())


def get_endow_summary(graph, show_all=False):
    """
    TODO: Write docstring, make number more readable
    :param show_all:
    :param graph:
    :return:
    """
    endowments = []
    with_endowments = 0
    for vert in graph.vert_list:
        if graph.get_vertex(vert).get_affil_endow() is not None and graph.get_vertex(vert).get_type() == 'institution':
            with_endowments += 1
            endow = graph.get_vertex(vert).get_affil_endow()
            endowments.append(parse_endow(endow))
    if show_all:
        return endowments
    else:
        return np.mean(endowments), np.median(endowments)


def parse_endow(endowment):
    """
    TODO: Write docstring
    :param endowment:
    :return:
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


def main():
    """
    Entry point for program.

    :params: none.
    :return: none.
    """
    umsi_net = build_graph(utl.read_json('cache.json'))
    # utl.print_pretty(umsi_net.vert_list)
    print(len(umsi_net.vert_list))
    print((umsi_net.get_vertex('Ixchel Faniel').get_id(), umsi_net.get_vertex('Ixchel Faniel').get_affiliation()))
    print((umsi_net.get_vertex('Stanford University').get_id(),
           umsi_net.get_vertex('Stanford University').get_affil_endow()))
    print(umsi_net.get_vertex('Michael S. Bernstein'))
    print(umsi_net.get_vertex('Mark Ackerman').get_affil_endow())
    print(bfs(umsi_net, umsi_net.get_vertex('Dan Jurafsky'), umsi_net.get_vertex('Ixchel Faniel')))
    utl.print_pretty(get_degrees(umsi_net)[:10])

    print(umsi_net.get_vertex('University of Michigan').get_connection_ids())
    print(get_avg_degree(umsi_net))
    print(get_endow_summary(umsi_net))


if __name__ == '__main__':
    main()
