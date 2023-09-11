import flet as ft
import threading
from functional import seq
from DATA.commands import get_bundle, Get_Bundle_Args, install, Install_Args, get_install_output
from components.Toast import Toast
import time

class BulkInstallModal(ft.UserControl):

    def __init__(self):
        super().__init__()
    
    def close_dialog(self):
        self.modal.open = False
        self.main_container.controls.clear()
        self.update()

    def open_dialog(self, bundle_info):
        self.modal.open = True
        self.update()
        self.on_install_bulk(bundle_info)

    def install_app(self, app_id):
        data = install(Install_Args(id=app_id, source="winget"))
        return get_install_output(data)
    
    def install_bulk(self, bundle_info):
        self.apps = bundle_info["apps"]["winget"]
        for app in self.apps:
            self.title.content = ft.Column([ft.Text(f"Installing {app['id']}..."), ft.ProgressBar()])
            self.update()
            result = self.install_app(app["id"])
            self.main_container.controls.append(ft.Container(ft.Text(f'Result for {app["name"]}')))
            self.main_container.controls.append(ft.Container(ft.Text(result), margin=ft.margin.only(bottom=10)))
            self.update()

        self.title.content = ft.Column([ft.Text(f"Bulk install finished")])
        self.update()

    def on_install_bulk(self, bundle_info):
        self.th = threading.Thread(
            target=self.install_bulk, args=(bundle_info,), daemon=True)
        self.th.start()
            

    def build(self):
        
        self.title = ft.Container(ft.Column([ft.Text(""), ft.ProgressBar()]))

        self.action_buttons = [
            ft.TextButton("Close", on_click = lambda e: self.close_dialog())
        ]

        self.main_container = ft.ListView(controls=[], width=500, height=500)

        self.modal = ft.AlertDialog(
            modal = True,
            title = self.title,
            content = self.main_container,
            actions = self.action_buttons,
            actions_alignment=ft.MainAxisAlignment.END
        )

        return self.modal




class ApplicationItem(ft.UserControl):
    def __init__(self, app_info: dict):
        super().__init__()
        self.app_info = app_info

    def build(self):
        self.columns = self.app_info.keys()
        self.row = seq(self.columns).map(lambda column: ft.Container(ft.Text(self.app_info[column]), width=300)).to_list()
        self.item = ft.Container(ft.Row([ft.Container(ft.Text(""),width=2, bgcolor=ft.colors.PRIMARY), *self.row]),
                                 bgcolor=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                                 padding=ft.padding.all(2),
                                 border_radius=ft.border_radius.all(5)
                                 
                                 )
        return self.item


class BundleInfo(ft.UserControl):

    def __init__(self, bundle_id):
        super().__init__()
        self.bundle_id = bundle_id

    def get_bundle_info(self):
        data = get_bundle(Get_Bundle_Args(False, self.bundle_id))
        self.populate_dialog(data)

    def will_unmount(self):
        self.close_dialog()

    def open_dialog(self):
        self.th = threading.Thread(
            target=self.get_bundle_info, args=(), daemon=True)
        self.th.start()
        self.dialog.open = True
        self.update()

    def close_dialog(self):
        self.dialog.open = False
        self.update()
    
    def populate_dialog(self, data):
        self.bundle_info = data
        self.install_bulk_button.disabled=False

        self.bundle_title.content = ft.Text(data["title"], size=20, color=ft.colors.PRIMARY)
        self.bundle_description.content = ft.Text(data["description"])

        self.winget_apps.controls.clear()
        self.winget_apps.controls.append(ft.Container(ft.Text("Winget Apps", size=20), margin=ft.margin.only(top=40)))
        for app in data["apps"]["winget"]:
            self.winget_apps.controls.append(ApplicationItem(app))

        self.readonly_apps.controls.clear()
        self.readonly_apps.controls.append(ft.Container(ft.Text("Readonly Apps", size=20), margin=ft.margin.only(top=40)))
        for app in data["apps"]["readonly"]:
            self.readonly_apps.controls.append(ApplicationItem(app))
        self.update()

    def on_install_bulk(self):
        self.install_bulk_modal.open_dialog(self.bundle_info)

    def build(self):

        self.install_bulk_modal = BulkInstallModal()

        self.bundle_title = ft.Container(None, 
                                         margin=ft.margin.only(bottom=20), 
                                         border=ft.border.only(bottom=ft.BorderSide(3, ft.colors.PRIMARY)),
                                         padding=ft.padding.only(bottom=5)
                                         )
        self.bundle_description = ft.Container(ft.Text(""))
        self.winget_apps = ft.Column([], spacing=4)
        self.readonly_apps = ft.Column([], spacing=4)

        self.layout = ft.Container(ft.ListView(
            [self.bundle_title, self.bundle_description, self.winget_apps, self.readonly_apps, self.install_bulk_modal]
        ), width=800, height=500)

        self.close_button = ft.TextButton("Close", on_click = lambda e: self.close_dialog())
        self.install_bulk_button = ft.TextButton("Install Bulk", on_click = lambda e: self.on_install_bulk(), disabled=True)

        self.action_buttons = [
            self.close_button,
            self.install_bulk_button
        ]

        self.dialog = ft.AlertDialog(
            content=self.layout,
            actions=self.action_buttons,
            actions_alignment=ft.MainAxisAlignment.END,
            modal=True
        )

        return self.dialog
