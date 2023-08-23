from mopyx import model, render, render_call, action


@model
class RouterModel:
    def __init__(self) -> None:
        self.HOME_ROUTE = '/home'
        self.SETTINGS_ROUTE = '/settings'
        self.active_route = self.HOME_ROUTE


router_model = RouterModel()


@model
class InstallAppState:
    def __init__(self) -> None:
        self.app_name = None
        self.app_id = None
    
    # def reset(self):
    #     self.app_name = None
    #     self.app_id = None
    
    # @action
    # def set_app(self, id, name):
    #     self.app_id = id
    #     self.app_name = name

    # def get_app(self):
    #     return {"id": self.app_id, "name": self.app_name}

install_app_state = InstallAppState()

