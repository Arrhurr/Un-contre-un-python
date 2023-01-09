import arcade
from class_main import main
from random import *

class menu(arcade.View):
    """ View to show instructions """

    def on_show(self):

        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)
        #On commence par charger toutes les images dont le menu aura besoin
        self.background = arcade.load_texture("./sprite/menu/menu_beta4_1.jpg")
        self.cursor1=arcade.load_texture("./sprite/menu/cursor_1.png")
        self.cursor2=arcade.load_texture("./sprite/menu/cursor_2.png")
        self.amongus=arcade.load_texture("./sprite/personnages/amongus/static0.png")
        self.amongus2=arcade.load_texture("./sprite/personnages/amongus2/static1.png")
        self.lorem=arcade.load_texture("./sprite/personnages/lorem/static2.png")
        self.lorem2=arcade.load_texture("./sprite/personnages/lorem2/static3.png")
        self.noita=arcade.load_texture("./sprite/personnages/noita/static4.png")
        self.noita2=arcade.load_texture("./sprite/personnages/noita2/static5.png")
        self.hasard=arcade.load_texture("./sprite/menu/random.png")
        self.musique = arcade.load_sound("./sprite/menu/main_theme.mp3")
        self.changement = arcade.load_sound("./sprite/menu/changement.mp3")

        #On lance la musique et on la boucle 
        self.musicien = self.musique.play(loop=True)
        self.posX=[190,690] #on forme une liste composé des positions en abscisse des curseurs du joueur 1 et 2
        self.posY=[520,520] #on forme une liste composé des positions en ordonné des curseurs du joueur 1 et 2
        self.picture_player=[1,1] #Liste qui prend en compte l'image des personnages selectionnés par les joueurs
        self.state=[0,0] #A quelle phase du menu se trouvent les joueurs 0 -> phase de séléction
        self.choice=[None,None] #Le choix des arènes de chaque joueurs est défini
        self.character=[None,None] #Le choix des personnages de chaque joueur est défini
        self.texte=["","Among us","Aleatoire","Lorem","Noita"]#on créé une liste avec les nom des personnages, qui changera en fonction de quel image doit apparaître

    def choix(self,choix_1,choix_2):
        back=choice([choix_1,choix_2]) #Le jeu choisit aléatoirement entre les deux terrains choisis par les joueurs
        if self.character[0]==self.character[1]: #Si les deux joueurs ont choisi les mêmes personnages un des deux joueurs prendra le sprite alternatif
            a=randint(0,1)
            self.character[a]=self.character[a]+"2"
        self.go_on(self.character[0],self.character[1],back) #Le jeu est lancé

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1000, 650, self.background)
        arcade.draw_lrwh_rectangle_textured(self.posX[1], self.posY[1], 130 + 155*(self.posY[1]//300), 55, self.cursor1) #Dessine le curseur 1 pour le joueur 2
        arcade.draw_lrwh_rectangle_textured(self.posX[0], self.posY[0], 130 + 155*(self.posY[0]//300), 55, self.cursor2) #Dessine le curseur 2 pour le joueur 1
        arcade.draw_lrwh_rectangle_textured(10, 370, 160, 160, self.appear_picture(self.picture_player[0], 1)) #Dessine l'image du personnage sélectionné par le joueur 1
        arcade.draw_lrwh_rectangle_textured(500, 370, 160, 160, self.appear_picture(self.picture_player[1], 2)) #Dessine l'image du personnage sélectionné par le joueur 2
        arcade.draw_text(self.texte[self.picture_player[1]*(self.posY[1]//300)],self.posX[1]+35,self.posY[1]+15,arcade.color.BLACK,35,font_name="Kenney Mini Square")#dessine le texte qui apparaît pour le personnage choisi pour le joueur 2
        arcade.draw_text(self.texte[self.picture_player[0]*(self.posY[0]//300)],self.posX[0]+35,self.posY[0]+15,arcade.color.BLACK,35,font_name="Kenney Mini Square")#dessine le texte qui apparaît pour le personnage choisi pour le joueur 1

    def action(self,chara):
        if self.state[chara]==0: #Si le joueur est a la phase de seletion de personnage
            if self.posY[chara]==520:
                self.character[chara]="amongus"
            elif self.posY[chara]==450:
                self.character[chara]="noita"
            elif self.posY[chara]==380:
                self.character[chara]="lorem"
            else:
                self.character[chara]=choice(["amongus","noita","lorem"]) #Si le joueur séléctionne l'aléatoire, il obtient un personnage radnom entre les 3
            self.state[chara]=1 #On passe le joueur de la phase de séléction d'arène
            self.posY[chara]=200 #On change la position du curseur
            self.posX[chara]=37
        #Selection d'arene
        elif self.state[chara]==1:
            if self.posX[chara]==822:
                self.choice[chara]="./sprite/background/896/backfnaf.jpg"
            elif self.posX[chara]==665:
                self.choice[chara]="./sprite/background/896/backpetscop.jpg"
            elif self.posX[chara]==508:
                self.choice[chara]="./sprite/background/896/backnsi.jpg"
            elif self.posX[chara]==351:
                self.choice[chara]="./sprite/background/896/backwindow_2.jpg"
            elif self.posX[chara]==194:
                self.choice[chara]="./sprite/background/896/backnoita.jpg"
            else:
                self.choice[chara]="./sprite/background/896/backamong.jpg"
            self.state[chara]=2 #Le joueur est prêt à se battre

        #Si les deux joueurs sont prêt et que l'un d'eux appuient sur entrée
        elif self.state[0]==2 and self.state[1]==2:
            self.choix(self.choice[0],self.choice[1])
            
    def tuchy(self,chara,dir):
        #Si un joueur va vers le bas
        if dir=="DOWN":
            if self.posY[chara]>320: #Si le curseur n'est pas trop bas
                self.posY[chara]=self.posY[chara]-70 #Change la pos du curseur
                self.changement.play() #bruitage se joue
            else:
                self.posY[chara]=520 #Le replacer en haut sinon
                self.changement.play()#bruitage se joue
            if self.picture_player[chara]!=1: #Change l'image qui doit appraître
                self.picture_player[chara]=self.picture_player[chara]-1
            else:
                self.picture_player[chara]=4
        #Si un joueur va vers le haut
        elif dir=="UP":
            if self.posY[chara]<460: #Si le curseur n'est pas trop haut
                self.posY[chara]=self.posY[chara]+70 #Change la pos du curseur
                self.changement.play()#bruitage se joue
            else:
                self.posY[chara]=310 #Sinon le replacer
                self.changement.play()
            if self.picture_player[chara]!=4:#Change l'image qui doit appraître
                self.picture_player[chara]=self.picture_player[chara]+1
            else:
                self.picture_player[chara]=1
        elif dir=="LEFT" and self.posX[chara]>39: 
            self.posX[chara]=self.posX[chara]-157 #Deplace le curseur a gauche
            self.changement.play()
        elif dir=="RIGHT" and self.posX[chara]<800:
            self.posX[chara]=self.posX[chara]+157 #Deplace le curseur a droite
            self.changement.play()
            
    def back(self,chara):
        if self.state[chara]==1: #Mettre le joeueur a l'étape 0 si il est à l'étape 1 et replacer le curseur et l'image dans la bonne position
            self.state[chara]=0
            if chara == 0:
                self.posX[chara]=190
            else:
                self.posX[chara]=690
            self.posY[chara]=520
            self.picture_player[chara]=1
        if self.state[chara]==2: #Mettre le joeueur a l'étape 1 si il est à l'étape 2 et le replacer correctement
            self.state[chara]=1
            self.posY[chara]=200
            self.posX[chara]=37
        
        
        
    
    def on_key_press(self, key, modifiers):
        #Le joueur 1 est au stade de choix de personnage
        if self.state[0]==0:
            #Touche du bas joueur 1
            if key == arcade.key.S:
                self.tuchy(0,"DOWN")
             #Touche du haut joueur 1
            if key == arcade.key.Z:
                self.tuchy(0,"UP")
                    
        #Le joueur 1 est au stade de choix d'arene
        elif self.state[0]==1:
            if key == arcade.key.Q:
                self.tuchy(0,"LEFT")
            if key == arcade.key.D:
                self.tuchy(0,"RIGHT")
            
        #Le joueur 2 est au stade de choix d'arene
        if self.state[1]==1:
            if key == arcade.key.LEFT:
                self.tuchy(1,"LEFT")
            if key == arcade.key.RIGHT:
                self.tuchy(1,"RIGHT")
                    
        #Le joueur 2 est au stade de choix de personnage
        elif self.state[1]==0:
            #Touche du bas joueur 2
            if key == arcade.key.DOWN:
                self.tuchy(1,"DOWN")
            #Touche du haut joueur 2
            if key == arcade.key.UP:
                self.tuchy(1,"UP")
                    
        # Retour arriere pour le joueur 2
        if key == arcade.key.NUM_2:
            self.changement.play()
            self.back(1)
        
        #Entree pour le joueur 2
        if key == arcade.key.NUM_1:
            self.changement.play()
            self.action(1)
                
        #Entree pour le joueur 1
        if key == arcade.key.ENTER:
            self.changement.play()
            self.action(0)
        # Retour arriere pour le joueur 1
        if key == arcade.key.BACKSPACE:
            self.changement.play()
            self.back(0)
        
    def appear_picture(self,number, player):
        """Definit l'image du personnage selectionné par les joueurs """
        same_choice = False
        if player == 2 and number == self.picture_player[0]:# les 2 ont fait le meme choix
            same_choice = True
        if number==1:
            if same_choice:
                return self.amongus2
            return self.amongus
        elif number==4:
            if same_choice:
                return self.noita2
            return self.noita
        elif number==3:
            if same_choice:
                return self.lorem2
            return self.lorem
        else:
            return self.hasard

    def go_on(self,chara1,chara2,back):
        #Lance le jeu
        self.musicien.pause() #La musique du menu s'arrête
        arcade.close_window() #On ferme la fenêtre du menu
        window = main(perso1=chara1,perso2=chara2,back=back) #La fenêtre de jeu est crée
        window.setup()
        arcade.run()

if __name__ == "__main__": #On crée la fenêtre du menu
    window = arcade.Window(1000, 650, "baTaiLle dE rUE")
    start_view = menu()
    window.show_view(start_view)
    arcade.run()


quit() # pour bien fermer le jeu
    
