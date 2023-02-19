###############################################################################
# DlgConfigPreset.py
# Author: Tom Kerr AB3GY
#
# DlgConfigPreset class for use with the pyRigPreset application.
# Implements a dialog box for configuring a transceiver preset consisting
# of a series of CAT commands.
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

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

# Local environment init.
import _env_init

# Local packages.
import globals
from src.pyRigPresetUtils import *
from src.ConfigPresetStore import ConfigPresetStore
from PyRigCat.PyRigCat import OperatingMode

##############################################################################
# Globals.
##############################################################################
ALLOWED_TEXT = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.+-?'


##############################################################################
# Functions.
##############################################################################


##############################################################################
# DlgConfigPreset class.
##############################################################################
class DlgConfigPreset(object):
    """
    DlgConfigPreset class for use with the pyRigPreset application.
    Implements a dialog box for configuring a transceiver preset consisting
    of a series of CAT commands.
    """

    # ------------------------------------------------------------------------
    def __init__(self, root, config):
        """
        Class constructor.
    
        Parameters
        ----------
        root : Tk object
            The parent object root window.
        config : ConfigPresetStore object
            The ConfigPresetStore object storing the configuration data.
        
        Returns
        -------
        None.
        """
        self.root = root # The root window
        self.dlg_config_preset = tk.Toplevel(root)  # The dialog box
        self.dlg_config_preset.title('Transceiver Preset Configuration')
        self.config = config  # ConfigPresetStore object
        
        self.PADX = 3
        self.PADY = 1
        
        # Text entry variables.
        self.preset_name_text = tk.StringVar(self.root)    # Preset name
        self.cmd = []
        for idx in range(globals.NUM_CONFIG_COMMANDS):
            self.cmd.append(tk.StringVar(self.root))
        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        # Input validation callbacks.
        validateTextCommand = self.dlg_config_preset.register(self._validate_text)
        
        # Initialize the GUI objects.
        row = 0
        
        # Preset name.
        lbl = tk.Label(self.dlg_config_preset, 
            text='Name:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset,
            width=32,
            textvariable=self.preset_name_text,
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX, 
            pady=self.PADY)
        row += 1
        
        # Transcriver configuration commands.
        for idx in range(globals.NUM_CONFIG_COMMANDS):
            lbl = tk.Label(self.dlg_config_preset, 
                text='Command {}:'.format(idx+1),
                font=tkFont.Font(size=10))
            lbl.grid(
                row=row, 
                column=0,
                sticky='E',
                padx=self.PADX,
                pady=self.PADY)
            tb = tk.Entry(self.dlg_config_preset,
                width=32,
                textvariable=self.cmd[idx],
                validate='key', 
                validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'),
                font=tkFont.Font(size=10))
            tb.grid(
                row=row, 
                column=1,
                sticky='W',
                padx=self.PADX,
                pady=self.PADY)
            row += 1

        # Button frame for OK/Cancel/Clear buttons.
        btn_frm = tk.Frame(self.dlg_config_preset)
        
        # OK button.
        btn_ok = tk.Button(btn_frm, 
            text='OK', 
            width=10, 
            command=self._dlg_config_preset_ok)
        btn_ok.grid(row=0, column=0, padx=6, pady=6)
        
        # Cancel button.
        btn_cancel = tk.Button(btn_frm, 
            text='Cancel', 
            width=10, 
            command=self._dlg_config_preset_cancel)
        btn_cancel.grid(row=0, column=1, padx=6, pady=6)
        
        # Clear button.
        btn_ok = tk.Button(btn_frm, 
            text='Clear', 
            width=10, 
            command=self._dlg_config_preset_clear)
        btn_ok.grid(row=0, column=2, padx=6, pady=6)
        
        # Center the buttons at the bottom of the dialog box.
        btn_frm.grid(row=row, column=0, columnspan=2, padx=6, pady=6)
        
        # Initialize dialog variables.
        #self.config.init()  # Do not init or default name could be lost.
        self.preset_name_text.set(self.config.get_preset_name())
        for idx in range(globals.NUM_CONFIG_COMMANDS):
            self.cmd[idx].set(self.config.get_config_cmd(idx))

        # Make the dialog modal.
        self.dlg_config_preset.grab_set() 
        
        # Set the proper window size and center it on the screen.
        set_geometry(self.dlg_config_preset)

    # ------------------------------------------------------------------------
    def _dlg_config_preset_cancel(self):
        """
        Dialog box Cancel button handler.
        """
        self.dlg_config_preset.grab_release()
        self.dlg_config_preset.destroy()
        
    # ------------------------------------------------------------------------
    def _dlg_config_preset_ok(self):
        """
        Dialog box OK button handler.
        """
        self.config.set_preset_name(self.preset_name_text.get())
        for idx in range(globals.NUM_CONFIG_COMMANDS):
            cmd = self.cmd[idx].get()
            self.config.set_config_cmd(idx, cmd)
 
        self.config.write_config()
        self.dlg_config_preset.grab_release()
        self.dlg_config_preset.destroy()
        
    # ------------------------------------------------------------------------     
    def _dlg_config_preset_clear(self):
        """
        Dialog box Clear button handler.
        """
        self.preset_name_text.set('')
        for idx in range(globals.NUM_CONFIG_COMMANDS):
            self.cmd[idx].set('')

    # ------------------------------------------------------------------------
    def _validate_text(self, why, where, what, all):
        """
        Validate a text command entry.

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
        if (why != '1'): return True                    # 1 = insertion
        if (what.upper() in ALLOWED_TEXT): return True  # Check against set of allowed characters
        return False  # Nothing else allowed


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('DlgConfigPreset test program.')
    globals.init()
    root = tk.Tk()
    id = 1
    pc = ConfigPresetStore(id)
    dlg = DlgConfigPreset(root, pc)
    root.mainloop()
