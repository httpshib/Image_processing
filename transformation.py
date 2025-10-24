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
    def restaurer_original(self):
        if self.original_image is None:
            return False
        self.image = self.original_image.copy()
        return True
    '''
    def rotation_manuelle(self, angle,center):
        if self.image is None:
            return False
        
        (h, w) = self.image.shape[:2]
        #center = (w // 2, h // 2)
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
        return True'''
    def rotation_manuelle_mapping(self, angle):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        cx, cy = w // 2, h // 2
        #cx , cy = centre[0],centre[1]
        rotated = np.zeros_like(self.image)
        theta = np.radians(-angle)
        cos_t = np.cos(theta)
        sin_t = np.sin(theta)
        # inverse mapping : pour chaque pixel destination, trouver la source
        for x in range(h):
            for y in range(w):
                #xd = j
                #yd = i
                xs = int(round(cx + cos_t * (y - cx) + sin_t * (x - cy)))
                ys =int(round( cy - sin_t * (y - cx) + cos_t * (x- cy)))
                
                #xs_i = int(round(xs))
                #ys_i = int(round(ys))
                # vérification des limites et assignation des pixels
                if 0 <= xs < w and 0 <= ys < h:
                    rotated[x, y] = self.image[ys, xs]
        self.image = rotated
        return True
    def rotation_opencv(self,angle):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.last_comparatif = cv2.warpAffine(self.image, M, (w, h))
        return True
    #///////////////////////////////////////////////////////////////////////////////////////////
    '''def homothétie_opencv(self, scale_x, scale_y):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        # Matrice de transformation pour l'homothétie
        M = np.array([[scale_x, 0, 0],[0, scale_y, 0]])
        new_w = int(w * scale_x)
        new_h = int(h * scale_y)
        self.last_comparatif = cv2.warpAffine(self.image, M, (new_w, new_h))
        return True'''
  
    def homothétie_opencv(self, Lambda ):
        if self.image is None:
            return False
        lambda_x,lambda_y = Lambda[0],Lambda[1]
        # utiliser l'original pour le comparatif si disponible (ne pas écraser self.image)
        src = self.original_image if self.original_image is not None else self.image
        (h, w) = src.shape[:2]
        # calcler la nouvelle taille
        new_w = int(w * lambda_x)
        new_h = int(h * lambda_y)
        #new_w = max(1, int(round(w * float(lambda_x))))
        #new_h = max(1, int(round(h * float(lambda_y))))
        # choisir l'interpolation adaptée
        interp = cv2.INTER_LINEAR if (new_w > w or new_h > h) else cv2.INTER_AREA
        self.last_comparatif = cv2.resize(src, (new_w, new_h), interpolation=interp)
        return True

    #///////////////////////////////////////////////////////////////////////////////////////////
    def homothétie_manuelle_mapping(self, Lambda):
        if self.image is None:
            return False
        (h, w) = self.image.shape[:2]
        lambda_x, lambda_y = Lambda[0], Lambda[1]
        new_w = int(w * lambda_x)
        new_h = int(h * lambda_y)
        resized = np.zeros((new_h, new_w, self.image.shape[2]), dtype=self.image.dtype)
        for i in range(new_h):
            for j in range(new_w):
                src_x = int(j / lambda_x)
                src_y = int(i / lambda_y)
                if 0 <= src_x < w and 0 <= src_y < h:
                    resized[i, j] = self.image[src_y, src_x]
        self.image = resized
        return True
    #////////////////////////////////////////////////////////////////////////////////////////
    
    #/////////////////////////////////////////////////////////////////////////////////////////
 
    def afficher_comparatif(self, titre1="Image original", titre2="Image manuelle",titre3="image opencv"):
        if self.image is None or self.last_comparatif is None or self.original_image is None:
            return False
        if not self.show_windows:
            return True

        def ensure_color(img):
            if img is None:
                return None
            if len(img.shape) == 2:
                return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            return img

        def fit_to_frame(img, target_h, target_w):
            img = ensure_color(img)
            h, w = img.shape[:2]
            # si déjà la bonne taille
            if h == target_h and w == target_w:
                return img
            # si l'image est plus grande dans les deux dimensions -> crop centre (préserve le zoom)
            if h >= target_h and w >= target_w:
                start_y = (h - target_h) // 2
                start_x = (w - target_w) // 2
                return img[start_y:start_y + target_h, start_x:start_x + target_w]
            # sinon on redimensionne pour couvrir le cadre puis on crop centre (remplit le cadre)
            scale_h = target_h / h
            scale_w = target_w / w
            scale = max(scale_h, scale_w)
            new_w = max(1, int(round(w * scale)))
            new_h = max(1, int(round(h * scale)))
            interp = cv2.INTER_LINEAR if scale >= 1.0 else cv2.INTER_AREA
            resized = cv2.resize(img, (new_w, new_h), interpolation=interp)
            start_y = (new_h - target_h) // 2
            start_x = (new_w - target_w) // 2
            return resized[start_y:start_y + target_h, start_x:start_x + target_w]

        img1 = ensure_color(self.original_image)
        img2 = ensure_color(self.image)
        img3 = ensure_color(self.last_comparatif)

        target_h, target_w = img1.shape[:2]  # utiliser la taille de l'original comme cadre

        img1_f = fit_to_frame(img1, target_h, target_w)
        img2_f = fit_to_frame(img2, target_h, target_w)
        img3_f = fit_to_frame(img3, target_h, target_w)

        combined = np.hstack((img1_f, img2_f, img3_f))
        cv2.imshow(f"{titre1} | {titre2} | {titre3}", combined)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    
    '''

    def afficher_comparatif(self, titre1="Image original", titre2="Image manuelle",titre3="image opencv"):
        if self.image is None or self.last_comparatif is None:
            return False
        if not self.show_windows:
            return True
        combined = np.hstack((self.original_image, self.image, self.last_comparatif))
        cv2.imshow(f"{titre1} | {titre2} | {titre3}", combined)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True'''
    
    
def main():
    t = transformation()
    if not t.charger_image(r"C:\Users\DELL\Downloads\exemple.png"):
        print("Échec du chargement de l'image")
        return
    t.show_windows = True
    #t.afficher_image("Image Originale")
    # appliquer rotation sur la même instance (ne PAS recréer t)
    #===================================test rotation=========================================
    t.rotation_opencv(90)
    t.rotation_manuelle_mapping(90)
    t.afficher_comparatif()
    t.restaurer_original()
    #===================================test homothétie=========================================
    t.homothétie_opencv([5,5])
    t.homothétie_manuelle_mapping([5, 5])
    t.afficher_comparatif("Image Originale","Image homothétie manuelle","Image homothétie opencv")
    
    #t.rotation_manuelle(90)
    #t.afficher_image("Image après rotation manuelle de 90 degrés")
    #t.rotation_manuelle_mapping(-90)
    #t.rotation_manuelle(-90)
    #t.afficher_image("Inverse rotation manuelle de -90 degrés")
    
    #image=t.ima

if __name__ == "__main__":
    main()