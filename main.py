import urwid
import os

ASCII_LOGO = urwid.Text((
    u"\n"
    u"╔══════════════════════════╗\n"
    u"║      MetaDigger 📂       ║\n"
    u"╚══════════════════════════╝\n"
), align='center')

class FileExplorer(urwid.WidgetWrap):
    def __init__(self, path='.', on_select=None):
        self.path = os.path.abspath(path)
        self.on_select = on_select
        self.body = urwid.SimpleListWalker([])
        self.update_list()
        listbox = urwid.ListBox(self.body)
        super().__init__(urwid.LineBox(listbox, title="Select File"))

    def update_list(self):
        items = []
        try:
            entries = sorted(os.listdir(self.path))
        except PermissionError:
            entries = []

        # Add '..' to go up a directory
        if os.path.dirname(self.path) != self.path:
            entries.insert(0, '..')

        for entry in entries:
            full_path = os.path.join(self.path, entry)
            button = urwid.Button(entry)
            urwid.connect_signal(button, 'click', self.on_click, full_path)
            items.append(urwid.AttrMap(button, None, focus_map='reversed'))

        self.body[:] = items

    def on_click(self, button, path):
        if os.path.isdir(path):
            self.path = os.path.abspath(path)
            self.update_list()
        else:
            if self.on_select:
                self.on_select(path)

class MetaDiggerApp:
    def __init__(self):
        self.footer = urwid.Text(" Press Q to Quit | Arrow keys to navigate")
        self.file_display = urwid.Text(" No file selected", align='center')
        self.layout = urwid.Frame(
            header=ASCII_LOGO,
            body=FileExplorer(on_select=self.on_file_selected),
            footer=urwid.Filler(self.footer)
        )
        self.loop = urwid.MainLoop(
            self.layout,
            palette=[('reversed', 'standout', '')],
            unhandled_input=self.unhandled_input
        )

    def on_file_selected(self, path):
        self.file_display.set_text(f" Selected: {path}")
        self.layout.body = urwid.Filler(self.file_display, valign='middle')

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    app = MetaDiggerApp()
    app.run()

