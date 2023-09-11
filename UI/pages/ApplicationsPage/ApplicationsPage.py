import flet as ft

from components.SearchBox import SearchBox
from components.ApplicationListItem import ApplicationListItem
from pages.ApplicationsPage.DiscoverApplicationList import DiscoverApplicationList
from pages.ApplicationsPage.InstalledApplicationsList import InstalledApplicationList


class ApplicationsPage(ft.UserControl):

    def build(self):

        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=200,
            divider_color=ft.colors.ON_SECONDARY,
            indicator_color=ft.colors.PRIMARY,
            tabs=[
                ft.Tab(
                    text="Discover Applications",
                    content=ft.Container(
                        content=DiscoverApplicationList(),
                        padding=ft.padding.only(left=15, right=15, top=10)
                    ),
                ),
                ft.Tab(
                    text="Installed Applications",
                    content=ft.Container(
                        content=InstalledApplicationList(),
                        padding=ft.padding.only(left=15, right=15, top=10)
                    ),
                ),
            ],
            expand=True
        )

        return ft.Container(tabs)