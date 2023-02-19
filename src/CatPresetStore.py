###############################################################################
# CatPresetStore.py
# Author: Tom Kerr AB3GY
#
# CatPresetStore class for use with the pyRigPreset application.
# Provides a data container and configuration file read/write methods for
# a saved transceiver CAT interface configuration.
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
from src.ConfigFile import ConfigFile


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# CatPresetStore class.
##############################################################################
class CatPresetStore(object):
    """
    CatPresetStore class for use with the pyRigPreset application.
    Provides a data container and configuration file read/write methods for
    a saved transceiver CAT interface configuration.
    """
    # ------------------------------------------------------------------------
    def __init__(self, id):
        """
        Class constructor.
        
        Parameters
        ----------
        id : int
            The configuration preset ID

        Returns
        -------
        None.
        """
        self._id = 0  # Configuration preset ID
        try:
            self._id = int(id)
        except Exception:
            print('CatPresetStore: Invalid configuration preset ID: {}'.format(id))
            self._id = 0
        
        self._preset_name = ''  # Preset name on button
        self._rig = ''          # Transceiver name
        self._port = ''         # COM port name
        self._baud = ''         # Baud rate
        self._data = ''         # Data bits size
        self._parity = ''       # COM port parity
        self._stop = ''         # Stop bits size

        self.init()

    # ------------------------------------------------------------------------
    def get_id(self):
        return self._id

    # ------------------------------------------------------------------------
    def set_id(self, val):
        self._id = to_int(val)
    
    # ------------------------------------------------------------------------
    def get_preset_name(self):
        return self._preset_name

    # ------------------------------------------------------------------------
    def set_preset_name(self, val):
        self._preset_name = str(val)

    # ------------------------------------------------------------------------
    def get_rig(self):
       return self._rig
       
    # ------------------------------------------------------------------------
    def set_rig(self, val):
        self._rig = str(val)
    
    # ------------------------------------------------------------------------
    def get_port(self):
       return self._port
       
    # ------------------------------------------------------------------------
    def set_port(self, val):
        self._port = str(val)
    
    # ------------------------------------------------------------------------
    def get_baud(self):
       return self._baud
       
    # ------------------------------------------------------------------------
    def set_baud(self, val):
        self._baud = str(val)
    
    # ------------------------------------------------------------------------
    def get_data(self):
       return self._data
       
    # ------------------------------------------------------------------------
    def set_data(self, val):
        self._data = str(val)

    # ------------------------------------------------------------------------
    def get_parity(self):
       return self._parity
       
    # ------------------------------------------------------------------------
    def set_parity(self, val):
        self._parity = str(val)
    
    # ------------------------------------------------------------------------
    def get_stop(self):
       return self._stop
       
    # ------------------------------------------------------------------------
    def set_stop(self, val):
        self._stop = str(val)
 
    # ------------------------------------------------------------------------
    def init(self):
        globals.config.read(create=False)
        if (self._id > 0):
            section = 'CAT_PRESET{:03d}'.format(self._id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
            
            self._preset_name = str(globals.config.get(section, 'PRESET_NAME'))
            self._rig = str(globals.config.get(section, 'RIG'))
            self._port = str(globals.config.get(section, 'PORT'))
            self._baud = str(globals.config.get(section, 'BAUD'))
            self._data = str(globals.config.get(section, 'DATA'))
            self._parity = str(globals.config.get(section, 'PARITY'))
            self._stop = str(globals.config.get(section, 'STOP'))
            
    
    # ------------------------------------------------------------------------
    def write_config(self):
        if (self._id > 0):
            section = 'CAT_PRESET{:03d}'.format(self._id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
                
            globals.config.set(section, 'PRESET_NAME', self._preset_name)
            globals.config.set(section, 'RIG', self._rig)
            globals.config.set(section, 'PORT', self._port)
            globals.config.set(section, 'BAUD', self._baud)
            globals.config.set(section, 'DATA', self._data)
            globals.config.set(section, 'PARITY', self._parity)
            globals.config.set(section, 'STOP', self._stop)
            
            globals.config.write()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('CatPresetStore test program.')
    globals.init()
    p1 = CatPresetStore(1)
    p1.set_preset_name('Preset One')
    p1.set_config_cmd(0, 'MODE USB')
    p1.set_config_cmd(1, 'MONITOR OFF')
    p1.set_config_cmd(2, 'POWER 100')
    p1.set_config_cmd(100, 'INVALID INDEX')
    p1.write_config()
   