###############################################################################
# WidgetTxRx.py
# Author: Tom Kerr AB3GY
#
# WidgetTxRx class for use with the pyRigPreset application.
# Provides a UI widget to turn PTT on and off.
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
from src.RigCat import init_rig_cat, send_rig_cat_cmd, close_rig_cat


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetTxRx class.
##############################################################################
class WidgetTxRx(object):
    """
    WidgetTxRx class for use with the pyRigPreset application.
    Provides a UI widget to turn PTT on and off.
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
        self.PADX = 3
        self.PADY = 3
        self.parent = parent
        self.frame = tk.Frame(parent,
            highlightbackground='black',
            highlightthickness=1,
            padx=self.PADX,
            pady=self.PADY,)
        self._widget_init()
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        tx_btn = tk.Button(self.frame,
            width=6,
            text='TX',
            fg='red',
            command=self._ptt_on,
            font=tkFont.Font(size=10, weight=tkFont.BOLD))
        tx_btn.grid(
            row=0, 
            column=0,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)
        rx_btn = tk.Button(self.frame,
            width=6,
            text='RX',
            fg='green',
            command=self._ptt_off,
            font=tkFont.Font(size=10, weight=tkFont.BOLD))
        rx_btn.grid(
            row=0, 
            column=1,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)

    # ------------------------------------------------------------------------
    def _ptt_on(self):
        """
        Event handler used to turn PTT on.
        """
        self._send_cmd('PTT ON')
        
    # ------------------------------------------------------------------------
    def _ptt_off(self):
        """
        Event handler used to turn PTT off.
        """
        self._send_cmd('PTT OFF')
    
    # ------------------------------------------------------------------------
    def _send_cmd(self, cmd):
        """
        Send a command to the transceiver.
        """
        if init_rig_cat(read_timeout=0.1):
            print(cmd)
            resp = send_rig_cat_cmd(cmd)
            if 'ERROR' in resp:
                print('Command: "{}" Response: "{}"'.format(cmd, resp))
        close_rig_cat()

##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('WidgetTxRx test application not implemented.')
   