###############################################################################
# ConfigPresetStore.py
# Author: Tom Kerr AB3GY
#
# ConfigPresetStore class for use with the pyRigPreset application.
# Provides a data container and configuration file read/write methods for
# a saved transceiver configuration consisting of a series of CAT commands.
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


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# ConfigPresetStore class.
##############################################################################
class ConfigPresetStore(object):
    """
    ConfigPresetStore class for use with the pyRigPreset application.
    Provides a data container and configuration file read/write methods for
    a saved transceiver configuration consisting of a series of CAT commands.
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
            print('ConfigPresetStore: Invalid configuration preset ID: {}'.format(id))
            self._id = 0
        
        self._preset_name = ''  # Preset description
        self._cmd = [''] * globals.NUM_CONFIG_COMMANDS  # List of configuration commands

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
    def get_config_cmd(self, idx):
        cmd = ''
        if (idx >= 0) and (idx < globals.NUM_CONFIG_COMMANDS):
            cmd = self._cmd[idx]
        return cmd

    # ------------------------------------------------------------------------
    def set_config_cmd(self, idx, cmd):
        if (idx >= 0) and (idx < globals.NUM_CONFIG_COMMANDS):
            self._cmd[idx] = str(cmd).strip()
 
    # ------------------------------------------------------------------------
    def init(self):
        globals.config.read(create=False)
        if (self._id > 0):
            section = 'CONFIG_PRESET{:03d}'.format(self._id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
            
            self._preset_name = str(globals.config.get(section, 'PRESET_NAME'))
            for idx in range(globals.NUM_CONFIG_COMMANDS):
                self._cmd[idx] = str(globals.config.get(section, 'CMD{:03d}'.format(idx+1)))
    
    # ------------------------------------------------------------------------
    def write_config(self):
        if (self._id > 0):
            section = 'CONFIG_PRESET{:03d}'.format(self._id)
            if not globals.config.has_section(section):
                globals.config.add_section(section)
            globals.config.set(section, 'PRESET_NAME', self._preset_name)
            for idx in range(globals.NUM_CONFIG_COMMANDS):
                globals.config.set(section, 'CMD{:03d}'.format(idx+1), self._cmd[idx])
            globals.config.write()


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    print('ConfigPresetStore test program.')
    globals.init()
    p1 = ConfigPresetStore(1)
    p1.set_preset_name('Preset One')
    p1.set_config_cmd(0, 'MODE USB')
    p1.set_config_cmd(1, 'MONITOR OFF')
    p1.set_config_cmd(2, 'POWER 100')
    p1.set_config_cmd(100, 'INVALID INDEX')
    p1.write_config()
   