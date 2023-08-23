from textual.app import App, ComposeResult
from textual.widgets import Header, Static, Button, MarkdownViewer, Markdown
from textual.containers import Widget, Vertical, Container, Horizontal, VerticalScroll, Center
from textual.screen import Screen


EXAMPLE_MARKDOWN = """
# Markdown Document
"""


class AppHeader(Static):
    def compose(self) -> ComposeResult:
        yield Static("Titlu", id="test")


class Nav(Static):
    def compose(self) -> ComposeResult:
        yield Container(
            Button("home", classes="nav-button"),
            Button("ceva1", classes="nav-button"),
            Button("ceva2", classes="nav-button"),
            Button("ceva2", classes="nav-button"),
            id='navdrawer-container'
        )


class Content(Static):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(Static("ceva content aici"))


class MainLayout(Static):

    def compose(self) -> ComposeResult:
        yield AppHeader()
        yield Horizontal(Nav(), Content())


class MyApp(App):
    CSS_PATH = "nav.tcss"

    def on_mount(self) -> None:
        self.install_screen(MyApp(), name="MyApp")
        self.dark = True

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield MainLayout()


if __name__ == "__main__":
    app = MyApp()
    app.run()
