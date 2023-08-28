from DATA.commands import get_bundle, Get_Bundle_Args
from store import set_bundles


class Global_Data_Fetching:
    def get_bundles():
        data = get_bundle(Get_Bundle_Args(all=True))
        set_bundles(bundles=data)