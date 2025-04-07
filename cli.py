#!/usr/bin/env python3
import argparse
import os
import sys
from main import html_to_pdf, batch_convert_html_to_pdf

def get_user_input(prompt, validator=None, error_message=None):
    """Get and validate user input."""
    while True:
        user_input = input(prompt)
        if validator is None or validator(user_input):
            return user_input
        print(error_message or "Invalid input. Please try again.")

def file_exists(path):
    """Check if a file exists."""
    return os.path.isfile(path)

def directory_exists(path):
    """Check if a directory exists."""
    return os.path.isdir(path)

def create_directory_if_not_exists(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    return True

def interactive_mode():
    """Run the CLI in interactive mode."""
    print("HTML to PDF Converter")
    print("=====================")
    
    # Ask for conversion type
    conversion_type = get_user_input(
        "Would you like to convert a single file (1) or a directory of files (2)? ",
        lambda x: x in ['1', '2'],
        "Please enter 1 for single file or 2 for directory."
    )
    
    if conversion_type == '1':
        # Single file conversion
        html_path = get_user_input(
            "Enter the path to the HTML file: ",
            file_exists,
            "File not found. Please enter a valid file path."
        )
        
        # Default PDF name
        default_pdf_path = os.path.splitext(html_path)[0] + '.pdf'
        pdf_path = input(f"Enter the output PDF path (press Enter for default: {default_pdf_path}): ")
        
        if not pdf_path:
            pdf_path = default_pdf_path
        
        # Create directory for the PDF if needed
        pdf_dir = os.path.dirname(pdf_path)
        if pdf_dir and not os.path.exists(pdf_dir):
            create_directory_if_not_exists(pdf_dir)
        
        # Convert the file
        result = html_to_pdf(html_path, pdf_path)
        if result:
            print(f"Conversion successful! PDF saved to: {result}")
        else:
            print("Conversion failed.")
    
    else:
        # Directory conversion
        input_dir = get_user_input(
            "Enter the input directory containing HTML files: ",
            directory_exists,
            "Directory not found. Please enter a valid directory path."
        )
        
        # Default output directory
        default_output_dir = input_dir
        output_dir = input(f"Enter the output directory for PDFs (press Enter for default: {default_output_dir}): ")
        
        if not output_dir:
            output_dir = default_output_dir
        
        # Create output directory if needed
        if not os.path.exists(output_dir):
            if not create_directory_if_not_exists(output_dir):
                print("Failed to create output directory. Exiting.")
                return
        
        # Ask for number of workers
        workers_input = input("Enter the number of parallel workers (press Enter for default): ")
        workers = None
        if workers_input:
            try:
                workers = int(workers_input)
                if workers <= 0:
                    print("Number of workers must be positive. Using default.")
                    workers = None
            except ValueError:
                print("Invalid number. Using default.")
        
        # Convert the files
        batch_convert_html_to_pdf(input_dir, output_dir, workers)

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='Convert HTML files to PDF with expanded content.')
    parser.add_argument('--file', '-f', help='Path to a single HTML file to convert')
    parser.add_argument('--output', '-o', help='Output PDF file path (for single file conversion)')
    parser.add_argument('--input-dir', '-i', help='Input directory containing HTML files')
    parser.add_argument('--output-dir', '-d', help='Output directory for PDF files')
    parser.add_argument('--workers', '-w', type=int, help='Number of parallel workers for batch conversion')
    
    args = parser.parse_args()
    
    # If no arguments provided, run in interactive mode
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    # Handle command-line arguments
    if args.file:
        # Single file conversion
        if not os.path.isfile(args.file):
            print(f"Error: File not found: {args.file}")
            return
        
        result = html_to_pdf(args.file, args.output)
        if result:
            print(f"Conversion successful! PDF saved to: {result}")
        else:
            print("Conversion failed.")
    
    elif args.input_dir:
        # Batch conversion
        if not os.path.isdir(args.input_dir):
            print(f"Error: Directory not found: {args.input_dir}")
            return
        
        batch_convert_html_to_pdf(args.input_dir, args.output_dir, args.workers)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 