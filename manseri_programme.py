#PROGRAMME_SYNTHESE
#La description des fonctions du programme se trouve en fin de page.
#Les fonctions appelées dans d'autres fonctions sont en fin de page.


#A REFAIRE À UN MOMENT ! Peut être optimiser maintenant :)
#IMPORTATION DES LIBRAIRIES
import sys #Pour mettre fin au programme si nécessaire.
import re #Pour utiliser une expression régulière.
import matplotlib.pyplot as plt #Pour la représentation graphique du signal.
import parselmouth #Pour rendre utilisable notre son et notre textgrid.
import textgrids #Pour rendre utilisable notre son et notre textgrid.
from parselmouth.praat import call #Pour appeler les commandes Praat.


#FONCTION MAIN
def main():
    global phrases
    global phrase
    
    phrase = ""
    #liste des phrases pré-définies : 
    phrases = ["Un jour, je serai le meilleur dresseur, j'attraperai tous les pokémons", "Je ferai tout pour être vainqueur et gagner les défis", "Je parcourrai la terre entière, traquant avec espoir", "Un jour, serai-je le meilleur dresseur ?", "Les pokémons et leurs mystères, le secret de leurs pouvoirs"]
   
    choix_programme()
    fichiers()
    transcription_phrase(phrase)
    synthese_phrase()

#FONCTION CHOIX PROGRAMME
def choix_programme():
    global phrase
    global choix_phrase
    global choix_utilisateur

    while True:
        choix_utilisateur = input("a. Synthétiser une phrase pré-définie. \nb. Synthétiser une phrase à partir des mots pris en compte par le dictionnaire. \n\nRentrez 'a' ou 'b' : ").lower()
        if choix_utilisateur == "b":
            phrase = demande_phrase()
            break
        elif choix_utilisateur == "a":
            while True:
                choix_phrase = input("Voici les phrases pré-définies de ce programme : \n 1 - Un jour je serai le meilleur dresseur, j'attraperai tous les pokémons? \n 2 - Je ferai tout pour être vainqueur et gagner les défis. \n 3 - Je parcourrai la terre entière, traquant avec espoir. \n 4 - Un jour, serai-je le meilleur dresseur ? \n 5 - Les pokémons et leurs mystères, le secret de leurs pouvoirs. \n\n Rentrez '1', '2', '3', '4' ou '5' : ")
                if choix_phrase in ["1", "2", "3", "4", "5"]:
                    choix_phrase = int(choix_phrase)
                    phrase = phrases[choix_phrase-1]
                    phrase = phrase.lower()
                    break
                else:
                    print("Veuillez rentrer une réponse valide")
            break
        else:
            print("Veuillez rentrer une réponse valide.")

#FONCTION FICHIERS
def fichiers():
    global resultat
    global son
    global segmentation
    global dictionnaire
    global mot

    #On nomme nos fichiers.
    source = 'manseri_logatomes_final.wav' 
    grille = 'manseri_logatomes_final.TextGrid'
    resultat = "manseri_resultat.wav"

    #On rend nos fichiers 'source' et 'grille' interprétables et utilisables grâce à Parselmouth.
    son = parselmouth.Sound(source) 
    segmentation = textgrids.TextGrid(grille)

    #On vient rendre utilisable notre fichier 'manseri_dico.txt'.
    #Cela revient à créer un dictionnaire de prononciation au sein du programme.
    dictionnaire = {}
    with open('manseri_dico.txt', 'r') as dico: #on ouvre le dictionnaire sous la variable 'dictionnaire'
        for line in dico:
            mot, transcription = line.split('    ') 
            #Linux (ou kate) semble avoir du mal à reconnaître les tabulations, je remplace donc '\t' par quatre espaces.
            dictionnaire[mot] = transcription

#FONCTION TRANSCRIPTION PHRASE
def transcription_phrase(phrase):
        global phrase_phonetique
        global mots_phrase
        phrase_phonetique = ""

        mots_phrase = re.findall(r"\b\w+'\w+\b|\b\w+\b|,", phrase)
        #Cette expression régulière permet de prendre en compte les virgules présentes dans notre dictionnaire.

        while True:
        #Ce while True permet de vérifier que tous les mots de notre phrases sont dans le dictionnaire.
        #La synthèse n'est effectuée que si tous les mots sont reconnus.
            
            phrase_phonetique = ""
            mots_reconnus = True
            
            for mot in mots_phrase:
                if mot in dictionnaire:
                    transcription_mot = str(dictionnaire[mot])
                    phrase_phonetique = phrase_phonetique + transcription_mot
                else:
                    print(f"Le mot '{mot}' n'est pas reconnu par le dictionnaire.")
                    mots_reconnus = False
                    break
            
            if mots_reconnus:
                phrase_phonetique = phrase_phonetique.strip().replace("\n", "") #Nous retirons tous les espaces et tabulations.
                liaison_phrase() #Nous ajoutons les liaisons si la phrase choisie est la troisième.
                #print(phrase_phonetique), utilisé pour vérification
                return phrase_phonetique
            else:
                phrase = demande_phrase()
                mots_phrase = re.findall(r"\b\w+'\w+\b|\b\w+\b|,", phrase)
                #La segmentation des mots se refait sur la nouvelle phrase rentrée.

#FONCTION SYNTHESE PHRASE
def synthese_phrase():
    global synthese
    global i
    global extrait
    global phrase_phonetique
    global diphone

    synthese = son.extract_part(0, 0.01, parselmouth.WindowShape.RECTANGULAR,1, False) #On initialise un signal sonore.
    phonemes = segmentation["logatome1"] #Nous venons chercher nos phonèmes.
    longueur_phrase = len(phrase_phonetique)

    if not phrase_phonetique: #Si la phrase rentrée par l'utilisateur est vide, le programme s'arrête.
        print("Vous n'avez aucun mot à synthétiser.")
        sys.exit()


    #Nous combinons l'ensemble de nos phonèmes pour former des diphones.
    #Des tirets sont ajoutés aux phonèmes initiaux et finaux pour former nos diphones.
    for i in range(longueur_phrase + 1): 
        if i == 0:
            diphone = "-" + phrase_phonetique[0]
        elif i == 1:
            diphone = phrase_phonetique[0] + phrase_phonetique[1]
        elif i == longueur_phrase:
            diphone = phrase_phonetique[-1] + "-"
        elif i == longueur_phrase + 1:
            diphone = phrase_phonetique[-1] + "-"
        else:
            diphone = phrase_phonetique[i-1] + phrase_phonetique[i]
    
        #print(diphone, i), pour vérification.
            
        phoneme1 = diphone[0]
        #Diphones initiaux et finaux.
        if len(diphone) > 1:
            phoneme2 = diphone[1]
        else:
            phoneme2 = "-"

        for position1 in range(len(phonemes)):
            position2 = position1 + 1
            #Nous vérifions que nos diphones correspondent à ceux de notre textgrid.
            if phonemes[position1].text == phoneme1 and phonemes[position2].text == phoneme2 :
                milieu_phoneme1 = phonemes[position1].xmin + (phonemes[position1].xmax - phonemes[position1].xmin)/2
                milieu_phoneme1 = son.get_nearest_zero_crossing(milieu_phoneme1,1)
        
                milieu_phoneme2 = phonemes[position2].xmin + (phonemes[position2].xmax - phonemes[position2].xmin)/2
                milieu_phoneme2 = son.get_nearest_zero_crossing(milieu_phoneme2,1)    
                #Nous récupérons les sons correspondant à nos diphones (entre millieu1 et milleu2).
                extrait = son.extract_part(milieu_phoneme1, milieu_phoneme2, parselmouth.WindowShape.RECTANGULAR,1,False)
                if choix_utilisateur == "a":
                    #Nous appliquons les manipulations de durée et de pitch si nous avons une phrase pré-définie.
                    choix_manipulation_duree()
                    choix_manipulation_pitch()
                synthese = son.concatenate([synthese,extrait], 0.005)
                synthese.save(resultat, parselmouth.SoundFileFormat.WAV)
                #Nous concaténons nos sons et enregistrons le signal final dans un fichier .wav
    
#FONCTION DEMANDE PHRASE (appelée dans choix_programme() et transcription_programme())      
def demande_phrase():

    global phrase
    phrase = input("Veuillez rentrer une phrase à synthétiser : ").lower()
    return phrase
#FONCTION LIAISON PHRASE (appelée dans transcription_phrase())
def liaison_phrase():
    global phrase_phonetique

    if choix_utilisateur == "a" and choix_phrase == 3:
        liaison = "t"
        id = 26
        phrase_phonetique = phrase_phonetique[:id] + liaison + phrase_phonetique[id:]
#FONCTION CHOIX MANIPULATION DUREE (appelée dans synthese_phrase())       
def choix_manipulation_duree():
#Nous définissons les phonèmes à modifier pour chaque phrase. Si ces phonèmes aparaissent plusieurs fois, nous utilisons les indices.
#Ces modifications sont effectuées grâce à l'appel de la fonction manipulation_duree().
    
    if choix_phrase == 1:
        mots_accentues1 = ["uR", "mE", "tu"]
        if diphone in mots_accentues1:
            manipulation_duree(1.5)
        elif diphone == "--":
            manipulation_duree(5)
        else:
            manipulation_duree(0.9)
    
    elif choix_phrase == 2:
        mots_accentues2 = ["tu", "up"]
        if diphone in mots_accentues2:
            manipulation_duree(1.5)
        else:
            manipulation_duree(0.9)

    elif choix_phrase == 3:
        mots_accentues3 = ["RA", "At"]
        if diphone in mots_accentues3:
            manipulation_duree(1.5)
        elif diphone == "aR" and i == 36:
            manipulation_duree(1.2)
        elif diphone == "--":
            manipulation_duree(8)
        else:
            manipulation_duree(0.9)

    elif choix_phrase == 4:
        mots_accentues4 = ["uR"]
        if diphone in mots_accentues4:
            manipulation_duree(1.5)
        elif diphone == "@R" and i == 30:
            manipulation_duree(1.2)
        elif diphone == "--":
            manipulation_duree(5)
        else:
            manipulation_duree(0.9)

    elif choix_phrase == 5:
        mots_accentues5 = ["tE", "ER", "aR", "R-"]
        if diphone in mots_accentues5:
            manipulation_duree(1.2)
        elif diphone == "--":
            manipulation_duree(5)
        else:
            manipulation_duree(0.9)
#FONCTION MANIPULATION DUREE (appelée dans choix_manipulation_duree())
def manipulation_duree(allongement):

    global extrait
    
    #Nous appelons des commandes Praat.
    #Une fois la durée extraite, nous la supprimons puis la remplaçons à l'aide du paramètre : allongement. 
    manipulation = call(extrait, "To Manipulation", 0.01, 75, 600)
    duration_tier = call(manipulation, "Extract duration tier")
    call(duration_tier, "Remove points between", 0, extrait.duration)
    call(duration_tier, "Add point", extrait.duration / 2, allongement)
    call([manipulation, duration_tier], "Replace duration tier")
    extrait = call(manipulation, "Get resynthesis (overlap-add)")
#FONCTION CHOIX MANIPULATION PITCH (appelée dans synthese_phrase())
def choix_manipulation_pitch():
#Nous définissons les phonèmes à modifier pour chaque phrase. Si ces phonèmes aparaissent plusieurs fois, nous utilisons les indices.
#Ces modifications sont effectuées grâce à l'appel de la fonction manipulation_pitch().
    
    if choix_phrase == 1:
        mots_descendants1 = ["uR", "s9", "mO", "On", "n-"]
        if diphone in mots_descendants1:
            manipulation_pitch(0.9)
        elif  diphone == "@R" and i == 24:
            manipulation_pitch(0.9)

    elif choix_phrase == 2:
        mots_descendants2 = ["k9", "9R", "fi", "i-"]
        if diphone in mots_descendants2:
            manipulation_pitch(0.9)
    
    elif choix_phrase == 3:
        mots_descendants3 = ["tj", "jE", "sp", "pw", "wa", "aR", "R-"]
        if diphone in mots_descendants3:
            manipulation_pitch(0.9)
        elif diphone == "ER" and i == 18:
            manipulation_pitch(0.9)
    
    elif choix_phrase == 4:
        mots_descendants4 = ["uR"]
        mots_interrogatif = ["s@", "Re", "EZ", "dR", "RE", "Es"]
        if diphone in mots_descendants4:
            manipulation_pitch(0.9)
        elif diphone in mots_interrogatif:
            manipulation_pitch(1.1)
        elif diphone == "@R":
            if i == 8:
                manipulation_pitch(1.1)
            elif i == 24:
                manipulation_pitch(1.3)
    
    elif choix_phrase == 5:
        mots_descendants5 = ["tE", "ER", "vw", "wa", "aR"]
        if diphone in mots_descendants5:
            manipulation_pitch(0.9)
#FONCTION MANIPULATION PITCH (appelée dans choix_manipulation_pitch())
def manipulation_pitch(hauteur):

    global extrait

    #Nous appelons des commandes Praat.
    #Une fois la hauteur extraite, nous la supprimons puis la remplaçons à l'aide du paramètre : hauteur.
    manipulation = call(extrait, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(manipulation, "Extract pitch tier")
    call(pitch_tier, "Get number of points")
    call(pitch_tier, "Multiply frequencies", extrait.xmin, extrait.xmax, hauteur)
    call([manipulation, pitch_tier], "Replace pitch tier")
    extrait = call(manipulation, "Get resynthesis (overlap-add)")


if __name__ == "__main__":
    main()
            

#DESCRIPTION DE L'ENSEMBLE DE NOS FONCTIONS
#Ces fonctions sont toutes comprises dans une fonction principale MAIN().

    ###FONCTION DEMANDE_PHRASE()
        #Cette fonction est appelée dans nos fonctions choix_programme() et transcription_phrase()
        #Cette fonction permet simplement de demander ou re-demander à l'utilisateur de rentrer une phrase.

    ###FONCTION LIAISON_PHRASE()
        #Cette fonction est appelée dans la fonction transcription_phrase()
        #Cette fonction n'est utilisée que dans le cas d'une phrase pré-défine.
        #Cette fonction permet d'ajouter des phonèmes pour les liaisions de la troisième phrase.

    ###FONCTION CHOIX_PROGRAMME()
        #Cette fonction permet de demander à l'utlisateur s'il veut choisir une phrase pré-définie ou en rentrer une. 

    ###FONCTION FICHIERS()
        #Cette fonction permet d'ouvrir et de rendre utilisable l'ensemble des fichiers utilisés dans notre programme.
    
    ###FONCTION TRANSCRIPTION_PHRASE()
        #Cette fonction transcrit phonétiquement la phrase choisie ou rentrée à l'aide de notre dictionnaire.

    ###FONCTION SYNTHESE_PHRASE()
        #Cette fonction associe chaque milieu de nos diphones à un son associé (à partir de notre fichier son et sa textgrid).           

    ###FONCTION CHOIX_MANIPULATION_DUREE()
        #Cette fonction est uniquement appelée pour les phrases-prédéfinies.
        #Cette fonction indique quels phonèmes doivent être rallongés pour chaque phrase.

    ###FONCTION CHOIX_MANIPULATION_PITCH()
        #Cette fonction est uniquement appelée pour les phrases-prédéfinies.
        #Cette fonction indique quels phonèmes doivent avoir leurs hauteurs augmentées ou diminuées pour chaque phrase.

    ###FONCTION MANIPULATION_DUREE()
        #Cette fonction est appelée dans la fonction choix_manipulation_duree().
        #Cette fonction permet la manipulation de la durée en appelant des commandes Praat.

    ###FONCTION MANIPULATION_PITCH()
       #Cette fonction est appelée dans la fonction choix_manipulation_pitch().
       #Cette fonction permet la manipulation de la hauteur en appelant des commandes Praat.










