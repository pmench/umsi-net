import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import graph
import helper as utl


def display_path(shortest_path, start, end):
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


def get_links(net, start=None, end=None, rand=False):
    """
    TODO: Write docstring
    :param net:
    :param rand:
    :param start:
    :param end:
    :return:
    """
    if rand:
        generator = np.random.default_rng()
        authors = generator.choice(list(net.get_vertices()), 2)
        author_links = graph.bfs(net, net.get_vertex(authors[0]), net.get_vertex(authors[1]))
    else:
        author_links = graph.bfs(net, net.get_vertex(start), net.get_vertex(end))
        authors = [start, end]
    for author in author_links[1]:
        pos = author_links[1].index(author)
        author_links[1].remove(author)
        author_links[1].insert(pos, (author, net.get_vertex(author).get_affiliation(),
                                     net.get_vertex(author).get_affil_endow()))
    display_path(author_links, authors[0], authors[1])


def display_degrees(degrees_data):
    """
    TODO: Write docstring
    :param degrees_data:
    :return:
    """
    entities = [ent[0] for ent in degrees_data]
    degrees = [ent[1] for ent in degrees_data]
    top_connects = pd.DataFrame({'Person/Institution': entities, 'Number of Connections': degrees})
    top_connects.index += 1
    print(top_connects.to_markdown(tablefmt='grid'))
    return top_connects


def visualize_endows(endowments):
    """
    TODO: Write docstring.

    Method for labeling median adapted from:
    https://stackoverflow.com/questions/38649501/labeling-boxplot-in-seaborn-with-median-value

    :param endowments:
    :return:
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 12), sharey='all')
    endows = pd.DataFrame({'endowments': endowments})
    box_plot = sns.boxplot(endows, y='endowments', ax=ax1)
    median = endows['endowments'].median()
    for xtick in box_plot.get_xticks():
        box_plot.text(xtick, median * 1.3, median,
                      horizontalalignment='center', size='x-small', color='w', weight='semibold')
    sns.histplot(endows, y='endowments', ax=ax2)
    fig.suptitle('Endowments of Institutions Connected to UMSI Faculty', fontsize=20)
    ax1.set_ylabel('Size of Endowments (tens of billions USD)')
    ax1.grid(visible=True, color='b', axis='y')
    ax2.grid(visible=True, color='b', axis='y')
    plt.show()


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
                choice = input('Would you like to choose two authors (enter 1) or '
                               + 'should I choose two for you (enter 2)?\n'
                                 'Exit or enter "menu" to return to the main menu.\n')
                if choice == '1':
                    try:
                        author_1 = input("Enter first author's name.\n")
                        author_2 = input("Enter second author's name.\n")
                        get_links(umsi_net, author_1, author_2)
                    except TypeError:
                        print("Sorry, I don't understand.\nCheck your spelling. It is also possible one of the authors"
                              + " you entered isn't in my data. Please try again.\n")
                if choice == '2':
                    get_links(umsi_net, rand=True)
                if choice == 'menu':
                    break
                if choice == 'exit':
                    sys.exit('Goodbye!')
                else:
                    print(f"Sorry, {choice} isn't an option I recognize. Please try again.")
        if usr == '2':
            display_degrees(graph.get_degrees(umsi_net)[:10])
            while True:
                x_num = input('Would you like to view more? Enter the number of results you would like to see.\n'
                              'You can also enter "exit" or "menu" to return to the main menu.\n')
                try:
                    x_num = int(x_num)
                    display_degrees(graph.get_degrees(umsi_net)[:x_num])
                except ValueError:
                    if x_num == 'exit':
                        sys.exit('Goodbye!')
                    if x_num == 'menu':
                        break
                    else:
                        print("I'm sorry. I don't understand. Please try again.")
        if usr == '3':
            stats = graph.get_endow_summary(umsi_net)
            print(
                f"Average endowment of institutions connected to UMSI faculty: ${'{:,}'.format(round(stats[0]))}\n"
                f"The median endowment is ${'{:,}'.format(round(stats[1]))}.\n"
                f"Foreign currencies (EUR, GBP) have been converted to USD based on exchange rates as of 2023-04-19.")
            choice = input('Would you like me to visualize endowment data for you? Enter "yes" or "no".\n')
            if choice == 'yes':
                visualize_endows(graph.get_endow_summary(umsi_net, show_all=True))


if __name__ == '__main__':
    main()
