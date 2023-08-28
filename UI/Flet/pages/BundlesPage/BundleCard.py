import flet as ft
from DATA.commands import delete_bundle, Delete_Args, get_bundle, Get_Bundle_Args
import threading
from store import set_bundles


class DeleteConfirmation(ft.UserControl):

    def __init__(self, on_confirm, on_reject):
        super().__init__()
        self.on_confirm = on_confirm
        self.on_reject = on_reject

    def will_unmount(self):
        self.close_dialog()

    def open_dialog(self):
        self.dialog.open = True
        self.update()

    def close_dialog(self):
        self.dialog.open = False
        self.update()

    def build(self):
        self.text = ft.Text("Are you sure you want to delete this bundle?")
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
        self.bundle_info = bundle_info
        super().__init__()

    def did_mount(self):
        self.is_mounted = True
    
    def will_unmount(self):
        self.is_mounted = False

    def on_delete(self):
        self.delete_th = threading.Thread(
            target=self.delete, args=(), daemon=True)
        self.delete_th.start()

    def delete(self):
        if self.is_mounted:
            data = delete_bundle(Delete_Args(self.bundle_info["id"]))
            if data["status"] == "success":
                bundles = get_bundle(Get_Bundle_Args(all=True))
                self.delte_confirmation_modal.close_dialog()
                set_bundles(bundles)
            else: 
                self.delte_confirmation_modal.close_dialog()

    def build(self):

        self.title_box = ft.Container(ft.Text(f'{self.bundle_info["title"]}', size=20))
        self.description_box = ft.Container(ft.Text(f'Description: {self.bundle_info["description"]}'))

        self.number_of_winget_applications = len(self.bundle_info["apps"]["winget"])
        self.number_of_readonly_applications = len(self.bundle_info["apps"]["readonly"])

        self.no_winget_apps_box = ft.Container(ft.Text(f'Winget applications: {self.number_of_winget_applications}'))
        self.no_readonly_apps_box = ft.Container(ft.Text(f'Readonly applications: {self.number_of_readonly_applications}'))

        self.action_buttons = ft.Container(
            ft.Row(controls=[
                ft.IconButton(icon=ft.icons.EDIT),
                ft.IconButton(icon=ft.icons.CONTROL_POINT_DUPLICATE),
                ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: self.delte_confirmation_modal.open_dialog()),
            ],
            alignment=ft.MainAxisAlignment.END),
        )

        self.delte_confirmation_modal = DeleteConfirmation(
            on_confirm=lambda: self.on_delete(),
            on_reject=lambda: self.delte_confirmation_modal.close_dialog(),
        )

        self.content = ft.Column(
            controls=[
                self.title_box,
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
                )
        )

        return self.card

