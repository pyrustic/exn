from tkinter import font
from tkinter.ttk import Style as TtkStyle


def get_standard_font_family(name="TkDefaultFont"):
    return font.nametofont(name).actual()["family"]


class Constants:
    FONT_FAMILY = "Helvetica"
    FONT_FAMILY_MONO = "Courier"
    BUTTON_FONT_SIZE = 10
    TEXT_FONT_SIZE = 11
    TOPLEVEL_BACKGROUND = "#F1EEFF"
    TOC_ENTRY_FOREGROUND = "#4A7BF8"
    TOC_ENTRY_ACTIVE_BACKGROUND = "#E2E2FF"
    ROLL_ENTRY_HIGHLIGHT = "#E2DFFF"
    ROLL_ENTRY_ACTIVE_HIGHLIGHT = "#9AA7B8"
    ROLL_ENTRY_BACKGROUND = "#E7E4FF"


class Theme:
    def __init__(self, root):
        self._root = root
        self._ttkstyle = TtkStyle()
        self._update_constants()
        self._set_classic_theme()
        self._set_modern_theme()

    def _update_constants(self):
        Constants.FONT_FAMILY = get_standard_font_family("TkTextFont")
        Constants.FONT_FAMILY_MONO = get_standard_font_family("TkFixedFont")

    def _set_classic_theme(self):
        # Frames
        self._root.option_add("*Frame.background", "white")
        # windows
        self._set_classic_window_style()
        # Text editor
        self._root.option_add("*Text.highlightThickness", 0)
        self._root.option_add("*Text.borderWidth", 0)
        # set classic entry style
        self._set_classic_entry_style()
        # set page number style
        self._set_classic_page_number_style()
        # set finder status
        self._set_classic_finder_status_style()
        # TOC editor
        self._root.option_add("*toc*Text.background", Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*toc*Text.highlightThickness", 0)
        self._root.option_add("*toc*Text.borderWidth", 0)
        # Toc info card
        self._set_classic_info_card_style()
        # Goto style
        self._set_classic_goto_style()
        # Roll entry card
        self._set_classic_roll_entry_card_style()
        # Roll nav status style
        self._set_classic_roll_nav_status_style()
        # Search window style
        self._set_classic_search_window_style()
        # About window style
        self._set_classic_about_window_style()

    def _set_modern_theme(self):
        self._ttkstyle.theme_use("classic")
        self._set_modern_frame_style()
        self._set_modern_button_style()
        self._set_modern_clear_button_style()
        self._set_modern_red_button_style()
        self._set_modern_scrollbar_style()
        self._set_modern_window_scrollbar_style()
        self._set_modern_checkbutton_style()
        self._set_modern_checkbutton2_style()
        self._set_modern_page_number_style()
        self._set_modern_mark_button_style()
        self._set_modern_mark_small_button_style()
        self._set_modern_blue_button_style()
        # calc style for the demo exclusively
        self._set_calc_style()

    # ====== CLASSIC THEME =======

    def _set_classic_window_style(self):
        # frames
        self._root.option_add("*Toplevel.background", Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*Toplevel*Frame.background", Constants.TOPLEVEL_BACKGROUND)
        # title
        self._root.option_add("*Toplevel*title.foreground", "#505050")
        self._root.option_add("*Toplevel*title.background", Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*Toplevel*title.font", (Constants.FONT_FAMILY_MONO,
                                                       Constants.TEXT_FONT_SIZE + 10, "bold"))

    def _set_classic_entry_style(self):
        # entries
        self._root.option_add("*Entry.font", (Constants.FONT_FAMILY_MONO,
                                              Constants.TEXT_FONT_SIZE, "normal"))
        self._root.option_add("*Entry.background", "white")
        self._root.option_add("*Entry.readonlyBackground", "white")
        self._root.option_add("*Entry.disabledBackground", "white")
        self._root.option_add("*Entry.foreground", "#64717A")
        self._root.option_add("*Entry.relief", "flat")
        self._root.option_add("*Entry.highlightThickness", 1)
        self._root.option_add("*Entry.highlightBackground", "#DCDCDC")
        self._root.option_add("*Entry.highlightColor", "#CCCCCC")
        self._root.option_add("*Entry.selectBackground", "#DCE7FF")
        self._root.option_add("*Entry.selectForeground", "#64717A")
        self._root.option_add("*Entry.insertBackground", "#64717A")
        #self._root.option_add("*Entry.padX", 3)
        #self._root.option_add("*Entry.padY", 10)

    def _set_classic_page_number_style(self):
        self._root.option_add("*navframe.page_number.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE , "bold"))
        self._root.option_add("*navframe.page_number.background", "white")
        self._root.option_add("*navframe.page_number.readonlyBackground", "white")
        self._root.option_add("*navframe.page_number.disabledBackground", "white")
        self._root.option_add("*navframe.page_number.foreground", "#64717A")
        self._root.option_add("*navframe.page_number.relief", "flat")
        self._root.option_add("*navframe.page_number.highlightThickness", 1)
        self._root.option_add("*navframe.page_number.highlightBackground", "white")
        self._root.option_add("*navframe.page_number.highlightColor", "#CCCCCC")
        self._root.option_add("*navframe.page_number.selectBackground", "#DCE7FF")
        self._root.option_add("*navframe.page_number.selectForeground", "#64717A")
        self._root.option_add("*navframe.page_number.insertBackground", "#64717A")

    def _set_classic_finder_status_style(self):
        # entries
        self._root.option_add("*finder_status*highlightThickness", 0)

    def _set_classic_info_card_style(self):
        # outer
        self._root.option_add("*info_card.background",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*info_card.highlightThickness", 5)
        self._root.option_add("*info_card.highlightBackground",
                              Constants.ROLL_ENTRY_HIGHLIGHT)
        # inner
        self._root.option_add("*info_card*Frame.background",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*info_card*Frame.highlightThickness", 0)
        # title field
        self._root.option_add("*info_card*title_field.disabledBackground",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*info_card*title_field.disabledForeground", "#2F5F64")
        self._root.option_add("*info_card*title_field.highlightThickness", 0)
        self._root.option_add("*info_card*title_field.borderWidth", 0)
        self._root.option_add("*info_card*title_field.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE, "normal"))
        # filename field
        self._root.option_add("*info_card*filename_field.disabledBackground",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*info_card*filename_field.disabledForeground", "#575757")
        self._root.option_add("*info_card*filename_field.highlightThickness", 0)
        self._root.option_add("*info_card*filename_field.borderWidth", 0)
        self._root.option_add("*info_card*filename_field.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE - 1, "normal"))
        # label page
        self._root.option_add("*info_card*page_label.background", Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*info_card*page_label.foreground", "#2F5F64")
        self._root.option_add("*info_card*page_label.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE - 1, "bold"))
        # tags field
        self._root.option_add("*info_card*tags_field.disabledBackground",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*info_card*tags_field.disabledForeground", "gray")
        self._root.option_add("*info_card*tags_field.highlightThickness", 0)
        self._root.option_add("*info_card*tags_field.borderWidth", 0)
        self._root.option_add("*info_card*tags_field.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE - 2, "normal"))

    def _set_classic_roll_entry_card_style(self):
        # outer
        self._root.option_add("*roll*main_frame.Frame.Frame.background",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*roll*main_frame.Frame.Frame.highlightThickness", 5)
        self._root.option_add("*roll*main_frame.Frame.Frame.highlightBackground",
                              Constants.ROLL_ENTRY_HIGHLIGHT)
        # inner
        self._root.option_add("*roll*main_frame.Frame.Frame*Frame.background",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("**roll*main_frame.Frame.Frame*Frame.highlightThickness", 0)
        # title field
        self._root.option_add("*roll*main_frame*title_field.disabledBackground",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*roll*main_frame*title_field.disabledForeground", "#2F5F64")
        self._root.option_add("*roll*main_frame*title_field.highlightThickness", 0)
        self._root.option_add("*roll*main_frame*title_field.borderWidth", 0)
        self._root.option_add("*roll*main_frame*title_field.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE, "normal"))
        # filename field
        self._root.option_add("*roll*main_frame*filename_field.disabledBackground",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*roll*main_frame*filename_field.disabledForeground", "#575757")
        self._root.option_add("*roll*main_frame*filename_field.highlightThickness", 0)
        self._root.option_add("*roll*main_frame*filename_field.borderWidth", 0)
        self._root.option_add("*roll*main_frame*filename_field.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE - 1, "normal"))
        # label page
        self._root.option_add("*roll*main_frame*page_label.background", Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*roll*main_frame*page_label.foreground", "#2F5F64")
        self._root.option_add("*roll*main_frame*page_label.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE - 1, "bold"))
        # tags field
        self._root.option_add("*roll*main_frame*tags_field.disabledBackground",
                              Constants.ROLL_ENTRY_BACKGROUND)
        self._root.option_add("*roll*main_frame*tags_field.disabledForeground", "gray")
        self._root.option_add("*roll*main_frame*tags_field.highlightThickness", 0)
        self._root.option_add("*roll*main_frame*tags_field.borderWidth", 0)
        self._root.option_add("*roll*main_frame*tags_field.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE - 2, "normal"))

    def _set_classic_goto_style(self):
        # entry
        self._root.option_add("*goto*Entry.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE, "normal"))
        self._root.option_add("*goto*Entry.background", "#F6F3FF")
        self._root.option_add("*goto*Entry.readonlyBackground", "white")
        self._root.option_add("*goto*Entry.disabledBackground", "white")
        self._root.option_add("*goto*Entry.foreground", "#64717A")
        self._root.option_add("*goto*Entry.relief", "flat")
        self._root.option_add("*goto*Entry.highlightThickness", 1)
        self._root.option_add("*goto*Entry.highlightBackground", "#DCDCDC")
        self._root.option_add("*goto*Entry.highlightColor", "#CCCCCC")
        self._root.option_add("*goto*Entry.selectBackground", "#DCE7FF")
        self._root.option_add("*goto*Entry.selectForeground", "#64717A")
        self._root.option_add("*goto*Entry.insertBackground", "#64717A")
        self._root.option_add("*goto*Entry.padX", 3)
        self._root.option_add("*goto*Entry.padY", 0)
        # description label style
        self._root.option_add("*goto*description_label.background",
                              Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*goto*description_label.foreground", "#64717A")
        self._root.option_add("*goto*description_label.foreground", "#3B4851")
        self._root.option_add("*goto*description_label.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE, "normal"))
        # status label style
        self._root.option_add("*goto*status_label.background",
                              Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*goto*status_label.foreground", "tomato")
        self._root.option_add("*goto*status_label.font",
                              (Constants.FONT_FAMILY, Constants.TEXT_FONT_SIZE, "normal"))

    def _set_classic_roll_nav_status_style(self):
        self._root.option_add("*roll*nav_status.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE, "bold"))
        self._root.option_add("*roll*nav_status.background",
                              Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*roll*nav_status.foreground", "#64717A")
        self._root.option_add("*roll*nav_status.activeBackground", "#111519")
        self._root.option_add("*roll*nav_status.activeForeground", "#A098A0")
        self._root.option_add("*roll*nav_status.highlightBackground", "#D0D0D0")
        self._root.option_add("*roll*nav_status.highlightThickness", 0)
        self._root.option_add("*roll*nav_status.highlightColor", "white")
        self._root.option_add("*roll*nav_status.borderWidth", 0)
        self._root.option_add("*roll*nav_status.cursor", "arrow")

    def _set_classic_search_window_style(self):
        # entry
        self._root.option_add("*search*search_field.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE, "normal"))
        self._root.option_add("*search*search_field.background", "#F6F3FF")
        self._root.option_add("*search*search_field.readonlyBackground", "white")
        self._root.option_add("*search*search_field.disabledBackground", "white")
        self._root.option_add("*search*search_field.foreground", "#64717A")
        self._root.option_add("*search*search_field.relief", "flat")
        self._root.option_add("*search*search_field.highlightThickness", 1)
        self._root.option_add("*search*search_field.highlightBackground", "#DCDCDC")
        self._root.option_add("*search*search_field.highlightColor", "#CCCCCC")
        self._root.option_add("*search*search_field.selectBackground", "#DCE7FF")
        self._root.option_add("*search*search_field.selectForeground", "#64717A")
        self._root.option_add("*search*search_field.insertBackground", "#64717A")
        self._root.option_add("*search*search_field.padX", 3)
        self._root.option_add("*search*search_field.padY", 0)

    def _set_classic_about_window_style(self):
        # logo
        self._root.option_add("*about*logo.background", Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*about*logo.foreground", "#64717A")
        self._root.option_add("*about*logo.foreground", "#8A9EB0")
        self._root.option_add("*about*logo.foreground", "#F28D71")
        self._root.option_add("*about*logo.font",
                              (Constants.FONT_FAMILY,
                               Constants.TEXT_FONT_SIZE + 42, "bold"))
        # text
        self._root.option_add("*about*Text.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE, "normal"))
        self._root.option_add("*about*Text.background", "#F6F3FF")
        self._root.option_add("*about*Text.background", Constants.TOPLEVEL_BACKGROUND)
        self._root.option_add("*about*Text.readonlyBackground", "white")
        self._root.option_add("*about*Text.disabledBackground", "white")
        self._root.option_add("*about*Text.foreground", "#64717A")
        self._root.option_add("*about*Text.relief", "flat")
        self._root.option_add("*about*Text.highlightThickness", 0)
        self._root.option_add("*about*Text.highlightBackground", "#E7E4FF")
        self._root.option_add("*about*Text.highlightColor", "#CCCCCC")
        self._root.option_add("*about*Text.inactiveSelectBackground", "#DCE7FF")
        self._root.option_add("*about*Text.selectForeground", "#64717A")
        self._root.option_add("*about*Text.insertBackground", "#64717A")
        self._root.option_add("*about*Text.padX", 3)
        self._root.option_add("*about*Text.padY", 0)

    # ====== MODERN THEME =======

    def _set_modern_frame_style(self):
        self._ttkstyle.configure("TFrame", background="white")

    def _set_modern_button_style(self):
        self._ttkstyle.configure("TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background="#F2F2F2",
                                 foreground="#838383", relief="flat",
                                 borderwidth=0, padding=(3, 0),
                                 highlightthickness=1,
                                 highlightcolor="#D0D0D0")
        self._ttkstyle.map("TButton", background=[("active", "#E6E6E6")],
                           highlightcolor=[("focus", "gray")])

    def _set_modern_red_button_style(self):
        self._ttkstyle.configure("red.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background="#FFEBFF",
                                 foreground="#F08EAC", relief="flat",
                                 borderwidth=0, padding=(3, 0),
                                 highlightthickness=1,
                                 highlightcolor="#ECAEC8")
        self._ttkstyle.map("red.TButton", background=[("active", "#FFD2EC")],
                           highlightcolor=[("focus", "gray")])

    def _set_modern_blue_button_style(self):
        self._ttkstyle.configure("blue.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background="#E7E4FF",
                                 foreground="#8A9EB0", relief="flat",
                                 borderwidth=0, padding=(3, 0),
                                 highlightthickness=1,
                                 highlightcolor="#CECBE6")
        self._ttkstyle.map("blue.TButton", background=[("active", "#DDDAFF")],
                           highlightcolor=[("focus", "gray")])

    def _set_modern_clear_button_style(self):
        self._ttkstyle.configure("clear.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background="white",
                                 foreground="#838383", relief="flat",
                                 borderwidth=0, padding=0,
                                 highlightcolor="white",
                                 highlightthickness=1)
        self._ttkstyle.map("clear.TButton", background=[("active", "#E6E6E6")],
                           highlightcolor=[("focus", "gainsboro")])
        self._set_modern_clear_button_style2()

    def _set_modern_clear_button_style2(self):
        self._ttkstyle.configure("clear2.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background=Constants.TOPLEVEL_BACKGROUND,
                                 foreground="#838383", relief="flat",
                                 borderwidth=0, padding=0,
                                 highlightcolor=Constants.TOPLEVEL_BACKGROUND,
                                 highlightthickness=1)
        self._ttkstyle.map("clear2.TButton", background=[("active", "#E6E6E6")],
                           highlightcolor=[("focus", "gainsboro")])

    def _set_modern_scrollbar_style(self):
        self._ttkstyle.configure("Vertical.TScrollbar",
                                 relief="flat", borderwidth=0,
                                 troughcolor="white", width=11,
                                 arrowsize=0,
                                 background="#E7E7E7")
        self._ttkstyle.map("Vertical.TScrollbar", background=[("active", "#D1D1D1")],
                           troughcolor=[("active", "#F4F4F4")])

    def _set_modern_window_scrollbar_style(self):
        self._ttkstyle.configure("window.Vertical.TScrollbar",
                                 relief="flat", borderwidth=0,
                                 troughcolor=Constants.TOPLEVEL_BACKGROUND,
                                 width=11, arrowsize=0,
                                 background="#E7E7E7")
        self._ttkstyle.map("window.Vertical.TScrollbar", background=[("active", "#D1D1D1")],
                           troughcolor=[("active", "#F4F4F4")])

    def _set_modern_checkbutton_style(self):
        self._ttkstyle.configure("TCheckbutton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background="white",
                                 foreground="#838383", relief="flat",
                                 borderwidth=0, padding=(5, 0),
                                 highlightcolor="white",
                                 indicatorcolor="gainsboro",
                                 highlightthickness=1)
        self._ttkstyle.map("TCheckbutton", background=[("active", "white")],
                           highlightcolor=[("focus", "gainsboro")],
                           indicatorcolor=[("selected", "gray")])

    def _set_modern_checkbutton2_style(self):
        self._ttkstyle.configure("toplevel.TCheckbutton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background=Constants.TOPLEVEL_BACKGROUND,
                                 foreground="#838383", relief="flat",
                                 borderwidth=0, padding=(5, 0),
                                 highlightcolor=Constants.TOPLEVEL_BACKGROUND,
                                 indicatorcolor="gainsboro",
                                 highlightthickness=1)
        self._ttkstyle.map("toplevel.TCheckbutton", background=[("active", "white")],
                           highlightcolor=[("focus", "gainsboro")],
                           indicatorcolor=[("selected", "gray")])

    def _set_modern_page_number_style(self):
        self._ttkstyle.configure("page_number.TEntry",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.TEXT_FONT_SIZE, "bold"),
                                 background="white",
                                 foreground="#64717A", relief="flat",
                                 borderwidth=0, padding=0,
                                 highlightcolor="white",
                                 indicatorcolor="gainsboro",
                                 highlightthickness=0)

    def _set_modern_mark_button_style(self):
        self._ttkstyle.configure("mark.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "normal"),
                                 background="#F2F2C0",
                                 foreground="#A8A860", relief="flat",
                                 borderwidth=0, padding=(3, 0),
                                 highlightthickness=1,
                                 highlightcolor="#D0D0D0")
        self._ttkstyle.map("mark.TButton", background=[("active", "#F2F2A5")],
                           highlightcolor=[("focus", "gray")])

    def _set_modern_mark_small_button_style(self):
        self._ttkstyle.configure("mark_small.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE - 2, "normal"),
                                 background="#F2F2C0",
                                 foreground="#A8A860", relief="flat",
                                 borderwidth=0, padding=(3, 0),
                                 highlightthickness=1,
                                 highlightcolor="#D0D0D0")
        self._ttkstyle.map("mark_small.TButton", background=[("active", "#F2F2A5")],
                           highlightcolor=[("focus", "gray")])
                         
    def _set_calc_style(self):
        # frame
        bg = "#FAFAFA"
        self._root.option_add("*calc.background", bg)
        self._root.option_add("*calc.highlightThickness", 1)
        self._root.option_add("*calc.highlightBackground", "#CCCCCC")
        self._root.option_add("*calc.highlightColor", "#CCCCCC")
        self._root.option_add("*calc*Frame.background", bg)
        # entry
        self._root.option_add("*calc*Entry.font",
                              (Constants.FONT_FAMILY_MONO,
                               Constants.TEXT_FONT_SIZE + 2, "normal"))
        self._root.option_add("*calc*Entry.background", "#F6F3FF")
        self._root.option_add("*calc*Entry.readonlyBackground", "white")
        self._root.option_add("*calc*Entry.disabledBackground", "white")
        self._root.option_add("*calc*Entry.foreground", "#8C8C9A")
        self._root.option_add("*calc*Entry.relief", "flat")
        self._root.option_add("*calc*Entry.highlightThickness", 1)
        self._root.option_add("*calc*Entry.highlightBackground", "#DCDCDC")
        self._root.option_add("*calc*Entry.highlightColor", "#CCCCCC")
        self._root.option_add("*calc*Entry.selectBackground", "#DCE7FF")
        self._root.option_add("*calc*Entry.selectForeground", "#64717A")
        self._root.option_add("*calc*Entry.insertBackground", "#64717A")
        # ttk
        self._ttkstyle.configure("calc.TButton",
                                 font=(Constants.FONT_FAMILY_MONO,
                                       Constants.BUTTON_FONT_SIZE, "bold"),
                                 background="#FAFAFA",
                                 foreground="#9D9DAB", relief="flat",
                                 borderwidth=0, padding=(3, 0),
                                 highlightthickness=1,
                                 highlightcolor="#D0D0D0")
        self._ttkstyle.map("calc.TButton", background=[("active", "#E0E5FF")],
                           highlightcolor=[("focus", "gray")])
