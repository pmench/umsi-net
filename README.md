# UMSI NET

## A Graph Network of The University of Michigan School of Information Faculty and Their Co-Authors

###### 2023-04-21

### Purpose

This goal of this project is to map the academic relationships between UMSI faculty and their co-authors examining both 
quantity and institutional affiliations.

Mapping this network can answer several questions: 
- Which UMSI faculty have published with the most co-authors?
- Are there people that UMSI faculty frequently publish with? 
- Are there other institutions that UMSI frequently collaborate with?
- What kind of institutions are those (e.g. public vs. private universities, wealth of institutions, etc.)?

### Features

The program provides a command line interface that allows a user to take a number of actions:
1. Find connections between authors.
2. See the top 10 most connected people and universities.
3. Get the average and median endowment size of universities.
   connected to UMSI faculty by their co-authors.
4. Get the number of connections for a specific person or institution.
5. Get the average number of connections in the graph (the degree).
6. Export the list of UMSI faculty to a CSV file.
7. Export the graph structure to JSON.
8. Export the list of institutions to a CSV file.

Selecting option 3 also allows provides the option to visualize endowment data contained in the
graph.

### Use

Interaction with the program is run by the main.py script, which relies on functions in and data
assembled by the graph.py module. The scrape.py, scholar.py, and finances.py files are used to obtain
data and write it to the cache. The scripts for obtaining data should be used with care, as they
could overwrite existing data in the cache. The helper.py module contains functions useful across all
scripts, such as functions to read and write JSON files.

Note that the cache file is required as it is the data source for constructing the graph. Make sure the
cache, graph.py, helper.py, and main.py are all in the same directory when running the program.

Beyond the standard Python library, this project makes use of: numpy, pandas, seaborn, tqdm, selenium,
scholarly, openai, and matplotlib (see requirements.txt).

### Data Structure

The graph is assembled as an adjacency list using class objects created from cached data. The graph is represented as
a dictionary containing Vertex objects, and each Vertex object contains a dictionary with the Vertex objects
to which it is connected (in the exported JSON representation of the graph structure, the “connected_to” attribute
is represented as a list of the keys of the connected Vertex objects).