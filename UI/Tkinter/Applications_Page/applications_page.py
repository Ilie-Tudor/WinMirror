from DATA.commands import search, get_search_output, Search_Args
from root import Page, root
import tkinter as tk
import sys
sys.path.insert(1, '../../')


class Application_List_Header:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.list_header = tk.Frame(parent)
        self.list_header.pack(fill='x', pady=1)
        self.checked_state = tk.BooleanVar()
        self.check_button = tk.Checkbutton(
            self.list_header, height=1, background="grey", variable=self.checked_state)
        self.check_button.pack(side="left")
        self.name_column = tk.Label(self.list_header, height=1, text="Name", font=(
            "Arial", 13), background="grey")
        self.name_column.pack(side="left", fill="x", expand=True)
        self.id_column = tk.Label(self.list_header, height=1, text="ID", font=(
            "Arial", 13), background="grey")
        self.id_column.pack(side="left", fill="x", expand=True)
        self.version_column = tk.Label(self.list_header, height=1, text="Version", font=(
            "Arial", 13), background="grey")
        self.version_column.pack(side="left", fill="x", expand=True)

    def get_checked_state(self):
        return self.checked_state.get()

    def add_event_on_check_press(self, event_handler):
        def event_wrapper():
            event_handler(self)
        self.check_button.configure(command=event_wrapper)


class Application_List_Item:
    def __init__(self, parent, app_name, app_id, app_version) -> None:
        self.parent = parent
        self.checked_state = tk.BooleanVar()
        self.list_item = tk.Frame(parent)
        self.list_item.pack(fill='x', pady=1)
        self.check_button = tk.Checkbutton(
            self.list_item, background="light grey", variable=self.checked_state)
        self.check_button.pack(side="left")
        self.name = tk.Label(self.list_item, text=app_name, font=(
            "Arial", 13), background="light grey")
        self.name.pack(side="left", fill="x", expand=True)
        self.id = tk.Label(self.list_item, text=app_id, font=(
            "Arial", 13), background="light grey")
        self.id.pack(side="left", fill="x", expand=True)
        self.version = tk.Label(self.list_item, text=app_version, font=(
            "Arial", 13), background="light grey")
        self.version.pack(side="left", fill="x", expand=True)

    def get_checked_state(self):
        return self.checked_state.get()

    def set_checked_state(self, value):
        self.checked_state.set(value)

    def add_event_on_check_press(self, event_handler):
        def event_wrapper():
            event_handler(self)
        self.check_button.configure(command=event_wrapper)

    def add_event_on_text(self, event_type: str, event_handler):
        def event_wrapper(event):
            event_handler(event, self)

        self.list_item.bind(event_type, event_wrapper)
        self.name.bind(event_type, event_wrapper)
        self.id.bind(event_type, event_wrapper)
        self.version.bind(event_type, event_wrapper)

    def show_info_modal(self):
        if hasattr(self, 'application_info_modal'):
            self.application_info_modal.modal.destroy()
        self.application_info_modal = Application_Info_Modal(
            self.list_item, self.name.cget("text"))


class Application_Info_Modal:
    def __init__(self, parent, name, id=None, version=None) -> None:
        # create modal dialog with app name
        self.parent = parent
        self.modal = tk.Toplevel(parent)
        self.modal.geometry("300x150")
        self.modal.resizable(False, False)
        self.modal.transient(parent)
        self.parent.update_idletasks()
        # create label with app name
        self.app_lbl = tk.Label(self.modal, text=name, font=("Arial", 16))
        self.app_lbl.pack(padx=10, pady=10)

        # create close button
        self.close_btn = tk.Button(
            self.modal, text="Close", command=self.modal.destroy)
        self.close_btn.pack(side="bottom", padx=10, pady=10)

        # center modal on main window
        main_x, main_y = root.winfo_x(), root.winfo_y()
        main_width, main_height = root.winfo_width(), root.winfo_height()
        modal_width, modal_height = self.modal.winfo_width(), self.modal.winfo_height()
        x = main_x + (main_width - modal_width) // 2
        y = main_y + (main_height - modal_height) // 2
        self.modal.geometry(f"+{x}+{y}")


data = get_search_output(
    search(Search_Args("vscode", None, None, None, False)))
# data = [
#     {"name": "Alice", "id": 1, "version": "1.0.0"},
#     {"name": "Bob", "id": 2, "version": "2.3.1"},
#     {"name": "Carol", "id": 3, "version": "1.2.7"},
#     {"name": "David", "id": 4, "version": "4.1.9"},
#     {"name": "Eve", "id": 5, "version": "3.0.0"},
# ]


def run():
    applications_page = Page("Applications",
                             "#applications")
    applications_page.register()

    applications_page_root = applications_page.get_content()

    header = tk.Frame(applications_page_root,
                      background="light grey", height=60)
    header.pack(side="top", fill="x")
    header.pack_propagate(False)

    page_title = tk.Label(header, text="Applications", font=(
        "Arial", 12), background="light grey")
    page_title.pack(side="left", fill="y")

    search_bar = tk.Entry(header, bg="white", font=("Arial", 12), width=30)
    search_bar.pack(side="right", padx=10)

    applications_list_container = tk.Frame(
        applications_page_root, background="white")
    applications_list_container.pack(
        side="left", fill="both", padx=10, pady=10, expand=True)

    applications_list_header = Application_List_Header(
        applications_list_container)

    def map_function(data):
        app = Application_List_Item(applications_list_container,
                                    data["name"], data["id"], data["version"])
        # app.add_event_on_check_press(lambda s: print(s.get_checked_state()))
        app.add_event_on_text("<Button-1>", lambda e,
                              s: s.show_info_modal())
        return app

    applications_list = list(map(map_function, data))

    def list_header_check_press_handler(s):
        for app in applications_list:
            app.set_checked_state(s.get_checked_state())
    applications_list_header.add_event_on_check_press(
        list_header_check_press_handler)
