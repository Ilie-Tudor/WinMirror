import tkinter as tk
root = tk.Tk()
root.title("Menu Example")
root.geometry("800x600")
root.minsize(800, 600)


menu_frame = tk.Frame(root, bg="light grey", width=200)
menu_frame.pack(side="left", fill="y")


menu_btns = {}
pages = {}


# create container frame on right
container_frame = tk.Frame(root)
container_frame.pack(side="left", fill="both", expand=True)


class Page:
    def __init__(self, menu_button_label, page_id):
        self.menu_button_label = menu_button_label,
        self.page_id = page_id
        self.tk_content = tk.Frame(master=container_frame)

        self.tk_content.pack(side="left", fill="both", expand=True)
        self.tk_content.configure(background="#F0F0F0")
        self.tk_content.pack_forget()

    def get_content(self):
        return self.tk_content

    def get_id(self):
        return self.page_id

    def set_id(self, page_id):
        self.page_id = page_id

    def get_menu_button_label(self):
        return self.menu_button_label

    def set_menu_button_label(self, menu_button_label):
        self.menu_button_label = menu_button_label

    def register(self):
        btn = tk.Button(menu_frame, text=self.get_menu_button_label(), bg="gray", font=("Arial", 14), width=20, height=2,
                        borderwidth=0, command=lambda: show_page(self.get_id()))
        btn.pack(side="top", padx=10, pady=5, fill="x")
        menu_btns[self.get_id()] = btn
        pages[self.get_id()] = self


def show_page(id):
    print(id)
    for page in pages.values():
        page.get_content().pack_forget()
    pages[id].get_content().pack(side="left", fill="both", expand=True)


def add_page(page):
    btn = tk.Button(menu_frame, text=page.get_menu_button_label(), bg="gray", font=("Arial", 14), width=20, height=2,
                    borderwidth=0, command=lambda: show_page(page.get_id()))
    btn.pack(side="top", padx=10, pady=5, fill="x")
    menu_btns[page.get_id()] = btn
    pages[page.get_id()] = page


# show_page("#applications")
