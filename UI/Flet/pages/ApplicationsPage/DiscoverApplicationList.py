import flet as ft
from DATA.commands import get_search_output, search, Search_Args, get_list_output, list_installed, List_Args, show, get_show_output, Show_Args
import threading
import copy

from components.SearchBox import SearchBox
from components.ApplicationListItem import ApplicationListItem
from components.ApplicationsInstallDialog import application_install_dialog
from components.ApplicationExporter import ApplicationExporter

from store import set_discover_page_selected

class DiscoverApplicationList(ft.UserControl):

    def did_mount(self):
        self.is_search_running = False

    def will_unmount(self):
        self.is_search_running = False

    def on_search_submit(self, search_input, callback):
        self.enable_loading_indicator()
        self.is_search_running = True
        self.th = threading.Thread(
            target=self.get_application_list, args=(search_input, callback,), daemon=True)
        self.th.start()

    def get_application_list(self, search_input, callback):
        if (self.is_search_running):
            data = get_search_output(
                search(Search_Args(search_input, None, None, None, False)))
            # print(data)
            self.is_search_running = False
            # print("search_input", search_input)
            self.populate_table(data)
            callback()

    def enable_loading_indicator(self):
        self.list_view.controls.clear()
        self.list_view.controls.append(self.loading_indicator)
        self.update()
    
    def populate_table(self, data):
        self.list_view.controls.clear()
        for elem in data:
                self.list_view.controls.append(
                    ApplicationListItem(copy.deepcopy(elem), True, self.get_checked_applications))
        self.update()

    def get_checked_applications(self):
        apps = []
        for item in self.list_view.controls:
            if item.get_selection_state():
                apps.append({"name": item.application_information["name"], "id": item.application_information["id"], "source": "winget"})
        set_discover_page_selected(apps)

        


        

    def build(self):
        self.application_install_dialog = application_install_dialog

        self.list_header = ft.ListView(
            controls=[ft.Row(
            [
                ft.Container(width=300, content=ft.Text("Application name", color=ft.colors.PRIMARY, size=15, weight=ft.FontWeight.BOLD), margin=ft.margin.only(left=42)),
                ft.Container(width=300, content=ft.Text("Application ID", color=ft.colors.PRIMARY, size=15, weight=ft.FontWeight.BOLD)),
                ft.Container(width=150, content=ft.Text("Latest version", color=ft.colors.PRIMARY, size=15, weight=ft.FontWeight.BOLD)),
                ft.Container(width=150, content=ft.Text("Source", color=ft.colors.PRIMARY, size=15, weight=ft.FontWeight.BOLD)),
            ])],
            padding=ft.padding.only(top=10)
        )

        self.list_view = ft.ListView(
            spacing=10, padding=ft.padding.symmetric(vertical=10))
        
        self.loading_indicator = ft.Container(ft.ProgressRing(width=20, height=20, stroke_width=2), height=300, alignment=ft.Alignment(0, 0))

        self.list_view.controls.append(ft.Container(ft.Text("Search for applications to install...", size=20, color=ft.colors.SECONDARY), height=300, alignment=ft.Alignment(0, 0)))

        self.search_field = SearchBox( on_click=self.on_search_submit)

        self.application_exporter = ApplicationExporter("discover_page_selected")

        return ft.Container(
            ft.Column([
                ft.Row([self.search_field, self.application_install_dialog, self.application_exporter], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), 
                self.list_header, 
                ft.Container(self.list_view, height=580, )])
        )
    