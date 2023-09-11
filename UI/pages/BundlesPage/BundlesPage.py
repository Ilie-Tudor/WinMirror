import flet as ft
from pages.BundlesPage.BundleCard import BundleCard
from pages.BundlesPage.NewBundleCard import NewBundleCard
import threading
from DATA.commands import get_bundle, Get_Bundle_Args, import_bundle, Import_Bundle_Args
from store import set_bundles, observe_bundles, get_bundles
from api import Global_Data_Fetching

class BundlesPage(ft.UserControl):

    def did_mount(self):
        self.is_mounted = True
        self.new_bundle_card = NewBundleCard()
        self.bundles = [self.new_bundle_card]
        self.populate_bundles(get_bundles())
        self.unsubscribe = observe_bundles(self.populate_bundles)
        self.bundles_th = threading.Thread(
            target=self.get_bundles, args=(), daemon=True)
        self.bundles_th.start()

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

    def on_import(self, filePath):
        if filePath is not None:
            self.import_th = threading.Thread(
                target=self.import_bundle, args=(filePath,), daemon=True)
            self.import_th.start()

    def import_bundle(self, filePath):
        data = import_bundle(Import_Bundle_Args(filePath))
        if(data["status"]=="success"):
            Global_Data_Fetching.get_bundles()

    def build(self):

        self.import_picker = ft.FilePicker(
            on_result=lambda e: self.on_import(e.files[0].path if e.files is not None else None))

        self.header = ft.Container(ft.Row([
            ft.Text("Bundles", size=20),
            ft.ElevatedButton("Import", icon=ft.icons.ADD_BOX, bgcolor=ft.colors.ON_SECONDARY, on_click=lambda e: self.import_picker.pick_files())
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), margin=ft.margin.only(bottom=20))

        self.bundles_grid = ft.GridView(
            controls= [
                ft.Text("Loading")
            ],
            runs_count=4,
            spacing=5,
            run_spacing=5,
        )
        
        self.content = ft.Container(self.bundles_grid, height=680)

        self.column_layout = ft.Column(controls=[
            self.header,
            self.import_picker,
            self.content
        ])

        return ft.Container(
            self.column_layout,
            padding=ft.padding.only(left=15, right=15, top=10)
        )

