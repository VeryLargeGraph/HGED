# Code for HGED Algorithm

This repository contains a reference implementation of Explainable Hyperlink Prediction: A Hypergraph Edit
Distance-Based Approach

## Environment setup

Codes run on Python 2.7 or later. [PyPy](http://pypy.org/) compiler is recommended because it can make the computations
quicker without change the codes.

You may use Git to clone the repository from
GitHub and run it manually like this:

    git clone https://github.com/VeryLargeGraph/HGED.git
    cd HGED
    pip install click
    python run.py

## Running example

You can type in dataset number, parameters l, delta and method number to control the program:

    Dataset name(str): dataset_name
    Tau(int): 5
    Lambda(float): 3
    Type one number to chose the algorithm: [1]HEP-JS; [2]HEP-DFS; [3]HEP-BFS. (int): 2
    
## Dataset Formats

dataset_name.data: each line is a hyperedge cantaining several ids of nodes

    205,258,292
    3,7,42,47
    65,117
    292,303
    9,269
    9,285
    ...

dataset_name.label : each line is the label of node with id equals current line id

    9
    9
    3
    3
    8
    ...