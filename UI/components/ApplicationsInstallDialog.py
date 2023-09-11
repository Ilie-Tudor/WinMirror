import flet as ft


class ApplicationInstallDialog(ft.UserControl):


    def open_modal(self, text):
        self.main_container.content = ft.Text(text)
        self.dialog.open = True
        self.update()

    def on_dismiss(self):
        self.dialog.open = False
        self.update()

    def build(self):

        self.main_container = ft.Container(ft.Text("Loading..."))

        self.dialog = ft.AlertDialog(
            title=ft.Text("Result"),
            content=self.main_container,
            on_dismiss = lambda e: self.on_dismiss()
        )

        return self.dialog
