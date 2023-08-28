import flet as ft
from pages.BundlesPage.BundleCard import BundleCard
from pages.BundlesPage.NewBundleCard import NewBundleCard
import threading
from DATA.commands import get_bundle, Get_Bundle_Args
from store import set_bundles, observe_bundles, get_bundles


class BundlesPage(ft.UserControl):

    def did_mount(self):
        self.is_mounted = True
        self.new_bundle_card = NewBundleCard()
        self.bundles = [self.new_bundle_card]
        self.populate_bundles(get_bundles())
        self.unsubscribe = observe_bundles(self.populate_bundles)
        self.th = threading.Thread(
            target=self.get_bundles, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.is_mounted = False
        self.unsubscribe()

    def populate_bundles(self, bundles):
        if self.is_mounted == True:
            self.bundles.clear()
            self.bundles = [self.new_bundle_card]
            for bundle in bundles:
                self.bundles.append(BundleCard(bundle))
            self.bundles_grid.controls = self.bundles
            self.update()

    def get_bundles(self):
        data = get_bundle(Get_Bundle_Args(all=True))
        set_bundles(bundles=data)


    def build(self):

        self.header = ft.Text("Bundles", size=20)

        self.bundles_grid = ft.GridView(
            controls= [
                ft.Text("Loading")
            ],
            runs_count=4,
            spacing=5,
            run_spacing=5,
        )
        
        self.content = ft.Container(self.bundles_grid, height=700)

        self.column_layout = ft.Column(controls=[
            self.header,
            self.content
        ])

        return ft.Container(
            self.column_layout,
            padding=ft.padding.only(left=15, right=15, top=10)
        )

