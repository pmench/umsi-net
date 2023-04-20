import sys

import numpy as np
import pandas as pd

import graph
import helper as utl


def display(shortest_path, start, end):
    """
    TODO: Write docstring.
    :param end:
    :param start:
    :param shortest_path:
    :return:
    """
    links = [link[0] for link in shortest_path[1]]
    affils = [link[1] for link in shortest_path[1]]
    endows = [link[2] for link in shortest_path[1]]
    display_df = pd.DataFrame({'connections': links, 'affiliations': affils, 'endowment': endows})
    print(display_df.to_markdown(tablefmt='grid'))
    print(f"{start} is {shortest_path[0]} degrees from {end}")
    return display_df


def main():
    """
    Entry point for program.

    :param: none.
    :return: none.
    """
    # Start
    umsi_net = graph.build_graph(utl.read_json('cache.json'))
    while True:
        print('\n***********************************************\n'
              + '#### Welcome to UMSI Net, a network graph ####\n'
              + '#### of UMSI faculty and their co-authors ####'
              + '\n**********************************************\n')
        print('Make a selection from the following options:\n'
              '1. Find connections between authors.\n'
              '2. See the top 10 most connected people and universities.\n'
              '3. Get average and median endowment size of universities\n'
              + '   connected to UMSI faculty by their co-authors.\n'
                '4. Get the number of connections for a specific person.\n'
                '5. Get the average number of connections in the graph (the degree).\n'
                '6. Get a list of UMSI faculty as a CSV file.')
        usr = input('\nEnter the number of your chosen action when ready. Type "exit" to quit.\n')
        if usr == 'exit':
            sys.exit('Goodbye!')
        if usr == '1':
            while True:
                choice = input('Would you like to choose two authors (1) or '
                               + 'should I choose two for you (2)?\n'
                                 'Type "menu" to return to the main menu.\n')
                if choice == '1':
                    pass
                if choice == '2':
                    generator = np.random.default_rng()
                    authors = generator.choice(list(umsi_net.get_vertices()), 2)
                    author_links = graph.bfs(umsi_net, umsi_net.get_vertex(authors[0]), umsi_net.get_vertex(authors[1]))
                    for author in author_links[1]:
                        pos = author_links[1].index(author)
                        author_links[1].remove(author)
                        author_links[1].insert(pos, (author, umsi_net.get_vertex(author).get_affiliation(),
                                                     umsi_net.get_vertex(author).get_affil_endow()))
                    display(author_links, authors[0], authors[1])
                if choice == 'menu':
                    break
                if choice == 'exit':
                    sys.exit('Goodbye!')


if __name__ == '__main__':
    main()
