import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from histogramme import Histogramme


class HistogrammeApp:
   
    def __init__(self, root):
        self.root = root
        self.root.title("Calcul d'Histogrammes - Comparaison OpenCV vs Manuel")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        
        # Instance de la classe Histogramme
        self.hist_processor = Histogramme()
        
        # Variables
        self.original_image = None
        self.image_path = None
        self.hist_manuel = None
        self.hist_opencv = None
        
        # Fenêtre de résultats
        self.result_window = None
        
        self.create_widgets()
    
    def create_widgets(self):
       
        
        title_frame = tk.Frame(self.root, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text=" Calcul et Visualisation d'Histogrammes",
            font=("Arial", 20, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack()
        
       
        control_frame = tk.Frame(self.root, bg="white", pady=20)
        control_frame.pack(fill=tk.X, padx=20)
        
        # Bouton Charger Image
        btn_load = tk.Button(
            control_frame,
            text=" Charger une Image",
            command=self.load_image,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_load.pack(side=tk.LEFT, padx=10)
        
        # Label du fichier chargé
        self.file_label = tk.Label(
            control_frame,
            text="Aucune image chargée",
            font=("Arial", 10, "italic"),
            bg="white",
            fg="#7f8c8d"
        )
        self.file_label.pack(side=tk.LEFT, padx=10)
        
       
        menu_frame = tk.Frame(self.root, bg="#f8f9fa", pady=20, relief=tk.GROOVE, borderwidth=2)
        menu_frame.pack(fill=tk.X, padx=20, pady=10)
        
        menu_label = tk.Label(
            menu_frame,
            text="Choisissez un type d'histogramme :",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        menu_label.pack(side=tk.LEFT, padx=20)
        
        
        self.treatment_var = tk.StringVar()
        self.treatment_combo = ttk.Combobox(
            menu_frame,
            textvariable=self.treatment_var,
            font=("Arial", 11),
            width=35,
            state="readonly"
        )
        self.treatment_combo['values'] = (
            " Histogramme Couleur (RGB)",
            " Histogramme Niveaux de Gris",
            " Histogramme Cumulé",
            " Égalisation d'Histogramme"

        )
        self.treatment_combo.set("Sélectionner un type...")
        self.treatment_combo.pack(side=tk.LEFT, padx=10)
        
        # Bouton Calculer
        btn_calculate = tk.Button(
            menu_frame,
            text=" Calculer",
            command=self.calculate_selected_histogram,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_calculate.pack(side=tk.LEFT, padx=10)
        
        
        preview_frame = tk.Frame(self.root, bg="white", pady=20)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        preview_title = tk.Label(
            preview_frame,
            text="Prévisualisation de l'image",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#34495e"
        )
        preview_title.pack(pady=10)
        
        # Canvas pour l'image
        self.canvas = tk.Canvas(
            preview_frame,
            bg="#ecf0f1",
            width=600,
            height=400,
            highlightthickness=2,
            highlightbackground="#95a5a6"
        )
        self.canvas.pack()
        
        # Texte par défaut
        self.canvas.create_text(
            300, 200,
            text="Chargez une image pour commencer",
            font=("Arial", 14, "italic"),
            fill="#7f8c8d",
            tags="placeholder"
        )
        
        
        info_frame = tk.Frame(self.root, bg="#f8f9fa", pady=10, relief=tk.FLAT)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.info_label = tk.Label(
            info_frame,
            text="ℹAstuce : Chargez une image puis sélectionnez un type d'histogramme",
            font=("Arial", 10),
            bg="#f8f9fa",
            fg="#7f8c8d"
        )
        self.info_label.pack()
    #Charge une image depuis le système de fichiers
    def load_image(self):
       
        file_path = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Charger avec la classe Histogramme
        if self.hist_processor.charger_image(file_path):
            self.image_path = file_path
            self.original_image = self.hist_processor.original_image.copy()
            
            # Mettre à jour l'interface
            filename = file_path.split("/")[-1]
            self.file_label.config(text=f" {filename}", fg="#27ae60")
            
            # Afficher dans le canvas
            self.display_preview()
            
            # Mettre à jour l'info
            h, w = self.hist_processor.get_dimensions()[:2]
            self.info_label.config(
                text=f" Image chargée : {w}x{h} pixels",
                fg="#27ae60"
            )
            
            messagebox.showinfo(
                "Succès",
                f"Image chargée avec succès !\n\nDimensions : {w}x{h} pixels"
            )
        else:
            messagebox.showerror(
                "Erreur",
                "Impossible de charger l'image.\nVérifiez le format du fichier."
            )
    #Affiche l'image dans le canvas de prévisualisation
    def display_preview(self):
       
        if self.original_image is None:
            return
        
        # Convertir BGR (OpenCV) vers RGB (PIL)
        img_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Redimensionner
        canvas_width = 600
        canvas_height = 400
        img_pil.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        # Convertir en PhotoImage
        self.preview_photo = ImageTk.PhotoImage(img_pil)
        
        # Afficher
        self.canvas.delete("all")
        x = canvas_width // 2
        y = canvas_height // 2
        self.canvas.create_image(x, y, image=self.preview_photo, anchor=tk.CENTER)

    #Vérifie qu'une image est chargée
    def check_image_loaded(self):
        
        if not self.hist_processor.a_image():
            messagebox.showwarning(
                "Aucune image",
                "Veuillez d'abord charger une image !"
            )
            return False
        return True
    
    def calculate_selected_histogram(self):
      
        if not self.check_image_loaded():
            return
        
        treatment = self.treatment_var.get()
        
        if treatment == "Sélectionner un type..." or not treatment:
            messagebox.showwarning(
                "Aucun type",
                "Veuillez sélectionner un type d'histogramme !"
            )
            return
        
        if treatment == " Histogramme Couleur (RGB)":
            self.calculate_color_histogram()
        elif treatment == " Histogramme Niveaux de Gris":
            self.calculate_gray_histogram()
        elif treatment == " Histogramme Cumulé":
            self.calculate_histogramme_cumule()
        elif treatment == " Égalisation d'Histogramme":
            self.calculate_equalization()

    #Calcule et affiche l'histogramme couleur
    def calculate_color_histogram(self):
        
        if not self.check_image_loaded():
            return
        
        # Calculer avec les deux méthodes
        self.hist_manuel = self.hist_processor.calculer_histogramme_manuel()
        self.hist_opencv = self.hist_processor.calculer_histogramme_opencv()
        
        # Afficher les résultats
        self.show_histogram_results("Histogramme Couleur (RGB)", mode="color")
    #Calcule et affiche l'histogramme couleur
    def calculate_gray_histogram(self):
        
        if not self.check_image_loaded():
            return
        
        # Calculer avec les deux méthodes
        self.hist_manuel = self.hist_processor.calculer_histogramme_gris_manuel()
        self.hist_opencv = self.hist_processor.calculer_histogramme_gris_opencv()
        
        # Afficher les résultats
        self.show_histogram_results("Histogramme Niveaux de Gris", mode="gray")


    def calculate_histogramme_cumule(self):
        if not self.check_image_loaded():
            return
        # Calculer les histogrammes de base avec les deux méthodes
        hist_manuel_base = self.hist_processor.calculer_histogramme_manuel()
        hist_opencv_base = self.hist_processor.calculer_histogramme_opencv()
        if hist_manuel_base is None or hist_opencv_base is None:
            messagebox.showerror("Erreur", "Impossible de calculer les histogrammes.")
            return

        # Fonction utilitaire pour cumuler un dict d'histogrammes
        def cumuler_histogramme(hist_dict):
            cumule = {}
            for k, v in hist_dict.items():
                arr = np.asarray(v).flatten()
                cumule[k] = np.cumsum(arr).astype(np.int32)
            return cumule

        # Calcul des cumulés
        self.hist_manuel = cumuler_histogramme(hist_manuel_base)
        self.hist_opencv = cumuler_histogramme(hist_opencv_base)

        # Déterminer le mode d'affichage (gray si seules 'gray' existent, sinon color)
        if 'gray' in self.hist_manuel and len(self.hist_manuel) == 1:
            mode = "gray"
        else:
            mode = "color"

        # Afficher les résultats
        self.show_histogram_cumule_results("Histogramme Cumulé", mode=mode)

    #Calcule et affiche l'égalisation d'histogramme
    def calculate_equalization(self):
        
        if not self.check_image_loaded():
            return
        
        # Égaliser avec les deux méthodes
        img_manuel = self.hist_processor.egaliser_histogramme_manuel()
        img_opencv = self.hist_processor.egaliser_histogramme_opencv()
        
        # Afficher les résultats
        self.show_equalization_results(img_manuel, img_opencv)
    
    def show_histogram_results(self, title, mode="color"):
        
        
        # Fermer la fenêtre précédente
        if self.result_window is not None:
            try:
                self.result_window.destroy()
            except:
                pass
        
        # Créer nouvelle fenêtre
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title(f"Résultats - {title}")
        self.result_window.geometry("1400x800")
        self.result_window.configure(bg="white")
        
        # Titre
        title_frame = tk.Frame(self.result_window, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text=f"Comparaison : {title}",
            font=("Arial", 18, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.result_window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurer colonnes
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        # Afficher image originale
        self.display_image_result(main_frame, self.original_image, "Image Originale", 0)
        
        # Afficher histogramme manuel
        self.display_histogram_plot(main_frame, self.hist_manuel, "Histogramme Manuel", 1, mode)
        
        # Afficher histogramme OpenCV
        self.display_histogram_plot(main_frame, self.hist_opencv, "Histogramme OpenCV", 2, mode)
        
        # Bouton fermer
        btn_close = tk.Button(
            self.result_window,
            text="Fermer",
            command=self.result_window.destroy,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_close.pack(pady=(0, 20))
    '''
    def show_histogram_cumule_results(self, title, mode="gray"):
        """Affiche les histogrammes dans une fenêtre séparée"""
        
        # Fermer la fenêtre précédente
        if self.result_window is not None:
            try:
                self.result_window.destroy()
            except:
                pass
        
        # Créer nouvelle fenêtre
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title(f"Résultats - {title}")
        self.result_window.geometry("1400x800")
        self.result_window.configure(bg="white")
        
        # Titre
        title_frame = tk.Frame(self.result_window, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text=f"Comparaison : {title}",
            font=("Arial", 18, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.result_window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurer colonnes
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        # Afficher image originale
        self.display_image_result(main_frame, self.original_image, "Image Originale", 0)
        
        # Afficher histogramme manuel
        self.display_histogram_plot(main_frame, self.hist_manuel, "Histogramme Cumulé Manuel", 1, mode)
        
        # Afficher histogramme OpenCV
        self.display_histogram_plot(main_frame, self.hist_opencv, "Histogramme Cumulé OpenCV", 2, mode)
        
        # Bouton fermer
        btn_close = tk.Button(
            self.result_window,
            text="Fermer",
            command=self.result_window.destroy,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_close.pack(pady=(0, 20))
    '''
    # ...existing code...
    def show_histogram_cumule_results(self, title, mode="gray"):
        
        
        # Fermer la fenêtre précédente
        if self.result_window is not None:
            try:
                self.result_window.destroy()
            except:
                pass
        
        # Créer nouvelle fenêtre
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title(f"Résultats - {title}")
        self.result_window.geometry("1400x800")
        self.result_window.configure(bg="white")
        
        # Titre
        title_frame = tk.Frame(self.result_window, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text=f"Comparaison : {title}",
            font=("Arial", 18, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.result_window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurer colonnes
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        # Afficher image originale
        self.display_image_result(main_frame, self.original_image, "Image Originale", 0)
        
        # Afficher histogramme manuel (en courbe car cumulé)
        self.display_histogram_plot(main_frame, self.hist_manuel, "Histogramme Cumulé Manuel", 1, mode, cumule=True)
        
        # Afficher histogramme OpenCV (en courbe car cumulé)
        self.display_histogram_plot(main_frame, self.hist_opencv, "Histogramme Cumulé OpenCV", 2, mode, cumule=True)
        
        # Bouton fermer
        btn_close = tk.Button(
            self.result_window,
            text="Fermer",
            command=self.result_window.destroy,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_close.pack(pady=(0, 20))

    def display_histogram_plot(self, parent, hist_data, title, column, mode, cumule=False):
       
        frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Titre
        color = "#e74c3c" if "Manuel" in title else "#27ae60"
        title_bg = tk.Frame(frame, bg=color, height=40)
        title_bg.pack(fill=tk.X)
        
        label_title = tk.Label(
            title_bg,
            text=title,
            font=("Arial", 12, "bold"),
            bg=color,
            fg="white",
            pady=10
        )
        label_title.pack()
        
        # Créer le graphique
        fig = Figure(figsize=(5, 5), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Préparer les données
        x = np.arange(256)
        
        if mode == "color":
            blue = np.asarray(hist_data.get('blue', np.zeros(256))).flatten().astype(float)
            green = np.asarray(hist_data.get('green', np.zeros(256))).flatten().astype(float)
            red = np.asarray(hist_data.get('red', np.zeros(256))).flatten().astype(float)
            
            if cumule:
                # Tracer en courbe pour cumulés et remplir sous la courbe
                ax.plot(x, blue, color='blue', label='Bleu', linewidth=1.5)
                ax.fill_between(x, blue, color='blue', alpha=0.15)
                ax.plot(x, green, color='green', label='Vert', linewidth=1.5)
                ax.fill_between(x, green, color='green', alpha=0.15)
                ax.plot(x, red, color='red', label='Rouge', linewidth=1.5)
                ax.fill_between(x, red, color='red', alpha=0.15)
            else:
                # Barres groupées pour histogramme classique
                width = 0.25
                ax.bar(x - width, blue, width=width, color='blue', label='Bleu', alpha=0.7)
                ax.bar(x, green, width=width, color='green', label='Vert', alpha=0.7)
                ax.bar(x + width, red, width=width, color='red', label='Rouge', alpha=0.7)
            ax.legend()
        else:
            gray = np.asarray(hist_data.get('gray', np.zeros(256))).flatten().astype(float)
            if cumule:
                ax.plot(x, gray, color='black', linewidth=2)
                ax.fill_between(x, gray, color='black', alpha=0.15)
            else:
                ax.bar(x, gray, color='black', width=1.0)
        
        ax.set_xlabel('Intensité des pixels', fontsize=10)
        ax.set_ylabel('Nombre de pixels', fontsize=10)
        ax.set_xlim([0, 255])
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        
        # Intégrer dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)


    def display_image_result(self, parent, image, title, column):
        
        frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Titre
        title_bg = tk.Frame(frame, bg="#3498db", height=40)
        title_bg.pack(fill=tk.X)
        
        label_title = tk.Label(
            title_bg,
            text=title,
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            pady=10
        )
        label_title.pack()
        
        # Image
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((400, 400), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img_pil)
        
        label_img = tk.Label(frame, image=photo, bg="white")
        label_img.image = photo
        label_img.pack(padx=10, pady=10)
    '''
    def display_histogram_plot(self, parent, hist_data, title, column, mode):
        """Affiche le graphique d'histogramme"""
        frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Titre
        color = "#e74c3c" if "Manuel" in title else "#27ae60"
        title_bg = tk.Frame(frame, bg=color, height=40)
        title_bg.pack(fill=tk.X)
        
        label_title = tk.Label(
            title_bg,
            text=title,
            font=("Arial", 12, "bold"),
            bg=color,
            fg="white",
            pady=10
        )
        label_title.pack()
        
        # Créer le graphique
        fig = Figure(figsize=(5, 5), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        if mode == "color":
            # Histogramme couleur
            ax.plot(hist_data['blue'], color='blue', label='Bleu', linewidth=1.5)
            ax.plot(hist_data['green'], color='green', label='Vert', linewidth=1.5)
            ax.plot(hist_data['red'], color='red', label='Rouge', linewidth=1.5)
            ax.legend()
        else:
            # Histogramme gris
            ax.plot(hist_data['gray'], color='black', linewidth=2)
        
        ax.set_xlabel('Intensité des pixels', fontsize=10)
        ax.set_ylabel('Nombre de pixels', fontsize=10)
        ax.set_xlim([0, 255])
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        
        # Intégrer dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
    '''


    '''
    def display_histogram_plot(self, parent, hist_data, title, column, mode):
        """Affiche le graphique d'histogramme"""
        frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Titre
        color = "#e74c3c" if "Manuel" in title else "#27ae60"
        title_bg = tk.Frame(frame, bg=color, height=40)
        title_bg.pack(fill=tk.X)
        
        label_title = tk.Label(
            title_bg,
            text=title,
            font=("Arial", 12, "bold"),
            bg=color,
            fg="white",
            pady=10
        )
        label_title.pack()
        
        # Créer le graphique
        fig = Figure(figsize=(5, 5), dpi=80, facecolor='white')
        ax = fig.add_subplot(111)
        
        # Préparer les données
        x = np.arange(256)
        
        if mode == "color":
            # Utiliser des barres groupées pour les 3 canaux
            blue = np.asarray(hist_data.get('blue', np.zeros(256))).flatten()
            green = np.asarray(hist_data.get('green', np.zeros(256))).flatten()
            red = np.asarray(hist_data.get('red', np.zeros(256))).flatten()
            
            width = 0.25
            ax.bar(x - width, blue, width=width, color='blue', label='Bleu', alpha=0.7)
            ax.bar(x, green, width=width, color='green', label='Vert', alpha=0.7)
            ax.bar(x + width, red, width=width, color='red', label='Rouge', alpha=0.7)
            ax.legend()
        else:
            # Histogramme gris en barres
            gray = np.asarray(hist_data.get('gray', np.zeros(256))).flatten()
            ax.bar(x, gray, color='black', width=1.0)
        
        ax.set_xlabel('Intensité des pixels', fontsize=10)
        ax.set_ylabel('Nombre de pixels', fontsize=10)
        ax.set_xlim([0, 255])
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        
        # Intégrer dans Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
    '''
    def show_equalization_results(self, img_manuel, img_opencv):
       
        
        # Fermer fenêtre précédente
        if self.result_window is not None:
            try:
                self.result_window.destroy()
            except:
                pass
        
        # Créer nouvelle fenêtre
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title("Résultats - Égalisation d'Histogramme")
        self.result_window.geometry("1400x700")
        self.result_window.configure(bg="white")
        
        # Titre
        title_frame = tk.Frame(self.result_window, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="Comparaison : Égalisation d'Histogramme",
            font=("Arial", 18, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack()
        
        # Frame principal
        main_frame = tk.Frame(self.result_window, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        
        # Afficher les 3 images
        self.display_image_result(main_frame, self.original_image, "Image Originale", 0)
        self.display_image_result(main_frame, img_opencv, "Égalisation OpenCV", 1)
        self.display_image_result(main_frame, img_manuel, "Égalisation Manuel", 2)
        
        # Bouton fermer
        btn_close = tk.Button(
            self.result_window,
            text="Fermer",
            command=self.result_window.destroy,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_close.pack(pady=(0, 20))


def main():
    
    root = tk.Tk()
    app = HistogrammeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()