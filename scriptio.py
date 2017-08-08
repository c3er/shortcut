#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import enum

import tkinter
import tkinter.ttk as ttk

import gui
import config


handler = None


class OutputType(enum.Enum):
    invalid   = 0
    debug     = 1
    standard  = 2
    error     = 4
    exception = 3


class Output:
    def __init__(self, outputtype, msg):
        self.type = outputtype
        self.msg = msg


class ScriptIOHandler:
    def __init__(self):
        self.output = []
        self.outputbox = None
        self._input = ""
        self._hasinput = False

    @property
    def input(self):
        if self._hasinput:
            self._hasinput = False
            return self._input
        return ""

    @input.setter
    def input(self, val):
        self._input = val
        self._hasinput = True

    def setup_gui(self, parent):
        output_area = ttk.Frame(parent)
        self.outputbox = tkinter.Text(
            output_area,
            font=(config.font, config.fontsize, 'normal'),
            background="black"
        )
        self.outputbox.config(state="disabled")
        gui.setup_scrollbars(output_area, self.outputbox)
        output_area.pack(expand=True, fill="both")

        self.inputbox = ttk.Entry(parent)
        self.inputbox.pack(expand=True, fill="x")
        self.inputbox.bind("<Return>", self.inputhandler)

        self._configcolors()

        for msg in self.output:
            self._write(msg)

    def out(self, msg):
        self._write(Output(OutputType.standard, msg))

    def error(self, msg):
        self._write(Output(OutputType.error, msg))

    def exception(self, msg):
        self._write(Output(OutputType.exception, msg))

    def inputhandler(self, event=None):
        self.input = self.inputbox.get() + "\n"
        self.inputbox.delete(0, "end")
        return "break"

    def _write(self, output):
        if self.outputbox:
            self.outputbox.config(state="normal")
            self.outputbox.insert("end", output.msg, output.type)
            self.outputbox.config(state="disabled")
            self.outputbox.yview("end")
        else:
            self.output.append(output)

    def _configcolors(self):
        self.outputbox.tag_config(str(OutputType.debug), foreground="grey")
        self.outputbox.tag_config(str(OutputType.standard), foreground="lightgrey")
        self.outputbox.tag_config(str(OutputType.error), foreground="orange")
        self.outputbox.tag_config(str(OutputType.exception), foreground="orangered")
