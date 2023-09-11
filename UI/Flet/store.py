import pydux
import copy

def observe(state, action, prev_check = True):
    if(state not in store.get_state()):
        raise Exception(f"State '{state}' doesn't exist")
    current_state = store.get_state()[state]
    def handler():
        nonlocal current_state
        next_state = store.get_state()[state]
        if not prev_check or current_state != next_state:
            current_state = copy.deepcopy(next_state)
            action(current_state)
    return store.subscribe(handler)

def get_state(state):
    if(state not in store.get_state()):
        raise Exception(f"State '{state}' doesn't exist")
    return store.get_state()[state]


# route state handling
class ROUTES_ENUM:
    def __init__(self) -> None:
        self.HOME_ROUTE = '/home'
        self.SETTINGS_ROUTE = '/settings'
        self.BUNDLES_ROUTE = '/bundles'
        
ROUTES = ROUTES_ENUM()

def route(state, action):
    if state is None:
        state = "/home"
    if action is None:
        return state
    elif action["type"] == "route":
        return action["payload"]
    return state

def route_to(route: str):
    store.dispatch({"type": "route", "payload": route})

def get_active_route():
    return get_state("route")

def observe_route(action, prev_check = True):
    return observe("route", action, prev_check=prev_check)


# bundles 
def bundles(state, action):
    if state is None:
        state = []
    if action is None:
        return state
    elif action["type"] == "bundles":
        return action["payload"]
    return state

def set_bundles(bundles):
    store.dispatch({"type": "bundles", "payload": bundles})

def get_bundles():
    return get_state("bundles")

def observe_bundles(action, prec_check = True):
    return observe("bundles", action, prev_check=prec_check)


# discover page selected applications
def discover_page_selected(state, action):
    if state is None:
        state = []
    if action is None:
        return state
    elif action["type"] == "discover_page_selected":
        return action["payload"]
    return state

def set_discover_page_selected(applications):
    store.dispatch({"type": "discover_page_selected", "payload": applications})

def get_discover_page_selected():
    return get_state("discover_page_selected")

def observe_discover_page_selected(action, prec_check = True):
    return observe("discover_page_selected", action, prev_check=prec_check)


# discover page selected applications
def installed_page_selected(state, action):
    if state is None:
        state = []
    if action is None:
        return state
    elif action["type"] == "installed_page_selected":
        return action["payload"]
    return state

def set_installed_page_selected(applications):
    store.dispatch({"type": "installed_page_selected", "payload": applications})

def get_installed_page_selected():
    return get_state("installed_page_selected")

def observe_installed_page_selected(action, prec_check = True):
    return observe("installed_page_selected", action, prev_check=prec_check)




# create store
store = pydux.create_store(pydux.combine_reducers({"route": route, "bundles": bundles, "discover_page_selected": discover_page_selected, "installed_page_selected": installed_page_selected}))

