import cv2 
import numpy as np
import os
import conversion

class transformation:
    def  __init__(self):
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
    def rotation_manuelle(self, angle):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        # creatiom de la nouvelle image vide
        rotated = np.zeros_like(self.image)
        for i in range(h):
            for j in range(w):
                # coordonnées relatives au centre
                y = i - center[1]
                x = j - center[0]
                # application de la rotation
                new_x = center[0]+int(x * np.cos(np.radians(angle)) - y * np.sin(np.radians(angle)))
                new_y = center[1]+int(x * np.sin(np.radians(angle)) + y * np.cos(np.radians(angle)))
               
                # vérification des limites et assignation des pixels
                if 0 <= new_x < w and 0 <= new_y < h:
                    rotated[new_y, new_x] = self.image[i, j]
        self.image = rotated
        return True
    def rotation_manuelle_mapping(self, angle):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        cx, cy = w // 2, h // 2
        rotated = np.zeros_like(self.image)
        theta = np.radians(angle)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        # inverse mapping : pour chaque pixel destination, trouver la source
        for i in range(h):
            for j in range(w):
                xd = j
                yd = i
                xs = cx + cos_t * (xd - cx) + sin_t * (yd - cy)
                ys = cy - sin_t * (xd - cx) + cos_t * (yd - cy)
                xs_i = int(round(xs))
                ys_i = int(round(ys))
                if 0 <= xs_i < w and 0 <= ys_i < h:
                    rotated[i, j] = self.image[ys_i, xs_i]
        self.image = rotated
        return True
    def rotation_opencv(self,angle):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(self.image, M, (w, h))
        self.image = rotated
        return True
def main():
    t = transformation()
    if not t.charger_image(r"C:\Users\DELL\Downloads\exemple.png"):
        print("Échec du chargement de l'image")
        return
    t.show_windows = True
    t.afficher_image("Image Originale")
    # appliquer rotation sur la même instance (ne PAS recréer t)
    t.rotation_manuelle_mapping(90)
    #t.rotation_manuelle(90)
    t.afficher_image("Image après rotation manuelle de 90 degrés")
    t.rotation_manuelle_mapping(-90)
    #t.rotation_manuelle(-90)
    t.afficher_image("Inverse rotation manuelle de -90 degrés")

    #image=t.ima

if __name__ == "__main__":
    main()