###############################################################################
# globals.py
# Author: Tom Kerr AB3GY
#
# Global objects and data for the pyRigPreset application.
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

# Local packages.
from src.ConfigFile import ConfigFile
from PyRigCat.PyRigCat import PyRigCat, RigName


##############################################################################
# Globals.
##############################################################################
APP_NAME = 'pyRigPreset'
APP_VERSION = '0.1'
APP_COPYRIGHT = '2023'
NUM_CONFIG_PRESETS = 6    # Number of configuration presets
NUM_CONFIG_COMMANDS = 10  # Number of transceiver configuration commands per preset
NUM_MEMORY_PRESETS = 32   # Number of emulated memory presets
NUM_CAT_PRESETS = 4       # Number of CAT interface presets

root = None           # The root window
config = None         # The config file object
rig_cat = PyRigCat()  # The rig CAT control object

# The list of supported transceivers.
RIG_LIST = RigName.RIG_LIST[1:]  # Assumes index 0 == NONE

##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def init():
    """
    Initialize global settings.
    """
    global root
    global config

    # Read the configuration file.
    config = ConfigFile()
    config.read()

# ------------------------------------------------------------------------
def close():
    """
    Perform graceful application shutdown.
    """
    global root
    global config
    
    # Write the configuration file.
    config.write()
