from os import system as system_call  # Execute a shell command
from platform import system as system_name  # Returns the system/OS name
from time import sleep
import sys

def clear_screen():
    """
    Clears the terminal screen.
    """

    # Clear command as function of OS
    command = "cls" if system_name().lower()=="windows" else "clear"

    # Action
    system_call(command)

def progressbar(rrange = 21, ssleep = 0.25):
    for i in range(rrange):
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
        sys.stdout.flush()
        sleep(ssleep)
