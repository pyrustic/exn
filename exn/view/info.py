import tkinter as tk
from tkinter import ttk
import tkutil
from viewable import Viewable
from exn.view import util


class Info(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front
        self._title_strvar = tk.StringVar()
        self._page_strvar = tk.StringVar()
        self._filename_strvar = tk.StringVar()
        self._tags_strvar = tk.StringVar()
        self._mark_button = None

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="info")

    def _build(self):
        self.body.bind("<Escape>", lambda e: self._on_close())
        self.body.title("")
        #self.body.minsize(*constant.WINDOW_MINSIZE)
        #tkutil.restore_size(self.body, name="exn_info",
        #                    default=constant.INFO_WINDOW_SIZE)
        # labels
        frame1 = tk.Frame(self.body)
        frame1.pack(pady=5)
        frame2 = tk.Frame(self.body, name="info_card")
        frame2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        frame3 = tk.Frame(self.body)
        frame3.pack(fill=tk.X, padx=3, pady=(15, 3))
        # Info
        info_label = tk.Label(frame1, name="title", text="Info")
        info_label.pack()
        # note title
        title_field = tk.Entry(frame2, name="title_field",
                               width=30,
                               textvariable=self._title_strvar,
                               state="disabled", takefocus=False,
                               cursor="arrow")
        title_field.pack(fill=tk.X, padx=5, pady=3)
        # page and filename frame
        frame = tk.Frame(frame2)
        frame.pack(fill=tk.X, padx=5, pady=(0, 3))
        # page number
        page_label = tk.Label(frame, name="page_label",
                              textvariable=self._page_strvar)
        page_label.pack(side=tk.LEFT)
        # note filename
        filename_field = tk.Entry(frame, name="filename_field",
                                  textvariable=self._filename_strvar,
                                  state="disabled", takefocus=False,
                                  cursor="arrow")
        filename_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        # note tags
        tags_field = tk.Entry(frame2, name="tags_field",
                              textvariable=self._tags_strvar,
                              state="disabled", takefocus=False,
                              cursor="arrow")
        tags_field.pack(fill=tk.X, padx=5, pady=(0, 3))
        # footer
        close_button = ttk.Button(frame3, name="close", style="red.TButton",
                                  text="Close", command=self._on_close)
        close_button.pack(side=tk.LEFT)
        self._mark_button = ttk.Button(frame3, name="mark", text="Mark",
                                      command=self._on_click_mark)
        self._mark_button.pack(side=tk.RIGHT)
        copy_button = ttk.Button(frame3, name="copy", text="Copy",
                                command=self._on_copy)
        copy_button.pack(side=tk.RIGHT, padx=3)
        # center the window
        editor = self._front.board.viewer.editor
        tkutil.align(self.body, parent=editor, side="n")
        tkutil.make_modal(self.body)

    def _on_map(self):
        self._populate()
        filename = self._front.filename
        if self._front.manager.dao.is_bookmarked(filename):
            util.set_marked_style(self._mark_button, small=False)

    def _on_destroy(self):
        return
        #tkutil.save_size(self.body, name="exn_past")

    def _populate(self):
        title, page, filename, tags = self._get_data()
        self._title_strvar.set(title)
        self._page_strvar.set(page + ".")
        self._filename_strvar.set(filename)
        self._tags_strvar.set(tags)

    def _get_data(self):
        index = self._front.manager.index
        title = page = filename = tags = ""
        for item in index:
            if item.filename == self._front.filename:
                title = item.title
                page = str(item.page)
                filename = item.filename
                tags = ["#{}".format(tag) for tag in item.tags]
                tags = " ".join(tags)
                break
        return title, page, filename, tags

    def _on_copy(self):
        title = self._title_strvar.get()
        page = self._page_strvar.get()
        filename = self._filename_strvar.get()
        tags = self._tags_strvar.get()
        text = "{}\n{} {}\n{}".format(title, page, filename, tags)
        util.update_clipboard(text, self.body)

    def _on_click_mark(self):
        filename = self._front.filename
        if not filename:
            return
        util.on_click_mark_button(self._mark_button, filename,
                                  self._front.manager.dao, small=False)

    def _on_close(self):
        self.body.withdraw()
        self.body.destroy()
