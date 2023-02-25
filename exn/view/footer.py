import tkinter as tk
from tkinter import ttk
from viewable import Viewable


class Footer(Viewable):
    def __init__(self, front, on_leave_focus=None):
        super().__init__()
        self._front = front
        self._on_leave_focus = on_leave_focus
        self._page_number = 0
        self._total_pages = 0
        self._finder = None
        self._page_status_strvar = tk.StringVar()
        self._page_status_entry = None
        self._right_frame = None

    @property
    def finder(self):
        return self._finder

    def update_page_status(self, filename):
        viewer = self._front.board.viewer
        pages = viewer.pages
        page_info = pages.get(filename)
        if not page_info:
            return
        self._total_pages = len(pages)
        self._page_number = page_info.page
        text = "Page {} of {}".format(self._page_number,
                                      self._total_pages)
        self._page_status_strvar.set(text)
        #n = len(text)
        #self._page_status_entry.config(width=n)

    def enable_finder(self):
        if not self._finder:
            return
        self._finder.enable()

    def open_prev_page(self):
        self._on_click_prev_page()

    def open_next_page(self):
        self._on_click_next_page()

    def _create_body(self, parent):
        return ttk.Frame(parent, name="footer")

    def _build(self):
        self._install_left_frame()
        self._install_right_frame()

    def _on_map(self):
        pass

    def _install_left_frame(self):
        # left frame
        left_frame = ttk.Frame(self.body)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3, pady=3)
        self._finder = Finder(self._front, on_enable=self._hide_right_frame,
                              on_disable=self._unhide_right_frame,
                              on_leave_focus=self._on_leave_focus)
        self._finder.build_pack(left_frame, side=tk.LEFT, fill=tk.X, expand=True)

    def _install_right_frame(self):
        # right frame
        self._right_frame = ttk.Frame(self.body, name="navframe")
        self._right_frame.pack(side=tk.RIGHT, pady=3,
                               fill=tk.X, expand=True)
        # button next
        next_button = ttk.Button(self._right_frame, text="Next",
                                takefocus=False,
                                command=self._on_click_next_page)
        next_button.pack(side=tk.RIGHT, padx=(0, 3))
        # button previous
        prev_button = ttk.Button(self._right_frame, text="Prev",
                                takefocus=False,
                                command=self._on_click_prev_page)
        prev_button.pack(side=tk.RIGHT, padx=(0, 3))
        # page number
        self._page_status_entry = tk.Entry(self._right_frame,
                                           name="page_number",
                                           justify=tk.RIGHT,
                                           width=0,
                                           takefocus=False,
                                           textvariable=self._page_status_strvar)
        self._page_status_entry.pack(side=tk.RIGHT, padx=(0, 15), fill=tk.X,
                                     expand=True)
        self._page_status_entry.bind("<FocusIn>",
                                     lambda e: self._on_page_status_entry_focus())

    def _on_click_next_page(self):
        if self._page_number == self._total_pages:
            next_page_number = 1
        else:
            next_page_number = self._page_number + 1
        self._page_number = next_page_number
        pages = self._front.board.viewer.pages
        page_info = list(pages.values())[next_page_number - 1]
        self._front.open(page_info.filename)
        #self._update_page_status()

    def _on_click_prev_page(self):
        if self._page_number == 0:
            next_page_number = self._total_pages
        else:
            next_page_number = self._page_number - 1
        self._page_number = next_page_number
        pages = self._front.board.viewer.pages
        page_info = list(pages.values())[next_page_number - 1]
        self._front.open(page_info.filename)
        #self._update_page_status()

    def _on_page_status_entry_focus(self):
        if self._on_leave_focus:
            self._on_leave_focus()

    def _hide_right_frame(self):
        if self._right_frame:
            self._right_frame.pack_forget()

    def _unhide_right_frame(self):
        if self._right_frame:
            self._right_frame.pack(side=tk.RIGHT, pady=3,
                                   fill=tk.X, expand=True)


class Finder(Viewable):
    def __init__(self, front, on_enable=None, on_disable=None,
                 on_leave_focus=None):
        super().__init__()
        self._front = front
        self._on_enable = on_enable
        self._on_disable = on_disable
        self._on_leave_focus = on_leave_focus
        self._input_strvar = tk.StringVar()
        self._case_intvar = tk.IntVar()
        self._regex_intvar = tk.IntVar()
        self._status_strvar = tk.StringVar()
        self._finder_entry = None
        self._options_frame = None
        self._nav_frame = None
        self._status_frame = None
        self._cancel_button = None
        self._highlights = list()
        self._highlighted = str()
        self._active_highlight_position = -1

    @property
    def finder_entry(self):
        return self._finder_entry

    def enable(self):
        if self._on_enable:
            self._on_enable()
        keep_input = True
        state = str(self._finder_entry.cget("state"))
        if state == "disabled":
            keep_input = False
        self._clear_finder(keep_input)
        self._options_frame.pack(side=tk.LEFT)
        self._cancel_button.pack(side=tk.RIGHT)
        self._finder_entry.config(cursor="xterm")

    def disable(self):
        if self._on_disable:
            self._on_disable()
        self._clear_finder_state()
        self._input_strvar.set("Find in page...")
        self._finder_entry.config(state="disabled", cursor="hand1")
        self._options_frame.pack_forget()
        self._nav_frame.pack_forget()
        self._status_frame.pack_forget()
        self._cancel_button.pack_forget()
        if self._on_leave_focus:
            self._on_leave_focus()

    def clear_finder(self, keep_input=False):
        self._clear_finder(keep_input)

    def _create_body(self, parent):
        return ttk.Frame(parent)

    def _build(self):
        # find entry
        self._finder_entry = tk.Entry(self.body, name="finder", takefocus=True,
                                      textvariable=self._input_strvar)
        self._finder_entry.pack(side=tk.LEFT)
        #self._finder_entry.bind("<FocusIn>",
        #                        lambda e: self._on_finder_focus(), True)
        self._finder_entry.bind("<Return>",
                                lambda e: self._on_find(), True)
        self._finder_entry.bind("<Up>", lambda e: self._on_click_prev_match())
        self._finder_entry.bind("<Down>", lambda e: self._on_click_next_match())
        self._finder_entry.bind("<Escape>", lambda e: self.disable(), True)
        self._finder_entry.bind("<FocusIn>", lambda e: self.enable(), True)
        self._finder_entry.bind("<Button-1>", lambda e: self.enable(), True)

        # finder controls
        self._options_frame = ttk.Frame(self.body)
        self._options_frame.pack(side=tk.LEFT)
        # button clear
        button_clear = ttk.Button(self._options_frame, style="clear.TButton",
                                  text="X", command=self._clear_finder)
        button_clear.pack(side=tk.LEFT, padx=3)
        # case checkbutton
        case_checkbutton = ttk.Checkbutton(self._options_frame,
                                          text="mc", variable=self._case_intvar,
                                          onvalue=1, offvalue=0)
        case_checkbutton.pack(side=tk.LEFT, padx=3, fill=tk.Y)
        # regex checkbutton
        regex_checkbutton = ttk.Checkbutton(self._options_frame,
                                           text="re", variable=self._regex_intvar,
                                           onvalue=1, offvalue=0)
        regex_checkbutton.pack(side=tk.LEFT, padx=(0, 3), fill=tk.Y)

        self._nav_frame = ttk.Frame(self.body)
        self._nav_frame.pack(side=tk.LEFT)
        # left arrow button
        left_arrow_button = ttk.Button(self._nav_frame, text="<",
                                      command=self._on_click_prev_match)
        left_arrow_button.pack(side=tk.LEFT, padx=(3, 0))
        # right arrow button
        right_arrow_button = ttk.Button(self._nav_frame, text=">",
                                       command=self._on_click_next_match)
        right_arrow_button.pack(side=tk.LEFT, padx=(3, 0))
        # status
        self._status_frame = ttk.Frame(self.body)
        self._status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._status_entry = tk.Entry(self._status_frame, name="finder_status",
                                      width=0, takefocus=False,
                                      state="readonly", cursor="arrow",
                                      textvariable=self._status_strvar)
        self._status_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        # button cancel
        self._cancel_button = ttk.Button(self.body, name="close", style="red.TButton",
                                         text="Cancel",
                                        command=self.disable)
        self._cancel_button.pack(side=tk.RIGHT)

    def _on_map(self):
        self.disable()

    def _on_find(self):
        if self._finder_entry.cget("state") == "disabled":
            return
        word = self._input_strvar.get()
        if not word or word.isspace():
            self._clear_finder()
            return
        if word == self._highlighted:
            self._on_click_next_match()
            return
        self._clear_finder(keep_input=True)
        self._nav_frame.pack(side=tk.LEFT)
        self._status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._highlighted = word
        index = "1.0"
        nocase = self._case_intvar.get()
        nocase = False if nocase == 1 else True
        use_regex = self._regex_intvar.get()
        use_regex = True if use_regex == 1 else False
        editor = self._front.board.editor
        # search
        while True:
            try:
                index = editor.search(word, index, stopindex=tk.END,
                                            nocase=nocase, regexp=use_regex)
            except Exception as e:
                return
            if not index:
                break
            index2 = "{}+{}c".format(index, len(word))
            editor.tag_add("highlight", index, index2)
            self._highlights.append((index, index2))
            index = index2
        if self._highlights:
            if len(self._highlights) == 1:
                self._nav_frame.pack_forget()
            self._on_click_next_match()
        else:
            self._clear_finder_state()
            self._clear_finder_ui(keep_input=True)
            self._status_strvar.set("No matches !")
            self._status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _on_click_prev_match(self):
        matches_count = len(self._highlights)
        if not matches_count:
            return
        if self._active_highlight_position == 0:
            next_position = matches_count - 1
        else:
            next_position = self._active_highlight_position - 1
        self._active_highlight_position = next_position
        if matches_count == 1:
            status = "1 match"
        else:
            status = "{} of {} matches".format(next_position+1, matches_count)
        self._status_strvar.set(status)
        x, y = self._highlights[next_position]
        editor = self._front.board.editor
        editor.tag_remove("active_highlight", "1.0", tk.END)
        editor.tag_add("active_highlight", x, y)
        editor.see(x)

    def _on_click_next_match(self):
        matches_count = len(self._highlights)
        if not matches_count:
            return
        if self._active_highlight_position == (matches_count - 1):
            next_position = 0
        else:
            next_position = self._active_highlight_position + 1
        self._active_highlight_position = next_position
        if matches_count == 1:
            status = "1 match"
        else:
            status = "{} of {} matches".format(next_position+1, matches_count)
        self._status_strvar.set(status)
        x, y = self._highlights[next_position]
        editor = self._front.board.editor
        editor.tag_remove("active_highlight", "1.0", tk.END)
        editor.tag_add("active_highlight", x, y)
        editor.see(x)

    def _clear_finder(self, keep_input=False):
        self._clear_finder_state()
        self._clear_finder_ui(keep_input)

    def _clear_finder_ui(self, keep_input=False):
        self._finder_entry.config(state="normal")
        if not keep_input:
            self._input_strvar.set("")
        self._nav_frame.pack_forget()
        self._status_frame.pack_forget()
        self._finder_entry.focus_set()

    def _clear_finder_state(self):
        self._highlights = list()
        self._highlighted = str()
        self._active_highlight_position = -1
        self._status_strvar.set("")
        editor = self._front.board.editor
        editor.tag_remove("active_highlight", "1.0", tk.END)
        editor.tag_remove("highlight", "1.0", tk.END)
