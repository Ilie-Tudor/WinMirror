import flet as ft
import threading
from DATA.commands import uninstall, Uninstall_Args, get_install_output
from store import observe_installed_page_selected, get_installed_page_selected

class UninstallModal(ft.UserControl):

    def did_mount(self):
        self.unobserve = observe_installed_page_selected(self.enable_handler)

    def will_unmount(self):
        self.unobserve()

    def on_uninstall(self):
        self.set_loading()
        self.th = threading.Thread(
            target=self.uninstall, args=(), daemon=True)
        self.uninstall()
    
    def uninstall(self):
        current_app = get_installed_page_selected()[0]
        data = get_install_output(uninstall(Uninstall_Args(id=current_app["id"])))
        self.dialog_content.content = ft.Text(data)
        self.set_done()
        self.update()
        pass

    def open_dialog(self):
        self.uninstall_dialog.open = True
        self.update()

    def close_dialog(self):
        self.uninstall_dialog.open = False
        self.update()
        self.dialog_content.content = ft.Text("")

    def set_loading(self):
        self.dialog_title.content = ft.Column([
                ft.Text("Uninstalling"),
                ft.ProgressBar()
            ])
        self.update()
        self.open_dialog()

    def set_done(self):
        self.dialog_title.content = ft.Column([
                ft.Text("Result")
            ])
        self.update()
    
    def enable_handler(self, applications_list):
        if len(applications_list)!=1:
            self.action_button.disabled = True
        else:
            self.action_button.disabled = False
        self.update()

    def build(self):

        self.action_button = ft.TextButton(on_click=lambda e: self.on_uninstall(), text="Uninstall", icon=ft.icons.DELETE, disabled=True)

        self.dialog_title = ft.Container(
            ft.Column([
                ft.Text("Uninstalling"),
                ft.ProgressBar()
            ])
        )

        self.dialog_content = ft.Container(ft.Text(""))

        self.close_button = ft.TextButton("Close", on_click=lambda e: self.close_dialog())

        self.uninstall_dialog = ft.AlertDialog(
            modal=True,
            title=self.dialog_title,
            content=self.dialog_content,
            actions=[self.close_button],
            actions_alignment=ft.MainAxisAlignment.END
        )

        return ft.Container(ft.Row([self.action_button,self.uninstall_dialog]), padding=ft.padding.only(top=15))


        