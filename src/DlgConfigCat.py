###############################################################################
# DlgConfigCat.py
# Author: Tom Kerr AB3GY
#
# DlgConfigCat class for use with the pyRigPreset application.
# Implements a dialog box for configuring transceiver CAT control.
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
from serial.tools import list_ports as lp

# Tkinter packages.
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

# Local packages.
import globals
from src.pyRigPresetUtils import set_geometry


##############################################################################
# Globals.
##############################################################################

# The list of supported transceivers.
rig_list = (
    'NONE',
    'FT-817',
    'FT-991',
    'IC-7000',
    )

# The list of selectable baud rates.
baud_list = (
    '1200',
    '2400',
    '4800',
    '9600',
    '19200',
    '38400',
    '57600',
    '115200',
)

# The list of selectable data bit sizes.
data_list = (
    '5',
    '6',
    '7',
    '8',
)

# The list of selectable parity types.
parity_list = (
    'NONE',
    'EVEN',
    'ODD',
)

# The list of selectable stop bit sizes.
stop_list = (
    '1',
    '1.5',
    '2',
)


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def get_serial_ports():
    """
    Return a list of serial ports on this machine.
    """
    port_list = []
    ports = lp.comports()
    for p in ports:
        port_list.append(p.device)
    return port_list


##############################################################################
# DlgConfigCat class.
##############################################################################
class DlgConfigCat(object):
    """
    DlgConfigCat class for use with the pySatCat application.
    Implements a dialog box for configuring the Computer Aided Transceiver (CAT)
    interface.
    """

    # ------------------------------------------------------------------------
    def __init__(self, root, id):
        """
        Class constructor.
    
        Parameters
        ----------
        root : Tk object
            The pySatCat application root window.
        id : int
            The CAT interface ID.
        
        Returns
        -------
        None.
        """
        self.root = root            # The root window
        self.id = id                # The CAT interface ID
        self.dlg_config_cat = tk.Toplevel(self.root)
        self.dlg_config_cat.title('CAT Interface {} Configuration'.format(id))
        self.section = 'CAT_PRESET{:03d}'.format(id)  # CAT interface preset section in config file
        
        # Control variables.
        self.name_text      = tk.StringVar(self.root)
        self.rig_text       = tk.StringVar(self.root)
        self.port_text      = tk.StringVar(self.root)
        self.baud_text      = tk.StringVar(self.root)
        self.parity_text    = tk.StringVar(self.root)
        self.stop_bits_text = tk.StringVar(self.root)
        self.data_bits_text = tk.StringVar(self.root)

        self._dlg_init()

    # ------------------------------------------------------------------------
    def _dlg_init(self):
        """
        Internal method to create and initialize the dialog box.
        """
        global rig_list
        global baud_list
        global data_list
        global parity_list
        global stop_list
        
        # Initialize parameters.
        
        # Build the list of serial ports on this machine.
        port_list = ['NONE']
        serial_list = get_serial_ports()
        for s in serial_list:
            port_list.append(s)
        
        # Get existing config settings.
        name = str(globals.config.get(self.section, 'NAME'))
        if (len(name) > 0): self.name_text.set(name)
        else: self.name_text.set('Rig {}'.format(self.id))
        
        rig = str(globals.config.get(self.section, 'RIG'))
        if (len(rig) > 0): self.rig_text.set(rig)
        else: self.rig_text.set(rig_list[0])
        
        port = str(globals.config.get(self.section, 'PORT'))
        if (len(port) > 0): self.port_text.set(port)
        else: self.port_text.set(port_list[0])
        
        self.baud_text.set(str(globals.config.get(self.section, 'BAUD')))
        
        data = str(globals.config.get(self.section, 'DATA'))
        if (len(data) > 0): self.data_bits_text.set(data)
        else: self.data_bits_text.set('8')
        
        parity = str(globals.config.get(self.section, 'PARITY'))
        if (len(parity) > 0): self.parity_text.set(parity)
        else: self.parity_text.set('NONE')
        
        stop = str(globals.config.get(self.section, 'STOP'))
        if (len(stop) > 0): self.stop_bits_text.set(stop)
        else: self.stop_bits_text.set('1')
        
        row = 0
        
        # Configuration name.
        ttk.Label(self.dlg_config_cat, text='Name:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        tb_name = tk.Entry(
            self.dlg_config_cat,
            width=12,
            textvariable=self.name_text,
            font=tkFont.Font(size=10))
        tb_name.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Rig selection menu.
        ttk.Label(self.dlg_config_cat, text='Rig:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_rig = tk.OptionMenu(
            self.dlg_config_cat,
            self.rig_text,
            *rig_list)
        mnu_rig.config(width=10)
        mnu_rig.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Port selection menu.
        ttk.Label(self.dlg_config_cat, text='Port:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_port = tk.OptionMenu(
            self.dlg_config_cat,
            self.port_text,
            *port_list)
        mnu_port.config(width=10)
        mnu_port.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Baud rate selection menu.
        ttk.Label(self.dlg_config_cat, text='Baud:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_baud = tk.OptionMenu(
            self.dlg_config_cat,
            self.baud_text,
            *baud_list)
        mnu_baud.config(width=10)
        mnu_baud.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Data bits selection menu.
        ttk.Label(self.dlg_config_cat, text='Data bits:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_data = tk.OptionMenu(
            self.dlg_config_cat,
            self.data_bits_text,
            *data_list)
        mnu_data.config(width=10)
        mnu_data.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Parity selection menu.
        ttk.Label(self.dlg_config_cat, text='Parity:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_parity = tk.OptionMenu(
            self.dlg_config_cat,
            self.parity_text,
            *parity_list)
        mnu_parity.config(width=10)
        mnu_parity.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1
        
        # Stop bits selection menu.
        ttk.Label(self.dlg_config_cat, text='Stop bits:  ').grid(row=row, column=0, padx=3, pady=6, sticky='E')
        mnu_stop = tk.OptionMenu(
            self.dlg_config_cat,
            self.stop_bits_text,
            *stop_list)
        mnu_stop.config(width=10)
        mnu_stop.grid(row=row, column=1, padx=6, pady=3, sticky='W')
        row += 1

        # Button frame for OK/Cancel buttons.
        btn_frm = tk.Frame(self.dlg_config_cat)
        
        # OK button.
        btn_ok = tk.Button(btn_frm, 
            text='OK', 
            width=10, 
            command=self._dlg_config_cat_ok)
        btn_ok.grid(row=0, column=0, padx=6, pady=6)
        
        # Cancel button.
        btn_cancel = tk.Button(btn_frm, 
            text='Cancel', 
            width=10, 
            command=self.dlg_config_cat.destroy)
        btn_cancel.grid(row=0, column=1, padx=6, pady=6)
        
        # Center the buttons at the bottom of the dialog box.
        btn_frm.grid(row=row, column=0, columnspan=4, padx=6, pady=6)
    
        mnu_rig.focus_set()
        self.dlg_config_cat.grab_set() # Make the dialog modal
        
        # Set the proper window size and center it on the screen.
        set_geometry(self.dlg_config_cat)

    # ------------------------------------------------------------------------
    def _dlg_config_cat_ok(self):
        """
        Dialog box OK button handler.
        """
        if not globals.config.has_section(self.section):
            globals.config.add_section(self.section)
        globals.config.set(self.section, 'NAME', self.name_text.get())
        globals.config.set(self.section, 'RIG', self.rig_text.get())
        globals.config.set(self.section, 'PORT', self.port_text.get())
        globals.config.set(self.section, 'BAUD', self.baud_text.get())
        globals.config.set(self.section, 'DATA', str(self.data_bits_text.get()))
        globals.config.set(self.section, 'PARITY', self.parity_text.get())
        globals.config.set(self.section, 'STOP', self.stop_bits_text.get())
        
        # Save parameters to .INI file.
        globals.config.write()

        self.dlg_config_cat.destroy()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('DlgConfigCat main program not implemented.')
