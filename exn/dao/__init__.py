import os
import os.path
import jesth
import atexit


class Dao:
    def __init__(self, dossier):
        self._dossier = dossier
        self._index_filename = None
        self._history_filename = None
        self._bookmarks_filename = None
        self._blocklist_filename = None
        self._history_cache = list()
        self._bookmarks_cache = list()
        self._blocklist = list()
        self._setup()

    def get_history(self):
        return self._history_cache

    def update_history(self, entry):
        history = self.get_history()
        for i, item in enumerate(history):
            if item == entry:
                del history[i]
                break
        history.insert(0, entry)

    def get_bookmarks(self):
        return self._bookmarks_cache

    def set_bookmark(self, path):
        bookmarks = self.get_bookmarks()
        if path not in bookmarks:
            bookmarks.insert(0, path)

    def unset_bookmark(self, path):
        bookmarks = self.get_bookmarks()
        for i, entry in enumerate(bookmarks):
            if entry == path:
                del bookmarks[i]
                break

    def is_bookmarked(self, path):
        bookmarks = self.get_bookmarks()
        for item in bookmarks:
            if item == path:
                return True
        return False

    def get_blocklist(self):
        return self._blocklist

    def _setup(self):
        self._index_filename = os.path.join(self._dossier, "index")
        self._history_filename = os.path.join(self._dossier, ".exn", "history")
        self._bookmarks_filename = os.path.join(self._dossier, ".exn", "bookmarks")
        self._blocklist_filename = os.path.join(self._dossier, ".exn", "blocklist")
        self._load_data()
        atexit.register(self._on_exit)

    def _load_data(self):
        if os.path.exists(self._history_filename):
            cache = jesth.read(self._history_filename, compact_mode=True)
            if cache:
                self._history_cache = cache.get("", list())
        if os.path.exists(self._bookmarks_filename):
            cache = jesth.read(self._bookmarks_filename, compact_mode=True)
            if cache:
                self._bookmarks_cache = cache.get("", list())
        if os.path.exists(self._blocklist_filename):
            cache = jesth.read(self._blocklist_filename, compact_mode=True)
            if cache:
                self._blocklist = cache.get("", list())

    def _save_state(self):
        self._create_dotexn_folder()
        items = [(self._history_filename, self.get_history),
                 (self._bookmarks_filename, self.get_bookmarks)]
        for filename, get_data in items:
            dirname = os.path.dirname(filename)
            if not os.path.isdir(dirname):
                continue
            data = dict()
            data[""] = get_data()
            jesth.write(data, filename)
            
    def _create_dotexn_folder(self):
        dotexn_folder = os.path.join(self._dossier, ".exn")
        if os.path.isdir(dotexn_folder):
            return
        try:
            os.makedirs(dotexn_folder)
        except Exception as e:
            print("Failed to create '.exn' folder")

    def _on_exit(self):
        atexit.unregister(self._on_exit)
        self._save_state()
