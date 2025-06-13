import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import sys

# Automatisk installation av pyperclip om det saknas
try:
    import pyperclip
except ImportError:
    print("Installerar pyperclip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        import pyperclip
        print("pyperclip installerat framgångsrikt!")
    except Exception as e:
        messagebox.showerror("Installationsfel", 
                           f"Kunde inte installera pyperclip automatiskt.\n"
                           f"Fel: {e}\n\n"
                           f"Installera manuellt med: pip install pyperclip")
        sys.exit(1)

class TextTemplateFiller:
    def __init__(self, root):
        self.root = root
        self.root.title("POB-Copytext")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variabel för att hålla template-filens sökväg
        self.template_file = "copytext.txt"
        
        # Skapa huvudframe
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfigurera grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Titel
        title_label = ttk.Label(main_frame, text="POB-Copytext", 
                               font=("Arial", 14, "bold"))
        by_label = ttk.Label(main_frame, text="Av: MAAND19", font=("Arial", 14, "italic"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        by_label.grid(row=0, column=2, columnspan=2, pady=(0, 20))
        
        # Template fil sektion
        ttk.Label(main_frame, text="Template fil:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_var = tk.StringVar(value=self.template_file)
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var, state="readonly")
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(file_frame, text="Bläddra", command=self.browse_file).grid(row=0, column=1)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, 
                                                           sticky=(tk.W, tk.E), pady=20)
        
        # Textfält sektion
        ttk.Label(main_frame, text="Textfält:", font=("Arial", 10, "bold")).grid(row=3, column=0, 
                                                                                 columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Dictionary för att lagra textfält
        self.text_fields = {}
        
        # Skapa textfält
        self.create_text_field(main_frame, 4, "Customer_field", "Kund:")
        self.create_text_field(main_frame, 5, "Model_field", "Modell:")
        self.create_text_field(main_frame, 6, "Serial_field", "Serienummer:")
        self.create_multiline_field(main_frame, 7, "Description_field", "Felbeskrivning:")
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=8, column=0, columnspan=2, 
                                                           sticky=(tk.W, tk.E), pady=20)
        
        # Knapp för att kopiera text
        copy_btn = ttk.Button(main_frame, text="Kopiera Text", command=self.copy_text)
        copy_btn.grid(row=9, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_var = tk.StringVar(value="Redo att användas")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=10, column=0, columnspan=2, pady=5)
        

        
        # Variabel för att hålla reda på nästa rad för dynamiska fält
        self.next_row = 11
    
    def create_text_field(self, parent, row, field_name, label_text):
        """Skapa ett textfält med label"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W, pady=2)
        
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        self.text_fields[field_name] = entry
    
    def create_multiline_field(self, parent, row, field_name, label_text):
        """Skapa ett multi-line textfält med label"""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=(tk.W, tk.N), pady=2)
        
        # Skapa frame för text widget och scrollbar
        text_frame = ttk.Frame(parent)
        text_frame.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        text_frame.columnconfigure(0, weight=1)
        
        # Text widget för multi-line input
        text_widget = tk.Text(text_frame, height=4, width=35, wrap=tk.WORD)
        text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar för text widget
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        text_widget.config(yscrollcommand=scrollbar.set)
        
        self.text_fields[field_name] = text_widget
    
    
    def browse_file(self):
        """Bläddra efter template-fil"""
        filename = filedialog.askopenfilename(
            title="Välj template-fil",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.template_file = filename
            self.file_var.set(filename)
    

    
    def copy_text(self):
        """Läs template-filen, ersätt platshållare och kopiera till clipboard"""
        try:
            # Läs template-filen
            with open(self.template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Ersätt platshållare med värden från textfält
            final_text = template_content
            
            for field_name, widget in self.text_fields.items():
                placeholder = "{" + field_name + "}"
                
                # Hantera både Entry och Text widgets
                if isinstance(widget, tk.Text):
                    field_value = widget.get("1.0", tk.END).strip()
                else:
                    field_value = widget.get()
                
                final_text = final_text.replace(placeholder, field_value)
            
            # Kopiera till clipboard
            pyperclip.copy(final_text)
            
            self.status_var.set("Text kopierad till clipboard!")
                
        except FileNotFoundError:
            messagebox.showerror("Fel", f"Template-filen '{self.template_file}' hittades inte!")
            self.status_var.set("Fel: Template-fil saknas")
        except Exception as e:
            messagebox.showerror("Fel", f"Ett fel uppstod: {e}")
            self.status_var.set(f"Fel: {e}")


def main():
    root = tk.Tk()
    app = TextTemplateFiller(root)
    root.mainloop()

if __name__ == "__main__":
    main()