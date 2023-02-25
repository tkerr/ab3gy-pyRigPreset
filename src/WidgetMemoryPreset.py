###############################################################################
# WidgetMemoryPreset.py
# Author: Tom Kerr AB3GY
#
# WidgetMemoryPreset class for use with the pyRigPreset application.
# Provides a UI widget to display and select an emulated memory preset similar
# to transceiver memories.
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
from src.DlgMemoryPreset import DlgMemoryPreset
from src.MemoryPresetStore import MemoryPresetStore
from src.RigCat import init_rig_cat, send_rig_cat_cmd, setup_split, close_rig_cat


##############################################################################
# Globals.
##############################################################################
DESCRIPTION_WIDTH = 48
FREQUENCY_WIDTH = 20
BUTTON_WIDTH = 8


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# WidgetMemoryPreset class.
##############################################################################
class WidgetMemoryPreset(object):
    """
    WidgetMemoryPreset class for use with the pyRigPreset application.
    Provides a UI widget to display and select an emulated memory preset similar
    to transceiver memories.
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
            The memory preset ID

        Returns
        -------
        None.
        """
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.id = 0  # Memory preset ID
        
        self.desc_text = tk.StringVar(self.frame)
        self.freq_text = tk.StringVar(self.frame)

        try:
            self.id = int(id)
        except Exception:
            print('WidgetMemoryPreset: Invalid memory preset ID: {}'.format(id))
            self.id = 0
            
        self.config = MemoryPresetStore(self.id)

        self.PADX = 3
        self.PADY = 1
        
        self._widget_init()
        
    # ------------------------------------------------------------------------
    def update_widget(self):
        """
        Update the widget UI fields.
        """
        desc = self.config.get_preset_desc()
        self.desc_text.set(desc)
        split = self.config.get_split()
        vfoa = '{:0.6f}'.format(self.config.get_vfoa_freq_mhz())
        vfob = '{:0.6f}'.format(self.config.get_vfob_freq_mhz())
        freq_text = ''
        if len(desc) > 0:
            freq_text = vfoa
            if split:
                freq_text += '/{}'.format(vfob)
        self.freq_text.set(freq_text)
        
    # ------------------------------------------------------------------------
    def _widget_init(self):
        """
        Internal method to create and initialize the UI widget.
        """
        col = 0
        
        lbl = tk.Label(self.frame, 
            textvariable=self.desc_text,
            font=tkFont.Font(size=10),
            width=DESCRIPTION_WIDTH,
            anchor='w',
            padx=3,
            pady=2,
            borderwidth=1,
            relief='solid')
        lbl.bind('<Button-3>', self._on_right_click)
        lbl.grid(
            row=0, 
            column=col,
            sticky='W',
            padx=(self.PADX, 1),
            pady=(0, self.PADY))
        col += 1
        
        lbl = tk.Label(self.frame, 
            textvariable=self.freq_text,
            font=tkFont.Font(size=10),
            width=FREQUENCY_WIDTH,
            anchor='e',
            padx=3,
            pady=2,
            borderwidth=1,
            relief='solid')
        lbl.bind('<Button-3>', self._on_right_click)
        lbl.grid(
            row=0, 
            column=col,
            sticky='W',
            padx=(0, self.PADX),
            pady=(0, self.PADY))
        col += 1
        
        btn = tk.Button(self.frame,
            width=BUTTON_WIDTH,
            text='M{}'.format(self.id),
            command=self._on_left_click,
            font=tkFont.Font(size=10))
        btn.bind('<Button-3>', self._on_right_click)
        btn.grid(
            row=0,
            column=col,
            padx=self.PADX,
            pady=(0, self.PADY))
        col += 1
        
        # Update the widget fields.
        self.update_widget()
    
    # ------------------------------------------------------------------------
    def _send_cat_cmd(self, cmd):
        """
        Send a CAT command to the transceiver.
        """
        if (len(cmd) > 0):
            print(cmd)
            resp = send_rig_cat_cmd(cmd)
            if 'ERROR' in resp: 
                print('Command: "{}" Response: "{}"'.format(cmd, resp))

    # ------------------------------------------------------------------------
    def _on_left_click(self):
        """
        Preset widget left click handler.
        """
        #print('Memory preset {} left button clicked.'.format(self.id))
        if init_rig_cat():
        
            # Use a single command to configure VFO, mode and split.
            vfoa_hz = int(self.config.get_vfoa_freq_mhz() * 1E6)
            vfob_hz = int(self.config.get_vfob_freq_mhz() * 1E6)
            resp = setup_split(
                vfoa_hz, 
                self.config.get_modea(), 
                self.config.get_split(), 
                vfob_hz, 
                self.config.get_modeb())
            if (resp != 'OK'):
                print('Error setting VFO and split parameters')

            # Set CTCSS config and tone.
            ctcss = self.config.get_ctcss_config()
            cmd = 'TONE ' + ctcss
            if (ctcss != 'OFF'):
                tone = str(self.config.get_ctcss_tone())
                cmd += (' ' + tone)
            self._send_cat_cmd(cmd)

            # Send commands 1 - 6.
            self._send_cat_cmd(self.config.get_command1())
            self._send_cat_cmd(self.config.get_command2())
            self._send_cat_cmd(self.config.get_command3())
            self._send_cat_cmd(self.config.get_command4())
            self._send_cat_cmd(self.config.get_command5())
            self._send_cat_cmd(self.config.get_command6())

        close_rig_cat()

    # ------------------------------------------------------------------------
    def _on_right_click(self, event):
        """
        Preset widget right click handler.
        """
        #print('Memory preset {} right button clicked.'.format(self.id))
        
        # Open the configuration dialog window and wait for it to complete.
        dlg = DlgMemoryPreset(self.parent, self.config)
        self.frame.wait_window(dlg.dlg_config_preset)
        
        # Update the widget fields.
        self.update_widget()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    globals.init()
    root = tk.Tk()
    root.title('WidgetMemoryPreset test application')
    wmb1 = WidgetMemoryPreset(root, id=1)
    wmb1.frame.grid(
        row=0,
        column=0,
        padx=6,
        pady=6)
    wmb2 = WidgetMemoryPreset(root, id=2)
    wmb2.frame.grid(
        row=1,
        column=0,
        padx=6,
        pady=6)
    root.mainloop()
   