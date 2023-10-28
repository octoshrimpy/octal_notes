from rich.console import RenderableType
from rich.text import Text, TextType

from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical, Horizontal, Container
from textual.widgets import Header, Static, Placeholder, Button, TextArea, ContentSwitcher, Pretty, DirectoryTree
from textual.binding import Binding
from textual import events

from textual.command import Hit, Hits, Provider

from urllib.parse import urlparse
import re

# FIXME: wet code
class SidebarButton(Button):
    def render(self) -> RenderableType:
        return self.label

class DragHandle(Button):

    def __init__(
        self, 
        drag: str,
        above: str, 
        below: str,
    ):
        super().__init__()
        self.drag = drag
        self.above = above
        self.below = below
        self.is_dragging = False
        self.label = ""
        
    def render(self) -> RenderableType:
        return self.label

    def on_mouse_down(self, event: events.MouseDown) -> None:
        event.stop()
        self.is_dragging = True

    def on_mouse_up(self, event: events.MouseUp) -> None:
        event.stop()
        self.is_dragging = False

        
    # TODO: finish me pls
    def on_mouse_move(self, event: events.MouseMove) -> None:
        if not self.is_dragging:
            return

        
        write = app.query_one("TextArea") 
        write.clear()
        write.insert(str(event.delta_y))

        self.parent.query_one("#notes").content = event

        above_elm = self.parent.query_one(self.above)
        below_elm = self.parent.query_one(self.below)

        if self.drag == "vertical":
            drag_dir = event.delta_y
            above_height = above_elm.get_content_height()
            below_height = below_elm.get_content_height()
                        
        elif self.drag == "horizontal":
            drag_dir = event.delta_x
        else:
            # malformed, ignore for now
            return

        if drag_dir > 0:
            above_elm.height -= 1
            below_elm.height += 1
        else:
            above_elm.height += 1
            below_elm.height -= 1


# class ThinScrollBar(ScrollBar):
#     bar = ["▗", "▄", "▖", " "]

class Card(Static):

    DEFAULT_CSS = """
    Card {
        width: 1fr;
        background: transparent;
        color: $text-muted;
    }
    
    Static {
        border: round transparent;
        border-title-color: $secondary-background;
        border-subtitle-align: right;
        border-subtitle-color: $secondary-background;
        border-title-align: left;
        border-title-color: $text-muted;
        border-title-style: bold;
        max-height: 6;
        height: auto;
        padding: 1 3;
        margin-bottom: 2;
    }

    Static:hover {
        border: round $secondary-background;
        color: $text;
    }

    Static.has-title {
        padding: 1 3 0 3;
    }

    """

    def __init__(
        self, 
        content: str, 
        title: str = "",
        url: str = ""
    ):
        super().__init__()
        self.title = title
        self.url = url
        self.content = content

    # text will wrap, 
    # one long line will multi-line and break limit
    # unused for now
    def trim_content(self, s, max_lines=3):
        lines = s.split("\n")
        trimmed = lines[:max_lines]
        return '\n'.join(trimmed)
        
    def modify_url(self, url):
        """Modify a given URL into the 'path @ base URL' format with spaces instead of dashes and underscores."""
        parsed_url = urlparse(url)
        
        # Remove leading and trailing slashes from the path, then split it into components
        path_components = parsed_url.path.strip('/').split('/')
        
        # Replace dashes and underscores with spaces in each component
        modified_path_components = [re.sub(r'[-_]', ' ', component) for component in path_components]
        
        # Join modified path components
        modified_path = '/'.join(modified_path_components)
        
        # Reassemble the URL in the new format
        modified_url = f"{modified_path} @ {parsed_url.netloc}"
        
        return modified_url
    
     
    def compose(self) -> ComposeResult:
        wrap = Static(self.content)

        if self.title != "": 
            wrap.border_title = self.title
            wrap.add_class("has-title")

        if self.url != "":
            url_text = self.modify_url(self.url)
            # wrap.border_subtitle = Text.assemble("[link=", self.url, "]", url_text, "[/link]")
            wrap.border_subtitle = url_text
        yield wrap
      
    
# =====================

class OctalCommands(Provider):

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)

        app = self.app
        assert isInstance(app, OctalApp) 

        command = f"trigger notification"
        score = matcher.match(command)
        if score > 0:
            yield Hit(
                score,
                matcher.highlight(command),
                partial(app.sendNotification, "test msg"),
                help="trigger notification",
            )




# =====================

class OctalApp(App):
    CSS_PATH="layout.tcss"

    COMMANDS = App.COMMANDS | {OctalCommands}

    def sendNotification(self, msg="(empty message)", title ="Octal") -> None:
        self.notify(msg, title=title)

    def compose(self) -> ComposeResult:
        
        yield Header()
        with Grid(id="app-grid"):
            with Vertical(id="sidebar"):
                yield SidebarButton("┌─┐\n╘─╛", classes="button", id="wrapper_inbox")
                yield SidebarButton("┌██\n└─┘", classes="button", id="wrapper_notes")
                yield SidebarButton("🞊  \n ╲ ", classes="button", id="wrapper_search")
                yield SidebarButton("● ๐\n┠─╯", classes="button", id="wrapper_git")
                yield SidebarButton("□ ⌐\n√ ╍", classes="button", id="wrapper_todo")
                yield Static(classes="spacer")
                yield SidebarButton("⚙ ⌝\n⌞ ⚙", classes="button")
            with ContentSwitcher(initial="wrapper_inbox"):
                with Horizontal(id="wrapper_inbox"):
                    with Vertical():
                        yield Card(
                            """flyscrape is an expressive and elegant web scraper, combining the speed of Go with the flexibility of JavaScript. — Focus on data extraction rather than request juggling. 
Domains and URL filtering
Depth control
Request caching
Rate limiting
Development mode
Single binary executable""", 
                            title="GitHub - philippta/flyscrape: An expressive and elegant web scraper", 
                            url="https://github.com/philippta/flyscrape"
                        )
                        yield Card(
                            """If you look purely at their form, Apple’s products are all rounded rectangular slabs. Make the slab as large and thin as an open coffee-table book, and you get a Studio Display. Make it tall and hand-held, and you get an iPhone. Make it an even smaller and thicker, and you get an AirPods case.
                            
The physical dimensions are dictated first by the human body. An iPhone or AirPods case must be hand-holdable by the majority of buyers. Dimensions are further dictated by components inside. A display (as far as it remains rigid and not bendable) can never get smaller than the panel.
                            
But how about the rounded corners?""",
                            title="The secret formula for Apple's rounded corners",
                            url="https://arun.is/blog/apple-rounded-corners/"
                        )
                        yield Card("inbox")
                        yield Card("inbox")
                        
                with Horizontal(id="wrapper_notes"):
                    with Vertical(id="left"):
                    
                        nb = DirectoryTree("./", id="notes")
                        nb.guide_depth = 2
                        nb.border_title = "notes"
                        
                        yield nb

                        # yield DragHandle(
                        #     drag="vertical", 
                        #     above="#notes",
                        #     below="#tags"
                        # )
                        
                        bb = Static("", id="tags")
                        bb.border_title = "tags"
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
