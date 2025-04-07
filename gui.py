#!/usr/bin/env python3
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import platform
from main import html_to_pdf, batch_convert_html_to_pdf

class HTMLtoPDFConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("HTML to PDF Converter")
        self.geometry("600x500")
        self.minsize(500, 400)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.single_file_tab = ttk.Frame(self.notebook)
        self.batch_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.single_file_tab, text="Single File")
        self.notebook.add(self.batch_tab, text="Batch Conversion")
        
        # Setup UI for each tab
        self.setup_single_file_tab()
        self.setup_batch_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        # Center window
        self.center_window()
    
    def center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_single_file_tab(self):
        """Setup UI elements for single file conversion tab."""
        frame = ttk.Frame(self.single_file_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # HTML file selection
        ttk.Label(frame, text="HTML File:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.html_file_var = tk.StringVar()
        html_entry = ttk.Entry(frame, textvariable=self.html_file_var, width=50)
        html_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_html_file).grid(column=2, row=0, padx=5, pady=5)
        
        # PDF file selection
        ttk.Label(frame, text="Output PDF:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.pdf_file_var = tk.StringVar()
        pdf_entry = ttk.Entry(frame, textvariable=self.pdf_file_var, width=50)
        pdf_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_pdf_file).grid(column=2, row=1, padx=5, pady=5)
        
        # Convert button
        convert_btn = ttk.Button(frame, text="Convert", command=self.convert_single_file)
        convert_btn.grid(column=1, row=2, pady=20)
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
    
    def setup_batch_tab(self):
        """Setup UI elements for batch conversion tab."""
        frame = ttk.Frame(self.batch_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Input directory selection
        ttk.Label(frame, text="Input Directory:").grid(column=0, row=0, sticky=tk.W, pady=5)
        self.input_dir_var = tk.StringVar()
        input_dir_entry = ttk.Entry(frame, textvariable=self.input_dir_var, width=50)
        input_dir_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_input_dir).grid(column=2, row=0, padx=5, pady=5)
        
        # Output directory selection
        ttk.Label(frame, text="Output Directory:").grid(column=0, row=1, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar()
        output_dir_entry = ttk.Entry(frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(frame, text="Browse...", command=self.browse_output_dir).grid(column=2, row=1, padx=5, pady=5)
        
        # Workers selection
        ttk.Label(frame, text="Workers:").grid(column=0, row=2, sticky=tk.W, pady=5)
        self.workers_var = tk.StringVar(value="4")
        workers_spinbox = ttk.Spinbox(frame, from_=1, to=16, textvariable=self.workers_var, width=5)
        workers_spinbox.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
        
        # Convert button
        convert_btn = ttk.Button(frame, text="Convert All", command=self.convert_batch)
        convert_btn.grid(column=1, row=3, pady=20)
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
    
    def browse_html_file(self):
        """Open file dialog to select HTML file."""
        # Fix for macOS: Don't specify filetypes if on Mac
        if platform.system() == 'Darwin':
            filename = filedialog.askopenfilename(title="Select HTML File")
        else:
            filetypes = [("HTML files", "*.html *.htm"), ("All files", "*.*")]
            filename = filedialog.askopenfilename(filetypes=filetypes, title="Select HTML File")
            
        if filename:
            self.html_file_var.set(filename)
            # Set default PDF output path
            default_pdf = os.path.splitext(filename)[0] + '.pdf'
            self.pdf_file_var.set(default_pdf)
    
    def browse_pdf_file(self):
        """Open file dialog to select PDF output file."""
        # Fix for macOS: Don't specify filetypes if on Mac
        if platform.system() == 'Darwin':
            filename = filedialog.asksaveasfilename(defaultextension=".pdf", title="Save PDF As")
        else:
            filetypes = [("PDF files", "*.pdf"), ("All files", "*.*")]
            filename = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=".pdf", title="Save PDF As")
            
        if filename:
            self.pdf_file_var.set(filename)
    
    def browse_input_dir(self):
        """Open directory dialog to select input directory."""
        directory = filedialog.askdirectory(title="Select Input Directory")
        if directory:
            self.input_dir_var.set(directory)
            # Set default output directory
            self.output_dir_var.set(directory)
    
    def browse_output_dir(self):
        """Open directory dialog to select output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def convert_single_file(self):
        """Convert a single HTML file to PDF."""
        html_file = self.html_file_var.get()
        pdf_file = self.pdf_file_var.get()
        
        if not html_file:
            messagebox.showerror("Error", "Please select an HTML file.")
            return
        
        if not os.path.isfile(html_file):
            messagebox.showerror("Error", f"HTML file not found: {html_file}")
            return
        
        # Create output directory if needed
        pdf_dir = os.path.dirname(pdf_file)
        if pdf_dir and not os.path.exists(pdf_dir):
            try:
                os.makedirs(pdf_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create output directory: {e}")
                return
        
        # Update UI
        self.status_var.set(f"Converting {html_file}...")
        self.progress_var.set(0)
        
        # Run conversion in a separate thread to keep UI responsive
        def conversion_thread():
            try:
                result = html_to_pdf(html_file, pdf_file)
                
                # Update UI from the main thread
                self.after(0, lambda: self.progress_var.set(100))
                
                if result:
                    self.after(0, lambda: self.status_var.set(f"Conversion successful! PDF saved to: {result}"))
                    self.after(0, lambda: messagebox.showinfo("Success", f"PDF saved to: {result}"))
                else:
                    self.after(0, lambda: self.status_var.set("Conversion failed."))
                    self.after(0, lambda: messagebox.showerror("Error", "Conversion failed."))
            except Exception as e:
                self.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
                self.after(0, lambda: messagebox.showerror("Error", f"Conversion failed: {str(e)}"))
        
        threading.Thread(target=conversion_thread, daemon=True).start()
    
    def convert_batch(self):
        """Convert all HTML files in a directory to PDFs."""
        input_dir = self.input_dir_var.get()
        output_dir = self.output_dir_var.get()
        
        if not input_dir:
            messagebox.showerror("Error", "Please select an input directory.")
            return
        
        if not os.path.isdir(input_dir):
            messagebox.showerror("Error", f"Input directory not found: {input_dir}")
            return
        
        if not output_dir:
            output_dir = input_dir
        
        # Create output directory if needed
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create output directory: {e}")
                return
        
        # Get workers count
        try:
            workers = int(self.workers_var.get())
            if workers <= 0:
                workers = None
        except ValueError:
            workers = None
        
        # Update UI
        self.status_var.set(f"Scanning for HTML files in {input_dir}...")
        self.progress_var.set(0)
        
        # Run conversion in a separate thread to keep UI responsive
        def batch_conversion_thread():
            try:
                # Find all HTML files
                html_files = []
                for root, _, files in os.walk(input_dir):
                    for file in files:
                        if file.lower().endswith(('.html', '.htm')):
                            html_files.append(os.path.join(root, file))
                
                if not html_files:
                    self.after(0, lambda: self.status_var.set(f"No HTML files found in {input_dir}"))
                    self.after(0, lambda: messagebox.showinfo("Info", f"No HTML files found in {input_dir}"))
                    return
                
                total_files = len(html_files)
                self.after(0, lambda: self.status_var.set(f"Converting {total_files} HTML files..."))
                
                # Custom callback to update progress
                completed = 0
                
                def progress_callback():
                    nonlocal completed
                    completed += 1
                    progress = (completed / total_files) * 100
                    self.after(0, lambda: self.progress_var.set(progress))
                    self.after(0, lambda: self.status_var.set(f"Converting files: {completed}/{total_files}"))
                
                # Process each file
                for i, html_file in enumerate(html_files):
                    # Determine relative path to maintain directory structure
                    rel_path = os.path.relpath(html_file, input_dir)
                    pdf_file = os.path.join(output_dir, os.path.splitext(rel_path)[0] + '.pdf')
                    
                    # Create subdirectory if needed
                    pdf_dir = os.path.dirname(pdf_file)
                    if pdf_dir and not os.path.exists(pdf_dir):
                        os.makedirs(pdf_dir, exist_ok=True)
                    
                    # Convert file
                    html_to_pdf(html_file, pdf_file)
                    progress_callback()
                
                self.after(0, lambda: self.status_var.set(f"Conversion complete. {total_files} files converted."))
                self.after(0, lambda: messagebox.showinfo("Success", f"All {total_files} files converted successfully!"))
                
            except Exception as e:
                self.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
                self.after(0, lambda: messagebox.showerror("Error", f"Batch conversion failed: {str(e)}"))
        
        threading.Thread(target=batch_conversion_thread, daemon=True).start()

if __name__ == "__main__":
    app = HTMLtoPDFConverter()
    app.mainloop() 