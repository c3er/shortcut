#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter.ttk as ttk


def setup_scrollbars(container, widget):
    vsb = ttk.Scrollbar(container, orient="vertical", command=widget.yview)
    widget.configure(yscrollcommand=vsb.set)

    widget.grid(column=0, row=0, sticky='nsew', in_=container)
    vsb.grid(column=1, row=0, sticky='ns')

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)
