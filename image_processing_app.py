import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os


class ImageProcessingMainApp:
    
    
    def __init__(self, root):
        self.root = root
        self.root.title("Traitement d'Images - Menu Principal")
        self.root.geometry("700x600")
        self.root.configure(bg="white")
        
        # Centrer la fenêtre
        self.center_window()
        
        self.create_widgets()
    
    def center_window(self):
        
        self.root.update_idletasks()
        width = 700
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
       
        header_frame = tk.Frame(self.root, bg="#3498db", height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Titre principal
        title_label = tk.Label(
            header_frame,
            text=" APPLICATION DE TRAITEMENT D'IMAGES",
            font=("Arial", 22, "bold"),
            bg="#3498db",
            fg="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Sélectionnez un module dans la liste ci-dessous",
            font=("Arial", 11, "italic"),
            bg="#3498db",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
     
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, pady=30, padx=40)
        
        # Titre de la liste
        list_title = tk.Label(
            main_frame,
            text="MODULES DISPONIBLES",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#2c3e50"
        )
        list_title.pack(pady=(0, 20))
       
        modules_frame = tk.Frame(main_frame, bg="white")
        modules_frame.pack(fill=tk.BOTH, expand=True)
        
        # Module 1: Conversion
        self.create_module_item(
            modules_frame,
            "",
            "MODULE CONVERSION",
            "Conversion d'images : Niveaux de gris, Binarisation, Zoom",
            "#e74c3c",
            self.open_conversion_module,
            0
        )
        
        # Séparateur
        separator1 = tk.Frame(modules_frame, bg="#ecf0f1", height=2)
        separator1.pack(fill=tk.X, padx=20, pady=5)
        
        # Module 2: Histogramme
        self.create_module_item(
            modules_frame,
           "",
            "MODULE HISTOGRAMME",
            "Calcul et analyse d'histogrammes :RGB,NG,Égalisation",
            "#27ae60",
            self.open_histogram_module,
            1
        )
        
        # Séparateur
        separator2 = tk.Frame(modules_frame, bg="#ecf0f1", height=2)
        separator2.pack(fill=tk.X, padx=20, pady=5)
        
        # Espace pour futurs modules
        future_label = tk.Label(
            modules_frame,
            text=" D'autres modules seront disponibles prochainement...",
            font=("Arial", 9, "italic"),
            bg="white",
            fg="#95a5a6"
        )
        future_label.pack(pady=20)
     
        footer_frame = tk.Frame(self.root, bg="#ecf0f1", height=70)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Bouton Quitter
        btn_quit = tk.Button(
            footer_frame,
            text=" Quitter ",
            command=self.quit_application,
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_quit.pack(pady=15)
        
        footer_label = tk.Label(
            footer_frame,
            text="2025 - Application de Traitement d'Images | Python & OpenCV",
            font=("Arial", 8),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        footer_label.pack(side=tk.BOTTOM, pady=5)
    
    def create_module_item(self, parent, icon, title, description, color, command, index):
       
        
        # Frame principal de l'élément
        item_frame = tk.Frame(
            parent,
            bg="white",
            relief=tk.FLAT,
            borderwidth=0
        )
        item_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Frame de contenu avec bordure
        content_frame = tk.Frame(
            item_frame,
            bg="white",
            relief=tk.RAISED,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        content_frame.pack(fill=tk.X)
        
        # Frame gauche (icône + texte)
        left_frame = tk.Frame(content_frame, bg="white")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icône et titre sur la même ligne
        header_frame = tk.Frame(left_frame, bg="white")
        header_frame.pack(anchor=tk.W, fill=tk.X)
        
        icon_label = tk.Label(
            header_frame,
            text=icon,
            font=("Arial", 24),
            bg="white"
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=("Arial", 14, "bold"),
            bg="white",
            fg=color
        )
        title_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Description
        desc_label = tk.Label(
            left_frame,
            text=description,
            font=("Arial", 10),
            bg="white",
            fg="#7f8c8d",
            justify=tk.LEFT
        )
        desc_label.pack(anchor=tk.W, pady=(5, 0), padx=(34, 0))
        
        # Frame droit (bouton)
        right_frame = tk.Frame(content_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, padx=15, pady=15)
        
        # Bouton Ouvrir
        btn_open = tk.Button(
            right_frame,
            text=" Ouvrir",
            command=command,
            font=("Arial", 11, "bold"),
            bg=color,
            fg="white",
            padx=25,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2,
            activebackground=color,
            activeforeground="white"
        )
        btn_open.pack()
        
        # Effets hover sur tout l'élément
        def on_enter(e):
            content_frame.config(
                relief=tk.RAISED,
                borderwidth=3,
                highlightbackground=color,
                highlightthickness=2
            )
            btn_open.config(relief=tk.SUNKEN)
        
        def on_leave(e):
            content_frame.config(
                relief=tk.RAISED,
                borderwidth=2,
                highlightbackground="#bdc3c7",
                highlightthickness=1
            )
            btn_open.config(relief=tk.RAISED)
        
        content_frame.bind("<Enter>", on_enter)
        content_frame.bind("<Leave>", on_leave)
        btn_open.bind("<Enter>", on_enter)
        btn_open.bind("<Leave>", on_leave)
        left_frame.bind("<Enter>", on_enter)
        left_frame.bind("<Leave>", on_leave)
    
    def open_conversion_module(self):
     
        try:
            # Vérifier si le fichier existe
            if not os.path.exists("conversion_interface.py"):
                messagebox.showerror(
                    "Erreur",
                    "Le fichier 'conversion_interface.py' est introuvable.\n\n"
                    "Assurez-vous que le fichier est dans le même répertoire."
                )
                return
            
            # Lancer le module de conversion dans un nouveau processus
            subprocess.Popen([sys.executable, "conversion_interface.py"])
            
            messagebox.showinfo(
                "Module Conversion",
                "Le module de conversion a été ouvert dans une nouvelle fenêtre."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ouvrir le module de conversion.\n\nErreur: {str(e)}"
            )
    
    def open_histogram_module(self):
       
        try:
            # Vérifier si le fichier existe
            if not os.path.exists("histogramme_interface.py"):
                messagebox.showerror(
                    "Erreur",
                    "Le fichier 'histogramme_interface.py' est introuvable.\n\n"
                    "Assurez-vous que le fichier est dans le même répertoire."
                )
                return
            
            # Lancer le module d'histogramme dans un nouveau processus
            subprocess.Popen([sys.executable, "histogramme_interface.py"])
            
            messagebox.showinfo(
                "Module Histogramme",
                " Le module d'histogramme a été ouvert dans une nouvelle fenêtre."
            )
            
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Impossible d'ouvrir le module d'histogramme.\n\nErreur: {str(e)}"
            )
    
    def quit_application(self):
       
        response = messagebox.askyesno(
            "Quitter",
            "Voulez-vous vraiment quitter l'application ?"
        )
        if response:
            self.root.destroy()


def main():
   
    root = tk.Tk()
    app = ImageProcessingMainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()