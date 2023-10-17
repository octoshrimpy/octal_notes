from rich.console import RenderableType

from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical, Horizontal, Container
from textual.widgets import Header, Static, Placeholder, Button, TextArea, ContentSwitcher
from textual.binding import Binding
from textual import events

class SidebarButton(Button):

    def render(self) -> RenderableType:
        return self.label


class OctalApp(App):
    CSS_PATH="layout.tcss"

    def compose(self) -> ComposeResult:
        
        yield Header()
        with Grid(id="app-grid"):
            with Vertical(id="sidebar"):
                yield SidebarButton("┌─┐\n╘─╛", classes="button", id="wrapper_inbox")
                yield SidebarButton("┌██\n└─┘", classes="button", id="wrapper_notes")
                yield SidebarButton("🞊  \n \\", classes="button", id="wrapper_search")
                yield SidebarButton("● ๐\n┠─╯", classes="button", id="wrapper_git")
                yield SidebarButton("□ ⌐\n√ ╍", classes="button", id="wrapper_todo")
            with ContentSwitcher(initial="wrapper_inbox"):
                with Horizontal(id="wrapper_inbox"):
                    yield Static("inbox")
                with Horizontal(id="wrapper_notes"):
                    with Vertical(id="left"):
                        nb = Static("")
                        nb.border_title = "notebooks"
                        yield nb
                        bb = Static("")
                        bb.border_title = "notes"
                        yield bb
                    center = Container(id="center")
                    center.border_title = "tabs go here"
                    with center:
                        yield TextArea("hello world", language="markdown")
                        
                    md = Static(id="metadata")
                    md.border_title = "metadata"
                    yield md
                with Horizontal(id="wrapper_search"):
                    yield Static("search")
                with Horizontal(id="wrapper_git"):
                    yield Static("git")
                with Horizontal(id="wrapper_todo"):
                    yield Static("todo")
            yield Static("bottom bar", id="bottom-bar")

    def on_button_pressed(self, event: SidebarButton.Pressed) -> None:
        me = event.button
        self.query_one(ContentSwitcher).current = me.id
        me.parent.query(".button.-selected").remove_class("-selected")
        me.add_class("-selected")


app = OctalApp()

def main() -> None:
    """Entrypoint for the application."""
    app.run()
        

if __name__ == '__main__':
    main()
