# Code for HGED Algorithm
This repository contains a reference implementation of Explainable Hyperlink Prediction: A Hypergraph Edit Distance-Based Approach

## Environment setup

Codes run on Python 2.7 or later. [PyPy](http://pypy.org/) compiler is recommended because it can make the computations quicker without change the codes.

You may use Git to clone the repository from
GitHub and run it manually like this:

    git clone https://github.com/VeryLargeGraph/HGED.git
    cd HGED
    pip install click
    python run.py

## Running example
You can type in dataset number, parameters l, delta and method number to control the program:

    Dataset name(str): HS
    Tau(int): 5
    Lambda(int): 3
    Type one number to chose the algorithm: [1]HEP-JS; [2]HEP-DFS; [3]HEP-BFS. (int): 2
    

    
## Tips

Due to the limit of space, we only upload some datasets of small size here. Welcome to e-mail me for more datasets of hypergraphs.