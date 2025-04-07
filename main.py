import fix_libraries  # Keep your existing import
from weasyprint import HTML, CSS
import os
from pathlib import Path
import concurrent.futures
import time

def html_to_pdf(html_path, pdf_path=None):
    """
    Convert HTML file to PDF with all collapsible sections expanded.
    Optimized for better performance.
    """
    # If pdf_path is not specified, use the same name with .pdf extension
    if pdf_path is None:
        pdf_path = os.path.splitext(html_path)[0] + '.pdf'
    
    # Read the HTML file - optimize by only reading once
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except UnicodeDecodeError:
        # Try another encoding if UTF-8 fails
        with open(html_path, 'r', encoding='latin-1') as f:
            html_content = f.read()
    
    # Create CSS for expanding content (more efficient than inline styling)
    expand_css = CSS(string="""
        .content { display: block !important; }
        .collapsible:after { content: "\\26C5" !important; }
    """)
    
    # Convert modified HTML to PDF with optimized settings
    try:
        start_time = time.time()
        
        # Only modify HTML content if necessary
        if ".content" in html_content and "display: none" in html_content:
            # Insert right before </head> if it exists, otherwise use as is
            if "</head>" in html_content:
                modified_html = html_content.replace("</head>", """<style>.content{display:block !important;}</style></head>""")
            else:
                modified_html = """<style>.content{display:block !important;}</style>""" + html_content
            
            # Use the optimized HTML
            html_obj = HTML(string=modified_html)
        else:
            # Skip HTML modification if not needed
            html_obj = HTML(filename=html_path)
        
        # Apply the CSS and render with optimized settings
        html_obj.write_pdf(pdf_path, stylesheets=[expand_css])
        
        end_time = time.time()
        print(f"Converted {html_path} to {pdf_path} in {end_time - start_time:.2f} seconds")
        
        return pdf_path
    except Exception as e:
        print(f"Error converting {html_path}: {str(e)}")
        return None

def batch_convert_html_to_pdf(input_dir='.', output_dir=None, workers=None):
    """
    Convert all HTML files in a directory to PDFs using parallel processing.
    
    Args:
        input_dir: Directory containing HTML files
        output_dir: Directory for output PDFs
        workers: Number of parallel workers (default: CPU count)
    """
    if output_dir is None:
        output_dir = input_dir
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all HTML files in the input directory
    input_path = Path(input_dir)
    html_files = list(input_path.glob('*.html')) + list(input_path.glob('*.htm'))
    
    if not html_files:
        print(f"No HTML files found in {input_dir}")
        return
    
    total_files = len(html_files)
    print(f"Found {total_files} HTML files to convert")
    
    # Use parallel processing for faster conversion
    start_time = time.time()
    
    # Determine number of workers (use max 4 by default to avoid memory issues)
    if workers is None:
        workers = min(os.cpu_count(), 4)
    
    # Create list of conversion tasks
    conversion_tasks = []
    for html_file in html_files:
        pdf_path = os.path.join(output_dir, html_file.stem + '.pdf')
        conversion_tasks.append((str(html_file), pdf_path))
    
    # Process files in parallel
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(html_to_pdf, html_path, pdf_path): html_path 
                  for html_path, pdf_path in conversion_tasks}
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            print(f"Progress: {completed}/{total_files} files ({(completed/total_files)*100:.1f}%)")
    
    end_time = time.time()
    print(f"All conversions complete. PDFs saved to {output_dir}")
    print(f"Total time: {end_time - start_time:.2f} seconds")

# Example usage
if __name__ == "__main__":
    # For single file conversion:
    #html_to_pdf('test3.html', 'output_complex.pdf')
    
    # For batch conversion with parallel processing:
    batch_convert_html_to_pdf('directoryTest','outputTest',workers=4)