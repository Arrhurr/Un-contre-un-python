import arcade
import os


class personnages(arcade.Sprite):

    def __init__(self, x:int, y:int, nom:str):
        super().__init__()
        self.nom = nom
        if nom.startswith("noita") or nom.startswith("lorem"):
            self.multiplier = 0.75 # baisser la range
        else:
            self.multiplier = 1 # basé sur le amongus
        self.pv = 100
        self.center_x = x
        self.center_y = y
        self.state = 0 # touchable ou pas 
        self.direction = 0 # droite = 0, gauche = 1
        self.time=0
        self.start_animation=0
        self.hadoken_cooldown = 0

        personnages_sprites = self.charger_les_srites()

        self.sprites = personnages_sprites[nom]
        self.texture = self.sprites["static"][0]
        self.animation_name = "static" #défini le sprite de quand le personnage apparaît

        tout_les_sons = self.charger_les_sons()
        for nom_son, sons in tout_les_sons.items():
            if nom.startswith(nom_son):
                self.son = sons
        
        self.victoires = 0
        self.vitesse = 7
        self.anip_x=x #cette variable prend la position du début du sprites
        self.liste_dep=[100] #met un nombre dans la liste pour la ligne 87, la liste dep garde les déplacement des personnages


    def update_animation(self,x1:int,x2:int,time:float,anim=None):
        """fonction qui change le sprite actuel et change la direction du personnage"""
        #changer les animations
        self.time = time #met à jour le temps avec le temps de la fenêtre
        self.liste_dep.append(x1) #rajoute la nouvelle position du personnage
        if x1 - x2 > 0:
            self.direction = 1 #le personage regarde à gauche
        elif x1 - x2 <= 0:
            self.direction = 0 #le personnage regarde à droite

        if anim == "coup1" and (self.time - self.start_animation >= 0.4 or self.start_animation == 0):#verifie quel anim est choisi
            self.texture = self.sprites["coup1"][self.direction]
            self.start_animation = time #la variable self_start_animation prend le début de l'animation pour vérifier le temps de recharges des attaques
            self.animation_name = anim #la variable qui garde le nom du sprite en cours
        elif self.animation_name == "coup1" and self.time- self.start_animation >= 0.05:#vérifie si le temps est assez avancer pour changer le sprite et avancer l'animation
            self.texture = self.sprites["coup2"][self.direction]
            self.start_animation = time
            self.animation_name = "coup2"
        elif self.animation_name == "coup2" and self.time - self.start_animation >=0.05: #même que au dessus
            self.texture = self.sprites["coup3"][self.direction]
            self.animation_name = "coup3"

        if anim == "tir1" and (self.time - self.start_animation >= 0.4 or self.start_animation == 0):
            self.texture = self.sprites["tir1"][self.direction]
            self.start_animation = time
            self.animation_name = anim
        elif self.animation_name == "tir1" and self.time- self.start_animation >= 0.05:
            self.texture = self.sprites["tir2"][self.direction]
            self.start_animation = time
            self.animation_name = "tir2"
        elif self.animation_name == "tir2" and self.time - self.start_animation >=0.075:
            self.texture = self.sprites["tir3"][self.direction]
            self.animation_name = "tir3"
            self.start_animation = time
        elif self.animation_name == "tir3" and self.time - self.start_animation >=0.075:#seul changement que au dessus sauf que il y a un sprite de plus
            self.texture = self.sprites["tir4"][self.direction]
            self.animation_name = "tir4"

        elif anim == "victoire": #si le personnage a gagné l'animation restera celle de la victoire
            self.texture = self.sprites["victoire"][self.direction]
            self.animation_name = "victoire"

        elif anim == "mort": #même que au dessus mais pour la défaite
            self.texture = self.sprites["mort"][self.direction]
            self.animation_name = "mort"

        elif self.time - self.start_animation >= 0.15 or self.start_animation == 0:#verifie que le temps de l'animation des coups est terminé
            if self.liste_dep[-1] == self.liste_dep[-2]: #verifie les 2 dernières position pour voir si il y a eu un déplacement
                self.texture = self.sprites["static"][self.direction]
                self.animation_name = "static"
                self.anip_x=x1
            else:
                if ((x1-self.anip_x <= -50 or x1-self.anip_x >= 50) and self.animation_name=="static") or ((x1-self.anip_x <= -50 or x1-self.anip_x >= 50) and self.animation_name=="courir3") or self.animation_name == "coup3" or self.animation_name == "tir4": #verifie quand il y a un mouvement si l'animation du coup ou du tir est fini, si l'animation vient de finir la boucle des 3 sprties ou si le sprite était immobile
                    self.texture = self.sprites["courir1"][self.direction]
                    self.animation_name="courir1"
                elif (x1-self.anip_x <= -50 or x1-self.anip_x >= 50) and self.animation_name == "courir1":#fait avancer la boucle de la course après qu'une distance est été traversé
                    self.texture = self.sprites["courir2"][self.direction]
                    self.animation_name = "courir2"
                    self.anip_x = x1 
                elif (x1-self.anip_x <= -50 or x1-self.anip_x >= 50) and self.animation_name == "courir2":#même que au dessus
                    self.texture = self.sprites["courir3"][self.direction]
                    self.animation_name= "courir3"
                    self.anip_x=x1

    def update_informations(self):
        """fonction qui change l'état du personnage"""
        if self.state > 0: #réduit le temps du temps d'invinsibilité
            self.state -= 1

        if self.hadoken_cooldown > 0:
            self.hadoken_cooldown -= 1

    def touche(self, taille:int):
        """gère le kb et le fait de ne pas sortir de l'ecran avec le kb"""
        self.center_y = 40 + self.center_y
        self.center_x = self.center_x + 100 * self.direction - 50
        if self.center_x < 50:
            self.center_x = 50
        elif self.center_x > taille - 75:
            self.center_x = taille -  75

    def charger_les_srites(self):
        actual_path = os.getcwd()
        os.chdir("./sprite/personnages")
        all_sprites = {} 
        all_sprites_dir = os.listdir()
        for dir in all_sprites_dir:
            os.chdir("./"+dir)
            dic = {}
            for file in os.listdir(): # -4 enleve le n.png (le n est necessaire sinon arcade fait une collision des données)
                dic[file[:-5]] = [arcade.load_texture("./"+file), arcade.load_texture("./"+file, flipped_horizontally=True)]
            os.chdir("..")
            all_sprites[dir] = dic
        os.chdir(actual_path)
        return all_sprites
    
    def charger_les_sons(self):
        actual_path = os.getcwd()
        os.chdir("./sprite/sons")
        all_sounds = {}
        scandir = os.listdir()
        all_sounds_dir = []
        for dir in scandir:
            if not "." in dir:
                all_sounds_dir.append(dir)
        for dir in all_sounds_dir:
            os.chdir("./"+dir)
            dic = {}
            for file in os.listdir(): # -4 enleve le n.png (le n est necessaire sinon arcade fait une collision des données)
                dic[file[:-5]] = arcade.load_sound("./"+file)
            os.chdir("..")
            all_sounds[dir] = dic
        os.chdir(actual_path)
        return all_sounds



class attaque(arcade.Sprite):
    """class qui lance une attaque invisible (pour utiliser la hitbox)"""
    def __init__(self, x:int, y:int, joueur:personnages, sprite=None, mouvement=0, multi=1):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.joueur = joueur
        self.mouvement = mouvement
        self.multi = multi
        if sprite == None:
            self.texture = arcade.load_texture("./sprite/menu/vide.png", hit_box_algorithm = "None")
            self.type = "coup de poing"
        else:
            self.type = "hadoken"
            self.texture = sprite
