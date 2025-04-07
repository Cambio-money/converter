

# HTML to PDF Converter

A powerful and user-friendly tool for converting HTML files to PDF with expanded collapsible sections. This application provides three different interfaces to suit your needs: a command-line interface, an interactive CLI, and a graphical user interface.

## Features

- Convert single HTML files or entire directories to PDF
- Automatically expands all collapsible sections in HTML files
- Preserves formatting and styling from the original HTML
- Parallel processing for faster batch conversions
- Multiple interfaces to choose from (GUI, CLI, or direct script usage)
- Cross-platform compatibility (Windows, macOS, Linux)

## Requirements

- Python 3.6 or higher
- Dependencies listed in requirements.txt

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Graphical User Interface (GUI)

The most user-friendly way to use the converter. Simply run:

```bash
python gui.py
```

The GUI provides:
- A tab for single file conversion
- A tab for batch directory conversion
- File/folder selection dialogs
- Progress tracking
- Status updates

### Command Line Interface (CLI)

For terminal users or automation scripts:

```bash
# Interactive mode
python cli.py

# Convert a single file
python cli.py --file input.html --output output.pdf

# Convert all HTML files in a directory
python cli.py --input-dir ./html_files --output-dir ./pdf_files --workers 4
```

#### CLI Options:
- `--file`, `-f`: Path to a single HTML file to convert
- `--output`, `-o`: Output PDF file path (for single file conversion)
- `--input-dir`, `-i`: Input directory containing HTML files
- `--output-dir`, `-d`: Output directory for PDF files
- `--workers`, `-w`: Number of parallel workers for batch conversion

### Direct Script Usage

You can also import the functions directly in your Python code:

```python
from main import html_to_pdf, batch_convert_html_to_pdf

# Convert a single file
html_to_pdf('input.html', 'output.pdf')

# Convert all HTML files in a directory
batch_convert_html_to_pdf('input_directory', 'output_directory', workers=4)
```

## How It Works

The converter:
1. Reads the HTML file(s)
2. Injects CSS to ensure all collapsible sections are expanded
3. Renders the HTML to PDF using WeasyPrint
4. Saves the output to the specified location

For batch processing, the application uses parallel processing to convert multiple files simultaneously, significantly improving performance.

## Troubleshooting

### Common Issues:

- **File encoding errors**: The converter attempts to handle different file encodings automatically (UTF-8 and Latin-1)
- **Memory issues during batch conversion**: Reduce the number of workers if you encounter memory problems
- **macOS file dialog issues**: The application has special handling for macOS file dialogs

### WeasyPrint Installation Issues:

If you encounter problems with WeasyPrint, you may need to install it properly according to your operating system. WeasyPrint has specific dependencies that vary by platform:

- **Linux**: Requires Pango ≥ 1.44.0 and other system libraries
- **macOS**: Best installed via Homebrew
- **Windows**: Requires special setup with MSYS2 for Pango libraries

For detailed installation instructions specific to your operating system, please refer to the [WeasyPrint documentation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html).

#### Platform-Specific Notes:

- **Windows users**: You may need to set the `WEASYPRINT_DLL_DIRECTORIES` environment variable to point to your MSYS2 libraries
- **macOS users**: If libraries can't be found, you may need to set the `DYLD_FALLBACK_LIBRARY_PATH` environment variable
- **Linux users**: Use your distribution's package manager to install Pango and other dependencies

### Debugging:

If you encounter issues, check the console output for error messages. The application provides detailed error information to help diagnose problems.

## Project Structure

- `main.py`: Core conversion functionality
- `cli.py`: Command-line interface
- `gui.py`: Graphical user interface
- `fix_libraries.py`: Helper module for library compatibility
- `requirements.txt`: List of required Python packages

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
