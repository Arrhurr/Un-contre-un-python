from personnages import personnages, attaque
import arcade
from random import randint
#arcade.Window.set_icon

class main(arcade.Window):
    def __init__(self, perso1="amongus", perso2="lorem", back="./sprite/background/896/background1.jpg"):
        super().__init__(1000, 650,"BaTaiLLe dE rUE", fullscreen = False) 
        self.perso1 = perso1
        self.perso2 = perso2
        self.back = back

    def setup(self):
        """Initilaisation du jeu"""

        self.time=0

        self.keylist = []

        self.attaques = []

         # Set up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Initialize Scene
        self.scene = arcade.Scene()
        
        self.gagnant = None

        self.player1 = personnages(50, 100 , self.perso1)
        self.scene.add_sprite("1", self.player1)


        self.player2 = personnages(self.width - 100, 100, self.perso2)
        self.scene.add_sprite("1", self.player2)

        

        # choix de la carte
        self.background = arcade.load_texture(self.back)
        
        self.pointeur1 = arcade.load_texture("./sprite/pointeur/pointeur1.png")
        self.pointeur2 = arcade.load_texture("./sprite/pointeur/pointeur2.png")

        
        for x in range(0, self.width, 10):# création du sol
            wall = arcade.Sprite("./sprite/menu/vide.png", 1, hit_box_algorithm = "None") # texture vide
            wall.center_x = x
            wall.center_y = 50
            self.scene.add_sprite("Walls", wall) # ajout des collisions
        
        for i in range(2):# création des bords
            for y in range(0, self.height, 10):
                wall = arcade.Sprite("./sprite/menu/vide.png", 1, hit_box_algorithm = "None") # texture vide
                wall.center_x = 45 + (self.width - 2*45)*i
                wall.center_y = y
                self.scene.add_sprite("Walls", wall) # ajout des collisions
                
        # musiques
        musiques = ["./sprite/musiques/deja_vu.mp3", "./sprite/musiques/runing_int_the_90s.mp3"] # choix de la musique
        musique = arcade.load_sound(musiques[randint(0, 1)])
        musique.play(loop=True, volume=0.1) # lancement de la musique a volume réduit
        

        

        # Création des colisions, de la gravité et des colisions
        self.physics_engine1 = arcade.PhysicsEnginePlatformer(self.player1, gravity_constant=1, walls=self.scene["Walls"])

        self.physics_engine2 = arcade.PhysicsEnginePlatformer(self.player2, gravity_constant=1, walls=self.scene["Walls"])
        
    
    def on_draw(self):
        """Fonction appelé à chaque """
        self.clear() # effacer la scene précédente


        self.camera.use()

        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background) # afficher le fond

        self.scene.draw()

        # afficher la vie
        arcade.draw_rectangle_filled(self.width/6 + 25, self.height*29/30 - 25, self.width/3, self.height/15, arcade.color.ALIZARIN_CRIMSON)
        arcade.draw_rectangle_filled(self.width/6 + 25 - self.width/6*((100-self.player1.pv)/100), self.height*29/30 - 25, (self.width/3)*(self.player1.pv/100), self.height/15, (10, 232, 4))


        arcade.draw_rectangle_filled(self.width*5/6 - 25, self.height*29/30 - 25, self.width/3, self.height/15, arcade.color.ALIZARIN_CRIMSON)
        arcade.draw_rectangle_filled(self.width*5/6 - 25 + self.width/6*((100-self.player2.pv)/100), self.height*29/30 - 25, self.width/3*(self.player2.pv/100), self.height/15, (10, 232, 4))


        #self.player1.draw_hit_box(arcade.color.RED, 3) # afficher la hitbox des persos
        #self.player2.draw_hit_box(arcade.color.RED, 3)
        
        #afficher le nom des personnages et les pointeurs
        arcade.draw_text("J1", self.player1.center_x - 5, self.player1.center_y + 100, arcade.color.BLUE, 20)
        arcade.draw_text("J2", self.player2.center_x - 25, self.player2.center_y + 100, arcade.color.RED, 20)
        
        arcade.draw_texture_rectangle(self.player1.center_x + 10, self.player1.center_y + 75, 50, 50, self.pointeur1)
        arcade.draw_texture_rectangle(self.player2.center_x - 10, self.player2.center_y + 75, 50, 50, self.pointeur2)
        
        
        if self.gagnant is not None:
            if self.gagnant == self.player1:
                #mettre l'anim de victoire pour le p1 et de défaite pour p2
                arcade.draw_text("J1 gagne la bAtaiLLe 2 rUe", 100, self.height/2, arcade.color.BLUE, 50)
                self.player1.update_animation(self.player1.center_x, self.player2.center_x, self.time, anim="victoire")
                self.player2.update_animation(self.player2.center_x, self.player1.center_x, self.time, anim="mort")
            else:
                #mettre l'anim victoire pour p2 et défate pour p1
                arcade.draw_text("J2 gagne la bAtaiLLe 2 rUe", 100, self.height/2, arcade.color.BLUE, 50)
                self.player2.update_animation(self.player1.center_x, self.player2.center_x, self.time, anim="victoire")
                self.player1.update_animation(self.player2.center_x, self.player1.center_x, self.time, anim="mort")   
        
        #afficher les hit box d'attaques
        #for attaque in self.attaques:
        #    attaque[0].draw_hit_box(arcade.color.RED, 3)



    def on_key_press(self, key, modifiers):
        """Appelé quand une touche est appuyée"""
        
        if self.gagnant is None: #tant qu'il n'y a pas de gagnant

            if key == arcade.key.Z: # sauter
                if self.physics_engine1.can_jump():
                    self.player1.change_y = 20
            
            if key == arcade.key.UP: # sauter
                if self.physics_engine2.can_jump():
                    self.player2.change_y = 20
    
            if key == arcade.key.Q: # gauche
                self.player1.change_x = -self.player1.vitesse
                self.keylist.append("q")
            if key == arcade.key.RIGHT: # droite
                self.player2.change_x = self.player2.vitesse
                self.keylist.append("right")
            if key == arcade.key.D: # droite
                self.player1.change_x = self.player1.vitesse
                self.keylist.append("d")
            if key == arcade.key.LEFT: # gauche
                self.player2.change_x = -self.player2.vitesse
                self.keylist.append("left")

            if key == arcade.key.G: # attaque au corps à corps
                if self.player1.time - self.player1.start_animation >= 0.4: # check le cooldown
                    self.player1.update_animation(self.player1.center_x, self.player2.center_x, self.time, anim="coup1")
                    self.attaques.append([attaque(self.player1.center_x + (-150 * self.player1.direction + 75)*self.player1.multiplier, self.player1.center_y, self.player1), 17, 10])
                    self.player1.son["bim"].play() # lance le son

            if key == arcade.key.NUM_1: # attaque au corpsà corps
                if self.player2.time - self.player2.start_animation >= 0.4:
                    self.player2.update_animation(self.player2.center_x, self.player1.center_x, self.time, anim="coup1")
                    self.attaques.append([attaque(self.player2.center_x + (-150 * self.player2.direction + 75)*self.player1.multiplier, self.player2.center_y, self.player2), 17, 10])
                    self.player2.son["bim"].play()

            if key == arcade.key.H: #attaque à distance
                if self.player1.hadoken_cooldown == 0:
                    self.player1.hadoken_cooldown = 120
                    self.attaques.append([attaque(self.player1.center_x - 200* self.player1.direction + 100, self.player1.center_y + 20, self.player1, sprite=self.player1.sprites["projectile"][self.player1.direction], mouvement=(-40)* self.player1.direction + 20, multi=self.player1.multiplier), 120, 12])
                    self.player1.update_animation(self.player1.center_x, self.player2.center_x, self.time, anim="tir1")


            
            if key == arcade.key.NUM_2: #attaque à distance
                if self.player2.hadoken_cooldown == 0:
                    self.player2.hadoken_cooldown = 120
                    self.attaques.append([attaque(self.player2.center_x - 200* self.player2.direction + 100, self.player2.center_y + 20, self.player2, sprite=self.player2.sprites["projectile"][self.player2.direction], mouvement=(-40)* self.player2.direction + 20, multi=self.player2.multiplier), 120, 12])
                    self.player2.update_animation(self.player2.center_x, self.player1.center_x, self.time, anim="tir1")
                    
            
    
    def on_key_release(self, key, modifiers):
        """Est appelé quand l'utilisateur relâche une touhce."""
        
        if self.gagnant is None: #tant qu'il n'y a pas de gagnant
        
            if key == arcade.key.Q:
                self.keylist.remove("q")
                if not "d" in self.keylist:
                    self.player1.change_x = 0
                else: # si il y a D pour empecher d'aaller dans la mauvaise direction
                    self.player1.change_x = self.player1.vitesse
            if key == arcade.key.RIGHT:
                self.keylist.remove("right")
                if not "left" in self.keylist:
                    self.player2.change_x = 0
                else:
                    self.player2.change_x = -self.player1.vitesse
            if key == arcade.key.D:
                self.keylist.remove("d")
                if not "q" in self.keylist:
                    self.player1.change_x = 0
                else:
                    self.player1.change_x = -self.player1.vitesse
            if key == arcade.key.LEFT:
                self.keylist.remove("left")
                if not "right" in self.keylist:
                    self.player2.change_x = 0
                else:
                    self.player2.change_x = self.player1.vitesse


    def on_update(self, delta_time):
        """Change les états des personnages et l'apparition et la disparition des sprites."""

        self.time=self.time+1/60
        # dans on_update car fonction plus constante que on_draw
        if self.gagnant is None:
            self.player1.update_animation(self.player1.center_x, self.player2.center_x, self.time)
            self.player2.update_animation(self.player2.center_x, self.player1.center_x, self.time)
        
        #check si il y a des morts
        if self.player1.pv <= 0:
            self.gagnant = self.player2
            self.player1.change_x = 0 # arreter les persos
            self.player2.change_x = 0
        elif self.player2.pv <= 0:
            self.gagnant = self.player1
            self.player1.change_x = 0
            self.player2.change_x = 0

        # change la position du joueur
        self.physics_engine1.update()
        self.physics_engine2.update()


        self.player1.update_informations()# gère l'invincibilitée après un coup
        self.player2.update_informations()
        
        # gere le moment d'apparition des sprites
        for attaque in self.attaques:
            if attaque[2] == 0:
                self.scene.add_sprite("oof1",attaque[0])
                if attaque[0].type == "hadoken":
                    attaque[0].joueur.son["piou"].play()
            elif attaque[2] > 0:
                attaque[0].center_y = attaque[0].joueur.center_y
                attaque[0].center_x = attaque[0].joueur.center_x - 200* attaque[0].joueur.direction + 100
            attaque[2] -= 1
        
        
        enlever = []
        for i in range(len(self.attaques)): # degats et colisions avec les balles/coups
            if self.attaques[i][2] < 0:
                if arcade.check_for_collision(self.player2, self.attaques[i][0]) and self.player2.state == 0 and self.attaques[i][0].joueur != self.player2: 
                        self.player2.pv -= 10
                        self.player2.state = 12
                        self.player2.touche(self.width)
                        self.player2.son["aie"].play() # son dégâts
                        enlever.append(i) # on enlève l'attaque de celles actuelles
                if arcade.check_for_collision(self.player1, self.attaques[i][0]) and self.player1.state == 0 and self.attaques[i][0].joueur != self.player1:
                        self.player1.pv -= 10
                        self.player1.state = 12
                        self.player1.touche(self.width)
                        self.player1.son["aie"].play()
                        enlever.append(i)
                
        for i in range(len(self.attaques)): # enlever l'attaque selon la durée
            if self.attaques[i][1] == 0 and not i in enlever:
                enlever.append(i)
            else:
                self.attaques[i][1] -= 1
                if self.attaques[i][0].type != "hadoken":
                    self.attaques[i][0].center_x = self.attaques[i][0].joueur.center_x + (-150 * self.attaques[i][0].joueur.direction + 75)*self.attaques[i][0].multi
                    self.attaques[i][0].center_y = self.attaques[i][0].joueur.center_y
                elif self.attaques[i][2] < 0:#bouger le hadoken
                    self.attaques[i][0].center_x += self.attaques[i][0].mouvement
                    
                    
        
        enlever = sorted(enlever, reverse=True) # enlever d'abord les plus grand pour eviter le out of range


        
        for i in enlever: # enlever les sprites a enlever
            self.attaques[i][0].kill()
            self.attaques.pop(i)
        

    


if __name__ == "__main__":
    window = main()
    window.setup()
    arcade.run()
    quit()


