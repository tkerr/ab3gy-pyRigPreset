###############################################################################
# RigCat.py
# Author: Tom Kerr AB3GY
#
# CAT control functions for the pyRigPreset application.
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

# Local environment init.
import _env_init

# Local packages.
import globals
from src.pyRigPresetUtils import *

# All the PyRigCat classes.
from PyRigCat.PyRigCat import *
from PyRigCat.PyRigCat_ft817 import PyRigCat_ft817
from PyRigCat.PyRigCat_ft991 import PyRigCat_ft991
from PyRigCat.PyRigCat_ic7000 import PyRigCat_ic7000


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def init_rig_cat(read_timeout=0.5):
    """
    Initialize the rig CAT control object.
    """
    #print('RigCat init_rig_cat enter', flush=True)
    section = 'CAT'
    rig = str(globals.config.get(section, 'RIG')).upper()
    port = str(globals.config.get(section, 'PORT'))
    baud = str(globals.config.get(section, 'BAUD'))
    data = str(globals.config.get(section, 'DATA'))
    parity = str(globals.config.get(section, 'PARITY'))
    stop = str(globals.config.get(section, 'STOP'))
    
    # Select the specified rig CAT object.
    if (rig == RigName.FT817):
        if (globals.rig_cat.NAME != RigName.FT817):
            globals.rig_cat = PyRigCat_ft817()
    elif (rig == RigName.FT991):
        if (globals.rig_cat.NAME != RigName.FT991):
            globals.rig_cat = PyRigCat_ft991()
    elif (rig == RigName.IC7000):
        if (globals.rig_cat.NAME != RigName.IC7000):
            globals.rig_cat = PyRigCat_ic7000()
    else:
        print ('Rig: ' + rig + ' not supported.')
        return False
    
    # Convert parameters to types expected by the PyRigCat classes.
    baud_t = int(baud)
    data_t = Datasize.EIGHT
    parity_t = Parity.NONE
    stop_t = Stopbits.ONE
    
    if (data == '5'): data_t = Datasize.FIVE
    elif (data == '6'): data_t = Datasize.SIX
    elif (data == '7'): data_t = Datasize.SEVEN
    
    if (parity == 'EVEN'): parity_t = Parity.EVEN
    elif (parity == 'ODD'): parity_t = Parity.ODD
    
    if (stop == '1.5'): stop_t = Stopbits.ONE_POINT_FIVE
    elif (stop == '2'): stop_t = Stopbits.TWO
    
    # Configure the serial port.
    config_ok = globals.rig_cat.config_port(
        port=port, 
        baudrate=baud_t,
        datasize=data_t,
        parity=parity_t,
        stopbits=stop_t,
        read_timeout=read_timeout)
    
    if config_ok:
        globals.rig_cat.init_rig()
    else:
        print('Transcriver serial port configuration error.')
    #print('RigCat init_rig_cat exit', flush=True)
    return config_ok

# ------------------------------------------------------------------------
def send_rig_cat_cmd(cmd_str):
    """
    Send an ASCII command string and return a response.
    """
    #print('RigCat send_cmd enter', flush=True)
    cmd_list = cmd_str.strip().split(' ')
    if (len(cmd_list) > 0):
        if (len(cmd_list) < 2): 
            cmd_list.append('')
        resp = globals.rig_cat.ascii_cmd(cmd_list[0], cmd_list[1:])
        print('Command: "{}" Response: "{}"'.format(cmd_str, resp))
    else:
        resp = globals.rig_cat.ERROR
    #print('RigCat send_cmd exit', flush=True)
    return resp

# ------------------------------------------------------------------------
def setup_split(vfoa_hz, modea, split, vfob_hz, modeb):
    """
    Single function to set all split operation parameters.
    """
    resp = globals.rig_cat.setup_split(vfoa_hz, modea, split, vfob_hz, modeb)
    return resp

# ------------------------------------------------------------------------
def close_rig_cat():
    """
    Close the rig CAT object.
    """
    #print('RigCat close_rig_cat enter', flush=True)
    if globals.rig_cat is not None:
        globals.rig_cat.close()
    #print('RigCat close_rig_cat exit', flush=True)
