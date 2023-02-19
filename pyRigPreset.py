###############################################################################
# pyRigPreset.py
# Author: Tom Kerr AB3GY
#
# Amateur radio application to provide transceiver configuration presets.
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

# Local environment init.
import _env_init

# Local packages.
import globals
from src.pyRigPresetUtils import app_close, set_geometry
from src.AppMenu import AppMenu
from src.ConfigFile import ConfigFile
from src.WidgetCatPreset import WidgetCatPreset
from src.WidgetCommandEntry import WidgetCommandEntry
from src.WidgetConfigPreset import WidgetConfigPreset
from src.WidgetMemoryPreset import WidgetMemoryPreset
from src.WidgetFrequencyEntry import WidgetFrequencyEntry
from src.WidgetTxRx import WidgetTxRx

from PyRigCat import *
from PyRigCat.PyRigCat_ft817 import PyRigCat_ft817
from PyRigCat.PyRigCat_ft991 import PyRigCat_ft991
from PyRigCat.PyRigCat_ic7000 import PyRigCat_ic7000


##############################################################################
# Globals.
############################################################################## 
window_width = 0

##############################################################################
# Functions.
############################################################################## 

def create_memory_preset_frame():
    """
    Create a scrollable frame of memory preset widgets.
    This is a rather complicated procedure in Tkinter and requires several 
    frames and a canvas.
    """
    # See the following references: 
    # https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
    # https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
    
    global window_width
    
    # Create an outer frame for memory preset widgets.
    mem_frame_outer = tk.Frame(globals.root,
        highlightbackground='black',
        highlightthickness=1,
        padx=3,
        pady=3,)
    
    # Create a vertical scrollbar to scroll the canvas of memory preset widgets.
    mem_vsb = tk.Scrollbar(mem_frame_outer, orient=tk.VERTICAL)
    mem_vsb.grid(row=0, rowspan=globals.NUM_MEMORY_PRESETS, column=1, sticky='NS')
    
    # Create a canvas to hold the inner frame.  
    # The canvas is the object that is scrolled.
    mem_canvas = tk.Canvas(mem_frame_outer,
        width=window_width,
        height=400,
        yscrollcommand=mem_vsb.set)
    mem_canvas.grid(row=0, column=0)
    mem_vsb.config(command=mem_canvas.yview)
    
    # Reset the view.
    mem_canvas.xview_moveto(0)
    mem_canvas.yview_moveto(0)

    # Create an inner frame for memory preset widgets.
    # This holds the widgets inside the scrollable canvas.
    mem_frame_inner = tk.Frame(mem_canvas)
    
    # Create a set of memory preset widgets.
    for idx in range(globals.NUM_MEMORY_PRESETS):
        wcp = WidgetMemoryPreset(mem_frame_inner, idx+1)
        wcp.frame.grid(row=idx, column=0, padx=6, pady=1)
        
    # Attach the inner frame to the canvas.
    interior_id = mem_canvas.create_window(0, 0, window=mem_frame_inner, anchor=tk.NW)

    def _configure_interior(event):
        # Update the scrollbars to match the size of the inner frame.
        size = (mem_frame_inner.winfo_reqwidth(), mem_frame_inner.winfo_reqheight())
        mem_canvas.config(scrollregion="0 0 %s %s" % size)
        if mem_frame_inner.winfo_reqwidth() != mem_canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            mem_canvas.config(width=mem_frame_inner.winfo_reqwidth())
    mem_frame_inner.bind('<Configure>', _configure_interior)
    
    def _configure_canvas(event):
        if mem_frame_inner.winfo_reqwidth() != mem_canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            mem_canvas.itemconfigure(interior_id, width=mem_canvas.winfo_width())
    mem_canvas.bind('<Configure>', _configure_canvas)
    
    return mem_frame_outer


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":

    app_width  = 400
    app_height = 400

    # Print a startup message in the command prompt window.
    print('Starting ' + globals.APP_NAME)
    
    # Initialize the application configuration.
    globals.init()
    
    # Create and initialize the root window.
    globals.root = tk.Tk()
    globals.root.minsize(app_width, app_height)
    globals.root.title(globals.APP_NAME + ' - Python Rig Configuration Presets')
    globals.root.protocol("WM_DELETE_WINDOW", lambda: app_close())
    
    # Create the main menu.
    globals.app_menu = AppMenu(globals.root)
    
    # Frame for configuration preset widgets.
    cfg_frame = tk.Frame(globals.root,
            highlightbackground='black',
            highlightthickness=1,
            padx=3,
            pady=3,)
    row = 0
        
    # Configuration preset widgets.
    for idx in range(globals.NUM_CONFIG_PRESETS):
        cfg_btn = WidgetConfigPreset(cfg_frame, idx+1)
        cfg_btn.frame.grid(row=0, column=idx, padx=6, pady=6)
    cfg_frame.grid(row=row, column=0, columnspan=3, padx=9, pady=6)
    row += 1
    
    # Match the memory preset widget canvas width to the configuration preset width.
    cfg_frame.update()
    window_width = cfg_frame.winfo_width()
    
    # Create a scrollable frame of memory preset widgets.
    # This is a rather complicated procedure in Tkinter and requires several 
    # frames and a canvas.
    mem_frame = create_memory_preset_frame()
    mem_frame.grid(row=row, column=0, columnspan=3, padx=9, pady=6)
    row += 1
    
    # Frequency entry widget.
    wfe = WidgetFrequencyEntry(globals.root)
    wfe.frame.grid(row=row, column=0, sticky='W', padx=9, pady=(6, 6))
    
    # Command entry widget.
    wce = WidgetCommandEntry(globals.root)
    wce.frame.grid(row=row, column=1, sticky='EW', padx=9, pady=(6, 6))
    
    # TX/RX buttons.
    ptt = WidgetTxRx(globals.root)
    ptt.frame.grid(row=row, column=2, sticky='E', padx=9, pady=(6, 6))
    row += 1
    
    # CAT interface selector.
    wcp = WidgetCatPreset(globals.root)
    wcp.frame.grid(row=row, column=0, columnspan=3, sticky='W', padx=9, pady=(3, 12))
    row += 1

    # Set the proper window size and center it on the screen.
    set_geometry(globals.root)

    # Loop forever.
    globals.root.mainloop()
