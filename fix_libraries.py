import os
import sys
import ctypes
from ctypes.util import find_library
from functools import partial

# Original find_library function
orig_find_library = find_library

# Define the library paths
library_paths = [
    "/usr/local/opt/pango/lib",
    "/usr/local/opt/cairo/lib",
    "/usr/local/opt/harfbuzz/lib",
    "/usr/local/opt/fontconfig/lib",
    "/usr/local/opt/freetype/lib",
]

# Add these paths to DYLD_LIBRARY_PATH
os.environ['DYLD_LIBRARY_PATH'] = ':'.join(library_paths + [os.environ.get('DYLD_LIBRARY_PATH', '')])

# Map library names to actual files
library_mapping = {
    'libpango-1.0-0': '/usr/local/opt/pango/lib/libpango-1.0.dylib',
    'pango-1.0': '/usr/local/opt/pango/lib/libpango-1.0.dylib',
    'pangocairo-1.0': '/usr/local/opt/pango/lib/libpangocairo-1.0.dylib',
    'pangoft2-1.0': '/usr/local/opt/pango/lib/libpangoft2-1.0.dylib',
    # Add more mappings as needed
}

# Overriding find_library function
def custom_find_library(name):
    if name in library_mapping:
        return library_mapping[name]
    
    # Try to find in our known library paths
    for path in library_paths:
        if os.path.exists(f"{path}/lib{name}.dylib"):
            return f"{path}/lib{name}.dylib"
        if os.path.exists(f"{path}/lib{name}.0.dylib"):
            return f"{path}/lib{name}.0.dylib"
    
    # Fall back to original function
    return orig_find_library(name)

# Replace the standard find_library function
ctypes.util.find_library = custom_find_library