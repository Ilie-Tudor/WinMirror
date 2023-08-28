import flet as ft
import threading
from DATA.commands import create_bundle, Create_Bundle_Args, get_bundle, Get_Bundle_Args
from store import set_bundles, get_bundles

class NewBundleDialog(ft.UserControl):

    def open_dialog(self):
        self.modal.open = True
        self.update()
    
    def close_dialog(self):
        self.modal.open = False
        self.update()
    
    def on_add(self):
        self.th = threading.Thread(
            target=self.create_new_bundle, args=(), daemon=True)
        self.th.start()

    def on_error(self, message):
        self.error_message.value = message
        self.update()
    
    def clear_error(self):
        self.error_message.value = " "
        self.update()
    
    def create_new_bundle(self):
        data = create_bundle(Create_Bundle_Args(self.title_field.value, self.description_field.value))
        if data["status"] == "success":
            self.clear_error()
            bundles = get_bundle(Get_Bundle_Args(all=True))
            set_bundles(bundles)
            self.close_dialog()
        else:
            self.on_error(data["message"])
            
        

    def build(self):

        self.error_message = ft.Text(" ", color="red")

        self.title_field = ft.TextField(label="Title",border_color=ft.colors.PRIMARY, 
                label_style=ft.TextStyle(color=ft.colors.SECONDARY),
                dense=True)

        self.description_field = ft.TextField(label="Description",border_color=ft.colors.PRIMARY, 
                label_style=ft.TextStyle(color=ft.colors.SECONDARY),
                dense=True)

        self.add_button = ft.ElevatedButton(text = "Add Bundle", on_click=lambda e: self.on_add())

        self.cancel_button = ft.TextButton("Cancel", on_click=lambda e:self.close_dialog())

        self.modal = ft.AlertDialog(
            content = ft.Container(ft.Column([
                self.title_field,
                self.description_field,
                self.error_message,
            ]), width=300, height=200), actions=[self.add_button,self.cancel_button], actions_alignment=ft.MainAxisAlignment.END
        )

        return self.modal


        

class NewBundleCard(ft.UserControl):

    def build(self):

        self.new_bundle_dialog = NewBundleDialog()

        self.card = ft.Container(ft.Card(
            elevation=15.0,
            color=ft.colors.SECONDARY_CONTAINER,
            surface_tint_color = ft.colors.PRIMARY,
            content=ft.Container(
                    content = ft.Icon(ft.icons.ADD, size=40),
                    padding= ft.padding.all(10),
                    alignment=ft.alignment.center,
                    width=150,
                    height=150
                )
            ),
        alignment=ft.alignment.center,
        on_click=lambda e: self.new_bundle_dialog.open_dialog()
        )

        return ft.Stack([self.new_bundle_dialog, self.card])
                

