#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import subprocess

import tkinter
import tkinter.ttk as ttk

import misc


class ScriptData:
    def __init__(self, *, name, filepath):
        self.name = name
        self.filepath = filepath

    def execute(self, currentdir):
        oldcwd = os.getcwd()
        os.chdir(currentdir)
        try:
            process = subprocess.Popen(
                'powershell -ExecutionPolicy Unrestricted "{}"'.format(self.filepath)
            )
            process.wait()
        finally:
            os.chdir(oldcwd)

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, encoding="utf8") as f:
            data = json.load(f)
        scripts = []
        for scriptentry in data["scripts"]:
            name = scriptentry["name"]
            filename = scriptentry["file"]
            scripts.append(cls(
                name=name,
                filepath=os.path.join(misc.getdirpath(filepath), filename)
            ))
        return scripts


class ScriptController:
    def __init__(self, script, cdentry):
        self.script = script
        self.cdentry = cdentry

    def __call__(self, event=None):
        self.script.execute(self.cdentry.value)


class CurrentDirEntry:
    def __init__(self, parent, label):
        ttk.Label(parent, text=label).pack(side='top', anchor='w')

        self.entry = ttk.Entry(parent, width=100)
        self.entry.pack(side="top")
        self._setentry(self.entry, "C:\\")

    @property
    def value(self):
        return self.entry.get()

    @staticmethod
    def _setentry(entry, text):
        entry.delete(0, 'end')
        entry.insert(0, text)


def create_menu(parent, scripts, cdentry):
    frame = ttk.Frame(parent)
    for script in scripts:
        ttk.Button(
            frame,
            text=script.name,
            command=ScriptController(script, cdentry)
        ).pack(fill="x")
    frame.pack(side="top", fill="both")


def main():
    jsonpath = os.path.join(misc.getdirpath(__file__), "scripts", "scripts.json")
    scripts = ScriptData.from_json(jsonpath)

    root = tkinter.Tk()
    root.wm_title("Shortcuts")
    cdentry = CurrentDirEntry(root, "Current directory")
    create_menu(root, scripts, cdentry)

    root.mainloop()


if __name__ == "__main__":
    main()
