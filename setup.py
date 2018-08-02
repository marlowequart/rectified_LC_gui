import cx_Freeze
import sys
import matplotlib
import tkinter
import os.path
import re
import glob


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
#Directory: C:\Anaconda\envs\controls


base = None
if sys.platform == 'win32':
	base = "Win32GUI"
if sys.platform == 'win64':
	base = "Win64GUI"


executables = [
	cx_Freeze.Executable("3phaseLC_gui.py", base = base),
	]
	
# Save matplotlib-data to mpl-data ( It is located in the matplotlib\mpl-data
# folder and the compiled programs will look for it in \mpl-data
# note: using matplotlib.get_mpldata_info

includes = ["matplotlib.backends", "matplotlib.backends.backend_qt4agg",
			"matplotlib.figure", "numpy", "matplotlib.backends.backend_tkagg",
			"re", "os","tkinter",
]

include_files = [
				os.path.join(PYTHON_INSTALL_DIR,'DLLs','tk86t.dll'),
				os.path.join(PYTHON_INSTALL_DIR,'DLLs','tcl86t.dll'),
#				os.path.join(PYTHON_INSTALL_DIR,'Library','bin','libpng16.dll'),
				]
exclude_files=[

]
# data_files = [
				# (r'mpl-data', glob.glob(r'C:\Anaconda\envs\controls\Lib\site-packages\matplotlib\mpl-data\*.*')),
				# #Because matplotlibrc does not have an extension, glob does not find it (at least I think that's why)
				# #So add it manually here:
				# (r'mpl-data', [r'C:\Anaconda\envs\controls\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
				# (r'mpl-data\images',glob.glob(r'C:\Anaconda\envs\controls\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
				# (r'mpl-data\fonts',glob.glob(r'C:\Anaconda\envs\controls\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))
				# ]
				
build_exe_options = {
						"includes":includes,
						"include_files":include_files,
						"excludes":exclude_files
					}

cx_Freeze.setup(
		name = "3phaseLC",
		options = {"build_exe": build_exe_options},
		executables = executables,
		
)

## Command to run this script: python setup.py build