import flet as ft
from store import route_to, ROUTES, observe_route



from pages.ApplicationsPage.ApplicationsPage import ApplicationsPage
from pages.SettingsPage.SettingsPage import SettingsPage
from pages.BundlesPage.BundlesPage import BundlesPage
from api import Global_Data_Fetching




class NavDrawer(ft.UserControl):

    def on_change_handler(self, e):
        if (e.control.selected_index == 0):
            route_to(ROUTES.HOME_ROUTE)
        elif (e.control.selected_index == 1):
            route_to(ROUTES.BUNDLES_ROUTE)
        elif (e.control.selected_index == 2):
            route_to(ROUTES.SETTINGS_ROUTE)

    def update_route(self, new_route):
        if (new_route == ROUTES.HOME_ROUTE):
            self.page_container.content = ApplicationsPage()
        elif (new_route == ROUTES.SETTINGS_ROUTE):
            self.page_container.content = SettingsPage()
        elif (new_route == ROUTES.BUNDLES_ROUTE):
            self.page_container.content = BundlesPage()
        self.update()

    def did_mount(self):
        observe_route(self.update_route)
        self.update_route(ROUTES.HOME_ROUTE)

    def build(self):
        self.page_container = ft.Container(
            ft.Text('Loading page'))
        self.rail = ft.Container(ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            width=100,
            bgcolor=ft.colors.ON_SECONDARY,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    padding=10,
                    icon = ft.icons.HOME,
                    label_content=ft.Text("Home"),
                ),
                ft.NavigationRailDestination(
                    padding=10,
                    icon = ft.icons.ALL_INBOX_ROUNDED,
                    label_content=ft.Text("Bundles"),

                ),
                ft.NavigationRailDestination(
                    padding=10,
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],

            on_change=self.on_change_handler,
        ), height=760)
        self.content = ft.Row(
            [
                self.rail,
                ft.Container(
                    self.page_container, bgcolor=ft.colors.SECONDARY_CONTAINER,  height=760, alignment=ft.Alignment(-1, -1), expand=True)
            ],
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )
        return self.content


def main(page: ft.Page):
    page.theme_mode = "dark"
    page.theme = ft.theme.Theme(color_scheme_seed='blue')
    page.title = "WinMirror"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0
    page.window_resizable = True
    page.window_resizable = False # to be activated when building the app 
    page.window_maximizable = False

    Global_Data_Fetching.get_bundles()

    page.add(NavDrawer())


ft.app(target=main, assets_dir="assets")
