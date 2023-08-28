import flet as ft
from DATA.commands import get_search_output, search, Search_Args, get_list_output, list_installed, List_Args, show, get_show_output, Show_Args
import threading
from components.ApplicationsInstallDialog import application_install_dialog

class ApplicationInformationDialog(ft.UserControl):
    def __init__(self, application_information: dict):
        super().__init__()
        self.application_information = application_information
        self.is_data_fetched = False

    def did_mount(self):
        self.is_fetch_running = False
        self.close_dialog()
        self.close_dialog()
        self.close_dialog()

    def will_unmount(self):
        self.is_fetch_running = False

    def get_app_info(self):
        if self.is_fetch_running and not self.is_data_fetched:
            data = get_show_output(show(Show_Args(self.application_information["name"], self.application_information["id"], None, None, None)))
            # print("application info for: ", self.application_information["name"], data)
            self.is_fetch_running = False
            self.is_data_fetched = True
            self.populate_dialog(data)

    def populate_dialog(self, content: list[str]):

        # self.main_container.content = ft.Text(content)
        self.main_container.content = ft.ListView(controls=list(map(lambda line: ft.Text(line), content)))
        
        self.update()

    def open_dialog(self):
        self.dialog.open=True
        self.is_fetch_running = True
        self.th = threading.Thread(
            target=self.get_app_info, args=(), daemon=True)
        self.th.start()
        self.update()
    
    def close_dialog(self):
        self.dialog.open=False
        self.update()
    
    def on_install(self):
        self.close_dialog()
        application_install_dialog.open_dialog(self.application_information)
        application_install_dialog.update()

        
        
    def build(self):

        self.main_container = ft.Container(
            ft.ProgressRing(width=20, height=20, stroke_width=2),  alignment=ft.Alignment(0, 0),
            height=600,
            width=600,
            )

        self.dialog = ft.AlertDialog(
            title = ft.Text("Application details"),
            content = self.main_container,
            actions = [
                ft.TextButton("Cancel", on_click=lambda e: self.close_dialog()),
                ft.TextButton("Install", on_click=lambda e: self.on_install())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return self.dialog