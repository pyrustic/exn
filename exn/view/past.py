import tkinter as tk
import tkutil
from viewable import Viewable
from exn import constant
from exn.view.roll import Roll


class Past(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front
        self._roll = None

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="past")

    def _build(self):
        self.body.bind("<Escape>", lambda e: self._on_close())
        self.body.title("")
        self.body.minsize(*constant.WINDOW_MINSIZE)
        tkutil.restore_size(self.body, name="exn_past",
                            default=constant.PAST_WINDOW_SIZE)

        #self.body.resizable(False, False)
        # label title
        frame1 = tk.Frame(self.body)
        frame1.pack(pady=5)
        label = tk.Label(frame1, name="title", text="Past history")
        label.pack()
        # get data and populate roll
        data = self._get_history_data()
        frame2 = tk.Frame(self.body)
        frame2.pack(fill=tk.BOTH, expand=True)
        self._roll = Roll(self._front, data, on_open=self._open_note,
                          on_close=self._on_close)
        self._roll.build_pack(frame2, fill=tk.BOTH, expand=True)
        self._roll.select(0)
        # center the window
        editor = self._front.board.viewer.editor
        tkutil.align(self.body, parent=editor, side="n")
        tkutil.make_modal(self.body)

    def _on_map(self):
        self._roll.body.focus_set()
        pass

    def _on_destroy(self):
        tkutil.save_size(self.body, name="exn_past")

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

    def _open_note(self, filename):
        self.body.withdraw()
        self._front.open(filename)
        self.body.destroy()

    def _on_close(self):
        self.body.withdraw()
        self.body.destroy()
