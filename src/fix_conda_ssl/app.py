import asyncio

from textual import work
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, Header, ListItem, ListView, Static

INFO_MSG = """It is that time of year again: conda environments are broken because of SSL library problems. In my experience, this is the case on Windows in either the base channel or conda-forge, every Fall for the past few years. I know, because I'm teaching a Fall coding course and my students can't install packages or use pipx-installed applications. Almost. Every. Year. Sigh."""


class CondaEnvironment(ListItem):
    def __init__(self, env_name, path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.env_name = env_name
        self.path = path

    def compose(self) -> ComposeResult:
        yield Static(self.env_name, id="env_name")
        yield Static("Fixing...", classes="busy")
        yield Static("Fixed!", classes="fixed")
        yield Static("Error", classes="error")


class FixCondaSSLApp(App[None]):
    BINDINGS = [("q", "quit()", "Quit")]
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Static(INFO_MSG, id="info_msg")
        yield Static("Select an environment to fix SSL", id="listview_header")
        yield ListView()

    def on_mount(self) -> None:
        list_view = self.query_one(ListView)
        list_view.loading = True
        self.load_conda_environments()

    @work
    async def load_conda_environments(self) -> None:
        list_view = self.query_one(ListView)
        for x in range(5):
            await list_view.append(CondaEnvironment(f"Environment {x}", path=None))
        list_view.loading = False


app = FixCondaSSLApp

if __name__ == "__main__":
    app().run()
