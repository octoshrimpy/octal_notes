from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical, Horizontal, Container
from textual.widgets import Header, Static, Placeholder, Button, TextArea
from textual.binding import Binding

class OctalApp(App):
    CSS_PATH="layout.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        with Grid(id="app-grid"):
            with Vertical(id="sidebar"):
                yield Static("┌─┐\n╘─╛", classes="button", id="inbox")
                yield Static("┌██\n└─┘", classes="button", id="notes")
                yield Static("🞊  \n \\", classes="button", id="search")
                yield Static("● ๐\n┠─╯", classes="button", id="git")
                yield Static("□ ⌐\n√ ╍", classes="button", id="todo")
            with Horizontal(id="content"):
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
            yield Static("bottom bar", id="bottom-bar")



app = OctalApp()

def main() -> None:
    """Entrypoint for the application."""
    app.run()
        

if __name__ == '__main__':
    main()
