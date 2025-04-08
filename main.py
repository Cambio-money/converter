import fix_libraries  # Keep your existing import
from weasyprint import HTML, CSS
import os
from pathlib import Path
import concurrent.futures
import time
import re

def html_to_pdf(html_path, pdf_path=None):
    """
    Convert HTML file to PDF with all hidden content expanded.
    Handles collapsible sections, checkboxes, and hidden divs.
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
    
    # Create comprehensive CSS for expanding all hidden content
    expand_css = CSS(string="""
        /* Show all collapsible content */
        .content { display: block !important; }
        .collapsible:after { content: "\\26C5" !important; }
        
        /* Show any elements with display:none */
        [style*="display: none"],
        [style*="display:none"] { display: block !important; }
        
        /* Check all checkboxes */
        input[type="checkbox"] { 
            -webkit-appearance: checkbox !important;
            -moz-appearance: checkbox !important;
            appearance: checkbox !important;
            opacity: 1 !important;
            display: inline-block !important;
            margin: 2px !important;
            position: static !important;
            visibility: visible !important;
            box-sizing: border-box !important;
        }
        
        /* Show any hidden content by ID */
        #hid { display: block !important; }
    """)
    
    # Convert modified HTML to PDF with optimized settings
    try:
        start_time = time.time()
        
        # Apply comprehensive modifications to HTML
        modified_html = html_content
        
        # 1. Replace display:none with display:block in style attributes
        modified_html = re.sub(r'style=(["\'])([^"\']*?)display:\s*none([^"\']*?)(\1)', 
                              r'style=\1\2display:block\3\1', modified_html)
        
        # 2. Add show-hidden-content CSS to head or create a head if not present
        css_injection = """<style>
        .content { display: block !important; }
        #hid, [style*="display: none"], [style*="display:none"] { display: block !important; }
        input[type="checkbox"] { checked: checked; }
        </style>"""
        
        if "</head>" in modified_html:
            modified_html = modified_html.replace("</head>", f"{css_injection}</head>")
        elif "<html" in modified_html:
            modified_html = modified_html.replace("<html", f"<html><head>{css_injection}</head>")
        else:
            modified_html = f"<html><head>{css_injection}</head>{modified_html}</html>"
        
        # 3. Directly modify any script-hidden content to be visible
        modified_html = modified_html.replace('id="hid" style="display:none"', 'id="hid" style="display:block"')
        
        # 4. Check all checkboxes
        modified_html = re.sub(r'<input type=["\']checkbox["\']', 
                             r'<input type="checkbox" checked="checked"', 
                             modified_html)
        
        # Use the optimized HTML
        html_obj = HTML(string=modified_html)
        
        # Apply the CSS and render with optimized settings
        html_obj.write_pdf(
            pdf_path, 
            stylesheets=[expand_css],
            presentational_hints=True
        )
        
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
    html_to_pdf('test3.html', 'output_complex.pdf')
    
    # For batch conversion with parallel processing:
    # batch_convert_html_to_pdf('directoryTest','outputTest', workers=4)