import tkinter as tk
from tkinter import ttk
from viewable import Viewable
from exn.view import util
from viewstack import ViewStack
from exn.theme import Constants as ThemeConstants


class Roll(Viewable):
    def __init__(self, front, data, on_open=None,
                 on_close=None, on_leave_focus=None,
                 max_entries=5):
        # target = "all" or "past"
        super().__init__()
        self._front = front
        self._data = data
        self._on_open = on_open
        self._on_close = on_close
        self._on_leave_focus = on_leave_focus
        self._max_entries = max_entries
        self._list_status_strvar = tk.StringVar()
        self._total_lists = 0
        self._main_frame = None
        self._footer_frame = None
        self._nav_frame = None
        self._cache = dict()
        self._current_list_index = 0
        self._current_entry_index = None
        self._entries_frames = list()
        self._viewstack = None

    @property
    def front(self):
        return self._front

    def select(self, entry_index=0):
        if not self.body or not self.body.winfo_exists():
            return
        s = self._viewstack.selection
        if not s:
            return
        self.body.focus_set()
        return s.view.select(entry_index)

    def get_selection(self):
        if not self.body or not self.body.winfo_exists():
            return
        s = self._viewstack.selection
        if not s:
            return
        return s.view.get_selection()

    def open_list(self, list_index):
        if not self.body or not self.body.winfo_exists():
            return
        if list_index != self._current_list_index:
            self._update_roll(list_index)

    def _create_body(self, parent):
        return tk.Frame(parent, name="roll", takefocus=True)

    def _build(self):
        #self.body.bind("<FocusIn>", lambda e: self._on_focus_in())
        self.body.bind("<Up>", lambda e: self._on_press_up())
        self.body.bind("<Down>", lambda e: self._on_press_down())
        self.body.bind("<Left>", lambda e: self._on_press_left())
        self.body.bind("<Right>", lambda e: self._on_press_right())
        self.body.bind("<Return>", lambda e: self._on_open_selection())
        self.body.bind("<Tab>", lambda e: self._on_press_down())
        self._install_main_frame()
        self._install_footer()
        self._update_total_lists_var()
        self._update_roll(0, None)

    def _on_map(self):
        pass

    def _install_main_frame(self):
        # install roll
        self._main_frame = tk.Frame(self.body, name="main_frame", takefocus=False)
        self._main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)
        self._main_frame.columnconfigure(0, weight=1)
        self._main_frame.rowconfigure(0, weight=1)
        # init viewstack
        self._viewstack = ViewStack(self._main_frame)

    def _install_footer(self):
        # install footer
        self._footer_frame = tk.Frame(self.body, takefocus=False)
        self._footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        button_close = ttk.Button(self._footer_frame, style="red.TButton",
                                  name="close", text="Close", command=self._on_close)
        button_close.pack(side=tk.LEFT, padx=3, pady=3)
        self._install_nav_frame()

    def _install_nav_frame(self):
        self._nav_frame = tk.Frame(self._footer_frame, name="nav_frame", takefocus=False)
        self._nav_frame.pack(side=tk.RIGHT, padx=3, pady=3)
        # button next
        next_button = ttk.Button(self._nav_frame, text="Next", command=self._on_click_next)
        next_button.pack(side=tk.RIGHT, padx=(3, 0))
        # button prev
        prev_button = ttk.Button(self._nav_frame, text="Prev", command=self._on_click_prev)
        prev_button.pack(side=tk.RIGHT, padx=(3, 0))
        # status
        nav_status = tk.Entry(self._nav_frame, name="nav_status",
                              justify=tk.RIGHT, width=0, takefocus=False,
                              textvariable=self._list_status_strvar)
        nav_status.pack(side=tk.RIGHT, padx=(3, 10), fill=tk.X, expand=True)

    def _update_roll(self, list_index=0, entry_index=None):
        self._update_total_lists_status()
        if list_index < 0 or list_index >= len(self._data):
            return
        list_name = "list_{}".format(list_index)
        if list_name in self._viewstack.views:
            self._viewstack.lift(list_name)
            view = self._viewstack.selection.view
        else:
            view = EntriesList(self._front, self._data, list_index,
                               self._on_open, self._on_leave_focus,
                               max_entries=5)
            self._viewstack.add(list_name, view)
        if entry_index is not None:
            view.select(entry_index)

    def _on_press_left(self):
        self._on_click_prev()

    def _on_press_right(self):
        self._on_click_next()

    def _on_click_next(self):
        self.body.focus_set()
        self._unhighlight_selection()
        self._current_entry_index = 0
        self._current_list_index += 1
        if self._current_list_index >= self._total_lists:
            self._current_list_index = 0
        self._update_roll(self._current_list_index, 0)
        self._highlight_selection()

    def _on_click_prev(self):
        self.body.focus_set()
        self._unhighlight_selection()
        self._current_entry_index = 0
        self._current_list_index -= 1
        if self._current_list_index < 0:
            self._current_list_index = self._total_lists - 1
        self._update_roll(self._current_list_index, 0)
        self._highlight_selection()

    def _on_press_up(self):
        s = self._viewstack.selection
        if not s:
            return
        s.view.go_up()

    def _on_press_down(self):
        s = self._viewstack.selection
        if not s:
            return
        s.view.go_down()

    def _on_open_selection(self):
        s = self._viewstack.selection
        if not s:
            return
        s.view.open_selection()

    def _update_total_lists_var(self):
        self._current_list_index = 0
        data_size = len(self._data)
        if data_size <= self._max_entries:
            self._total_lists = 1
            return
        x = data_size // self._max_entries
        y = data_size % self._max_entries
        if y != 0:
            x += 1
        self._total_lists = x

    def _update_total_lists_status(self):
        text = "List {} of {}".format(self._current_list_index + 1,
                                      self._total_lists)
        self._list_status_strvar.set(text)

    def _highlight_selection(self):
        s = self._viewstack.selection
        if not s:
            return
        s.view.highlight_selection()

    def _unhighlight_selection(self):
        s = self._viewstack.selection
        if not s:
            return
        s.view.unhighlight_selection()


class EntriesList(Viewable):
    def __init__(self, front, data, list_index, on_open,
                 on_leave_focus, max_entries=5):
        super().__init__()
        self._front = front
        self._data = data
        self._list_index = list_index
        self._on_open = on_open
        self._on_leave_focus = on_leave_focus
        self._max_entries = max_entries
        self._list_status_strvar = tk.StringVar()
        self._total_lists = 0
        self._main_frame = None
        self._footer_frame = None
        self._nav_frame = None
        self._cache = dict()
        self._selected_entry_index = None
        self._entries_frames = list()

    def select(self, entry_index=0):
        if not self.body:
            return
        if entry_index is None:
            self.unhighlight_selection()
            self._selected_entry_index = None
            return
        n = len(self._entries_frames)
        if entry_index < 0:
            entry_index = n - abs(entry_index)
        if entry_index > n - 1:
            return False
        self.unhighlight_selection()
        self._selected_entry_index = entry_index
        self.highlight_selection()
        return True

    def open_selection(self):
        if self._selected_entry_index is None:
            return
        if self._list_index is None:
            return
        i = (self._list_index * self._max_entries) + self._selected_entry_index
        try:
            item = self._data[i]
        except IndexError as e:
            return False
        self._on_click_open(item.filename)
        return True

    def get_selection(self):
        if self._selected_entry_index is None:
            return
        x = self._max_entries * self._list_index
        x += self._selected_entry_index
        info = self._data[x]
        return info

    def highlight_selection(self):
        if self._selected_entry_index is None:
            return
        try:
            entry_frame = self._entries_frames[self._selected_entry_index]
        except IndexError as e:
            return
        color = ThemeConstants.ROLL_ENTRY_ACTIVE_HIGHLIGHT
        entry_frame.config(highlightbackground=color)
        #entry_frame.focus_set()

    def unhighlight_selection(self):
        if self._selected_entry_index is None:
            return
        try:
            entry_frame = self._entries_frames[self._selected_entry_index]
            self.body.focus_lastfor()
        except IndexError as e:
            return
        color = ThemeConstants.ROLL_ENTRY_HIGHLIGHT
        entry_frame.config(highlightbackground=color)

    def go_up(self):
        self._on_press_up()

    def go_down(self):
        self._on_press_down()

    def _build(self):
        data = self._extract_list_data(self._list_index)
        for i, item in enumerate(data):
            title = item.title if item.title else "- No title -"
            tags = ["#" + tag for tag in item.tags]
            tags = " ".join(tags)
            ef = self._install_result_entry(self.body, i, item.filename, item.page,
                                            title, tags)
            self._entries_frames.append(ef)

    def _install_result_entry(self, parent, index, filename, page, title, tags):
        frame = tk.Frame(parent, takefocus=False)
        frame.pack(padx=10, pady=5, fill=tk.X)
        # left frame
        left_frame = tk.Frame(frame, takefocus=False)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True,
                        padx=5, pady=5)
        left_frame.bind("<Enter>", lambda e: self.select(index))
        left_frame.bind("<Button-1>",
                        lambda e: self._on_click_open(filename))
        # right frame
        right_frame = tk.Frame(frame, takefocus=False)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        right_frame.bind("<Enter>", lambda e: self.select(index))
        right_frame.bind("<Button-1>",
                         lambda e: self._on_click_open(filename))
        # title entry
        title_entry = tk.Entry(left_frame, name="title_field",
                               takefocus=False, cursor="arrow")
        title_entry.pack(fill=tk.X, pady=(0, 2))
        title_entry.insert(0, title)
        title_entry.config(state="disabled")
        title_entry.bind("<Enter>", lambda e: self.select(index))
        title_entry.bind("<Button-1>", lambda e: self._on_click_open(filename))
        command = lambda e: util.update_clipboard(title, self.body)
        title_entry.bind("<Button-3>", command)
        #title_entry.bind("<FocusIn>", lambda e: self.select(index))
        # filename entry and page number
        filename_frame = tk.Frame(left_frame)
        filename_frame.pack(fill=tk.X, pady=(0, 2))
        text = "{}.".format(page)
        page_label = tk.Label(filename_frame, padx=0, name="page_label", text=text)
        page_label.pack(side=tk.LEFT, pady=0)
        filename_entry = tk.Entry(filename_frame, name="filename_field",
                                  takefocus=False, cursor="arrow")
        filename_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 0))
        filename_entry.insert(0, filename)
        filename_entry.config(state="disabled")
        filename_entry.bind("<Enter>", lambda e: self.select(index))
        filename_entry.bind("<Button-1>", lambda e: self._on_click_open(filename))
        command = lambda e: util.update_clipboard(filename, self.body)
        filename_entry.bind("<Button-3>", command)
        # tags entry
        tags_entry = tk.Entry(left_frame, name="tags_field",
                              takefocus=False, cursor="arrow")
        tags_entry.pack(fill=tk.X)
        tags_entry.insert(0, tags)
        tags_entry.config(state="disabled")
        tags_entry.bind("<Enter>", lambda e: self.select(index))
        tags_entry.bind("<Button-1>", lambda e: self._on_click_open(filename))
        command = lambda e: util.update_clipboard(tags, self.body)
        tags_entry.bind("<Button-3>", command)
        # mark button
        mark_button = ttk.Button(right_frame, text="Mark", takefocus=False)
        mark_button.pack(side=tk.TOP, pady=(0, 3))
        command = lambda: self._on_click_mark(mark_button, filename)
        mark_button.config(command=command)
        if self._front.manager.dao.is_bookmarked(filename):
            util.set_marked_style(mark_button, small=False)
        # copy button
        text = "{}\n{}. {}\n{}".format(title, page, filename, tags)
        command = lambda: util.update_clipboard(text, self.body)
        copy_button = ttk.Button(right_frame, text="Copy",
                                command=command, takefocus=False)
        copy_button.pack(side=tk.BOTTOM, pady=0)

        return frame

    def _extract_list_data(self, list_index):
        list_index = list_index if list_index == 0 else self._max_entries * list_index
        index_begin = list_index
        index_end = index_begin + self._max_entries
        if not self._data:
            return list()
        return self._data[index_begin:index_end]

    def _update_total_lists_var(self):
        self._list_index = 0
        data_size = len(self._data)
        if data_size <= self._max_entries:
            self._total_lists = 1
            return
        x = data_size // self._max_entries
        y = data_size % self._max_entries
        if y != 0:
            x += 1
        self._total_lists = x

    def _on_press_up(self):
        if self._selected_entry_index is None:
            return
        self.unhighlight_selection()
        self._selected_entry_index -= 1
        if self._selected_entry_index < 0:
            if self._on_leave_focus and self._on_leave_focus():
                self._selected_entry_index = None
                return
            n = len(self._entries_frames)
            self._selected_entry_index = n - 1
        self.highlight_selection()

    def _on_press_down(self):
        if self._selected_entry_index is None:
            return
        self.unhighlight_selection()
        self._selected_entry_index += 1
        n = len(self._entries_frames)
        if self._selected_entry_index >= n:
            if self._on_leave_focus and self._on_leave_focus():
                self._selected_entry_index = None
                return
            self._selected_entry_index = 0
        self.highlight_selection()

    def _on_open_selection(self):
        if not self._on_open:
            return
        info = self.get_selection()
        self._on_open(info.filename)

    def _on_click_open(self, filename):
        if not self._on_open:
            return
        self._on_open(filename)

    def _on_click_mark(self, button, filename):
        util.on_click_mark_button(button, filename,
                                  self._front.manager.dao,
                                  small=False)
