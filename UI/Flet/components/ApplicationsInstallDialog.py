import flet as ft
from DATA.commands import Install_Args, install, get_install_output
import threading

class ApplicationInstallDialog(ft.UserControl):
    def __init__(self):
        super().__init__()
        

    def did_mount(self):
        self.is_fetch_running = False

    def will_unmount(self):
        self.is_fetch_running = False

    def get_app_info(self):
        if self.is_fetch_running:
            data = get_install_output(install(Install_Args(install_query=self.application_information["name"], 
                                                           id=self.application_information["id"], 
                                                           source="winget"
                                                           )))
            # print("application info for: ", self.application_information["name"], data)
            self.is_fetch_running = False
            self.populate_dialog(data)

    def populate_dialog(self, content: list[str]):

        # self.main_container.content = ft.Text(content)
        self.main_container.content = ft.ListView(controls=list(map(lambda line: ft.Text(line), content)))
        
        self.update()

    def open_dialog(self, application_information):
        self.application_information = application_information
        self.dialog.title = ft.Text(f'Installing {self.application_information["name"]} [id: {self.application_information["id"]}]')
        self.dialog.open=True
        self.is_fetch_running = True
        self.th = threading.Thread(
            target=self.get_app_info, args=(), daemon=True)
        self.th.start()
        self.update()
    
    def close_dialog(self):
        self.dialog.open=False
        self.main_container = ft.Container(
            ft.ProgressRing(width=20, height=20, stroke_width=2),  alignment=ft.Alignment(0, 0),
            height=600,
            width=600,
            )
        self.update()
        
        
    def build(self):

        self.main_container = ft.Container(
            ft.ProgressRing(width=20, height=20, stroke_width=2),  alignment=ft.Alignment(0, 0),
            height=600,
            width=600,
            )

        self.dialog = ft.AlertDialog(
            modal=True,
            content = self.main_container,
            actions = [
                ft.TextButton("Cancel", on_click=lambda e: self.close_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return self.dialog
    
application_install_dialog = ApplicationInstallDialog()

