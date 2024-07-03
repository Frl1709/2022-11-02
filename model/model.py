import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listGenre = []

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}
        self.connesse = []

        self.bestPath = []
        self.bestCost = 0

        self.loadGenre()

    def getBestPath(self, dTot):
        self.bestPath = []
        self.bestCost = 0
        nodi = []
        for track in self.connesse[0]:
            nodi.append(track)

        for n in nodi:
            parziale = [n]
            rimanenti = copy.deepcopy(nodi)

            self._ricorsione(parziale, rimanenti, dTot)

    def _ricorsione(self, parziale, rimanenti, dTot):
        rimanenti.remove(parziale[-1])
        if len(rimanenti) == 0 or self.getDurata(parziale) == dTot:
            if len(parziale) > len(self.bestPath):
                self.bestPath = copy.deepcopy(parziale)
                return

        for n in rimanenti:
            durata = self.getDurata(parziale)
            if n not in parziale and durata + n.Milliseconds <= dTot:
                parziale.append(n)
                self._ricorsione(parziale, rimanenti, dTot)
                parziale.pop()


    def getDurata(self, lista):
        durata = 0
        for t in lista:
            durata += t.Milliseconds

        return durata

    def loadGenre(self):
        self.listGenre = DAO.getGenre()

    def buildGraph(self, genere, dMin, dMax):
        self.graph.clear()
        self.nodes = DAO.getNodes(genere, dMin, dMax)
        self.graph.add_nodes_from(self.nodes)
        for n in self.nodes:
            self.idMap[n.TrackId] = n

        self.edges = DAO.getEdge(genere, dMin, dMax, self.idMap)
        self.graph.add_edges_from(self.edges)

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getConnessa(self):
        self.connesse = []
        """archi = []
        c = list(nx.connected_components(self.graph))
        for p in c:
            playlist = 0
            for i in p:
                vicini = self.graph[i]
                for j in vicini:
                    if (i, j) not in archi or (j, i) not in archi and self.graph[i][j] is not None:
                        archi.append((i, j))
            self.connesse.append((len(p), playlist))"""
        c = list(nx.connected_components(self.graph))
        for p in c:
            self.connesse.append(p)
        self.connesse = sorted(self.connesse, key=lambda x: len(x), reverse=True)
        print(self.connesse)
        #return self.connesse
