import os
import os.path
import importlib
import jesth
from operator import itemgetter
from exonote import IndexParser, dto


# no usage (for the moment)
def load_extensions(context):
    # context = dto.ExtensionContext(dossier_path, app_instance, manager)
    dossier = os.getcwd()
    extensions_filename = os.path.join(dossier, ".exn", "extensions")
    if not os.path.isfile(extensions_filename):
        return None
    doc = jesth.read(extensions_filename)
    section = doc.get("")
    body = section.body if section else list()
    if not body:
        return None
    for line in body:
        if line.startswith("#"):
            continue
        if not line:
            continue
        cache = line.split(":")
        if len(cache) > 2:
            continue
        if len(cache) == 1:
            module_name, callable_name = cache[0], "main"
        else:
            module_name, callable_name = cache
        callable_object = get_callable(module_name, callable_name)
        if not callable_object:
            continue
        try:
            callable_object(context)
        except Exception as e:
            pass


# no usage (for the moment)
def get_callable(module_name, callable_name):
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        return None
    try:
        callable_object = getattr(module, callable_name)
    except AttributeError as e:
        return None
    return callable_object


class IndexBuilder:
    @staticmethod
    def build(dossier):
        index_path = os.path.join(dossier, "index")
        index = list()
        if os.path.isfile(index_path):
            index = IndexParser.parse(index_path)
        registered_targets = {item.filename for item in index}
        unordered_files = IndexBuilder._get_unordered_files(dossier)
        ordered_files = sorted(unordered_files, key=itemgetter(2))
        for item in ordered_files:
            target, base, _ = item
            if target in registered_targets:
                continue
            title, tags = IndexBuilder._get_title_and_tags(base)
            page = dto.PageInfo(target, 0, title, tags)
            index.append(page)
        IndexBuilder._save_index(index, index_path)

    @staticmethod
    def _get_unordered_files(dossier):
        unordered_files = list()
        for root, dirs, files in os.walk(dossier):
            if os.path.samefile(root, dossier):
                folder = ""
            else:
                relpath = os.path.relpath(root, dossier).strip(os.sep)
                cache = relpath.split(os.sep)
                folder = "/".join(cache)
            for base in files:
                if not base.endswith(".exn"):
                    continue
                filename = os.path.join(root, base)
                target = folder + "/" + base if folder else base
                creation_time = os.path.getctime(filename)
                cache = (target, base, creation_time)
                unordered_files.append(cache)
        return unordered_files

    @staticmethod
    def _get_title_and_tags(base):
        base, ext = os.path.splitext(base)
        tags = base.strip("_").split("_")
        title = base.replace("_", " ").capitalize()
        return title, tags

    @staticmethod
    def _save_index(index, path):
        sections = list()
        for item in index:
            cache = list()
            title = item.title if item.title else "- No title -"
            tags = item.tags if item.tags else ("note", )
            cache.append(item.filename)
            cache.append(title)
            tags = ["#"+tag for tag in tags]
            cache.append(" ".join(tags))
            sections.append("\n".join(cache))
        text = "\n\n".join(sections)
        with open(path, "w") as file:
            file.write(text)


def read_style_file(path):
    doc = jesth.read(path)
    if not doc:
        return
    section = doc.get("")
    body = section.body if section else list()
    style_data = dict()
    if not body:
        return
    for line in body:
        if not line or line.startswith("#"):
            continue
        k, v = jesth.split_key_value(line)
        if not k:
            continue
        style_data[k] = v
    return style_data
