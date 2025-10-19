import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from conversion import conversion


class ImageProcessingApp:
    """Application de traitement d'images avec comparaison OpenCV vs Manuel"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Traitement d'Images - Comparaison OpenCV vs Manuel")
        self.root.geometry("1000x700")
        self.root.configure(bg="white")
        
        # Instance de la classe conversion
        self.converter = conversion()
        
        # Variables pour stocker les images
        self.original_image = None
        self.opencv_image = None
        self.manual_image = None
        self.image_path = None
        
        # Fenêtre de résultats (sera créée à la demande)
        self.result_window = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface principale"""
        
        # ===== FRAME TITRE =====
        title_frame = tk.Frame(self.root, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="🖼️ Application de Traitement d'Images",
            font=("Arial", 20, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title_label.pack()
        
        # ===== FRAME CONTRÔLES =====
        control_frame = tk.Frame(self.root, bg="white", pady=20)
        control_frame.pack(fill=tk.X, padx=20)
        
        # Bouton Charger Image
        btn_load = tk.Button(
            control_frame,
            text="📁 Charger une Image",
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
        
        # ===== FRAME MENU TRAITEMENTS =====
        menu_frame = tk.Frame(self.root, bg="#f8f9fa", pady=20, relief=tk.GROOVE, borderwidth=2)
        menu_frame.pack(fill=tk.X, padx=20, pady=10)
        
        menu_label = tk.Label(
            menu_frame,
            text="Choisissez un traitement :",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        menu_label.pack(side=tk.LEFT, padx=20)
        
        # Liste déroulante (Combobox) pour les traitements
        self.treatment_var = tk.StringVar()
        self.treatment_combo = ttk.Combobox(
            menu_frame,
            textvariable=self.treatment_var,
            font=("Arial", 11),
            width=30,
            state="readonly"
        )
        self.treatment_combo['values'] = (
            "🎨 Niveaux de Gris",
            "⚫⚪ Binarisation",
            "🔍 Zoom x2",
            "🌈RGB TO HSV",
            "🌈RGB To yCrCb"
        )
        self.treatment_combo.set("Sélectionner un traitement...")
        self.treatment_combo.pack(side=tk.LEFT, padx=10)
        
        # Bouton Appliquer
        btn_apply = tk.Button(
            menu_frame,
            text="▶ Appliquer",
            command=self.apply_selected_treatment,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_apply.pack(side=tk.LEFT, padx=10)
        
        # Bouton Restaurer
        btn_restore = tk.Button(
            menu_frame,
            text="🔄 Restaurer Original",
            command=self.restore_original,
            font=("Arial", 11, "bold"),
            bg="#e67e22",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        btn_restore.pack(side=tk.LEFT, padx=10)
        
        # ===== FRAME PRÉVISUALISATION =====
        preview_frame = tk.Frame(self.root, bg="white", pady=20)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        preview_title = tk.Label(
            preview_frame,
            text="Prévisualisation de l'image originale",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#34495e"
        )
        preview_title.pack(pady=10)
        
        # Canvas pour l'image originale
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
        
        # ===== FRAME INFO =====
        info_frame = tk.Frame(self.root, bg="#f8f9fa", pady=10, relief=tk.FLAT)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.info_label = tk.Label(
            info_frame,
            text="ℹ️ Astuce : Chargez une image puis sélectionnez un traitement dans la liste",
            font=("Arial", 10),
            bg="#f8f9fa",
            fg="#7f8c8d"
        )
        self.info_label.pack()
    
    def load_image(self):
        """Charge une image depuis le système de fichiers"""
        file_path = filedialog.askopenfilename(
            title="Sélectionner une image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("Tous les fichiers", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Charger avec la classe conversion
        if self.converter.charger_image(file_path):
            self.image_path = file_path
            self.original_image = self.converter.original_image.copy()
            
            # Mettre à jour l'interface
            filename = file_path.split("/")[-1]
            self.file_label.config(text=f"✅ {filename}", fg="#27ae60")
            
            # Afficher dans le canvas
            self.display_preview()
            
            # Mettre à jour l'info
            h, w = self.converter.get_dimensions()[:2]
            self.info_label.config(
                text=f"📊 Image chargée : {w}x{h} pixels",
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
    
    def display_preview(self):
        """Affiche l'image originale dans le canvas de prévisualisation"""
        if self.original_image is None:
            return
        
        # Convertir BGR (OpenCV) vers RGB (PIL)
        img_rgb = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Redimensionner pour s'adapter au canvas
        canvas_width = 600
        canvas_height = 400
        img_pil.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        # Convertir en PhotoImage
        self.preview_photo = ImageTk.PhotoImage(img_pil)
        
        # Effacer et afficher
        self.canvas.delete("all")
        x = canvas_width // 2
        y = canvas_height // 2
        self.canvas.create_image(x, y, image=self.preview_photo, anchor=tk.CENTER)
    
    def check_image_loaded(self):
        """Vérifie qu'une image est chargée avant traitement"""
        if not self.converter.a_image():
            messagebox.showwarning(
                "Aucune image",
                "Veuillez d'abord charger une image !"
            )
            return False
        return True
    
    def apply_selected_treatment(self):
        """Applique le traitement sélectionné dans la liste déroulante"""
        if not self.check_image_loaded():
            return
        
        treatment = self.treatment_var.get()
        
        if treatment == "Sélectionner un traitement..." or not treatment:
            messagebox.showwarning(
                "Aucun traitement",
                "Veuillez sélectionner un traitement dans la liste !"
            )
            return
        
        if treatment == "🎨 Niveaux de Gris":
            self.apply_grayscale()
        elif treatment == "⚫⚪ Binarisation":
            self.apply_binary()
        elif treatment == "🔍 Zoom x2":
            self.apply_zoom()
        elif treatment == "🌈RGB TO HSV":
            self.apply_RGB_to_HSV()
        elif treatment == "🌈RGB To yCrCb":
            self.apply_RGB_to_YCbCr()
        
    
    def apply_grayscale(self):
        """Applique la conversion en niveaux de gris"""
        if not self.check_image_loaded():
            return
        
        # Restaurer l'original avant traitement
        self.converter.restaurer_original()
        
        # OpenCV
        converter_opencv = conversion()
        converter_opencv.charger_image(self.image_path)
        converter_opencv.convertir_en_gris_opencv()
        self.opencv_image = converter_opencv.image.copy()
        
        # Manuel
        self.converter.convertir_en_gris()
        self.manual_image = self.converter.image.copy()
        
        # Afficher les résultats
        self.show_results("Conversion en Niveaux de Gris")
    
    def apply_binary(self):
        """Applique la binarisation"""
        if not self.check_image_loaded():
            return
        
        # Restaurer l'original avant traitement
        self.converter.restaurer_original()
        
        # OpenCV
        converter_opencv = conversion()
        converter_opencv.charger_image(self.image_path)
        converter_opencv.convertir_binaire_opencv()
        self.opencv_image = converter_opencv.image.copy()
        
        # Manuel
        self.converter.convertir_binaire()
        self.manual_image = self.converter.image.copy()
        
        # Afficher les résultats
        self.show_results("Binarisation (Seuil = 127)")
    
    def apply_zoom(self):
        """Applique un zoom x2"""
        if not self.check_image_loaded():
            return
        
        # Restaurer l'original avant traitement
        self.converter.restaurer_original()
        
        # OpenCV - utiliser la même méthode que le manuel
        h, w = self.converter.image.shape[:2]
        c = self.converter.image.shape[2] if len(self.converter.image.shape) == 3 else 1
        
        if c == 1:
            opencv_zoomed = np.zeros((h * 2, w * 2), dtype=np.uint8)
        else:
            opencv_zoomed = np.zeros((h * 2, w * 2, c), dtype=np.uint8)
        
        # Remplissage avec nearest neighbor
        for i in range(h):
            for j in range(w):
                opencv_zoomed[2 * i:2 * i + 2, 2 * j:2 * j + 2] = self.converter.image[i, j]
        
        self.opencv_image = opencv_zoomed.copy()
        
        # Manuel
        self.converter.zoom(facteur=2)
        self.manual_image = self.converter.image.copy()
        
        # Afficher les résultats
        self.show_results("Zoom x2 (Nearest Neighbor)")
    
    def restore_original(self):
        """Restaure l'image originale"""
        if not self.check_image_loaded():
            return
        
        self.converter.restaurer_original()
        self.display_preview()
        self.info_label.config(text="✅ Image originale restaurée", fg="#27ae60")
        messagebox.showinfo("Restauration", "Image originale restaurée avec succès !")
    
    def show_results(self, treatment_name):
        """Affiche les résultats dans une fenêtre séparée"""
        
        # Fermer la fenêtre précédente si elle existe
        if self.result_window is not None:
            try:
                self.result_window.destroy()
            except:
                pass
        
        # Créer une nouvelle fenêtre
        self.result_window = tk.Toplevel(self.root)
        self.result_window.title(f"Résultats - {treatment_name}")
        self.result_window.geometry("1400x700")
        self.result_window.configure(bg="white")
        
        # Titre
        title_frame = tk.Frame(self.result_window, bg="#f8f9fa", pady=15, relief=tk.RAISED, borderwidth=1)
        title_frame.pack(fill=tk.X)
        
        title = tk.Label(
            title_frame,
            text=f"Comparaison : {treatment_name}",
            font=("Arial", 18, "bold"),
            bg="#f8f9fa",
            fg="#2c3e50"
        )
        title.pack()
        
        # Frame pour les 3 images
        images_frame = tk.Frame(self.result_window, bg="white")
        images_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurer 3 colonnes égales
        images_frame.columnconfigure(0, weight=1)
        images_frame.columnconfigure(1, weight=1)
        images_frame.columnconfigure(2, weight=1)
        
        # Afficher les 3 images
        self.display_image_in_frame(
            images_frame, self.original_image,
            "Image Originale", 0, "#3498db"
        )
        self.display_image_in_frame(
            images_frame, self.opencv_image,
            "Traitement OpenCV", 1, "#e74c3c"
        )
        self.display_image_in_frame(
            images_frame, self.manual_image,
            "Traitement Manuel", 2, "#27ae60"
        )
        
        # Bouton de fermeture
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
    
    def display_image_in_frame(self, parent, image, title, column, color):
        """Affiche une image dans un frame avec titre"""
        
        # Frame conteneur
        frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, borderwidth=2)
        frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        
        # Titre avec couleur
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
        
        # Convertir et redimensionner l'image
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        # Redimensionner pour s'adapter (max 400x400)
        img_pil.thumbnail((400, 400), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(img_pil)
        
        # Label pour l'image
        label_img = tk.Label(frame, image=photo, bg="white")
        label_img.image = photo  # Garder une référence
        label_img.pack(padx=10, pady=10)
        
        # Dimensions
        h, w = image.shape[:2]
        dim_label = tk.Label(
            frame,
            text=f"📐 {w} x {h} pixels",
            font=("Arial", 9),
            bg="white",
            fg="#7f8c8d",
            pady=5
        )
        dim_label.pack()

    def apply_RGB_to_HSV(self):
        """Applique la conversion RGB vers HSV"""
        if not self.check_image_loaded():
            return
        
        # Restaurer l'original avant traitement
        self.converter.restaurer_original()
        
        # OpenCV
        converter_opencv = conversion()
        converter_opencv.charger_image(self.image_path)
        converter_opencv.RGB_to_HSV()
        self.opencv_image = converter_opencv.image.copy()
        
        # Manuel
        self.converter.RGB_to_HSV()
        self.manual_image = self.converter.image.copy()
        # Afficher les résultats
        self.show_results("Conversion RGB vers HSV")
    def apply_RGB_to_YCbCr(self):
        """Applique la conversion RGB vers YCbCr"""
        if not self.check_image_loaded():
            return
        
        # Restaurer l'original avant traitement
        self.converter.restaurer_original()
        
        # OpenCV
        converter_opencv = conversion()
        converter_opencv.charger_image(self.image_path)
        converter_opencv.RGB_to_YCbCr()
        self.opencv_image = converter_opencv.image.copy()
        
        # Manuel
        self.converter.RGB_to_YCbCr()
        self.manual_image = self.converter.image.copy()
        
        # Afficher les résultats
        self.show_results("Conversion RGB vers YCbCr")

def main():
    """Point d'entrée de l'application"""
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()