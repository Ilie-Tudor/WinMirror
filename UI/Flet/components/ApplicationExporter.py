import flet as ft
from store import get_bundles, observe_bundles, observe
from DATA.commands import add_application_to_bundle, Add_Application_To_Bundle_Args
import threading
from api import Global_Data_Fetching
from components.Toast import Toast

class ApplicationExporter(ft.UserControl):
    def __init__(self, application_list_state_name):
        super().__init__()
        self.application_list_state_name = application_list_state_name

    def did_mount(self):
        self.active_bundle_id = None
        self.app_list = []
        self.is_mounted = True
        self.populate_bundles_list(get_bundles())
        self.unsubscribe_bundles = observe_bundles(self.populate_bundles_list)
        self.unsubsctibe_app_list = observe(self.application_list_state_name, self.populate_app_list)

    def will_unmount(self):
        self.unsubscribe_bundles()
        self.unsubsctibe_app_list()
        self.is_mounted = False

    def populate_bundles_list(self, bundles):
        if(self.is_mounted):
            self.drop_down.options.clear()
            for bundle in bundles:
                self.drop_down.options.append(ft.dropdown.Option(key=bundle["id"], text=bundle["title"]))
            self.update()

    def populate_app_list(self, apps):
        self.app_list = apps
        self.enabled_handler()

    def dropdown_changed(self, e):
        self.active_bundle_id = self.drop_down.value
        self.enabled_handler()

    def enabled_handler(self):
        if self.active_bundle_id != None and len(self.app_list)>0:
            self.submit_button.disabled = False
        else:
            self.submit_button.disabled = True
        self.update()

    def on_submit(self):
        self.th = threading.Thread(
            target=self.on_export, args=(), daemon=True)
        self.th.start()
        
    def on_export(self):
        unsuccessful_ids = []
        for app in self.app_list:
            app_content = { key:val
                            for key, val
                            in app.items()
                            if key!="source" }
            data = add_application_to_bundle(Add_Application_To_Bundle_Args(
                self.active_bundle_id,
                "winget" if app["source"] != "" else "readonly",
                app_content
                ))
            if(not data["status"]=="success"):
                unsuccessful_ids.append(app["id"])
        if len(unsuccessful_ids)!=0:
            self.toast.open(f'The following apps couldn\'t be added {unsuccessful_ids}', variant="error")
        else:
            self.toast.open("Apps added to bunddle!")
        Global_Data_Fetching.get_bundles()


    def build(self):

        self.toast = Toast()

        self.submit_button = ft.IconButton(ft.icons.CHECK, bgcolor=ft.colors.ON_SECONDARY, disabled=True, on_click=lambda e: self.on_submit())
        
        self.drop_down = ft.Dropdown(
            on_change=self.dropdown_changed,
            width=200,
            label="Add apps to bundle: ",
            dense=True,
            border_color=ft.colors.PRIMARY, 
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            options=[
                
            ]
        )

        return ft.Container(
            ft.Row([self.toast, self.drop_down, self.submit_button]),
            margin=ft.margin.only(top=15)
        )