import click
import HyperG

@click.command()
@click.option('--name', prompt='Dataset name(str)', help='The name of the loaded dataset')
@click.option('--tau', prompt='Tau(int)', help='The value of the parameter Tau')
@click.option('--lambdax', prompt='Lambda(int)', help='The value of the parameter Lambda')
@click.option('--method', prompt='Type one number to chose the algorithm: [1]HEP-JS; [2]HEP-DFS; [3]HEP-BFS. (int)', help='Three stable community detection methods')
def doit(name, tau, lambdax, method):
    tau = int(tau)
    lambdax = float(lambdax)
    name = name + ".data"
    G = HyperG.HyperG(name)
    if method == "1":
        G.HEP_JS(lambdax,tau)
    if method == "2":
        G.HEP_DFS(lambdax,tau)
    if method == "3":
        G.HEP_BFS(lambdax,tau)

if __name__ == '__main__':
    doit()