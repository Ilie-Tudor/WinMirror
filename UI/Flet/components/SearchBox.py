import flet as ft

class SearchBox(ft.UserControl):
    def __init__(self, on_click: callable = None, start_disabled = False, has_validation = True):
        super().__init__()
        self.start_disabled = start_disabled
        self.on_click = self.on_click_fallback_handler
        if on_click is None:
            return
        def on_click_wrapper(e):
            if has_validation and len(self.search_field.value.strip()) < 3:
                self.set_search_error("3 or more alphanumeric characters are required")
                return
            self.disable_button()
            on_click(self.search_field.value, lambda: self.enable_button())
        self.on_click = on_click_wrapper

    def disable_button(self):
        self.button.disabled = True
        self.update()
    
    def enable_button(self):
        self.button.disabled = False
        self.update()

    def on_click_fallback_handler(self, e):
        print(self.search_field.value)

    def set_search_error(self, value: str | None):
        self.search_field.error_text = value
        self.update()


    def build(self):
        self.search_field = ft.TextField(
                label="Search applications", 
                border_color=ft.colors.PRIMARY, 
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                label_style=ft.TextStyle(color=ft.colors.SECONDARY),
                dense=True,
                width=350,
                on_change=lambda e: self.set_search_error(None)
                )
        self.button = ft.IconButton(icon = ft.icons.SEARCH_ROUNDED, bgcolor=ft.colors.ON_SECONDARY, on_click=self.on_click, disabled=self.start_disabled)
        return ft.Container(
                    ft.Row(
                        [
                            self.search_field,
                            self.button
                        ]
                    ),
                    margin=ft.margin.only(top=15)
                )