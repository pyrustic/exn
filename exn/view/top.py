import tkinter as tk
from tkinter import ttk
from viewable import Viewable
from exn.view.search import Search
from exn.view.toc import Toc
from exn.view.past import Past
from exn.view.info import Info
from exn.view.about import About
from exn.view.goto import Goto


class Top(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front
        self._manager = front.manager
        self._title_strvar = tk.StringVar()
        self._title = None
        self._search_view = None

    def click_home(self):
        self._on_click_home()

    def click_toc(self):
        self._on_click_toc()

    def click_info(self):
        self._on_click_info()

    def click_goto(self):
        self._on_click_goto()

    def click_past(self):
        self._on_click_past()

    def click_search(self):
        self._on_click_search()

    def click_about(self):
        self._on_click_about()

    def _create_body(self, parent):
        return ttk.Frame(parent, name="top")

    def _build(self):
        self._install_menu_bar()
        #self._install_right_frame()

    def _install_left_frame(self):
        # left frame
        left_frame = ttk.Frame(self.body)
        #left_frame.grid(row=0, column=0, sticky="we")
        #left_frame.rowconfigure(0, weight=1)
        #left_frame.columnconfigure(1, weight=1)
        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH,
                        pady=5)
        """
        # title label
        title_label = tk.Label(left_frame,
                               textvariable=self._title_label_strvar,
                               cursor="hand1")
        title_label.grid(row=0, column=0)
        title_label.bind("<Button-1>", self._on_click_title)
        title_label.bind("<Button-3>", self._on_right_click_title)
        """
        # title entry
        title_entry = tk.Entry(left_frame, textvariable=self._title_strvar,
                               takefocus=False, state="readonly",
                               cursor="hand1")
        #title_entry.grid(row=0, column=1, sticky="nswe")
        title_entry.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=1)
        title_entry.bind("<Button-1>", self._on_click_title)
        title_entry.bind("<Button-3>", self._on_right_click_title)
        title_entry.bind("<FocusIn>", lambda e: self._on_title_focus())

    def _install_menu_bar(self):
        # right frame
        frame = ttk.Frame(self.body)
        #right_frame.grid(row=0, column=1, sticky="e")
        frame.pack(pady=3)
        # about button
        about_button = ttk.Button(frame, text="About",
                                 takefocus=False,
                                 command=self._on_click_about)
        about_button.pack(side=tk.RIGHT, padx=(0, 3))
        # search button
        search_button = ttk.Button(frame, text="Search",
                                  takefocus=False,
                                  command=self._on_click_search)
        search_button.pack(side=tk.RIGHT, padx=(0, 3))
        # past history button
        past_button = ttk.Button(frame, text="Past",
                                takefocus=False,
                                command=self._on_click_past)
        past_button.pack(side=tk.RIGHT, padx=(0, 3))
        # goto button
        goto_button = ttk.Button(frame, text="Goto",
                                takefocus=False,
                                command=self._on_click_goto)
        goto_button.pack(side=tk.RIGHT, padx=(0, 3))
        # info button
        info_button = ttk.Button(frame, text="Info",
                                takefocus=False,
                                command=self._on_click_info)
        info_button.pack(side=tk.RIGHT, padx=(0, 3))
        # Table of Contents button
        toc_button = ttk.Button(frame, text="Toc",
                               takefocus=False,
                               command=self._on_click_toc)
        toc_button.pack(side=tk.RIGHT, padx=(0, 3))
        # home button
        home_button = ttk.Button(frame, text="Home",
                                takefocus=False,
                                command=self._on_click_home)
        home_button.pack(side=tk.RIGHT, padx=(0, 3))

    def _on_right_click_title(self, event):
        self._update_clipboard(self._title_strvar.get())
        # TODO
        #Toast(self.body, message="Copied !")

    def _on_click_home(self):
        pages = self._front.board.viewer.pages
        if not pages:
            return
        home = list(pages.values())[0]
        self._front.open(home.filename)

    def _on_click_past(self):
        past = Past(self._front)
        past.build(self.body)

    def _on_click_search(self):
        if self._search_view and self._search_view.body.winfo_exists():
            self._search_view.body.deiconify()
            self._search_view.body.grab_set()
            return
        self._search_view = Search(self._front)
        self._search_view.build(self.body)

    def _on_click_info(self):
        info = Info(self._front)
        info.build(self.body)

    def _on_click_goto(self):
        goto = Goto(self._front)
        goto.build(self.body)

    def _on_click_toc(self):
        viewer = self._front.board.viewer
        if not viewer:
            return
        if not viewer.sids:
            statusbar = viewer.statusbar
            statusbar.show("No sections !", duration=1500, delay=0)
            return
        toc = Toc(self._front)
        toc.build(self.body)

    def _on_click_about(self):
        goto = About(self._front)
        goto.build(self.body)

    def _on_title_focus(self):
        viewer = self._front.board.viewer
        if not viewer:
            return
        viewer.editor.focus_set()

    def _update_clipboard(self, text):
        self.body.clipboard_clear()
        self.body.clipboard_append(text)
