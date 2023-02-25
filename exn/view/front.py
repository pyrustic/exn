import tkinter as tk
from viewable import Viewable
from exn.view.top import Top
from exn.view.board import Board
from exn.view.footer import Footer
from exonote import split_target
from viewstack import ViewStack


class Front(Viewable):
    def __init__(self, context, target):
        super().__init__()
        self._context = context
        self._target = target
        self._manager = context.manager
        self._dao = context.manager.dao
        self._app = context.manager.app
        self._top = None
        self._board = None
        self._footer = None
        self._viewstack = None
        self._board_container = None
        self._new = True

    @property
    def manager(self):
        return self._manager

    @property
    def filename(self):
        return self._filename

    @property
    def top(self):
        return self._top

    @property
    def board(self):
        return self._board

    @property
    def footer(self):
        return self._footer

    def open(self, target):
        filename, sid = split_target(target)
        if filename in self._dao.get_blocklist():
            return False
        self._filename = filename
        self._board = self._viewstack.views.get(filename)
        if self._board:
            self._viewstack.lift(filename)
        else:
            old_selection = self._viewstack.selection
            self._board = Board(self, filename)
            self._viewstack.add(filename, self._board)
            if self._board.failed:
                self._viewstack.destroy(filename)
                if old_selection:
                    filename = old_selection.name
                    self._board = self._viewstack.lift(filename)
                    self._filename = filename
                return False
        if sid:
            self._board.viewer.goto(sid)
        self._dao.update_history(self._filename)
        self._update_app_title(filename)
        self._footer.update_page_status(filename)
        self._footer.finder.disable()
        return True

    def refresh(self):
        if not self._filename:
            return
        filename = self._filename
        if self._filename not in self._viewstack.views:
            return
        self._viewstack.destroy(filename)
        self.open(filename)

    def _create_body(self, parent):
        return tk.Frame(parent, name="front")

    def _build(self):
        #self.body.bind("<Visibility>", self._handle_visibility_event)
        # top
        self._top = Top(self)
        self._top.build_pack(self.body, fill=tk.X)
        # board container
        self._board_container = tk.Frame(self.body, name="board_stack")
        self._board_container.pack(fill=tk.BOTH, expand=True)
        self._viewstack = ViewStack(self._board_container)
        #self._board = Board(self)
        #self._board.build_pack(self.body, fill=tk.BOTH, expand=True)
        # footer
        on_leave_focus = lambda: self._board.editor.focus_set()
        self._footer = Footer(self, on_leave_focus=on_leave_focus)
        self._footer.build_pack(self.body, fill=tk.X)
        self.open(self._target)

    def _on_map(self):
        pass

    def _on_remap(self):
        #print(event.state)
        #if event.state != "VisibilityUnobscured":
        #    return
        if not self._board:
            return
        self._board.viewer.editor.focus_set()

    def _on_destroy(self):
        if not self._board:
            return
        images = self._board.viewer.data.get("images")
        if not images:
            return
        images[:] = []

    def _update_app_title(self, filename):
        for item in self._manager.index:
            if item.filename == filename:
                cache = item.title if item.title else "- No Title -"
                #title = "{}   |   {}   |   Exonote Reader".format(cache, filename)
                title = "{}   -   Exonote Reader".format(cache)
                self._app.root.title(title)
