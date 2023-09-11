import flet as ft
import threading
from DATA.commands import info

class SettingsPage(ft.UserControl):

    def did_mount(self):
        self.th = threading.Thread(
            target=self.get_system_info, args=(), daemon=True)
        self.th.start()

    def get_system_info(self):
        data = info(None)
        self.content.content = ft.Text(data)
        self.update()

    def build(self):

        self.header = ft.Container(ft.Text("Winget information", size=20), margin=ft.margin.only(bottom=20))

        self.loading_indicator = self.loading_indicator = ft.Container(ft.ProgressRing(width=20, height=20, stroke_width=2), height=300, alignment=ft.Alignment(0, 0))

        self.content = ft.Container(self.loading_indicator)

        self.column_layout = ft.Column(controls=[
            self.header,
            self.content
        ])

        return ft.Container(
            self.column_layout,
            padding=ft.padding.only(left=15, right=15, top=10)
        )

