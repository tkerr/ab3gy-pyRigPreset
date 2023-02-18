###############################################################################
# WidgetCommandEntry.py
# Author: Tom Kerr AB3GY
#
# WidgetCommandEntry class for use with the pyRigPreset application.
# Provides a UI widget to enter a transceiver command.
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2023 Tom Kerr AB3GY (ab3gy@arrl.net).
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,   
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,  
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################

# System level packages.
import os

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

# Local packages.
import globals
from RigCat import init_rig_cat, send_rig_cat_cmd, close_rig_cat


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetCommandEntry class.
##############################################################################
class WidgetCommandEntry(object):
    """
    WidgetCommandEntry class for use with the pyRigPreset application.
    Provides a UI widget to enter a transceiver command.
    """
    # ------------------------------------------------------------------------
    def __init__(self, parent):
        """
        Class constructor.
        
        Parameters
        ----------
        parent : Tk object
            The parent object containing the widget

        Returns
        -------
        None.
        """
        self.parent = parent
        self.frame = tk.Frame(parent,
            highlightbackground='black',
            highlightthickness=1,
            padx=3,
            pady=3,)
        self.tb_cmd = None # The command text box
        self.command_text = tk.StringVar(self.frame)

        self.PADX = 3
        self.PADY = 3
        
        self._widget_init()
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        lbl = tk.Label(self.frame, 
            text='Command:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=0, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        self.tb_cmd = tk.Entry(self.frame,
            width=20,
            textvariable=self.command_text,
            validate='key', 
            font=tkFont.Font(size=10))
        self.tb_cmd.grid(
            row=0, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)
        self.tb_cmd.bind('<Return>', self._send_command)

    # ------------------------------------------------------------------------
    def _send_command(self, event):
        """
        Event handler used to set the transceiver VFO-A frequency.
        """
        #print(event)
        cmd = self.command_text.get().strip()
        if init_rig_cat():
            resp = send_rig_cat_cmd(cmd)
        close_rig_cat()
        self.tb_cmd.delete(0, tk.END)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetCommandEntry test application not implemented.')
   