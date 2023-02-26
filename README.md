<!-- Cover -->
<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/assets/exn/cover.png" alt="Demo" width="683">
    <p align="center">
    <a href="https://github.com/pyrustic/exn-demo/blob/master/home.exn">Home.exn</a> from the <a href="https://github.com/pyrustic/exn-demo">demo</a> dossier
    </p>
</div>


<!-- Intro Text -->
# Exonote / Exn
<b> Write and render rich, scriptable, and interactive notes </b>
    
This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Installation](#installation) &nbsp; &nbsp; [Demo](#demo) &nbsp; &nbsp; [Latest](https://github.com/pyrustic/exn/tags) &nbsp; &nbsp; [Modules](https://github.com/pyrustic/exn/tree/master/docs/modules#readme)


## Table of contents

- [Overview](#overview)
- [Why use this project ?](#why-use-this-project-)
- [Demo](#demo)
- [Markup language](#markup-language)
- [Command line interface](#command-line-interface)
- [Scripting with Python](#scripting-with-Python)
- [Viewer API](#viewer-api)
- [Embedding GUI programs](#embedding-gui-programs)
- [Key bindings](#key-bindings)
- [Miscellaneous](#miscellaneous)
- [Installation](#installation)


# Overview
Exn is a lightweight Python application for browsing a dossier of exonotes. An exonote is **plain text** written with an [eponymous](https://github.com/pyrustic/exonote) markup language inspired by [Markdown](https://en.wikipedia.org/wiki/Markdown) and rendered with [Tkinter](https://en.wikipedia.org/wiki/Tkinter) (the default GUI library for [Python](https://www.python.org/downloads/)).

**Interactivity** can be added to an exonote by **embedding GUI programs** written in Python with Tkinter. Additionally, all or part of an exonote can be arbitrarily generated using **custom Python scripts**.

This application is built with the [Gaspium](https://github.com/pyrustic/gaspium) framework and uses [Shared](https://github.com/pyrustic/shared) and [Jesth](https://github.com/pyrustic/jesth) extensively to manipulate data.

This project is built on top of [Exonote](https://github.com/pyrustic/exonote). Solving issues in **Exonote** means improving **Exn**. Check the [issues](https://github.com/pyrustic/exonote/issues) !

## Dossier of exonotes
A **dossier** is a directory containing exonotes and resources such as attachments and Python source code. At the root of a dossier should be an index file containing an ordered list of exonotes filenames, titles, and their associated tags. The index file is generated automatically by the `--build` command in the command line (the order is based on the creation timestamp of the exonotes).

Exn treats each exonote with the `.exn` extension as the page of a virtual book, so the graphical user interface of Exn is a metaphor for a book with controls to move from one page to the next or to the previous one.

## The Search feature
Exn has a search interface that allows the user to search for exonotes in the dossier by specifying tags, words or a phrase. The search mechanism has an optional [regular expression](https://en.wikipedia.org/wiki/Regular_expression) mode.

## On security: run untrusted exonotes
The command line interface exposes two options for running exonotes:

|Option|Description|
|---|---|
|`-r`, `--restrict [<filename>]`| Open a note with low restriction, i.e., block the execution of embedded programs|
|`-R`, `--Restrict [<filename>]`| Open a note with high restriction, i.e., block executable links and also the execution of embedded programs|


# Why use this project ?
Despite the existence of interesting note-taking solutions and the storm of AI-powered projects, there are compelling arguments for adopting Exonote and Exn. Let's explore some characteristics and concrete examples.

## Characteristics
Here are some characteristics and their consequences:

|Characteristic|Consequence|
|---|---|
|Plain old text file|Since an exonote is just plain text, you can always use your favorite text editor (Vim, Sublime Text, Visual Studio Code, et cetera) to write your notes. Exonotes are also de facto compatible with [VCS](https://en.wikipedia.org/wiki/Version_control).|
|Minimalism|Exonote's minimalist markup language specification made Tkinter a good candidate to render it, eliminating the need for web-based technology (browser, html, css, et cetera). Hence, we got Exn, a lightweight, cross-platform app to view exonotes.|
|Scripting with Python|Python is one of the [most popular](https://www.wired.com/story/python-language-more-popular-than-ever/) programming languages in the world. Since people like to tinker with Python, it would be fun to write scripts with this language for personal exonotes.|
|Embed GUI programs written with Tkinter|[Tcl/Tk](https://www.tcl.tk/) is one of the easiest GUI toolkits to use, unsurprisingly, it's the default solution for GUI programming in Python via Tkinter. In the demo, a working calculator was built with Tkinter and embedded into an exonote.|

## Examples
These are few concrete examples of what can be done with Exonote and Exn:

- create interactive courses;
- build programming puzzles with levels and backstory;
- make a [proof of concept](https://www.malwarebytes.com/glossary/proof-of-concept);
- use the `exonote.Viewer` class to make rich and/or interactive documentation inside another application. Exn itself uses the default viewer in the Exonote library.
- Whistleblowing and censorship bypass: Due to its nature, a dossier of exonotes is very convenient for disclosing information that can be easily replicated and consumed by people.
- Decent alternative to a personal website: it is as simple as creating a GitHub repository, upload a dossier of exonote, share the link with readers, then regularly update the contents with `git commit`.

> **Note**: you can define a `blocklist` file in `$dossier/.exn` to block access to a list of exonotes (filenames). This mechanism with the help of custom scripts, allows the implementation of a system of levels where certain conditions must be met before opening specific exonotes.

# Demo
A [demo](https://github.com/pyrustic/exn-demo) is available that you can play with. You will need to clone the demo repository, install Exn with [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) and then run it without any arguments. By default, it executes the last exonote opened or runs the home page (first exonote referenced in the index).

```bash
# 1- clone the repository
$ git clone https://github.com/pyrustic/exn-demo
$ cd exn-demo

# 2- install exn
$ pip install exn

# 3- run exn with zero restriction
$ exn
```
You can still run Exn with restriction:
```bash
# run exn with low restriction
$ exn -r

# run exn with high restriction
$ exn -R
```

# Markup language
|Element|Description|
|---|---|
|ANCHOR|Create an anchor in a specific location of an exonote that can be accessed when its name is appended to the filename of the exonote. Syntax: `<anchor_name>`|
|ATTACHMENT|Insert an asset like an image. Syntax: `@[optional text](path/to/assets/resource.png)`|
|BOLD|Make a text bold. Syntax: `*bold*`|
|CODE|Surrounding a word or phrase with double backticks will apply a monospace font to it and also a colored background.|
|CODEBLOCK|Same as in Markdown|
|DINKUS|Three asterisks at the start of a blank will be centered and bolded like a [dinkus](https://en.wikipedia.org/wiki/Dinkus).|
|GAP|Leave at least one blank line between a group de sentences to create paragraphs.|
|HEADING|An exonote is made up of sections, which are made up of paragraphs. A section title is the Heading and it a section can have an identifier (section id, A.K.A. sid). A header follows the same pattern as in Markdown. Syntax: `# Title of section <section_id>`.|
|ITALIC|Apply italic to a text. Syntax: `_my sentence_`.|
|ITEM|Use a hyphen at the beginning of a line, with or without indent, to declare an item of a list.|
|LINK|Exonote supports link to websites, link to exonotes in the same dossier, link to anchors, and executable links (clicking such link will run a Python function. The documentation is a work in progress. Check the demo.|
|MONOSPACE|Surround a text with backticks to apply a monospaced font to it.|
|NOTICE|Surround a text with `%` to apply a green color to it.|
|PROGRAM|Reference a function or a view class. Syntax: `${path.to.module:functionOrClass arg1 arg2 "arg arg"}`|
|STRIKETHROUGH|Surround text with `~` to strikethrough it.|
|TABLE|Check the example below.|
|UNDERLINE|Surround a text with `__` to underline it.|
|VARIABLE|A variable is defined at the beginning of an empty line. This line will not be rendered. The value of a variable can be used to fill in the location placeholder of an attachment or link. Syntax: `[variable_name] Value`.|
|WARNING|Surround a text with `%%` to apply a red color to it.|

This is a table:
```
| Col 1 | Col 2 | Col 3
| val A | val B | val C
| val D | val E | val F
| val G | val H | val I 
```

> **Note:** you can add a caption to tables, attachments, and views (GUI programs) by written its content in front of a `&` just under the target element.

Example:
```
@[Alt text](path/to/image.png)
& This is a *caption* !
```


# Command line interface
Type `exn -h` or `exn --help` in the command line to display the help text.

Usage:

```
$ exn
$ exn <filename>
$ exn <option> [<arg> ...]
```

Options:
```
-b, --build                     Build the index file
-r, --restrict [<filename>]     Open a note with low restriction
-R, --Restrict [<filename>]     Open a note with high restriction
-h, --help                      Show help text
```

<p align="right"><a href="#readme">Back to top</a></p>

# Scripting with Python
It's as simple as referencing a Python function whose module is in the dossier or virtual environment. This Python function must accept a context argument and optionally return a string that will be rendered to where the function was called.

Inside the exonote:
```
This is an *exonote*. 
Let's make a call to a Python function here: 
${path.to.module:func arg1 arg2 "args..."}
```
The called function:
```python
def func(context):
    print(context.viewer)
    print(context.arguments)
    return "Hello World !"
```
<p align="right"><a href="#readme">Back to top</a></p>

# Viewer API
The viewer exposes an API to open a new exonote, refresh the current exonote, render a string to a specific location of the current exonote, scroll the current exonote to a specific location, compute a location index, modify the headings, programmatically read and modify sections, and more.

The documentation is a work in progress. Check the API [here](https://github.com/pyrustic/exonote/blob/master/exonote/viewer/__init__.py) !

<p align="right"><a href="#readme">Back to top</a></p>

# Embedding GUI programs
You can embed GUI views in an exonote by referencing a class that has a `build` method returning a Tkinter widget. The constructor of this class must accept a context argument.

> **Note:** It is recommended to subclass the `viewable.Viewable` class to create a view.

Inside the exonote:
```
This is an exonote.
Let's embed a view here:
${path.to.module:MyView arg1 arg2}

```

The view:
```python
from viewable import Viewable

class MyView(Viewable):
    def __init__(self, context):
        super().__init__()
    
    def _build(self):
        # build the interface of the view
        pass
```

<p align="right"><a href="#readme">Back to top</a></p>

# Miscellaneous

## Keymap
For a smooth user experience, keyboard keys are mapped to certain functions in Exn. For example, pressing `F` would activate the `Find in Page` functionality. Pressing `H` would open the home page. Pressing `S` would open the search interface. Pressing `T` would open the table of contents. Pressing `F5` would refresh the page. Et cetera.

> **Note:** `Ctrl+Tab` will open the **switcher** to allow you to go back to the previously opened exonote.

## Quick-copy
Quickly copy the contents of a codeblock or the address of a link with a right-click over it !

## Attachments
For the moments only images are supported.

## Path separator
The separator symbol inside the path to an exonote or asset is the slash `/` symbol. Also, a path must not start with a separator.

## Filenames
Exn only recognizes files with the extension `.exn`. Also, to reference a specific filename as a link in an exonote, you must write its path relative to the root of the folder. Filename and Path can be used as synonyms.

Example:
```
dossier
    exonote1.exn
    exonote2.exn
    folder
        exonote3.exn
```
The path to `exonote3.exn` is `folder/exonote3.exn` 

## The context object
The context object is a namedtuple instance whose fields are:
- viewer: the `exonote.Viewer` instance which exposes the API to manipulate the representation of the currently displayed exonote;
- arguments: list of arguments passed to this function in the exonote.

## ASCII Art
The ASCII Art at the beginning of the CLI help text is made with [patorjk's TAAG](https://patorjk.com/software/taag/#p=display&f=Roman&t=E%20X%20N)


# Installation
**Exn** is **cross platform** and versions under **1.0.0** will be considered **Beta** at best. It is built on [Ubuntu](https://ubuntu.com/download/desktop) with [Python 3.8](https://www.python.org/downloads/) and should work on **Python 3.5** or **newer**.

## For the first time

```bash
$ pip install exn
```

## Upgrade
```bash
$ pip install exn --upgrade --upgrade-strategy eager

```

<br>
<br>
<br>

[Back to top](#readme)




















