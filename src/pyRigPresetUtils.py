###############################################################################
# pyRigPresetUtils.py
# Author: Tom Kerr AB3GY
#
# Utility functions for the pyRigPreset application.
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
import tkinter.messagebox as messagebox

# Local packages.
import globals


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

# ------------------------------------------------------------------------
def app_close():
    """
    Close the pySatCat application.
    
    Parameters
    ----------
    root : Tk object
        The pySatCat application root window.
        
    Returns
    -------
    None.  The root window, and hence the application, is closed.
    """
    global APP_NAME
    global root
    if messagebox.askokcancel(title='Exit ' + globals.APP_NAME, 
        message='Do you want to exit ' + globals.APP_NAME + '?'):
        globals.close()
        globals.root.destroy()
        print('Exiting  ' + globals.APP_NAME)

# ------------------------------------------------------------------------
def set_geometry(window, new_width=0, new_height=0, x_offset=0, y_offset=0):
    """
    Set the geometry of the specified window.
    
    Parameters
    ----------
    window : Tk object
        The window to set.

    new_width : int
        The new window width.  If set to zero (default), the width will be
        automatically set based on its required width.

    new_height : int
        The new window height.  If set to zero (default), the height will be
        automatically set based on its required height.

    x_offset : int
        The new window x offset. If set to zero (default), then the x offset
        will be set to the center of the screen.

    y_offset : int
        The new window y offset. If set to zero (default), then the y offset
        will be set to the center of the screen.
        
    Returns
    -------
    None.
    """
    window.update() # Update window to get required width and height
    
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    
    if (new_width <= 0):
        new_width = window.winfo_reqwidth() + 6
    if (new_height <= 0):
        new_height = window.winfo_reqheight() + 6
    if (x_offset <= 0):
        x_offset = int(sw/2 - new_width/2) # Center X
    if (y_offset <= 0):
        y_offset = int(sh/2 - new_height/2) # Center Y
    window.geometry(f'{new_width}x{new_height}+{x_offset}+{y_offset}')

# ------------------------------------------------------------------------
def to_int(val):
    n = 0
    try:
        n = int(val)
    except ValueError:
        n = 0
    return n
    
# ------------------------------------------------------------------------
def to_float(val):
    n = 0.0
    try:
        n = float(val)
    except ValueError:
        n = 0.0
    return n


