import flet as ft
from DATA.commands import get_search_output, search, Search_Args, get_list_output, list_installed, List_Args, show, get_show_output, Show_Args, install, Install_Args, get_install_output
import threading
from components.ApplicationsInstallDialog import ApplicationInstallDialog




class ApplicationInformationDialog(ft.UserControl):
    def __init__(self, application_information: dict):
        super().__init__()
        self.application_information = application_information
        self.id_app_info_fetched = False

    def did_mount(self):
        self.getting_app_info = False
        self.installing = False
        self.close_dialog()

    def will_unmount(self):
        self.getting_app_info = False

    def get_app_info(self):
        if self.getting_app_info and not self.id_app_info_fetched:
            data = get_show_output(show(Show_Args(id = self.application_information["id"])))
            self.getting_app_info = False
            self.id_app_info_fetched = True
            self.populate_dialog(data)

    def populate_dialog(self, content: list[str]):

        # self.main_container.content = ft.Text(content)
        self.main_container.content = ft.ListView(controls=list(map(lambda line: ft.Text(line), content)))
        
        self.update()

    def open_dialog(self):
        self.dialog.open=True
        self.getting_app_info = True
        self.show_th = threading.Thread(
            target=self.get_app_info, args=(), daemon=True)
        self.show_th.start()
        self.update()
    
    def close_dialog(self):
        self.dialog.open=False
        self.update()
    
    def on_install(self):
        self.installing = True
        self.render_install_visual_indicator()
        self.install_th = threading.Thread(
            target=self.install, args=(), daemon=True)
        self.install_th.start()

    def render_install_visual_indicator(self):
         self.title.content = ft.Column([ft.Text(f'Installing {self.application_information["id"]} ...'), ft.ProgressBar()])
         self.install_button.disabled = True
         self.update()

    def reset_install_visual_indicator(self):
         self.title.content = ft.Text("Application details")
         self.install_button.disabled = False
         self.update()

    def install(self):
        if self.installing:
            data = get_install_output(install(Install_Args(id=self.application_information["id"], source="winget")))
            self.install_dialog.open_modal(data)
            self.reset_install_visual_indicator()


    def build(self):

        self.install_dialog = ApplicationInstallDialog()

        self.main_container = ft.Container(
            ft.ProgressRing(width=20, height=20, stroke_width=2),  alignment=ft.Alignment(0, 0),
            height=600,
            width=600,
            )
        
        self.title = ft.Container(ft.Text("Application details"))

        self.cancel_button = ft.TextButton("Cancel", on_click=lambda e: self.close_dialog())
        self.install_button = ft.TextButton("Install", on_click=lambda e: self.on_install())

        self.dialog = ft.AlertDialog(
            modal=True,
            title = self.title,
            content = ft.Row([self.install_dialog, self.main_container]),
            actions = [
                self.cancel_button,
                self.install_button
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return self.dialog