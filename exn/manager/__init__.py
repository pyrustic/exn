import os
import os.path
import sys
from exn import constant, utils
from exonote import Style, split_target, get_callable
from gaspium import App
from exn.view import Front
from exn.dao import Dao
from exn.theme import Theme, Constants as theme_const, get_standard_font_family


class Manager:
    def __init__(self, dossier, restriction):
        self._dossier = dossier
        self._restriction = restriction
        self._app = None
        self._dao = Dao(dossier)
        self._app_theme = None
        self._embedded_gui_theme = None
        self._viewer_style = None
        self._index = None
        self._setup()

    @property
    def app(self):
        return self._app

    @property
    def dossier(self):
        return self._dossier

    @property
    def restriction(self):
        return self._restriction

    @property
    def index(self):
        return self._index

    @property
    def dao(self):
        return self._dao

    @property
    def app_theme(self):
        return self._app_theme

    @property
    def viewer_style(self):
        return self._viewer_style

    @property
    def embedded_gui_theme(self):
        return self._embedded_gui_theme

    def start(self, target=None):
        if not target:
            target = self._get_default_note()
            if not target:
                return
        filename, sid = split_target(target)
        if filename in self._dao.get_blocklist():
            msg = "'{}' appears in the blocklist !"
            print(msg.format(filename))
            return
        #self._dao.update_history(filename)
        self._app = App(name="exn", title="Exonote Reader",
                        manager=self, geometry="700x600",
                        remember_geometry_change=True,
                        resizable=(True, True),
                        caching=True, show_page_title=False,
                        navbar=None, page_from_cli=False)
        self._app.root.minsize(*constant.WINDOW_MINSIZE)
        self._app_theme(self._app.root)
        self._update_theme_const()
        kwargs = {"target": target}
        self._app.attach(Front, pid="front", kwargs=kwargs)
        self._app.open("front")
        self._app.start()

    def _setup(self):
        # update sys.path
        sys.path.insert(1, self._dossier)
        # default themes
        self._app_theme = Theme
        #self._embedded_gui_theme = Theme2
        # default viewer style
        self._viewer_style = Style()
        # load user defined style
        data = self._load_user_defined_style()
        # update app and embedded gui themes
        self._update_themes(data)
        # update viewer style
        self._update_viewer_style(data)
        # get index data
        self._load_index()

    def _load_user_defined_style(self):
        # read style file
        style_file = os.path.join(self._dossier, ".exn", "style")
        return utils.read_style_file(style_file)

    def _update_themes(self, data):
        if not data:
            return
        # get app theme
        app_theme = data.get("app_theme")
        if app_theme:
            cache = get_callable(app_theme)
            if cache:
                self._app_theme = cache[1]
        # get app theme
        embedded_gui_theme = data.get("embedded_gui_theme")
        if embedded_gui_theme:
            # get app theme
            cache = get_callable(embedded_gui_theme)
            if cache:
                self._embedded_gui_theme = cache[1]

    def _update_viewer_style(self, data):
        if not data:
            return
        valid_options = {"horizontal_margin", "vertical_margin",
                         "foreground_color", "background_color",
                         "selection_background_color", "highlight_color",
                         "active_highlight_color", "spacing", "font_family",
                         "font_size", "codeblock_foreground_color",
                         "heading_foreground_color", "link_foreground_color",
                         "executable_link_foreground_color", "code_background_color",
                         "monospace_font_family", "warning_color", "notice_color"}
        integers_options = {"horizontal_margin", "vertical_margin",
                            "spacing", "font_size"}
        for option in valid_options:
            value = data.get(option, "")
            if not value:
                continue
            if option in integers_options:
                try:
                    value = int(value)
                except ValueError as e:
                    continue
            setattr(self._viewer_style, option, value)

    def _get_default_note(self):
        history = self._dao.get_history()
        if not history:
            index_path = os.path.join(self._dossier, "index")
            index = utils.IndexParser.parse(index_path)
            if not index:
                return
            return index[0].filename
        return history[0]

    def _load_index(self):
        path = os.path.join(self._dossier, "index")
        self._index = utils.IndexParser.parse(path)
        self._index = self._index if self._index else list()

    def _update_theme_const(self):
        theme_const.FONT_FAMILY = get_standard_font_family(name="TkTextFont")
        theme_const.FONT_FAMILY_MONO = get_standard_font_family(name="TkFixedFont")
