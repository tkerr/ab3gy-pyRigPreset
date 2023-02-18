###############################################################################
# DlgMemoryPreset.py
# Author: Tom Kerr AB3GY
#
# DlgMemoryPreset class for use with the pyRigPreset application.
# Implements a dialog box for configuring an emulated memory preset.
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
from pyRigPresetUtils import *
from PyRigCat.PyRigCat import OperatingMode
from MemoryPresetStore import MemoryPresetStore, CTCSS_CONFIG

##############################################################################
# Globals.
##############################################################################

# Dictionary of CTCSS tones for satellites that require them.
# Key = tone frequency, value = CAT control parameter
CTCSS_TONES = [
      '0.0',
     '67.0',  '69.3',  '71.9',  '74.4',  '77.0',
     '79.7',  '82.5',  '85.4',  '88.5',  '91.5',
     '94.8',  '97.4', '100.0', '103.5', '107.2',
    '110.9', '114.8', '118.8', '123.0', '127.3',
    '131.8', '136.5', '141.3', '146.2', '151.4',
    '156.7', '159.8', '162.2', '165.5', '167.9',
    '171.3', '177.3', '179.9', '183.5', '186.2',
    '189.9', '192.8', '196.6', '199.5', '203.5',
    '206.5', '210.7', '218.1', '225.7', '229.1',
    '233.6', '241.8', '250.3', '254.1']

ALLOWED_TEXT = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.+-?'


##############################################################################
# Functions.
##############################################################################


##############################################################################
# DlgMemoryPreset class.
##############################################################################
class DlgMemoryPreset(object):
    """
    DlgMemoryPreset class for use with the pyRigPreset application.
    Implements a dialog box for configuring an emulated memory preset.
    """

    # ------------------------------------------------------------------------
    def __init__(self, root, config):
        """
        Class constructor.
    
        Parameters
        ----------
        root : Tk object
            The parent object root window.
        config : MemoryPresetStore object
            The MemoryPresetStore object storing the configuration data.
        
        Returns
        -------
        None.
        """
        self.root = root # The root window
        self.dlg_config_preset = tk.Toplevel(root)  # The dialog box
        self.dlg_config_preset.title('Memory Preset Configuration')
        self.config = config  # MemoryPresetStore object
        self.tb_vfob = None   # Text entry box for VFO-B
        self.mnu_modeb = None # Menu for VFO-B operating mode
        
        self.PADX = 3
        self.PADY = 1
        
        # Text entry variables.
        self.preset_desc_text = tk.StringVar(self.root)    # Preset description
        self.vfoa_freq_mhz_text = tk.StringVar(self.root)  # VFO-A frequency in MHz
        self.vfob_freq_mhz_text = tk.StringVar(self.root)  # VFO-B frequency in MHz
        self.split_text = tk.StringVar(self.root)          # Split mode operation
        self.split_text.trace('w', self._split_handler)    # Event handler when split mode changes
        self.modea_text = tk.StringVar(self.root)          # VFO-A operating mode
        self.modeb_text = tk.StringVar(self.root)          # VFO-B operating mode
        self.ctcss_config_text = tk.StringVar(self.root)   # CTCSS configuration
        self.ctcss_tone_text = tk.StringVar(self.root)     # CTCSS tone
        self.command1_text = tk.StringVar(self.root)       # Additional text command 1
        self.command2_text = tk.StringVar(self.root)       # Additional text command 2
        self.command3_text = tk.StringVar(self.root)       # Additional text command 3
        self.command4_text = tk.StringVar(self.root)       # Additional text command 4
        self.command5_text = tk.StringVar(self.root)       # Additional text command 5
        self.command6_text = tk.StringVar(self.root)       # Additional text command 6

        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        # Input validation callbacks.
        validateFloatCommand = self.dlg_config_preset.register(self._validate_float)
        validateTextCommand = self.dlg_config_preset.register(self._validate_text)
        
        # Initialize the GUI objects.
        row = 0
        
        # Preset description.
        lbl = tk.Label(self.dlg_config_preset, 
            text='Description:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset,
            width=48,
            textvariable=self.preset_desc_text,
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX, 
            pady=(8, self.PADY))
        row += 1
        
        # VFO-A frequency.
        lbl = tk.Label(self.dlg_config_preset, 
            text='VFO-A frequency:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset,
            width=12,
            textvariable=self.vfoa_freq_mhz_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        tb.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)
        row += 1
        
        # VFO-B frequency.
        lbl = tk.Label(self.dlg_config_preset, 
            text='VFO-B frequency:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        self.tb_vfob = tk.Entry(self.dlg_config_preset,
            width=12,
            textvariable=self.vfob_freq_mhz_text,
            validate='key', 
            validatecommand=(validateFloatCommand, '%d', '%i', '%S', '%P'),
            font=tkFont.Font(size=10))
        self.tb_vfob.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)
        row += 1
        
        # Split mode operation menu.
        lbl = tk.Label(self.dlg_config_preset, 
            text='Split:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.split_text,
            'OFF', 'ON')
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)    
        row += 1
        
        # VFO-A mode selection menu.
        lbl = tk.Label(self.dlg_config_preset, 
            text='VFO-A mode:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.modea_text,
            *OperatingMode.MODE_LIST)
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)    
        row += 1
        
        # VFO-B mode selection menu.
        lbl = tk.Label(self.dlg_config_preset, 
            text='VFO-B mode:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        self.mnu_modeb = tk.OptionMenu(
            self.dlg_config_preset,
            self.modeb_text,
            *OperatingMode.MODE_LIST)
        self.mnu_modeb.config(width=10)
        self.mnu_modeb.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)    
        row += 1
        
        # CTCSS configuration menu.
        lbl = tk.Label(self.dlg_config_preset, 
            text='CTCSS:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.ctcss_config_text,
            *CTCSS_CONFIG)
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)    
        row += 1
        
        # CTCSS tone selection menu.
        lbl = tk.Label(self.dlg_config_preset, 
            text='CTCSS tone:',
            font=tkFont.Font(size=10))
        lbl.grid(
            row=row, 
            column=0,
            sticky='E',
            padx=self.PADX,
            pady=self.PADY)
        mnu = tk.OptionMenu(
            self.dlg_config_preset,
            self.ctcss_tone_text,
            *CTCSS_TONES)
        mnu.config(width=10)
        mnu.grid(
            row=row, 
            column=1,
            sticky='W',
            padx=self.PADX,
            pady=self.PADY)    
        row += 1
        
        # Additional text commands.
        lbl = tk.Label(self.dlg_config_preset, text='Command 1:', font=tkFont.Font(size=10))
        lbl.grid(row=row, column=0, sticky='E', padx=self.PADX, pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset, width=32, textvariable=self.command1_text, font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'))
        tb.grid(row=row, column=1, sticky='W', padx=self.PADX, pady=self.PADY)
        row += 1
        
        lbl = tk.Label(self.dlg_config_preset, text='Command 2:', font=tkFont.Font(size=10))
        lbl.grid(row=row, column=0, sticky='E', padx=self.PADX, pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset, width=32, textvariable=self.command2_text, font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'))
        tb.grid(row=row, column=1, sticky='W', padx=self.PADX, pady=self.PADY)
        row += 1
        
        lbl = tk.Label(self.dlg_config_preset, text='Command 3:', font=tkFont.Font(size=10))
        lbl.grid(row=row, column=0, sticky='E', padx=self.PADX, pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset, width=32, textvariable=self.command3_text, font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'))
        tb.grid(row=row, column=1, sticky='W', padx=self.PADX, pady=self.PADY)
        row += 1
        
        lbl = tk.Label(self.dlg_config_preset, text='Command 4:', font=tkFont.Font(size=10))
        lbl.grid(row=row, column=0, sticky='E', padx=self.PADX, pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset, width=32, textvariable=self.command4_text, font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'))
        tb.grid(row=row, column=1, sticky='W', padx=self.PADX, pady=self.PADY)
        row += 1
        
        lbl = tk.Label(self.dlg_config_preset, text='Command 5:', font=tkFont.Font(size=10))
        lbl.grid(row=row, column=0, sticky='E', padx=self.PADX, pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset, width=32, textvariable=self.command5_text, font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'))
        tb.grid(row=row, column=1, sticky='W', padx=self.PADX, pady=self.PADY)
        row += 1
        
        lbl = tk.Label(self.dlg_config_preset, text='Command 6:', font=tkFont.Font(size=10))
        lbl.grid(row=row, column=0, sticky='E', padx=self.PADX, pady=self.PADY)
        tb = tk.Entry(self.dlg_config_preset, width=32, textvariable=self.command6_text, font=tkFont.Font(size=10),
            validate='key', 
            validatecommand=(validateTextCommand, '%d', '%i', '%S', '%P'))
        tb.grid(row=row, column=1, sticky='W', padx=self.PADX, pady=self.PADY)
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
        self.config.init()
        self.preset_desc_text.set(self.config.get_preset_desc())
        
        vfoa_mhz = self.config.get_vfoa_freq_mhz()
        self.vfoa_freq_mhz_text.set('{:0.6f}'.format(vfoa_mhz))
        
        vfob_mhz = self.config.get_vfob_freq_mhz()
        self.vfob_freq_mhz_text.set('{:0.6f}'.format(vfob_mhz))
        
        split = self.config.get_split()
        if split: self.split_text.set('ON')
        else: self.split_text.set('OFF')
        
        self.modea_text.set(self.config.get_modea())
        self.modeb_text.set(self.config.get_modeb())
        
        ctcss = 'OFF'
        if (len(self.config.get_ctcss_config()) > 0):
            ctcss = self.config.get_ctcss_config()
        self.ctcss_config_text.set(ctcss)
        
        tone = self.config.get_ctcss_tone() / 10.0
        self.ctcss_tone_text.set('{:0.1f}'.format(tone))
        
        self.command1_text.set(self.config.get_command1())
        self.command2_text.set(self.config.get_command2())
        self.command3_text.set(self.config.get_command3())
        self.command4_text.set(self.config.get_command4())
        self.command5_text.set(self.config.get_command5())
        self.command6_text.set(self.config.get_command6())

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
        self.config.set_preset_desc(self.preset_desc_text.get())
        self.config.set_vfoa_freq_mhz(self.vfoa_freq_mhz_text.get())
        self.config.set_vfob_freq_mhz(self.vfob_freq_mhz_text.get())
        self.config.set_modea(self.modea_text.get())
        self.config.set_modeb(self.modeb_text.get())
        self.config.set_ctcss_config(self.ctcss_config_text.get())
        
        split = self.split_text.get()
        if (split == 'ON'):
            self.config.set_split(True)
        else:
            self.config.set_split(False)
        
        tone = float(self.ctcss_tone_text.get()) * 10.0
        self.config.set_ctcss_tone(tone)
        
        self.config.set_command1(self.command1_text.get())
        self.config.set_command2(self.command2_text.get())
        self.config.set_command3(self.command3_text.get())
        self.config.set_command4(self.command4_text.get())
        self.config.set_command5(self.command5_text.get())
        self.config.set_command6(self.command6_text.get())
        
        self.config.write_config()
        self.dlg_config_preset.grab_release()
        self.dlg_config_preset.destroy()
        
    # ------------------------------------------------------------------------     
    def _dlg_config_preset_clear(self):
        """
        Dialog box Clear button handler.
        """
        self.preset_desc_text.set('')
        self.vfoa_freq_mhz_text.set('0.000000')
        self.vfob_freq_mhz_text.set('0.000000')
        self.split_text.set('OFF')
        self.ctcss_config_text.set('OFF')
        self.ctcss_tone_text.set('0.0')
        self.command1_text.set('')
        self.command2_text.set('')
        self.command3_text.set('')
        self.command4_text.set('')
        self.command5_text.set('')
        self.command6_text.set('')
        
    # ------------------------------------------------------------------------    
    def _split_handler(self, *args):
        """
        Event handler for split mode operation variable changes.
        """
        split = self.split_text.get()
        #print('Split mode set to {}'.format(split))
        if split == 'OFF':
            # Disable VFO-B frequency entry if split mode is off.
            self.vfob_freq_mhz_text.set('{:0.6f}'.format(0.0))
            self.tb_vfob.config(state='disabled')
            self.mnu_modeb.config(state='disabled')
        else:
            self.tb_vfob.config(state='normal')
            self.mnu_modeb.config(state='normal')
    
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
    print('DlgMemoryPreset test program.')
    globals.init()
    root = tk.Tk()
    id = 1
    pc = MemoryPresetStore(id)
    dlg = DlgMemoryPreset(root, pc)
    root.mainloop()
