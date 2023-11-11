import asyncio
import subprocess

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, ListItem, ListView, Static

INFO_MSG = """It is that time of year again: conda environments are broken because of SSL library problems. In my experience, this is the case on Windows in either the base channel or conda-forge, every Fall for the past few years. I know, because I'm teaching a Fall coding course and my students can't install packages or use pipx-installed applications. Almost. Every. Year. Sigh."""


class ErrorDialog(ModalScreen):
    def __init__(self, exc: Exception, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.exc = exc

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(f"{type(self.exc).__name__}: {self.exc}", id="msg")
            with Center():
                yield Button("Dismiss", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()

    def on_mount(self) -> None:
        widget = self.query_one("Vertical")
        widget.border_title = "An error occured"


class CondaEnvironment(ListItem):
    def __init__(self, env_name, path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.env_name = env_name
        self.path = path

    def compose(self) -> ComposeResult:
        yield Static(self.env_name, id="env_name")
        yield Static("[bold green]Fixed[/]", id="fixed")
        yield Static("[bold red]Error", id="error")


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

    @on(ListView.Selected)
    def fix_environment(self, event: ListView.Selected) -> None:
        try:
            1 / 0
        except Exception as exc:
            self.app.push_screen(ErrorDialog(exc))
            event.item.add_class("error")

    @work
    async def load_conda_environments(self) -> None:
        list_view = self.query_one(ListView)

        process = await asyncio.create_subprocess_shell(
            "conda env list", stdout=subprocess.PIPE
        )
        output = await process.stdout.read()
        list_view.loading = False
        for line in output.decode().splitlines():
            if line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) >= 2:
                env, *_, path = fields
                await list_view.append(CondaEnvironment(f"{env}", path))


app = FixCondaSSLApp

if __name__ == "__main__":
    app().run()