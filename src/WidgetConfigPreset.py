###############################################################################
# WidgetConfigPreset.py
# Author: Tom Kerr AB3GY
#
# WidgetConfigPreset class for use with the pyRigPreset application.
# Provides a UI widget to display and select a transceiver configuration
# preset consisting of a series of CAT commands.
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
from src.DlgConfigPreset import DlgConfigPreset
from src.ConfigPresetStore import ConfigPresetStore
from src.RigCat import init_rig_cat, send_rig_cat_cmd, close_rig_cat


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetConfigPreset class.
##############################################################################
class WidgetConfigPreset(object):
    """
    WidgetConfigPreset class for use with the pyRigPreset application.
    Provides a UI widget to display and select a transceiver configuration
    preset consisting of a series of CAT commands.
    """
    # ------------------------------------------------------------------------
    def __init__(self, parent, id):
        """
        Class constructor.
        
        Parameters
        ----------
        parent : Tk object
            The parent object containing the widget
        id : int
            The configuration preset ID

        Returns
        -------
        None.
        """
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.id = 0  # Memory preset ID
        
        self.name_text = tk.StringVar(self.frame)

        try:
            self.id = int(id)
        except Exception:
            print('WidgetConfigPreset: Invalid memory preset ID: {}'.format(id))
            self.id = 0
            
        self.config = ConfigPresetStore(self.id)

        self.PADX = 3
        self.PADY = 1
        
        self._widget_init()
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        btn = tk.Button(self.frame,
            width=10,
            textvariable=self.name_text,
            command=self._on_left_click,
            font=tkFont.Font(size=10))
        btn.bind('<Button-3>', self._on_right_click)
        btn.grid(
            row=0,
            column=0,
            padx=self.PADX,
            pady=(0, self.PADY))
        # Update the button text.
        self._set_name()

    # ------------------------------------------------------------------------
    def _set_name(self):
        """
        Set the button text with the preset name.
        """
        cfg_name = self.config.get_preset_name()
        if (len(cfg_name) == 0):
            cfg_name = 'C{}'.format(self.id)
            self.config.set_preset_name(cfg_name)
        self.name_text.set(cfg_name)
        
    # ------------------------------------------------------------------------
    def _on_left_click(self):
        """
        Preset widget left click handler.
        Send commands to the transceiver.
        """
        #print('Configuration preset {} left button clicked.'.format(self.id))
        if init_rig_cat():
            for idx in range(globals.NUM_CONFIG_COMMANDS):
                cmd = self.config.get_config_cmd(idx).strip()
                if (len(cmd) > 0):
                    resp = send_rig_cat_cmd(cmd)
        close_rig_cat()

    # ------------------------------------------------------------------------
    def _on_right_click(self, event):
        """
        Preset widget right click handler.
        """
        #print('Configuration preset {} right button clicked.'.format(self.id))
        
        # Open the configuration dialog window and wait for it to complete.
        dlg = DlgConfigPreset(self.parent, self.config)
        self.frame.wait_window(dlg.dlg_config_preset)
        
        # Update the button text.
        self._set_name()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    globals.init()
    root = tk.Tk()
    root.title('WidgetConfigPreset test application')
    wmb1 = WidgetConfigPreset(root, id=1)
    wmb1.frame.grid(
        row=0,
        column=0,
        padx=6,
        pady=6)
    wmb2 = WidgetConfigPreset(root, id=2)
    wmb2.frame.grid(
        row=1,
        column=0,
        padx=6,
        pady=6)
    root.mainloop()
   