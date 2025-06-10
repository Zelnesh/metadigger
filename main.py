import urwid
import os
from magic_number_checker import check_file_and_extract_metadata

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
        self.listbox = urwid.ListBox(self.body)
        self.update_list()
        super().__init__(urwid.LineBox(self.listbox, title="Select File"))

    def update_list(self):
        items = []
        try:
            entries = sorted(os.listdir(self.path))
        except PermissionError:
            entries = []

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
        self.footer = urwid.Text(" Press Q to Quit | Arrow keys to navigate | Enter to select")
        self.file_display = urwid.Text(" No file selected", align='center')
        self.file_explorer = FileExplorer(on_select=self.on_file_selected)
        self.layout = urwid.Frame(
            header=ASCII_LOGO,
            body=self.file_explorer,
            footer=urwid.Filler(self.footer)
        )
        self.loop = urwid.MainLoop(
            self.layout,
            palette=[('reversed', 'standout', '')],
            unhandled_input=self.unhandled_input
        )

    def on_file_selected(self, path):
        metadata = check_file_and_extract_metadata(path)
        if metadata:
            lines = [f"{k}: {v}" for k, v in metadata.items()]
            text = f"Metadata for {os.path.basename(path)}\n\n" + "\n".join(lines)
        else:
            text = f"Could not extract metadata for {os.path.basename(path)}"

        metadata_widget = urwid.Text(text, align='left')
        back_button = urwid.Button("Back to File Picker", on_press=self.back_to_picker)
        pile = urwid.Pile([
            urwid.Filler(ASCII_LOGO),
            urwid.Divider(),
            urwid.Filler(metadata_widget, valign='top'),
            urwid.Divider(),
            urwid.AttrMap(back_button, None, focus_map='reversed'),
        ])
        self.layout.body = urwid.Filler(pile, valign='top')

    def back_to_picker(self, button):
        self.layout.body = self.file_explorer

    def unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def run(self):
        self.loop.run()

if __name__ == "__main__":
    app = MetaDiggerApp()
    app.run()

