def on_click_mark_button(button, filename, dao, small=True):
    if dao.is_bookmarked(filename):
        dao.unset_bookmark(filename)
        unset_marked_style(button, small)
    else:
        dao.set_bookmark(filename)
        set_marked_style(button, small)


def set_marked_style(button, small=True):
    style_name = "mark.TButton"
    if small:
        style_name = "small_mark.TButton"
    button.config(style=style_name)


def unset_marked_style(button, small=True):
    style_name = "TButton"
    if small:
        style_name = "small.TButton"
    button.config(style=style_name)


def update_clipboard(text, widget):
    widget.clipboard_clear()
    widget.clipboard_append(text)
