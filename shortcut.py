#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import subprocess

import tkinter
import tkinter.ttk as ttk


class ScriptData:
    def __init__(self, *, name, filename):
        self.name = name
        self.filename = filename

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, encoding="utf8") as f:
            data = json.load(f)
        scripts = []
        for scriptentry in data["scripts"]:
            name = scriptentry["name"]
            filename = scriptentry["file"]
            scripts.append(cls(name=name, filename=filename))
        return scripts


class CurrentDirEntry:
    def __init__(self, parent, label):
        ttk.Label(parent, text=label).pack(side='top', anchor='w')

        self.entry = ttk.Entry(parent, width=100)
        self.entry.pack(side="top")

    @property
    def value(self):
        return self.entry.get()


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def create_menu(parent, scripts):
    frame = ttk.Frame(parent)
    for script in scripts:
        ttk.Button(
            frame,
            text=script.name,
            command=lambda: print(script.filename)
        ).pack(fill="x")
    frame.pack(side="top", fill="both")


def main():
    # script = "{\n" + _test_script + "\n}"
    # process = subprocess.Popen(
    #     # A "script block" can only be used if powershell is executed inside powershell
    #     "powershell -Command powershell -Command " + script
    # )
    # process.wait()

    jsonpath = os.path.join(getscriptpath(__file__), "scripts", "scripts.json")
    scripts = ScriptData.from_json(jsonpath)

    root = tkinter.Tk()
    cdentry = CurrentDirEntry(root, "Current directory")
    create_menu(root, scripts)

    root.mainloop()


if __name__ == "__main__":
    main()
