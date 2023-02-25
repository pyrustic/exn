import tkinter as tk
from viewable import Viewable
from exonote import Viewer
from exonote.editor import Editor
from exn.view.switcher import Switcher


class Board(Viewable):
    def __init__(self, front, filename):
        super().__init__()
        self._front = front
        self._filename = filename
        self._editor = None
        self._viewer = None
        self._toc_frame = None
        self._toc = None
        self._toc_is_visible = False
        self._failed = False

    @property
    def front(self):
        return self._front

    @property
    def editor(self):
        return self._editor

    @property
    def viewer(self):
        return self._viewer

    @property
    def failed(self):
        return self._failed

    def _create_body(self, parent):
        return tk.Frame(parent)

    def _build(self):
        self._toc_frame = tk.Frame(self.body)
        self._toc_frame.pack(side=tk.LEFT, fill=tk.Y)
        self._editor = Editor(self.body, width=0, height=0,
                              takefocus=False)
        self._editor.vbar.config(takefocus=False)
        self._editor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        #style = self._reader.style
        #inserter = self._reader.inserter
        restriction = self._front.manager.restriction
        self._viewer = Viewer(self._editor, restriction=restriction,
                              style=self._front.manager.viewer_style,
                              on_press_left=self._open_prev_page,
                              on_press_right=self._open_next_page,
                              update_sys_path=False)
        if not self._viewer.open(self._filename):
            self._failed = True
            return
        on_open = lambda viewer, filename: self._open_page(filename)
        self._viewer.on_open = on_open

    def _on_map(self):
        self._bind_events_handlers()
        self._editor.focus_set()

    def _on_remap(self):
        self._editor.focus_set()

    def _bind_events_handlers(self):
        top = self._front.top
        # refresh
        self._editor.bind("<F5>", lambda e: self._front.refresh())
        # home
        self._editor.bind("<h>", lambda e: top.click_home())
        self._editor.bind("<H>", lambda e: top.click_home())
        # toc
        self._editor.bind("<t>", lambda e: top.click_toc())
        self._editor.bind("<T>", lambda e: top.click_toc())
        # mark
        self._editor.bind("<i>", lambda e: top.click_info())
        self._editor.bind("<I>", lambda e: top.click_info())
        # goto
        self._editor.bind("<g>", lambda e: top.click_goto())
        self._editor.bind("<G>", lambda e: top.click_goto())
        # past
        self._editor.bind("<p>", lambda e: top.click_past())
        self._editor.bind("<P>", lambda e: top.click_past())
        # search
        self._editor.bind("<s>", lambda e: top.click_search())
        self._editor.bind("<S>", lambda e: top.click_search())
        # about
        self._editor.bind("<a>", lambda e: top.click_about())
        self._editor.bind("<A>", lambda e: top.click_about())
        # find
        self._editor.bind("<f>", lambda e: self._on_press_key_f())
        self._editor.bind("<F>", lambda e: self._on_press_key_f())
        # switcher controls
        self._editor.bind("<Control-KeyPress-Tab>", self._open_switcher)

    def _open_switcher(self, e):
        switcher = Switcher(self._front)
        switcher.build(self.body)
        return "break"

    def _on_press_key_f(self):
        self._front.footer.enable_finder()

    def _open_page(self, filename):
        self._front.open(filename)

    def _open_prev_page(self):
        footer = self._front.footer
        if not footer:
            return
        footer.open_prev_page()

    def _open_next_page(self):
        footer = self._front.footer
        if not footer:
            return
        footer.open_next_page()
