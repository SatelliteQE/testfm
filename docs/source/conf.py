# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config
# -- Project information -----------------------------------------------------

project = "TestFM"
copyright = "2018, satellite6qe"
author = "satellite6qe"

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = "0.1.4"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = "python3"
exclude_patterns = ["_build"]
pygments_style = None
autodoc_default_options = {"members": None, "undoc-members": None}

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = "Testfmdoc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
latex_documents = [
    (master_doc, "Testfm.tex", "Testfm Documentation", "satellite6qe", "manual"),
]

# -- Options for manual page output ------------------------------------------

man_pages = [(master_doc, "testfm", "Testfm Documentation", [author], 1)]
texinfo_documents = [
    (
        master_doc,
        "Testfm",
        "Testfm Documentation",
        author,
        "Testfm",
        "A test suite based on pytest-ansible that exercises The Foreman-maintain tool.",
        "Miscellaneous",
    ),
]

# -- Options for Epub output -------------------------------------------------

epub_title = project
epub_exclude_files = ["search.html"]
