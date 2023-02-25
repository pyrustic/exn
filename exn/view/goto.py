import tkinter as tk
from tkinter import ttk
import tkutil
from viewable import Viewable


class Goto(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front
        self._input_strvar = tk.StringVar()
        self._status_strvar = tk.StringVar()

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="goto")

    def _build(self):
        self.body.bind("<Escape>", lambda e: self._on_close())
        self.body.title("")
        #self.body.minsize(*constant.WINDOW_MINSIZE)
        #tkutil.restore_size(self.body, name="exn_info",
        #                    default=constant.INFO_WINDOW_SIZE)
        # labels
        frame1 = tk.Frame(self.body)
        frame1.pack(pady=5)
        frame2 = tk.Frame(self.body)
        frame2.pack(fill=tk.BOTH, expand=True, padx=3, pady=(5, 0))
        frame3 = tk.Frame(self.body)
        frame3.pack(fill=tk.BOTH, expand=True, padx=3, pady=(3, 5))
        frame4 = tk.Frame(self.body)
        frame4.pack(fill=tk.BOTH, expand=True, padx=3, pady=5)
        frame5 = tk.Frame(self.body)
        frame5.pack(fill=tk.X, padx=3, pady=(10, 3))
        # Info
        info_label = tk.Label(frame1, name="title", text="Goto")
        info_label.pack()
        # description label
        text = "Filename, anchor, or page number"
        description_label = tk.Label(frame2, name="description_label",
                                     text=text, anchor="w")
        description_label.pack(fill=tk.X)
        #
        # entry field
        field = tk.Entry(frame3, name="field", width=30,
                         textvariable=self._input_strvar)
        field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        command = lambda e: self._on_click_goto()
        field.bind("<Return>", command, True)
        field.focus_set()
        # clear button
        command = lambda: self._input_strvar.set("")
        clear_button = ttk.Button(frame3, text="X", style="clear2.TButton",
                                  command=command)
        clear_button.pack(side=tk.RIGHT)
        # status label
        status_label = tk.Label(frame4, name="status_label",
                                textvariable=self._status_strvar)
        status_label.pack(fill=tk.X)
        # footer
        close_button = ttk.Button(frame5, name="close", text="Close",
                                  style="red.TButton", command=self._on_close)
        close_button.pack(side=tk.LEFT)
        goto_button = ttk.Button(frame5, name="goto_button",
                                 text="Goto !", command=self._on_click_goto)
        goto_button.pack(side=tk.RIGHT)
        # center the window
        editor = self._front.board.viewer.editor
        tkutil.align(self.body, parent=editor, side="n")
        tkutil.make_modal(self.body)

    def _on_map(self):
        pass

    def _get_data(self):
        return "title", "filename", "#tag1 #tag2"

    def _on_click_goto(self):
        val = self._input_strvar.get().strip()
        if not val:
            return
        try:
            page = int(val)
        except ValueError as e:
            pass
        else:
            self._open_page(page)
            return
        viewer = self._front.board.viewer
        failure = False
        is_anchor = False
        if val.startswith("<") and val.endswith(">"):
            is_anchor = True
            if not viewer.goto(val):
                failure = True
        else:
            if not self._front.open(val):
                failure = True
        if failure:
            self._status_strvar.set("Failed to process the request !")
        else:
            if is_anchor:
                self._status_strvar.set("Anchor found !")
            else:
                self._status_strvar.set("Page found !")
            self._on_close()

    def _open_page(self, x):
        x -= 1
        pages = self._front.board.viewer.pages
        match = None
        for i, item in enumerate(pages.values()):
            if i == x:
                match = item
                break
        if not match:
            self._status_strvar.set("Page not found !")
            return
        if not self._front.open(match.filename):
            self._status_strvar.set("Failed to open the page")
            return
        self._status_strvar.set("Page found !")
        self._on_close()

    def _on_close(self):
        self.body.withdraw()
        self.body.destroy()
