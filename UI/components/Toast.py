import flet as ft



class Toast(ft.UserControl):

    def __init__(self,):
        super().__init__()
        self.toast =  self.toast = ft.SnackBar(
            content=ft.Text(" "), duration=3000, show_close_icon=True, close_icon_color=ft.colors.WHITE)
    
    def open(self, message, variant="success"):
        self.toast.content = ft.Text(message, color=ft.colors.WHITE)
        if variant == "success":
            self.toast.bgcolor = ft.colors.GREEN_400
        if variant == "error":
            self.toast.bgcolor = ft.colors.RED_400
        self.toast.open = True
        self.update()

    def build(self):
        return self.toast

