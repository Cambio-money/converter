import os

# Get the WeasyPrint library path issue file
venv_path = os.path.expanduser("~/docConverter/.venv")
ffi_path = f"{venv_path}/lib/python3.12/site-packages/weasyprint/text/ffi.py"

# Read the file
with open(ffi_path, "r") as file:
    content = file.read()

# Replace Intel paths with ARM paths
modified_content = content.replace(
    "'/usr/local/opt/pango/lib/libpango-1.0.dylib'", 
    "'/opt/homebrew/lib/libpango-1.0.dylib'"
)
modified_content = modified_content.replace(
    "'/usr/local/opt/cairo/lib/libcairo.dylib'", 
    "'/opt/homebrew/lib/libcairo.dylib'"
)
modified_content = modified_content.replace(
    "'/usr/local/opt/fontconfig/lib/libfontconfig.dylib'", 
    "'/opt/homebrew/lib/libfontconfig.dylib'"
)
modified_content = modified_content.replace(
    "'/usr/local/opt/glib/lib/libgobject-2.0.dylib'", 
    "'/opt/homebrew/lib/libgobject-2.0.dylib'"
)
modified_content = modified_content.replace(
    "'/usr/local/opt/", 
    "'/opt/homebrew/"
)

# Write the modified content back
with open(ffi_path, "w") as file:
    file.write(modified_content)

print("WeasyPrint library paths updated successfully!")