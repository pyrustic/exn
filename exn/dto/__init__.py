from collections import namedtuple


IndexEntry = namedtuple("IndexEntry", ["filename", "title", "tags"])

ExtensionContext = namedtuple("ExtensionContext", ["dossier", "app", "manager"])

SidebarContext = namedtuple("SidebarContext", ["dossier", "app", "manager", "path"])
