import flet as ft
from DATA.commands import get_search_output, search, Search_Args, get_list_output, list_installed, List_Args, show, get_show_output, Show_Args
from functional import seq

from components.ApplicationInformationDialog import ApplicationInformationDialog

class ApplicationListItem(ft.UserControl):
    def __init__(self, application_information: dict, has_dialog=False, on_select = None):
        super().__init__()
        self.application_information = application_information
        self.information_dialog = ft.Text("")
        self.has_dialog = has_dialog
        self.on_select = lambda: print("selected")
        if on_select:
            self.on_select = on_select
        if has_dialog:
            self.information_dialog = ApplicationInformationDialog(application_information)

    def on_hover(self, e):
        e.control.bgcolor = ft.colors.ON_SECONDARY if e.data == "true" else None
        e.control.update()

    def on_click(self, e):
        self.information_dialog.open_dialog()

    def get_selection_state(self):
        return self.checkbox.value

    def build(self):
        self.checkbox = ft.Checkbox(value=False, on_change=lambda e: self.on_select())
        
        item_name = self.application_information["name"] if "name" in self.application_information else ""
        item_id = self.application_information["id"] if "id" in self.application_information else ""
        item_version = self.application_information["version"] if "version" in self.application_information else ""
        item_source = self.application_information["source"] if "source" in self.application_information else ""
        
        self.container_control = ft.Container(
            ft.Row(
                [
                    ft.Container(content=self.checkbox),
                    ft.Container(on_click=self.on_click if self.has_dialog else None, width=300, content=ft.Text(
                        f"{item_name}")),
                    ft.Container(width=300, content=ft.Text(
                        f"{item_id}")),
                    ft.Container(width=150, content=ft.Text(
                        f"{item_version}")),
                    ft.Container(width=150, content=ft.Text(
                        f"{item_source}")),
                    self.information_dialog
                ]
            ),
            on_hover=self.on_hover,
            border_radius=ft.border_radius.all(value=10)
        )

        return self.container_control