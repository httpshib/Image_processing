import cv2 
import numpy as np
import os
import ctypes


class conversion:

    
    def __init__(self):
        self.image = None
        self.original_image = None
        self.image_path = None
        self.show_windows = False
        self.last_comparatif = None
    
    def charger_image(self, chemin):
     
        if os.path.exists(chemin):
            self.image = cv2.imread(chemin)
            if self.image is not None:
                self.original_image = self.image.copy()
                self.image_path = chemin
                return True
        return False
    
    def get_dimensions(self):
        if self.image is not None:
            return self.image.shape
        return None
    
    def afficher_image(self, titre="Image"):
   
        if self.image is None:
            return False
        # affichage désactivé par défaut pour garder uniquement le traitement
        if not self.show_windows:
            return True
        cv2.imshow(titre, self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    
    def afficher_image_original(self, titre="Image_Originale"):
   
        if self.image is None:
            return False
        if not self.show_windows:
            return True
        cv2.imshow(titre, self.original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
   
    def sauvegarder_image(self, chemin):
   
        if self.image is None:
            return False
        return cv2.imwrite(chemin, self.image)
    
    def restaurer_original(self):
       
        if self.original_image is None:
            return False
        self.image = self.original_image.copy()
        return True
    
    def zoom(self, facteur=2):
   
        if self.image is None:
            return False
        
        h, w = self.image.shape[:2]
        c = self.image.shape[2] if len(self.image.shape) == 3 else 1
       
        if c == 1:
            zoomedimg = np.zeros((h * facteur, w * facteur), dtype=np.uint8)
        else:
            zoomedimg = np.zeros((h * facteur, w * facteur, c), dtype=np.uint8)
        
        # Remplissage de l'image zoomée
        for i in range(h):
            for j in range(w):
                zoomedimg[facteur * i:facteur * i + facteur, 
                         facteur * j:facteur * j + facteur] = self.image[i, j]
        
        self.image = zoomedimg
        # ne pas afficher automatiquement ; stocke le comparatif si besoin
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='Zoom - Comparatif')
            except Exception:
                pass
        return True
    
    def a_image(self):
        return self.image is not None
    #///////////////////////////////////////////////////////////////////////////////////////////////////////////
    def convertir_en_gris(self):
        if self.image is None:
            return False
        h, w = self.image.shape[:2]
        
        for i in range(h):
            for j in range(w):
               R, G, B = self.image[i, j]
               gris= 0.299*R +0.587*G +0.114*B
               #gris = (R + G + B)//3
               self.image[i, j] = [gris, gris, gris]
        # ne pas afficher par défaut
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='Gris - Comparatif')
            except Exception:
                pass
        return True
    
    def convertir_en_gris_opencv(self):
        if self.image is None:
            return False
        gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='Gris OpenCV - Comparatif')
            except Exception:
                pass
        return True

    #/////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def convertir_binaire(self):
        if self.image is None:
            return False

        h, w = self.image.shape[:2]
        
        R_min, G_min, B_min = 127, 127, 127

        binary = np.where(
            (self.image[:, :, 2] > R_min) & (self.image[:, :, 1] > G_min) & (self.image[:, :, 0] > B_min),
              255,
              0
               ).astype(np.uint8)
               
        # remplacer l'image manuelle par la binaire (3 canaux si besoin)
        if len(binary.shape) == 2:
            manu_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        else:
            manu_img = binary
        # temporisation : ne pas remplacer self.image si vous voulez garder état différent; ici on met à jour
        self.image = manu_img
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='Binaire - Comparatif')
            except Exception:
                pass
        return True
    def convertir_binaire_opencv(self):
        if self.image is None:
            return False

        gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gris, 127, 255, cv2.THRESH_BINARY)
        self.image = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='Binaire OpenCV - Comparatif')
            except Exception:
                pass
        return True
    #//////////////////////////////////////////////////////////////////////////////////////////
    def RGB_to_HSV(self):
        if self.image is None:
            return False

        h, w = self.image.shape[:2]
        hsv_image = np.zeros((h, w, 3), dtype=np.uint8)

        for i in range(h):
            for j in range(w):
                R, G, B = self.image[i, j] / 255.0
                Cmax = max(R, G, B)
                Cmin = min(R, G, B)
                delta = Cmax - Cmin

                # Hue calculation
                if delta == 0:
                    H = 0
                elif Cmax == R:
                    H = (60 * ((G - B) / delta) + 360) % 360
                elif Cmax == G:
                    H = (60 * ((B - R) / delta) + 120) % 360
                else:  # Cmax == B
                    H = (60 * ((R - G) / delta) + 240) % 360

                # Saturation calculation
                S = 0 if Cmax == 0 else (delta / Cmax)

                # Value calculation
                V = Cmax

                hsv_image[i, j] = [int(H / 2), int(S * 255), int(V * 255)]

        self.image = hsv_image
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='RGB to HSV - Comparatif')
            except Exception:
                pass
        return True
    
    def RGB_to_HSV_opencv(self):
        if self.image is None:
            return False

        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.image = hsv_image
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='RGB to HSV OpenCV - Comparatif')
            except Exception:
                pass
        return True
    #///////////////////////////////////////////////////////////////////////////////////////////////////////////
    def RGB_to_YCbCr(self):
        if self.image is None:
            return False

        h, w = self.image.shape[:2]
        ycbcr_image = np.zeros((h, w, 3), dtype=np.uint8)

        for i in range(h):
            for j in range(w):
                R, G, B = self.image[i, j]
                Y  = 0.299 * R + 0.587 * G + 0.114 * B
                Cb = 128 - 0.168736 * R - 0.331264 * G + 0.5 * B
                Cr = 128 + 0.5 * R - 0.460525 * G - 0.081975 * B
                ycbcr_image[i, j] = [int(Y), int(Cb), int(Cr)]

        self.image = ycbcr_image
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='RGB to YCbCr - Comparatif')
            except Exception:
                pass
        return True
    def RGB_to_YCbCr_opencv(self):
        if self.image is None:
            return False

        ycbcr_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2YCrCb)
        self.image = ycbcr_image
        if self.show_windows:
            try:
                self.afficher_comparatif_standard(opencv_image=None, titre='RGB to YCbCr OpenCV - Comparatif')
            except Exception:
                pass
        return True
    