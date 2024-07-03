import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP - Esame del 14/09/2022"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None
        self.txtMax = None
        self.txtDTot = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP - Esame del 14/09/2022", color="red", size=24)
        self._page.controls.append(self._title)

        #ROW1
        self.ddGenere = ft.Dropdown(label="Genere")
        self.txtMin = ft.TextField(label="Min")
        self.txtMax = ft.TextField(label="Max")
        self.txtDTot = ft.TextField(label="dTot")
        row1 = ft.Row([self.ddGenere, self.txtMin, self.txtMax, self.txtDTot], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._controller.fillDD()

        #ROW2
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnPlaylist = ft.ElevatedButton(text="La mia playlist",
                                                 on_click=self._controller.handlePlaylist)

        row2 = ft.Row([self._btnCreaGrafo, self._btnPlaylist], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()