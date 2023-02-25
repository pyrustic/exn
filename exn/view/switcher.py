import tkinter as tk
from tkinter import ttk
import tkutil
from viewable import Viewable
from exn import constant
from exn.view.roll import Roll


class Switcher(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front
        self._scrolled_text = None
        self._current_index = 0
        self._previous_index = None
        self._history = list()
        self._widgets = list()

    @property
    def front(self):
        return self._front

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="switcher")

    def _build(self):
        self.body.bind("<Tab>", lambda e: "break", add=True)
        self.body.bind("<KeyRelease>", self._on_key_release, add=True)
        self.body.title("")
        self.body.minsize(*constant.WINDOW_MINSIZE)
        tkutil.restore_size(self.body, name="exn_switcher",
                            default=constant.SWITCHER_WINDOW_SIZE)
        # label title
        frame1 = ttk.Frame(self.body)
        frame1.pack()
        label = tk.Label(frame1, name="title", text="Switcher")
        label.pack()
        frame2 = ttk.Frame(self.body)
        frame2.pack(fill=tk.BOTH, expand=True)
        # get history data and populate roll
        self._history = self._get_history_data()
        self._roll = Roll(self._front, self._history,
                          on_close=self._on_close,
                          on_open=self._open_note)
        self._roll.build_pack(frame2, fill=tk.BOTH, expand=True)
        # center window
        editor = self._front.board.viewer.editor
        tkutil.center(self.body, parent=editor)
        tkutil.make_modal(self.body)

    def _on_map(self):
        if not self._history:
            self.body.destroy()
            return
        current_index = 0
        if len(self._history) >= 2:
            current_index = 1
        self._roll.select(current_index)

    def _on_destroy(self):
        tkutil.save_size(self.body, name="exn.view.switcher")

    def _on_key_release(self, e):
        keysym = e.keysym
        if keysym in constant.CONTROL_KEYS:
            info = self._roll.get_selection()
            if info:
                self._open_note(info)
            self.body.destroy()

    def _on_select_prev(self, e):
        return "break"

    def _on_select_next(self, e):
        return "break"

    def _open_note(self, info):
        self._front.open(info.filename)

    def _get_history_data(self):
        manager = self._front.manager
        viewer = self._front.board.viewer
        #h = manager.history
        h = manager.dao.get_history()
        data = list()
        for item in h:
            info = viewer.pages.get(item)
            if not info:
                continue
            data.append(info)
        return data

    def _on_close(self):
        self.body.destroy()
