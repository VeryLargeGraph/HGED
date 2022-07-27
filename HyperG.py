# -*- coding: utf-8 -*-
import pickle
import os.path


class HyperG:
    def __init__(self, path):
        filenameE = path + ".data#E"
        filenameV = path + ".data#V"
        file_label = path + ".label"
        if os.path.isfile(filenameE) and os.path.isfile(filenameV):
            self.E, self.V = self.loadHyperGraph(path)
        else:
            self.formatHyperG(path)
            self.E, self.V = self.loadHyperGraph(path)
        self.L = {}
        with open(file_label, "r") as f:
            lines = f.readlines()
            count = 1
            for line in lines:
                self.L[count] = int(line.strip("\n"))
                count += 1
        del (lines)

        print("#nodes:" + str(len(self.V)))
        print("#hyper edges:" + str(len(self.E)))
        print("HyperGraph Loaded!")

        self.EGO = {}
        self.edc = len(self.V) + len(self.E)
        self.D = {}

    def formatHyperG(self, path):
        E = {}
        with open(path, 'r') as f:
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
        filename = path + ".data#E"
        pickfile = open(filename, 'rb')
        E = pickle.load(pickfile)
        pickfile.close()
        filename = path + ".data#V"
        pickfile = open(filename, 'rb')
        V = pickle.load(pickfile)
        pickfile.close()
        return E, V

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
        self.edc = len(self.V) + len(self.E)
        if u not in self.EGO:
            self.EGO[u] = self.egonetwork(self.E, self.V, u)
        if v not in self.EGO:
            self.EGO[v] = self.egonetwork(self.E, self.V, v)
        if len(self.EGO[u]) < len(self.EGO[v]):
            tempu, tempv = u, v
            u, v = tempv, tempu

        Vu = list(self.EGO[u].keys())
        Vu.sort()
        Vv = list(self.EGO[v].keys())
        Vv.sort()
        Vv += list(range(len(Vv) - len(Vu), 0))
        f = {}
        self.DFS(0, {}, len(Vu), f, Vu, Vv, u, v)
        return self.edc

    def DFS(self, level, visited, n, f, Vu, Vv, u, v):
        if level == n:
            I = {}
            I_reverse = {}
            for item in range(len(Vu)):
                I[Vu[f[item]]] = Vv[item]
                I_reverse[Vv[item]] = [Vu[f[item]]]
            self.EDC_INAC(self.EGO[u], self.EGO[v], I, I_reverse)
        for i in range(len(Vu)):
            if i not in visited:
                visited[i] = True
                f[level] = i
                self.DFS(level + 1, visited, n, f, Vu, Vv, u, v)
                del (visited[i])

    def node_label(self, id):
        if id > 0:
            return self.L[id]
        else:
            return -1

    def ego_list(self, v, id):
        if id > 0:
            return self.EGO[v][id]
        else:
            return []

    def neighour(self, v, V):
        results = set()
        for edge in V[v]:
            temp = set(self.E[edge])
            results |= temp
        return list(results)

    def EDC_INAC(self, EGO1, EGO2, I, I_reverse):
        EDC = 0
        for key, value in I.items():
            if self.node_label(key) != self.node_label(value):
                EDC += 1

        if EDC >= self.edc: return

        for node in EGO1:
            for hedge in EGO1[node]:
                for node2 in self.E[hedge]:
                    if I[node2] not in self.E[hedge]:
                        EDC += 1

        for node in EGO2:
            for hedge in EGO2[node]:
                for node2 in self.E[hedge]:
                    if I_reverse[node2] not in self.E[hedge]:
                        EDC += 1

        if EDC >= self.edc:
            return
        else:
            self.edc = EDC
            print("EDC updated to:" + str(EDC))

    def HGED_BFS(self, u, v):
        self.edc = len(self.V) + len(self.E)
        if u not in self.EGO:
            self.EGO[u] = self.egonetwork(self.E, self.V, u)
        if v not in self.EGO:
            self.EGO[v] = self.egonetwork(self.E, self.V, v)
        if len(self.EGO[u]) < len(self.EGO[v]):
            tempu, tempv = u, v
            u, v = tempv, tempu
        Vu = list(self.EGO[u].keys())
        Vu.sort()
        Vv = list(self.EGO[v].keys())
        Vv.sort()
        Vv += list(range(len(Vv) - len(Vu), 0))

        for node in Vu:
            edgeset1 = set()
            for edgelist in self.EGO[u][node]:
                edgeset1 |= set(edgelist)
        for node in Vv:
            edgeset2 = set()
            for edgelist in self.EGO[v][node]:
                edgeset2 |= set(edgelist)
        Eu = list(edgeset1)
        Eu.sort()
        Ev = list(edgeset1)
        Ev.sort()
        E_add = list(range(-abs(len(Eu) - len(Ev)), 0))
        if len(Eu) >= len(Ev):
            Ev += E_add
        else:
            Eu += E_add

        self.edc = 1000

        Q = [[0, {}, {}]]
        while len(Q) > 0:
            [level, visited, f] = Q.pop()
            for x in range(level, len(Vu) + len(Eu)):
                if x not in visited:
                    Cx = 1
                    if x + 1 == len(Vu) + len(Eu):
                        pass
                    else:
                        visited[level] = True
                        f[level] = x
                        self.edc += Cx
                        Q.append([level + 1, visited, f])
        return self.edc

    def EDC(self, EGO1, EGO2, I, I_reverse):
        EDC = 0
        for key, value in I.items():
            if self.node_label(key) != self.node_label(value):
                EDC += 1

        if EDC >= self.edc: return

        for node in EGO1:
            for hedge in EGO1[node]:
                for node2 in self.E[hedge]:
                    if I[node2] not in self.E[hedge]:
                        EDC += 1

        for node in EGO2:
            for hedge in EGO2[node]:
                for node2 in self.E[hedge]:
                    if I_reverse[node2] not in self.E[hedge]:
                        EDC += 1

        if EDC >= self.edc:
            return
        else:
            self.edc = EDC
            print("EDC updated to:" + str(EDC))

    def JS(self, u, v):
        if u not in self.EGO:
            self.EGO[u] = self.egonetwork(self.E, self.V, u)
        if v not in self.EGO:
            self.EGO[v] = self.egonetwork(self.E, self.V, v)
        set1 = set(self.EGO[u].keys())
        set2 = set(self.EGO[v].keys())
        return len(set1 & set2) / len(set1 | set2)

    def HEP_DFS(self, lambdax, tau):
        SetS = []
        for u in self.V:
            S = [u]
            Q = [u]
            while len(Q) > 0:
                v = Q.pop()
                for w in self.neighour(v, self.V):
                    if w not in S:
                        if v > w:
                            v_rerank, w_rerank = w, v
                        else:
                            v_rerank, w_rerank = v, w
                        if (v_rerank, w_rerank) not in self.D:
                            self.D[(v_rerank, w_rerank)] = self.HGED_HEU(v_rerank, w_rerank)
                        if self.D[(v_rerank, w_rerank)] >= tau:
                            S.append(w)
                            Q.append(w)
            if len(S) > 1:
                SetS.append(S)

        SetS_new = []
        for S in SetS:
            for v in S:
                for w in S:
                    remove_S = []
                    if w != v and w not in self.neighour(v, self.V):
                        if v > w:
                            v_rerank, w_rerank = w, v
                        else:
                            v_rerank, w_rerank = v, w
                        if (v_rerank, w_rerank) not in self.D:
                            self.D[(v_rerank, w_rerank)] = self.HGED_HEU(v_rerank, w_rerank)
                        if self.D[(v_rerank, w_rerank)] >= tau * lambdax:
                            remove_S.append(w)
                tempSet = set(S) - set(remove_S)
                SetS_new.append(tempSet)
        return SetS_new

    def HEP_BFS(self, lambdax, tau):
        SetS = []
        for u in self.V:
            S = [u]
            Q = [u]
            while len(Q) > 0:
                v = Q.pop()
                for w in self.neighour(v, self.V):
                    if w not in S:
                        if v > w:
                            v_rerank, w_rerank = w, v
                        else:
                            v_rerank, w_rerank = v, w
                        if (v_rerank, w_rerank) not in self.D:
                            self.D[(v_rerank, w_rerank)] = self.HGED_BFS(v_rerank, w_rerank)
                        if self.D[(v_rerank, w_rerank)] >= tau:
                            S.append(w)
                            Q.append(w)
            if len(S) > 1:
                SetS.append(S)

        SetS_new = []
        for S in SetS:
            for v in S:
                for w in S:
                    remove_S = []
                    if w != v and w not in self.neighour(v, self.V):
                        if v > w:
                            v_rerank, w_rerank = w, v
                        else:
                            v_rerank, w_rerank = v, w
                        if (v_rerank, w_rerank) not in self.D:
                            self.D[(v_rerank, w_rerank)] = self.HGED_BFS(v_rerank, w_rerank)
                        if self.D[(v_rerank, w_rerank)] >= tau * lambdax:
                            remove_S.append(w)
                tempSet = set(S) - set(remove_S)
                SetS_new.append(tempSet)
        return SetS_new

    def HEP_JS(self, lambdax, tau):
        SetS = []
        for u in self.V:
            S = [u]
            Q = [u]
            while len(Q) > 0:
                v = Q.pop()
                for w in self.neighour(v, self.V):
                    if w not in S:
                        if v > w:
                            v_rerank, w_rerank = w, v
                        else:
                            v_rerank, w_rerank = v, w
                        if (v_rerank, w_rerank) not in self.D:
                            self.D[(v_rerank, w_rerank)] = self.JS(v_rerank, w_rerank)
                        if self.D[(v_rerank, w_rerank)] >= 1 / tau:
                            S.append(w)
                            Q.append(w)
            if len(S) > 1:
                SetS.append(S)

        SetS_new = []
        for S in SetS:
            for v in S:
                for w in S:
                    remove_S = []
                    if w != v and w not in self.neighour(v, self.V):
                        if v > w:
                            v_rerank, w_rerank = w, v
                        else:
                            v_rerank, w_rerank = v, w
                        if (v_rerank, w_rerank) not in self.D:
                            self.D[(v_rerank, w_rerank)] = self.JS(v_rerank, w_rerank)
                        if self.D[(v_rerank, w_rerank)] <= 1.0 / tau / lambdax:
                            remove_S.append(w)
                tempSet = set(S) - set(remove_S)
                SetS_new.append(tempSet)
        return SetS_new


if __name__ == '__main__':
    HG = HyperG("HS")
    # HG = HyperG("PS")
    HG.HGED_HEU(10, 11)
