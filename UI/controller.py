import copy
import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre = None

    def fillDD(self):
        generi = self._model.listGenre
        for g in generi:
            self._view.ddGenere.options.append(ft.dropdown.Option(data=g, text=g.Name, on_click=self.readChoice))

        self._view.update_page()

    def readChoice(self, e):
        if e.control.data is None:
            self._choiceGenre = None
        else:
            self._choiceGenre = e.control.data

    def handleCreaGrafo(self, e):
        try:
            dMin = int(self._view.txtMin.value) * 1000
            dMax = int(self._view.txtMax.value) * 1000
        except ValueError:
            self._view.create_alert("Inserire la durata minima e la durata massima")

        genere = self._choiceGenre
        self._model.buildGraph(genere.GenreId, dMin, dMax)
        nN, nE = self._model.getGraphSize()
        self._model.getConnessa()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))

        self._view.update_page()

    def handlePlaylist(self, e):
        try:
            dTot = int(self._view.txtDTot.value) * 60 * 1000
        except ValueError:
            self._view.create_alert("Inserire la durata totale")
        self._model.getBestPath(dTot)



