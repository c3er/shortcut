#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess


_test_script = """\
for ($i = 1; $i -le 10; $i++) {
    Write-Host "Iteration" + $i
    Start-Sleep 1
}
"""


def main():
    script = "{\n" + _test_script + "\n}"
    process = subprocess.Popen(
        # A "script block" can only be used if powershell is executed inside powershell
        "powershell -Command powershell -Command " + script
    )
    process.wait()


if __name__ == "__main__":
    main()