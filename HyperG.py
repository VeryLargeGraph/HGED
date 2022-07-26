# -*- coding: utf-8 -*-
import pickle
import os.path

class HyperG:
    def __init__(self, path):
        filenameE = path + "#" + "E"
        filenameV = path + "#" + "E"
        if os.path.isfile(filenameE) and os.path.isfile(filenameV):
            self.E, self.V = self.loadHyperGraph(path)
        else:
            self.formatHyperG(path)
            self.E, self.V = self.loadHyperGraph(path)
        self.EGO = {}
        print("#nodes:"+str(len(self.V)))
        print("#hyper edges:"+str(len(self.E)))
        print("HyperGraph Loaded!")

    def formatHyperG(self, path):
        E = {}
        with open(path,'r') as f:
            line = f.readlines()
            count = 0
            for item in line:
                hedge = item.strip("\n").split(",")
                E[count] = list(map(int, hedge))
                count += 1

        V = {}
        for k, v in E.items():
            for item in v:
                if item in V:
                    V[item].append(k)
                else:
                    V[item] = [k]
        filename = path + "#" + "E"
        file_obj = open(filename, 'wb')
        pickle.dump(E, file_obj)
        file_obj.close()

        filename = path + "#" + "V"
        file_obj = open(filename, 'wb')
        pickle.dump(V, file_obj)
        file_obj.close()

    def loadHyperGraph(self, path):
        filename = path + "#" + "E"
        pickfile = open(filename, 'rb')
        E = pickle.load(pickfile)
        pickfile.close()
        filename = path + "#" + "V"
        pickfile = open(filename, 'rb')
        V = pickle.load(pickfile)
        pickfile.close()
        return E,V

    def egonetwork(self, E, V, v):
        EGO_V = {}
        NEI = set()
        for hyperE in V[v]:
            set_temp = set(E[hyperE])
            NEI |= set_temp
        # print(NEI)
        EGO_V[v] = V[v].copy()
        for u in NEI:
            if u != v:
                hyperElist = []
                for hyperE in V[u]:
                    temset = set(E[hyperE])
                    if temset.issubset(NEI):
                        hyperElist.append(hyperE)
                EGO_V[u] = hyperElist.copy()
        return EGO_V

    def HGED_HEU(self, u, v):
        if u not in self.EGO:
            self.EGO[u] = self.egonetwork(self.E, self.V, u)
        if v not in self.EGO:
            self.EGO[v] = self.egonetwork(self.E, self.V, v)
        if len(self.EGO[u]) < len(self.EGO[v]):
            tempu, tempv = u, v
            u, v = tempv, tempu
        Vu = list(self.EGO[u].keys())
        Vv = list(self.EGO[v].keys())
        Vv += list(range(len(Vv) - len(Vu), 0))
        I = list(range(len(Vu)))
        f = {}
        self.DFS(0, {}, len(Vu), f, I)


    def DFS(self, level, visited, n, f, I):
        if level == n:

            return
        for i in I:
            if i not in visited:
                visited[i] = True
                f[level] = i
                self.DFS(level+1, visited, n, f, I)
                del(visited[i])


if __name__ == '__main__':
    HG = HyperG("HS.data")
    # HG = HyperG("PS.data")
    HG.HGED_HEU(46, 45)

