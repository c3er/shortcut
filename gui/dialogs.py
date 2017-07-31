#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess

import tkinter
import tkinter.ttk as ttk

import scriptio


class _DialogBase(tkinter.Toplevel):
    def __init__(self, parent, title = None):
        """Must be called after initialization of inheriting classes."""

        super().__init__(parent)

        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.canceled = False
        self.result = None

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50)
        )
        self.initial_focus.focus_set()
        self.wait_window(self)

    def close(self, event = None):
        """Give focus back to the parent window and close the dialog."""
        self.parent.focus_set()
        self.destroy()

    # Methods to overwrite #####################################################
    def body(self, master):
        """Create dialog
        Returns a widget, which should have the focus immediatly. This method
        should be overwritten.
        """
        pass

    def buttonbox(self):
        """Add standard button box
        Overwrite, if there are no standard buttons wanted.
        """
        box = ttk.Frame(self)

        ttk.Button(
            box,
            text="Cancel",
            width=10,
            command=self.cancel
        ).pack(side='right', padx=5, pady=5)

        ttk.Button(
            box,
            text="OK",
            width=10,
            command=self.ok,
            default=tkinter.ACTIVE
        ).pack(side='right', padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(fill='x')

    # Standard button behavior ###
    def ok(self, event=None):
        """Execute the validate function and if it returns False, it will just
        set the focus right and return.
        If validate returns True, then the apply function will be called and the
        dialog will be closed.
        """
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.close()

    def cancel(self, event=None):
        """Performs an Abortion of the dialog."""
        self.canceled = True
        self.close(event)
    ###

    # Command hooks ###
    def validate(self):
        """Overwrite.
        Validate the input. If the function returns false, the dialog will stay
        open.
        """
        return True

    def apply(self):
        """Overwrite.
        Process the input. This function will be called, after the dialog was
        closed.
        """
        pass
    ###
    ############################################################################


class ExecutionDialog(_DialogBase):
    def __init__(self, parent, script):
        self.parent = parent
        self.handler = scriptio.ScriptIOHandler()
        self.process = subprocess.Popen(
            'powershell -ExecutionPolicy Unrestricted "{}"'.format(script.filepath),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            universal_newlines=True
        )
        parent.after(100, self._poll_process)
        super().__init__(parent, "Executing {}".format(script.name))

    @property
    def executing(self):
        return self.process.poll() is None

    def stop(self, event=None):
        self.process.kill()
        self.set_close(True)
        self.set_stop(False)

    def set_stop(self, isenabled):
        self.stopbutton.config(state=self._statestr(isenabled))        

    def set_close(self, isenabled):
        self.closebutton.config(state=self._statestr(isenabled))

    # Inherited from _DialogBase ###############################################
    def body(self, parent):
        self.handler.setup_gui(parent)
        return self.handler.inputbox

    def buttonbox(self):
        box = ttk.Frame(self)

        self.stopbutton = ttk.Button(
            box,
            text="Stop",
            width=10,
            command=self.stop
        )
        self.stopbutton.pack(side='right', padx=5, pady=5)

        self.closebutton = ttk.Button(
            box,
            text="Close",
            width=10,
            command=self.ok,
            state="disabled"
        )
        self.closebutton.pack(side='right', padx=5, pady=5)

        box.pack(fill='x')

    def validate(self):
        return not self.executing
    ############################################################################

    def _poll_process(self):
        if self.executing:
            stdout = self.process.stdout.read()
            stderr = self.process.stderr.read()
            stdin = self.handler.input

            if stdout:
                self.handler.out(stdout)
            if stderr:
                self.handler.error(stderr)
            if stdin:
                self.process.stdin.write(stdin)

            self.parent.after(100, self._poll_process)
        else:
            self.set_close(True)
            self.set_stop(False)

    @staticmethod
    def _statestr(isenabled):
        return "enabled" if isenabled else "disabled"
