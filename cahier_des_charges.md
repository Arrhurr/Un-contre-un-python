# Cahier des charges

## Fonctionalité
Le jeu s'ouvrera d'abord sue un écran d'acceuil avec de quoi lancer le jeu ou accéder aux option pour changer les touches des 2 joueurs. Ensuite un écran avec le choix des personnages et de l'arène s'ouvrira et les 2 joueurs choisironts leurs champions puis voterons pour l'arène qu'ils veulent. Ensuite le combat se lance, il y a une attaque coup de poing et une attaque à distance. Quand un les pv d'un joueurs tombe à 0, alors la partie est terminé et un menu de fin se lance avec de quoi demander une revanche et de quoi retourner au menu ou quitter.






## Solutions techniques

|Classe de menu| Cette classe comprend l'interface graphique du menu, qui après avoir reçu tout les parametres (pressonages choisis, map), va lancer la classe main |
|:----|:------|
|Classe main| Cette classe hérite de la classe arcade.Window, utilise/change les informations de la classe personnge, gère les entrées et update l'écran |
|Classe personnage| Contient les informations du personnage (pv, x y, état, sprite) et qui hérite de arcade.Sprite |
|Class attaque | Cette class créer la hitbox des attaques et si cette hitbox touche l'adversaire elle le blesse.

### fonction des classes:  

#### main:  
- setup : initialise les variables  
- on_draw : fonction appelée a chaque frame et qui dessine l'écran  
- on_keypress/on_key_release : fonction qui gere les controles et est appelé a chque fois qu'un touche est appuyée/relanchée  
- on_update : fonction qui gère la gravitée , les sauts, états (intouchable) et hitbox

### personnages:

- update_animation : change le sprite actuel en fonction de l'action
- update_informations : gère le cooldown (hadoken + invinciblitée)
- touche : paramatètre taille -> taille de l'écran, cette fonction gère le kb(knock back) aprèss que le personnage ce soit pris un coup







## Calendrier de développement

### Faire un jeu qui fonctionne
1. Faire une plateforme sur lequel le personnage peut se déplacer
2. Les déplacement
3. Faire une bar de vie
4. Définir les coups (+dégât)
5. Faire les hitbox
6. Mettre les sprites finaux



### Les menus
1. Menu d'acceuil(Jouer, Quitter)
2. Menu de fin + Menu de victoire



### Faire un combat avec plateforme(optionnel)
