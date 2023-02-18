###############################################################################
# WidgetCatPreset.py
# Author: Tom Kerr AB3GY
#
# WidgetCatPreset class for use with the pyRigPreset application.
# Provides a UI widget to display and select a transceiver CAT interface
# configuration.
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

# Local environment init.
import _env_init

# Local packages.
import globals
from DlgConfigCat import DlgConfigCat
from CatPresetStore import CatPresetStore


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetCatPreset class.
##############################################################################
class WidgetCatPreset(object):
    """
    WidgetCatPreset class for use with the pyRigPreset application.
    Provides a UI widget to display and select a transceiver CAT interface
    configuration.
    """
    # ------------------------------------------------------------------------
    def __init__(self, parent):
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
        self.frame = tk.Frame(parent,
            highlightbackground='black',
            highlightthickness=1,
            padx=3,
            pady=3,)
        
        # Radio button labels.
        self.labels = []
        for idx in range(globals.NUM_CAT_PRESETS):
            self.labels.append(tk.StringVar(self.frame))
        
        # Radio button selection value.
        self.value = tk.IntVar(self.frame)

        self.PADX = 3
        self.PADY = 1
        
        self._widget_init()
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        globals.config.read(create=False)
        for idx in range(globals.NUM_CAT_PRESETS):
            pnum = idx + 1  # Preset number in configuration file
            self._set_label(pnum)
            btn = tk.Radiobutton(self.frame,
                textvariable=self.labels[idx],
                variable=self.value,
                value=pnum,
                command=self._on_left_click)
            btn.bind('<Button-3>', lambda event, a=pnum: self._on_right_click(a))
            btn.grid(
                row=0,
                column=idx,
                padx=self.PADX,
                pady=(self.PADY))
        
        pnum = 0
        preset = str(globals.config.get('CAT', 'PRESET'))
        if (len(preset) > 0): pnum = int(preset)
        self.value.set(pnum)
    
    # ------------------------------------------------------------------------
    def _set_label(self, pnum):
        """
        Set the radio button label from the config file.
        """
        idx = pnum - 1
        # Get preset name from config file.
        section = 'CAT_PRESET{:03d}'.format(pnum)  # CAT interface preset section in config file
        name = str(globals.config.get(section, 'NAME'))
        if (len(name) > 0):
            self.labels[idx].set(name)
        else:
            self.labels[idx].set('Rig {}'.format(pnum))
        
    # ------------------------------------------------------------------------
    def _on_left_click(self):
        """
        CAT preset widget left click handler.
        Selects the CAT interface.
        """
        pnum = self.value.get()
        #print('Left click, value = {}'.format(pnum))
        
        # Read the preset values.
        section = 'CAT_PRESET{:03d}'.format(pnum)
        if not globals.config.has_section(section):
            globals.config.add_section(section)
        rig = str(globals.config.get(section, 'RIG'))
        port = str(globals.config.get(section, 'PORT'))
        baud = str(globals.config.get(section, 'BAUD'))
        data = str(globals.config.get(section, 'DATA'))
        parity = str(globals.config.get(section, 'PARITY'))
        stop = str(globals.config.get(section, 'STOP'))
        
        # Write them to the current CAT selection.
        section = 'CAT'
        if not globals.config.has_section(section):
            globals.config.add_section(section)
        globals.config.set(section, 'PRESET', pnum)
        globals.config.set(section, 'RIG', rig)
        globals.config.set(section, 'PORT', port)
        globals.config.set(section, 'BAUD', baud)
        globals.config.set(section, 'DATA', data)
        globals.config.set(section, 'PARITY', parity)
        globals.config.set(section, 'STOP', stop)
        globals.config.write()

    # ------------------------------------------------------------------------
    def _on_right_click(self, pnum):
        """
        CAT preset widget right click handler.
        Opens a dilog box to configure the preset.
        """
        #print('Right click, pnum = {}'.format(pnum))
        dlg = DlgConfigCat(self.parent, pnum)
        self.frame.wait_window(dlg.dlg_config_cat)
        self._set_label(pnum)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    globals.init()
    root = tk.Tk()
    root.title('WidgetCatPreset test application')
    wcp = WidgetCatPreset(root)
    wcp.frame.grid(
        row=0,
        column=0,
        padx=6,
        pady=6)
    root.mainloop()
   