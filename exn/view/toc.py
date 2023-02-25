import tkinter as tk
from tkinter import ttk
import tkutil
from viewable import Viewable
from exn import constant
from tkinter.font import Font
from exonote.editor import Editor
from exn.theme import Constants as theme_const


class Toc(Viewable):
    def __init__(self, front):
        super().__init__()
        self._front = front
        self._editor = None
        self._sections = list()
        self._sid = None
        self._index = -1

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="toc")

    def _build(self):
        self.body.title("")
        self.body.minsize(*constant.WINDOW_MINSIZE)
        self.body.bind("<Escape>", lambda e: self.body.destroy())
        tkutil.restore_size(self.body, name="exn_toc",
                            default=constant.TOC_WINDOW_SIZE)
        #self.body.geometry(constant.DIALOG_GEOMETRY)
        #self.body.resizable(False, False)
        # frame 1
        frame1 = tk.Frame(self.body)
        frame1.pack(pady=5)
        # frame 2
        frame2 = tk.Frame(self.body)
        frame2.pack(fill=tk.BOTH, expand=True)
        # frame 3
        frame3 = tk.Frame(self.body)
        frame3.pack(fill=tk.X)
        # label Toc
        label = tk.Label(frame1, name="title",
                         text="Table of contents")
        label.pack()
        # install scrolled text
        self._editor = Editor(frame2, wrap="word", cursor="arrow", takefocus=True,
                              scrollbar_style="window.Vertical.TScrollbar")
        self._editor.pack(fill=tk.BOTH, expand=True)
        self._editor.config(padx=10, pady=20)
        self._editor.bind("<Left>", lambda e: self._on_press_up())
        self._editor.bind("<Right>", lambda e: self._on_press_down())
        self._editor.bind("<Up>", lambda e: self._on_press_up())
        self._editor.bind("<Down>", lambda e: self._on_press_down())
        self._editor.bind("<Return>", lambda e: self._on_open())
        # button close
        button = ttk.Button(frame3, name="close", style="red.TButton", text="Close",
                           command=self.body.destroy)
        button.pack(side=tk.LEFT, padx=3, pady=3)

        # center the window
        editor = self._front.board.viewer.editor
        tkutil.align(self.body, parent=editor, side="nw",
                     correction=(10, 10))
        tkutil.make_modal(self.body)

    def _on_map(self):
        self._define_tag()
        self._bind_handlers_to_tag()
        sections = self._get_sections()
        self._sections = sections
        self._n = len(sections)
        for section in sections:
            sid = section.sid
            indent = "  " * (section.level)
            text = indent + section.text + "\n"
            self._editor.insert(tk.INSERT, text, ("link", sid))
            self._editor.insert(tk.INSERT, "\n")
            command = lambda e, sid=section.sid: self._on_click_link(sid)
            self._editor.tag_bind(section.sid, "<ButtonPress-1>",
                                  command, True)
            command = lambda e, sid=sid: self._on_enter(sid)
            self._editor.tag_bind(sid, "<Enter>", command, True)
            command = lambda e, sid=sid: self._on_leave(sid)
            self._editor.tag_bind(sid, "<Leave>", command, True)
        height = 3
        if sections:
            n = (len(sections) * 2) - 1
            height = 10
            if n < height:
                height = n
        self._editor.config(height=height, state="disabled")
        self._editor.focus_set()

    def _on_remap(self):
        pass

    def _on_destroy(self):
        tkutil.save_size(self.body, name="exn_toc")

    def _define_tag(self):
        style = self._front.manager.viewer_style
        # link
        font = Font(family=style.font_family,
                    size=style.font_size)
        foreground = theme_const.TOC_ENTRY_FOREGROUND
        spacing1 = spacing3 = 5
        spacing2 = spacing1 + spacing3
        self._editor.tag_configure("link", font=font, spacing1=spacing1,
                                   spacing2=spacing2, spacing3=spacing3,
                                   foreground=foreground)

    def _bind_handlers_to_tag(self):
        on_enter = lambda event, editor=self._editor: editor.config(cursor="hand1")
        on_leave = lambda event, editor=self._editor: editor.config(cursor="")
        # bind hand icon to codeblock (enter vs leave)
        self._editor.tag_bind("link", "<Enter>", on_enter, True)
        #self._editor.tag_bind("link", "<Leave>", on_leave, True)

    def _on_enter(self, sid):
        if self._sid:
            self._unhighlight(self._sid)
        for i, section in enumerate(self._sections):
            if section.sid == sid:
                self._index = i
        self._sid = sid
        self._highlight(sid)

    def _on_leave(self, sid):
        return
        #self._sid = sid
        #self._unhighlight(sid)

    def _highlight(self, sid):
        background = theme_const.TOC_ENTRY_ACTIVE_BACKGROUND
        self._editor.tag_configure(sid, background=background)

    def _unhighlight(self, sid):
        background = theme_const.TOPLEVEL_BACKGROUND
        self._editor.tag_configure(sid, background=background)

    def _get_sections(self):
        sections = list()
        viewer = self._front.board.viewer
        if not viewer:
            return sections
        for sid in viewer.sids:
            info = viewer.get_heading(sid, include_text=True)
            sections.append(info)
        return sections

    def _on_click_link(self, sid):
        self._front.board.viewer.goto(sid)
        self.body.destroy()

    def _on_press_up(self):
        if self._sid:
            self._unhighlight(self._sid)
        self._index -= 1
        n = len(self._sections)
        if self._index < 0:
            self._index = n - 1
        section = self._sections[self._index]
        sid = section.sid
        self._sid = sid
        self._highlight(sid)
        return "break"

    def _on_press_down(self):
        if self._sid:
            self._unhighlight(self._sid)
        self._index += 1
        n = len(self._sections)
        if self._index >= n:
            self._index = 0
        section = self._sections[self._index]
        sid = section.sid
        self._sid = sid
        self._highlight(sid)
        return "break"

    def _on_open(self):
        if not self._sid:
            return
        self._on_click_link(self._sid)
