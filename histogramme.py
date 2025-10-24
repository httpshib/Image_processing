import cv2
import numpy as np
import os


class Histogramme:
    
    def __init__(self):
        self.image = None
        self.original_image = None
        self.image_path = None
        self.histogramme_manuel = None
        self.histogramme_opencv = None
        
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
    
    def a_image(self):
        return self.image is not None
    
    def restaurer_original(self):
        if self.original_image is None:
            return False
        self.image = self.original_image.copy()
        return True
    
    
    def calculer_histogramme_manuel(self):
       
        if self.image is None:
            return None
        
        h, w = self.image.shape[:2]
        
        # Initialiser les histogrammes pour chaque canal (256 niveaux)
        hist_b = np.zeros(256, dtype=np.int32)
        hist_g = np.zeros(256, dtype=np.int32)
        hist_r = np.zeros(256, dtype=np.int32)
        
        # Parcourir tous les pixels
        for i in range(h):
            for j in range(w):
                b, g, r = self.image[i, j]
                hist_b[b] += 1
                hist_g[g] += 1
                hist_r[r] += 1
        
        self.histogramme_manuel = {
            'blue': hist_b,
            'green': hist_g,
            'red': hist_r
        }
        
        return self.histogramme_manuel
    
    def calculer_histogramme_gris_manuel(self):
       
        if self.image is None:
            return None
        
        # Convertir en niveaux de gris d'abord
        h, w = self.image.shape[:2]
        image_gris = np.zeros((h, w), dtype=np.uint8)
        
        for i in range(h):
            for j in range(w):
                b, g, r = self.image[i, j]
                gris = int(0.299 * r + 0.587 * g + 0.114 * b)
                image_gris[i, j] = gris
        
        # Calculer l'histogramme
        hist = np.zeros(256, dtype=np.int32)
        for i in range(h):
            for j in range(w):
                hist[image_gris[i, j]] += 1
        
        self.histogramme_manuel = {'gray': hist}
        return self.histogramme_manuel
    
    
    
    def calculer_histogramme_opencv(self):
      
        if self.image is None:
            return None
        
        # Séparer les canaux
        canaux = cv2.split(self.image)
        
        # Calculer l'histogramme pour chaque canal
        hist_b = cv2.calcHist([canaux[0]], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([canaux[1]], [0], None, [256], [0, 256])
        hist_r = cv2.calcHist([canaux[2]], [0], None, [256], [0, 256])
        
        # Aplatir les résultats (OpenCV retourne des tableaux 2D)
        self.histogramme_opencv = {
            'blue': hist_b.flatten().astype(np.int32),
            'green': hist_g.flatten().astype(np.int32),
            'red': hist_r.flatten().astype(np.int32)
        }
        
        return self.histogramme_opencv
    
    def calculer_histogramme_gris_opencv(self):
      
        if self.image is None:
            return None
        
        # Convertir en niveaux de gris
        image_gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        # Calculer l'histogramme
        hist = cv2.calcHist([image_gris], [0], None, [256], [0, 256])
        
        self.histogramme_opencv = {'gray': hist.flatten().astype(np.int32)}
        return self.histogramme_opencv
    
    def calculer_histogramme_cumule_manuel(self):
       
        if self.image is None:
            return None
        
        hist_manuel = self.calculer_histogramme_manuel()
        if hist_manuel is None:
            return None
        
        hist_cumule = {}
        
        for canal in hist_manuel.keys():
            hist = hist_manuel[canal]
            hist_cum = np.zeros(256, dtype=np.int32)
            hist_cum[0] = hist[0]
            for i in range(1, 256):
                hist_cum[i] = hist_cum[i-1] + hist[i]
            hist_cumule[canal] = hist_cum
        
        return hist_cumule
    
    def egaliser_histogramme_manuel(self):
      
        if self.image is None:
            return None
        
        h, w = self.image.shape[:2]
        image_egalisee = np.zeros_like(self.image)
        
        # Pour chaque canal
        for canal in range(3):
            # Calculer l'histogramme
            hist = np.zeros(256, dtype=np.int32)
            for i in range(h):
                for j in range(w):
                    hist[self.image[i, j, canal]] += 1
            
            # Calculer l'histogramme cumulé
            hist_cum = np.zeros(256, dtype=np.int32)
            hist_cum[0] = hist[0]
            for i in range(1, 256):
                hist_cum[i] = hist_cum[i-1] + hist[i]
            
            # Normaliser
            hist_cum_norm = (hist_cum * 255) / (h * w)
            
            # Appliquer la transformation
            for i in range(h):
                for j in range(w):
                    image_egalisee[i, j, canal] = int(hist_cum_norm[self.image[i, j, canal]])
        
        return image_egalisee
    
    def egaliser_histogramme_opencv(self):
       
        if self.image is None:
            return None
        
        # Séparer les canaux
        canaux = cv2.split(self.image)
        
        # Égaliser chaque canal
        canaux_egalisees = []
        for canal in canaux:
            canal_egalise = cv2.equalizeHist(canal)
            canaux_egalisees.append(canal_egalise)
        
        # Fusionner les canaux
        image_egalisee = cv2.merge(canaux_egalisees)
        
        return image_egalisee
    
    
    '''
    def etirer_histogramme_manuel(self):
       
        if self.image is None:
            return None
        
        h, w = self.image.shape[:2]
        image_etiree = np.zeros_like(self.image)
        
        # Pour chaque canal
        for canal in range(3):
            # Trouver min et max
            min_val = 255
            max_val = 0
            
            for i in range(h):
                for j in range(w):
                    pixel = self.image[i, j, canal]
                    if pixel < min_val:
                        min_val = pixel
                    if pixel > max_val:
                        max_val = pixel
            
            # Appliquer l'étirement
            if max_val != min_val:
                for i in range(h):
                    for j in range(w):
                        pixel = self.image[i, j, canal]
                        nouveau_pixel = int(((pixel - min_val) * 255) / (max_val - min_val))
                        image_etiree[i, j, canal] = nouveau_pixel
            else:
                image_etiree[:, :, canal] = self.image[:, :, canal]
        
        return image_etiree
    
    def etirer_histogramme_opencv(self):
       
        if self.image is None:
            return None
        
        image_etiree = np.zeros_like(self.image)
        
        # Pour chaque canal
        for canal in range(3):
            cv2.normalize(
                self.image[:, :, canal],
                image_etiree[:, :, canal],
                0, 255,
                cv2.NORM_MINMAX
            )
        
        return image_etiree
    
    
    
    def comparer_histogrammes(self, hist1, hist2):
        """
        Compare deux histogrammes et calcule la différence
        Retourne un score de similarité (0 = identique)
        """
        if hist1 is None or hist2 is None:
            return None
        
        # Calculer la différence absolue moyenne
        diff = 0
        for key in hist1.keys():
            diff += np.sum(np.abs(hist1[key] - hist2[key]))
        
        return diff
    
    def sauvegarder_image(self, chemin, image=None):
        """Sauvegarde une image"""
        if image is None:
            image = self.image
        if image is None:
            return False
        return cv2.imwrite(chemin, image)
    
    def obtenir_statistiques_histogramme(self, hist_data):
        """
        Calcule les statistiques d'un histogramme
        Retourne: moyenne, écart-type, médiane
        """
        if hist_data is None:
            return None
        
        stats = {}
        
        for canal, hist in hist_data.items():
            # Calculer la moyenne pondérée
            total_pixels = np.sum(hist)
            if total_pixels == 0:
                stats[canal] = {'moyenne': 0, 'ecart_type': 0, 'mediane': 0}
                continue
            
            moyenne = np.sum([i * hist[i] for i in range(256)]) / total_pixels
            
            # Calculer l'écart-type
            variance = np.sum([hist[i] * ((i - moyenne) ** 2) for i in range(256)]) / total_pixels
            ecart_type = np.sqrt(variance)
            
            # Calculer la médiane
            cumul = 0
            mediane = 0
            for i in range(256):
                cumul += hist[i]
                if cumul >= total_pixels / 2:
                    mediane = i
                    break
            
            stats[canal] = {
                'moyenne': round(moyenne, 2),
                'ecart_type': round(ecart_type, 2),
                'mediane': mediane
            }
        
        return stats '''