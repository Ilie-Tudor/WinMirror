import flet as ft
from DATA.commands import delete_bundle, Delete_Args, get_bundle, Get_Bundle_Args, export_bundle, Export_Bundle_Args
import threading
from store import set_bundles
from components.Toast import Toast
from pages.BundlesPage.BundleInfo import BundleInfo
import time

class DeleteConfirmation(ft.UserControl):

    def __init__(self, on_confirm, on_reject, bundle_name):
        super().__init__()
        self.on_confirm = on_confirm
        self.on_reject = on_reject
        self.bundle_name = bundle_name

    def will_unmount(self):
        self.close_dialog()

    def open_dialog(self):
        self.dialog.open = True
        self.update()

    def close_dialog(self):
        self.dialog.open = False
        self.update()

    def build(self):
        self.text = ft.Text(f"Are you sure you want to delete the bundle '{self.bundle_name}'?")
        self.action_buttons = [
            ft.TextButton("Yes", on_click = lambda e: self.on_confirm()),
            ft.TextButton("No", on_click = lambda e: self.on_reject())
        ]

        self.dialog = ft.AlertDialog(
            content=self.text,
            actions=self.action_buttons,
            actions_alignment=ft.MainAxisAlignment.END
        )

        return self.dialog


class BundleCard(ft.UserControl):

    def __init__(self, bundle_info):
        super().__init__()
        self.bundle_info = bundle_info
        def export_handler(result):
            print(result.path, self.bundle_info["id"])
        self.export_handdler = export_handler

    def did_mount(self):
        self.is_mounted = True
    
    def will_unmount(self):
        self.is_mounted = False

    def on_delete(self):
        self.delte_confirmation_modal.close_dialog()
        self.delete_th = threading.Thread(
            target=self.delete, args=(), daemon=True)
        self.delete_th.start()


    def delete(self):
        if self.is_mounted:
            data = delete_bundle(Delete_Args(self.bundle_info["id"]))
            if data["status"] == "success":
                bundles = get_bundle(Get_Bundle_Args(all=True))
                self.delte_confirmation_modal.close_dialog()
                # this time.sleep solves a bug with the modal not closing when deleting element, must investigate
                time.sleep(0.2)
                set_bundles(bundles)
            else: 
                pass        

    def on_export(self, result):
        if result.path is not None:
            self.import_th = threading.Thread(
                target=self.export_bundle, args=(result.path,), daemon=True)
            self.import_th.start()

    def export_bundle(self, filePath):
        data = export_bundle(Export_Bundle_Args(filePath, self.bundle_info["id"]))
        if data["status"] == "success":
            self.toast.open("Bundle exported successfuly!")

    def build(self):

        self.toast = Toast()

        self.export_picker = ft.FilePicker(on_result=self.on_export)

        self.title_box = ft.Container(ft.Text(f'{self.bundle_info["title"]}', size=20))
        self.description_box = ft.Container(ft.Text(f'Description: {self.bundle_info["description"]}'))

        self.number_of_winget_applications = len(self.bundle_info["apps"]["winget"])
        self.number_of_readonly_applications = len(self.bundle_info["apps"]["readonly"])

        self.no_winget_apps_box = ft.Container(ft.Text(f'Winget applications: {self.number_of_winget_applications}'))
        self.no_readonly_apps_box = ft.Container(ft.Text(f'Readonly applications: {self.number_of_readonly_applications}'))

        self.action_buttons = ft.Container(
            ft.Row(controls=[
                ft.IconButton(icon=ft.icons.SCREEN_SHARE
                               ,on_click=lambda e: self.export_picker.save_file()
                            ),
                ft.IconButton(icon=ft.icons.EDIT),
                ft.IconButton(icon=ft.icons.CONTROL_POINT_DUPLICATE),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: self.delte_confirmation_modal.open_dialog()),
            ],
            alignment=ft.MainAxisAlignment.END),
        )

        self.delte_confirmation_modal = DeleteConfirmation(
            on_confirm=lambda: self.on_delete(),
            on_reject=lambda: self.delte_confirmation_modal.close_dialog(),
            bundle_name=self.bundle_info["title"]
        )

        self.bundle_info_modal = BundleInfo(self.bundle_info["id"])

        self.content = ft.Column(
            controls=[
                ft.Row([self.title_box, self.export_picker, self.bundle_info_modal, self.toast]),
                ft.Divider(color=ft.colors.PRIMARY, height=4),
                ft.ListView(controls = [
                        self.description_box,
                        self.no_winget_apps_box,
                        self.no_readonly_apps_box
                    ], height=135),
                self.action_buttons,
                self.delte_confirmation_modal
            ]
        )

        self.card = ft.Card(
            elevation=15.0,
            color=ft.colors.SECONDARY_CONTAINER,
            surface_tint_color = ft.colors.PRIMARY,
            content=ft.Container(
                    content = self.content,
                    padding= ft.padding.all(10)
                , on_click=lambda e: self.bundle_info_modal.open_dialog())
        )

        return self.card

