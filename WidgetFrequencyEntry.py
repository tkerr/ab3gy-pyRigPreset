###############################################################################
# WidgetFrequencyEntry.py
# Author: Tom Kerr AB3GY
#
# WidgetFrequencyEntry class for use with the pyRigPreset application.
# Provides a UI widget to enter the VFO frequency.
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
# WidgetFrequencyEntry class.
##############################################################################
class WidgetFrequencyEntry(object):
    """
    WidgetFrequencyEntry class for use with the pyRigPreset application.
    Provides a UI widget to enter the VFO frequency.
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
        self.freq_mhz_text = tk.StringVar(self.frame)

        self.PADX = 3
        self.PADY = 3
        
        self._widget_init()
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        validateFloatCommand = self.frame.register(self._validate_float)
        lbl = tk.Label(self.frame, 
            text='VFO-A frequency (MHz):',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=0, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        tb = tk.Entry(self.frame,
            width=12,
            textvariable=self.freq_mhz_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=0, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)
        tb.bind('<Return>', self._set_frequency)

    # ------------------------------------------------------------------------
    def _set_frequency(self, event):
        """
        Event handler used to set the transceiver VFO-A frequency.
        """
        #print(event)
        freq_str = self.freq_mhz_text.get().strip()
        if (len(freq_str) > 0):
            freq_hz = int(float(freq_str) * 1E6)
            if init_rig_cat():
                cmd = 'FREQA {}'.format(freq_hz)
                resp = send_rig_cat_cmd(cmd)
            close_rig_cat()

    # ------------------------------------------------------------------------
    def _validate_float(self, why, where, what, all):
        """
        Validate a floating point number entry.

        Parameters
        ----------
            why : int
                Action code: 0 for an attempted deletion, 1 for an attempted 
                insertion, or -1 for everything else.
            where : int
                Index of the beginning of the insertion or deletion.
            what : str
                The text being inserted or deleted.
            all : str
                The value that the text will have if the change is allowed. 
        Returns
        -------
            status : bool
                True if the character string is allowable, False otherwise.
                The text entry box will accept the character if True, or reject it if False.
        """
        #print(str(why), str(where), str(what), str(all))
        idx = int(where)
        if (why != '1'): return True         # 1 = insertion
        if (len(all) > 10): return False     # Limit entry length
        if what.isnumeric(): return True
        if (what == '.'):
            if '.' in all[:idx]: return False # Only one occurrence allowed
            else: return True
        return False  # Nothing else allowed


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetFrequencyEntry test application not implemented.')
   