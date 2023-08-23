import flet as ft
from store import router_model
from mopyx import model, render, render_call, action
from DATA.commands import get_search_output, search, Search_Args, get_list_output, list_installed, List_Args, show, get_show_output, Show_Args

from pages.ApplicationsPage.ApplicationsPage import ApplicationsPage
from pages.SettingsPage.SettingsPage import SettingsPage


class NavDrawer(ft.UserControl):

    def on_change_handler(self, e):
        if (e.control.selected_index == 0):
            router_model.active_route = router_model.HOME_ROUTE
        elif (e.control.selected_index == 1):
            router_model.active_route = router_model.SETTINGS_ROUTE
        print("Selected destination:", e.control.selected_index)

    @render
    def update_route(self):
        if (router_model.active_route == router_model.HOME_ROUTE):
            self.page_container.content = ApplicationsPage()
        elif (router_model.active_route == router_model.SETTINGS_ROUTE):
            self.page_container.content = SettingsPage()
        self.update()

    def did_mount(self):
        self.update_route()

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
                    icon_content=ft.Container(
                        ft.Text("Home", color=ft.colors.SECONDARY)),
                    selected_icon_content=ft.Container(
                        ft.Text("Home", color=ft.colors.PRIMARY, size=15))
                ),
                ft.NavigationRailDestination(
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
    page.title = "WinMirror"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 0
    page.window_resizable = True
    page.add(NavDrawer())


ft.app(target=main)
