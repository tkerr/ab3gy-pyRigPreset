###############################################################################
# MemoryPresetStore.py
# Author: Tom Kerr AB3GY
#
# MemoryPresetStore class for use with the pyRigPreset application.
# Provides a data container and configuration file read/write methods for
# an emulated memory preset.
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
from pyRigPresetUtils import *
from ConfigFile import ConfigFile
from PyRigCat.PyRigCat import OperatingMode


##############################################################################
# Globals.
##############################################################################

# CTCSS/DCS configuration list.
CTCSS_CONFIG = ['OFF', 'ENC', 'DEC']


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# MemoryPresetStore class.
##############################################################################
class MemoryPresetStore(object):
    """
    MemoryPresetStore class for use with the pyRigPreset application.
    Provides a data container and configuration file read/write methods for
    an emulated memory preset.
    """
    # ------------------------------------------------------------------------
    def __init__(self, id):
        """
        Class constructor.
        
        Parameters
        ----------
        id : int
            The memory preset ID

        Returns
        -------
        None.
        """
        self._id = 0  # Memory preset ID
        try:
            self._id = int(id)
        except Exception:
            print('MemoryPresetStore: Invalid memory preset ID: {}'.format(id))
            self._id = 0
        
        self._preset_desc = ''                   # Preset description
        self._vfoa_freq_mhz = 0.0                # VFO-A frequency in MHz
        self._vfob_freq_mhz = 0.0                # VFO-B frequency in MHz
        self._split = False                      # Split mode operation
        self._modea = OperatingMode.UNKNOWN      # VFO-A operating mode string
        self._modeb = OperatingMode.UNKNOWN      # VFO-B operating mode string
        self._ctcss_config = 'OFF'               # CTCSS configuration
        self._ctcss_tone = int(0)                # CTCSS tone number
        self._command1 = ''                      # Text command 1
        self._command2 = ''                      # Text command 2
        self._command3 = ''                      # Text command 3
        self._command4 = ''                      # Text command 4
        self._command5 = ''                      # Text command 5
        self._command6 = ''                      # Text command 6

        self.init()

    # ------------------------------------------------------------------------
    def get_id(self):
        return self._id

    # ------------------------------------------------------------------------
    def set_id(self, val):
        self._id = to_int(val)
    
    # ------------------------------------------------------------------------
    def get_preset_desc(self):
        return self._preset_desc

    # ------------------------------------------------------------------------
    def set_preset_desc(self, val):
        self._preset_desc = str(val)

    # ------------------------------------------------------------------------
    def get_vfoa_freq_mhz(self):
        return self._vfoa_freq_mhz

    # ------------------------------------------------------------------------
    def set_vfoa_freq_mhz(self, val):
        self._vfoa_freq_mhz = to_float(val)
    
    # ------------------------------------------------------------------------
    def get_vfob_freq_mhz(self):
        return self._vfob_freq_mhz

    # ------------------------------------------------------------------------
    def set_vfob_freq_mhz(self, val):
        self._vfob_freq_mhz = to_float(val)

    # ------------------------------------------------------------------------
    def get_split(self):
        return self._split

    # ------------------------------------------------------------------------
    def set_split(self, val):
        self._split = bool(val)

    # ------------------------------------------------------------------------
    def get_modea(self):
        return self._modea

    # ------------------------------------------------------------------------
    def set_modea(self, val):
        mode = str(val).upper()
        if OperatingMode.is_valid(mode):
            self._modea = str(mode)
    
    # ------------------------------------------------------------------------
    def get_modeb(self):
        return self._modeb

    # ------------------------------------------------------------------------
    def set_modeb(self, val):
        mode = str(val).upper()
        if OperatingMode.is_valid(mode):
            self._modeb = str(mode)

    # ------------------------------------------------------------------------
    def get_ctcss_config(self):
        return self._ctcss_config

    # ------------------------------------------------------------------------
    def set_ctcss_config(self, val):
        if val in CTCSS_CONFIG:
            self._ctcss_config = val

    # ------------------------------------------------------------------------
    def get_ctcss_tone(self):
        return self._ctcss_tone

    # ------------------------------------------------------------------------
    def set_ctcss_tone(self, val):
        self._ctcss_tone = to_int(val)

    # ------------------------------------------------------------------------
    def get_command1(self):
        return self._command1

    # ------------------------------------------------------------------------
    def set_command1(self, val):
        self._command1 = str(val).strip()
    
    # ------------------------------------------------------------------------
    def get_command2(self):
        return self._command2

    # ------------------------------------------------------------------------
    def set_command2(self, val):
        self._command2 = str(val).strip()
    
    # ------------------------------------------------------------------------
    def get_command3(self):
        return self._command3

    # ------------------------------------------------------------------------
    def set_command3(self, val):
        self._command3 = str(val).strip()
    
    # ------------------------------------------------------------------------
    def get_command4(self):
        return self._command4

    # ------------------------------------------------------------------------
    def set_command4(self, val):
        self._command4 = str(val).strip()
    
    # ------------------------------------------------------------------------
    def get_command5(self):
        return self._command5

    # ------------------------------------------------------------------------
    def set_command5(self, val):
        self._command5 = str(val).strip()
    
    # ------------------------------------------------------------------------
    def get_command6(self):
        return self._command6

    # ------------------------------------------------------------------------
    def set_command6(self, val):
        self._command6 = str(val).strip()
        
    # ------------------------------------------------------------------------
    def init(self):
        globals.config.read(create=False)
        if (self._id > 0):
            section = 'MEMORY_PRESET{:03d}'.format(self._id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
            
            self._preset_desc = str(globals.config.get(section, 'PRESET_DESC'))
            self._vfoa_freq_mhz = to_float(globals.config.get(section, 'VFOA_FREQ_MHZ'))
            self._vfob_freq_mhz = to_float(globals.config.get(section, 'VFOB_FREQ_MHZ'))
            self._split = str(globals.config.get(section, 'SPLIT')) == 'ON'
            self._modea = str(globals.config.get(section, 'MODEA'))
            self._modeb = str(globals.config.get(section, 'MODEB'))
            self._ctcss_config = str(globals.config.get(section, 'CTCSS_CONFIG'))
            self._ctcss_tone = to_int(globals.config.get(section, 'CTCSS_TONE'))
            self._command1 = str(globals.config.get(section, 'COMMAND1'))
            self._command2 = str(globals.config.get(section, 'COMMAND2'))
            self._command3 = str(globals.config.get(section, 'COMMAND3'))
            self._command4 = str(globals.config.get(section, 'COMMAND4'))
            self._command5 = str(globals.config.get(section, 'COMMAND5'))
            self._command6 = str(globals.config.get(section, 'COMMAND6'))
    
    # ------------------------------------------------------------------------
    def write_config(self):
        if (self._id > 0):
            section = 'MEMORY_PRESET{:03d}'.format(self._id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
                
            globals.config.set(section, 'PRESET_DESC', self._preset_desc)
            globals.config.set(section, 'VFOA_FREQ_MHZ', self._vfoa_freq_mhz)
            globals.config.set(section, 'VFOB_FREQ_MHZ', self._vfob_freq_mhz)
            if self._split:
                globals.config.set(section, 'SPLIT', 'ON')
            else:
                globals.config.set(section, 'SPLIT', 'OFF')
            globals.config.set(section, 'MODEA', self._modea)
            globals.config.set(section, 'MODEB', self._modeb)
            globals.config.set(section, 'CTCSS_CONFIG', self._ctcss_config)
            globals.config.set(section, 'CTCSS_TONE', self._ctcss_tone)
            globals.config.set(section, 'COMMAND1', self._command1)
            globals.config.set(section, 'COMMAND2', self._command2)
            globals.config.set(section, 'COMMAND3', self._command3)
            globals.config.set(section, 'COMMAND4', self._command4)
            globals.config.set(section, 'COMMAND5', self._command5)
            globals.config.set(section, 'COMMAND6', self._command6)
            
            globals.config.write()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('MemoryPresetStore test program.')
    globals.init()
    p1 = MemoryPresetStore(1)
    p1.set_preset_desc('Preset One')
    p1.set_vfoa_freq_mhz(146.640)
    p1.set_vfob_freq_mhz(146.040)
    p1.set_split(True)
    p1.set_modea(OperatingMode.FM)
    p1.set_modeb(OperatingMode.USB)
    p1.set_ctcss_config('ENC')
    p1.set_ctcss_tone(1318)
    p1.set_command1('MONITOR ON 20')
    p1.write_config()
   