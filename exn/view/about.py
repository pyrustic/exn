import tkinter as tk
import webbrowser
from tkinter import ttk
import tkutil
from viewable import Viewable

TEXT = """\
This software is the official Exonote Reader to read a dossier of interactive notes.

Visit website for documentation and updates: https://github.com/pyrustic/exn\
"""


class About(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="about")

    def _build(self):
        self.body.bind("<Escape>", lambda e: self._on_close())
        self.body.title("")
        #self.body.minsize(*constant.WINDOW_MINSIZE)
        #tkutil.restore_size(self.body, name="exn_info",
        #                    default=constant.INFO_WINDOW_SIZE)
        # labels
        frame1 = tk.Frame(self.body)
        frame1.pack(fill=tk.BOTH, expand=True, padx=3, pady=5)
        frame2 = tk.Frame(self.body)
        frame2.pack(fill=tk.X, padx=3, pady=(10, 3))
        # logo
        logo_label = tk.Label(frame1, name="logo", text="EXN")
        logo_label.pack()
        # text
        text = tk.Text(frame1, name="title_field", wrap="word",
                       width=40, height=8,
                       takefocus=False,
                       cursor="arrow")
        text.pack(fill=tk.BOTH, expand=True, pady=5)
        text.insert("1.0", TEXT)
        text.config(state="disabled")
        # footer
        close_button = ttk.Button(frame2, name="close", text="Close",
                                  style="red.TButton",
                                  command=self._on_close)
        close_button.pack(side=tk.LEFT)
        visit_website_button = ttk.Button(frame2, name="website_button",
                                          style="blue.TButton", text="Visit Website",
                                          command=self._on_visit_website)
        visit_website_button.pack(side=tk.RIGHT)
        # center the window
        editor = self._front.board.viewer.editor
        tkutil.align(self.body, parent=editor, side="n")
        tkutil.make_modal(self.body)

    def _on_map(self):
        pass

    def _on_visit_website(self):
        url = "https://github.com/pyrustic/exn"
        command = lambda: webbrowser.open(url, new=0)
        self.body.after(1, command)

    def _on_close(self):
        self.body.withdraw()
        self.body.destroy()
