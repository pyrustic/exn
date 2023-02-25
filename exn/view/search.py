import os.path
import tkinter as tk
from tkinter import ttk
import re
import tkutil
from exn.view.roll import Roll
from viewable import Viewable
from exn import constant


class Search(Viewable):
    def __init__(self, front):
        # target = "all" or "past"
        super().__init__()
        self._front = front
        self._results_frame = None
        self._results_front_frame = None
        self._search_strvar = tk.StringVar()
        self._found_status_strvar = tk.StringVar()
        self._list_status_strvar = tk.StringVar()
        self._deep_search_intvar = tk.IntVar()
        self._use_regex_intvar = tk.IntVar()
        self._marked_only_intvar = tk.IntVar()
        self._current_list_number = 0
        self._previously_mapped = False
        self._total_lists = 0
        self._roll = None
        self._search_entry = None
        self._matches = list()
        self._suggestion = None
        self._index_data = list()
        self._bookmarks = list()

    def _create_body(self, parent):
        return tk.Toplevel(parent, name="search")

    def _build(self):
        self.body.bind("<Escape>", lambda e: self._hide_window())
        self.body.title("")
        self.body.minsize(*constant.WINDOW_MINSIZE)
        tkutil.restore_size(self.body, name="exn_search",
                            default=constant.SEARCH_WINDOW_SIZE)
        # frames
        frame1 = tk.Frame(self.body)
        frame1.pack()
        frame2 = tk.Frame(self.body)
        frame2.pack(fill=tk.X, pady=(7,3))
        frame3 = tk.Frame(self.body)
        frame3.pack(pady=(7, 5))
        # SEARCH label
        label = tk.Label(frame1, name="title", text="Search")
        label.pack()
        # search entry
        self._search_entry = tk.Entry(frame2, name="search_field",
                                      textvariable=self._search_strvar)
        self._search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))
        self._search_entry.bind("<Up>", lambda e: self._on_press_up())
        self._search_entry.bind("<Down>", lambda e: self._on_press_down())
        self._search_entry.focus_set()
        clear_entry = ttk.Button(frame2, text="x", style="clear2.TButton",
                                 command=self._on_clear_search)
        clear_entry.pack(side=tk.LEFT, padx=3)
        search_button = ttk.Button(frame2, name="search_button",
                                   style="blue.TButton",
                                   text="Search!", command=self._on_search)
        search_button.pack(side=tk.RIGHT, padx=(0, 3))
        # checkbuttons
        deep_search_checkbutton = ttk.Checkbutton(frame3, text="Deep Search",
                                                  style="toplevel.TCheckbutton",
                                                  variable=self._deep_search_intvar,
                                                  onvalue=1, offvalue=0,
                                                  command=self._on_toggle_deep_search)
        deep_search_checkbutton.pack(side=tk.LEFT, padx=2)
        regex_checkbutton = ttk.Checkbutton(frame3, text="Use RegEx",
                                            style="toplevel.TCheckbutton",
                                            variable=self._use_regex_intvar,
                                            onvalue=1, offvalue=0,
                                            command=self._on_toggle_use_regex)
        regex_checkbutton.pack(side=tk.LEFT, padx=2)
        marked_only_checkbutton = ttk.Checkbutton(frame3, text="Marked Only",
                                                  style="toplevel.TCheckbutton",
                                                  variable=self._marked_only_intvar,
                                                  onvalue=1, offvalue=0,
                                                  command=self._on_toggle_marked_only)
        marked_only_checkbutton.pack(side=tk.LEFT, padx=2)
        # center window
        editor = self._front.board.viewer.editor
        tkutil.align(self.body, parent=editor, side="n")
        tkutil.make_modal(self.body)

    def _on_map(self):
        self._index_data = list(self._front.board.viewer.pages.values())
        # suggestion
        dataset = list()
        for x in self._index_data:
            for tag in x.tags:
                tag = "#"+tag
                if tag in dataset:
                    continue
                dataset.append(tag)
        # TODO: uncomment the next two line, set the dropdown style, and fix Up/Down events conflicts
        #self._suggestion = Suggestion(self._search_entry, dataset=dataset)
        #self._suggestion.activate()
        self._search_entry.bind("<Return>", lambda e: self._on_search(), True)
        self._bookmarks = self._front.manager.dao.get_bookmarks()
        self._matches = self._index_data
        self._populate_roll(self._matches)

    def _on_destroy(self):
        tkutil.save_size(self.body, name="exn_search")

    def _install_header(self):
        header = tk.Frame(self.body)
        header.pack(fill=tk.X)
        # top side
        top_frame = tk.Frame(header)
        top_frame.pack(fill=tk.X)
        title_label = tk.Label(top_frame, text="Search")
        title_label.pack(side=tk.LEFT)
        # bottom side
        bottom_frame = tk.Frame(header)
        bottom_frame.pack()
        search_entry = tk.Entry(bottom_frame, textvariable=self._search_strvar)
        search_entry.pack(side=tk.LEFT)
        #search_entry.bind("<KeyRelease>", self._on_press_key, True)
        search_entry.bind("<Return>", self._on_click_search, True)
        #lite_search_checkbutton = tk.Checkbutton(frame, text="Lite Search")
        #lite_search_checkbutton.pack(side=tk.RIGHT)

    def _on_click_search(self, event):
        self._on_search()

    def _on_clear_search(self):
        self._search_strvar.set("")
        self._on_search()

    def _on_search(self):
        search_str = self._search_strvar.get()
        use_regex = True if self._use_regex_intvar.get() == 1 else False
        if self._deep_search_intvar.get() == 0:
            tags = [tag.strip("#") for tag in search_str.split()]
            results = self._lite_search(tags, use_regex)
        else:
            results = self._deep_search(search_str, use_regex)
        if self._marked_only_intvar.get() == 1:
            results = self._filter_marked_only(results)
        self._matches = results
        self._populate_roll(self._matches)

    def _on_toggle_deep_search(self):
        # TODO: reintegrate the commented lines
        self._on_search()
        if self._deep_search_intvar.get() == 1:
            #self._suggestion.deactivate()
            pass
        else:
            #self._suggestion.activate()
            pass

    def _on_toggle_use_regex(self):
        self._on_search()

    def _on_toggle_marked_only(self):
        if self._marked_only_intvar.get() == 1:
            self._matches = self._filter_marked_only(self._matches)
            self._populate_roll(self._matches)
        else:
            self._on_search()

    def _lite_search(self, tags, use_regex):
        results = list()
        for item in self._index_data:
            if not item.tags:
                continue
            matched = True
            if use_regex:  # if RegEx
                for tag in tags:
                    sub_matched = False
                    for x in item.tags:
                        if re.fullmatch(tag, x):
                            sub_matched = True
                            break
                    if not sub_matched:
                        matched = False
                        break
            else:  # No regex
                for tag in tags:
                    if tag not in item.tags:
                        matched = False
                        break
            if matched:
                results.append(item)
        return results

    def _deep_search(self, search_str, use_regex):
        results = list()
        dossier = self._front.manager.dossier
        for item in self._index_data:
            filename = item.filename
            path = os.path.join(dossier, *filename.split("/"))
            if not os.path.isfile(path):
                continue
            try:
                with open(path, "r") as file:
                    data = file.read()
                    if use_regex:
                        found = False
                        for _ in re.finditer(search_str, data):
                            found = True
                        if found:
                            results.append(item)
                    else:
                        if search_str in data:
                            results.append(item)
            except Exception as e:
                pass
        return results

    def _filter_marked_only(self, items):
        results = list()
        for item in items:
            if item.filename in self._bookmarks:
                results.append(item)
        return results

    def _on_press_up(self):
        self._roll.select(-1)

    def _on_press_down(self):
        self._roll.select(0)

    def _populate_roll(self, data):
        # Roll
        if self._roll and self._roll.body:
            self._roll.body.destroy()
        if not data:
            return
        self._roll = Roll(self._front, data, on_open=self._open_note,
                          on_close=self._hide_window,
                          on_leave_focus=self._on_leave_roll_focus)
        self._roll.build_pack(self.body, fill=tk.BOTH, expand=True)
        self._search_entry.focus_set()

    def _on_leave_roll_focus(self):
        self._search_entry.focus_set()
        return True

    def _open_note(self, filename):
        self.body.withdraw()
        self._front.open(filename)
        self._hide_window()

    def _hide_window(self):
        self.body.grab_release()
        self.body.withdraw()
