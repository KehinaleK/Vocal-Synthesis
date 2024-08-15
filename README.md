# SYNTHÈSE VOCALE :
*Kehina MANSERI*

- Ce fichier **README** visant à expliquer le programme python.
- Le fichier **son : manseri_logatomes_final** sous format wav comprenant l'ensemble des logatomes.
- Le fichier **TextGrid : manseri_logatomes_final** ayant permis de segmenter ces logatomes.
- Le **dictionnaire : manseri_dico** sous format txt comprenant les mots pris en compte par notre programme.
- Le **programme python : manseri_programme** ayant permis de réaliser cette synthèse. 
- Le fichier **manseri_resultat** qui correspond au résultat du programme.

## Programme python :

Le programme vise à réaliser une synthèse par concaténation de diphones de cinq phrases pré-définies pendant le semestre. Ces cinq phrases sont inspirées ou tirées du générique français de l'animé *Pokémon* :

**1 - Un jour, je serai le meilleur dresseur, j'attraperai tous les pokémons.**

    Diphones : -I IZ Zu uR RZ Z@ @s s@ @R Re el l@ @m mE Ej j@ @R Rd dR RE Es s@ @R RZ Za at tR Ra ap p@ @R Re et tu ul le ep pO Ok ke em mO On n-


**2 - Je ferai tout pour être vainqueur et gagner les défis.**

    Diphones : -Z Z@ @f f@ @R Re et tu up pu uR RE Et tR R@ @v vI Ik k9 9R Re eg ga an nJ Je el le ed de ef fi i-

**3 - Je parcourrai la terre entière, traquant avec espoir.**

    Diphones : -Z Z@ @p pa aR Rk ku uR Re el la at tE ER RA At tj jE ER Rt tR Ra ak kA At ta av vE Ek kE es sp pw wa aR R-

**4 - Un jour, serai-je le meilleur dresseur ?**

    Diphones : -I IZ Zu uR Rs s@ @R RE EZ Z@ @l l@ @m mE Ej j9 9R Rd dR RE Es s9 9R R-

**5 - Les pokémons et leurs mystères, le secret de leurs pouvoirs.**

    Diphones : -l le ep pO Ok ke em mO On ne el l9 9R Rm mi is st tE ER R@ @l l@ @s s@ @k kR RE Ed d@ @l l9 9R Rp pu uv vw wa aR R-

Le programme est organisé en 4 fonctions regroupées dans une fonction main :
```
def main():
    global phrase
    global phrases
   
    choix_programme()
    fichiers()
    transcription_phrase(phrase)
    synthese_phrase()
```
En haut du programme, nous appelons toutes les librairies utilisées :

**import sys** Pour mettre fin au programme si nécessaire.

**import re** Pour utiliser une expression régulière.

**import matplotlib.pyplot as plt** Pour la représentation graphique du signal. (non utilisée)

**import parselmouth** Pour rendre utilisable notre son et notre textgrid.

**import textgrids** Pour rendre utilisable notre son et notre textgrid.

**from parselmouth.praat import call** Pour appeler les commandes Praat.




D'autres fonctions sont appelées au sein de ces quatre fonctions.
Voici une présentation de chacune des fonctions du programme : 

### Fonction choix_programme() :

La fonction choix programme sert à demander à l'utilisateur de choisir parmis deux choix. Le premier est celui de choisir une phrase à synthétiser parmis les phrases pré-définies, le deuxième est celui de rentrer une phrase en input.

- Si l'utilisateur choisi le premier choix (a) : 

    L'utilisateur doit choisir parmis les 5 phrases en entrant "1", "2", "3", "4" ou "5". Ce choix est ensuite converti en entier pour qu'il puisse correspondre à la numérotation des phrases (Le premier indice des listes étant 0). La phrase est ensuite passée en minuscule car les mots de notre dictionnaire ne contiennent pas de majuscules. 

- Si l'utilisateur choisi le second choix (b) : 

    Une fonction demande_phrase() est appelée.

    #### Fonction demande_phrase() :
    Cette fonction lance un input demandant à l'utilisateur de rentrer une phrase. Cette phrase est sauvegardée et utilisée dans le reste du programme. 


### Fonction fichiers() :

Cette fonction permet d'ouvrir et d'adapter l'ensemble de nos fichiers pour qu'ils soient utilisables dans notre programme.

- Nous attribuons premièrement à des variables nos fichiers son (logatomes et résultat) et TextGrid. Nous utilisons ensuite les librairies parselmouth et textgrids pour rendre utilisable notre son et notre textgrid, donc notre segmentation de diphones.

- Nous ouvrons ensuite notre dictionnaire et associons chaque mot à sa transcription à l'aide de la fonction split(). Le dictionnaire utilisé contient uniquement les mots contenus dans les phrases pré-définies. Ces mots et leurs transcriptions sont séparés par 4 espaces. Les tabulations n'étant précédemment pas reconnues.


### Fonction transcription_phrase(phrase) : 

Cette fonction prend en argument la phrase à synthétiser (sous forme de chaine de caractères). 

- Cette fonction permet de créer une chaine de caractères phrase_phonetique composée des transcriptions phonétiques de chaque mot de notre phrase. Les virgules sont représentées par deux tirets.

- Cette fonction vérifie également que chaque mot de notre phrase se trouve dans notre dictionnaire. Si ce n'est pas le cas (ce qui arrive uniquement quand la phrase n'est pas parmis les pré-définies), le programme renvoie à l'utilisateur un message lui indiquant que tel mot n'est pas pris en compte par le dictionnaire. Cette boucle se répète jusqu'à ce que l'utilisateur rentre une phrase valide. Nous pouvons arriver à cette boucle grâce à un while True et grâce à la fonction demande_phrase(). 

- J'ai utilisé une expression régulière afin d'isoler tous les mots de mes phrases en prenant en compte les virgules. Ces dernières étant retranscrites "-", nous pouvons marquer des silences dans nos phrases car "-" correspond aux silences dans ma segmentation. 

- La fonction appelle une autre fonction nommée liaison_phrase() :

    #### Fonction liaison_phrase() :
    Cette fonction est utilisée dans le cas ou le choix de l'utilisateur se serait porté sur la troisième phrase. Cette dernière contient des liaisons n'apparaissant pas dans la transcription phonétique. Par exemple : traquant avec = trakA avEk. Nous désirons avoir un "t" entre ces deux mots. Cette fonction vient incorporer ces phonèmes de liaison dans la phrase phonetique.

### Fonction synthese_phrase() :

La fonction synthese_phrase() permet d'extraire les diphones et phonèmes de notre phrase_phonetique afin de les associer à un son. 

- Avant toute chose, la fonction vérifie que la variable phrase_phonetique n'est pas vide. Si c'est le cas, le programme s'arrête.
- Nous commencons premièrement par initialiser un séquence sonore auquelle viendra s'ajouter nos sons. 
- Nous allons ensuite chercher à obtenir chaque paire de phonèmes consécutives de notre phrases phonétique, ce qui forme donc nos diphones. 
- Ces paires de phonèmes permettent ensuite grâce à leurs positions de récupérer le milleu de chaque diphone.
- Les sons associés à ces milleux de diphones sont stockés dans la variable extrait.
- Ces extraits sonores sont ensuite tous concatenés à des intervalles de 0.005 secondes. 
- Pour chaque itération, nos sons sont stockés puis sauvegardés en fin de programme dans un fichier wav.

Cependant, avant de concatener nos milieux de diphones, nous appelons deux fonctions choix_manipulation_duree(). et choix_manipulation_pitch().

### Fonction choix_manipulation_duree():

Cette fonction permet d'identifier les diphones que l'on souhaite modifier en terme de durée. Ces fonctions ne sont appelées que si les phrases synthétisées sont parmis celles pré-définies.

- Cette fonction utilise plusieurs conditions if correspondant au choix de phrase en début de programme. Dépendamment de quelle phrase est choisie, certains diphones vont être rallongés.
- Pour ce qui est du choix de ces diphones, j'ai préféré rallonger ceux précédent une virgule ou qui me semblaient intéressant de mettre en valeur au vu de nos phrases. J'ai par exemple rallongé les mots "tout" et "tous" pour appuyer sur la détérmination du dresseur de pokémons. J'ai également rallongé certains mots en fin de phrase car cela me semblait adéquat. J'essayais d'imaginer un narrateur les réciter et certains m'ont parus plus adéquates que d'autres. 
- Pour ce qui est des diphones présents en double dans nos phrases, j'ai rajouté une condition supplémentaire à nos boucles if demandant que le diphone soit dans notre liste de diphones à rallonger et qu'il corresponde également au diphone présent à l'indice (i) indiqué. 
- Cette fonction appelle après chaque condition la fonction manipulation_duree():

    #### manipulation_duree(allongement) : 

    Cette fonction prend en facteur l'allongement, la durée souhaitée par l'utilisateur pour chaque diphone.

    - La fonctionalité Manipulation n'est pas pris en compte par la librairie Python Parselmouth, nous devons donc utiliser Parselmouth pour accéder aux commandes de Praat.

    - Les lignes de code correspondant à ces appels de commandes Praat permettent d'extraire la durée de notre diphone, de la supprimer, puis de la remplacer par une durée détérminée par la variable allongement. Cela nous permet ainsi de choisir des durées différentes pour chacun de nos diphones dans la fonction choix_manipulation_duree().

### Fonction choix_manipulation_pitch():

Cette fonction fonctionne de la même manière que la fonction choix_manipulation_duree().

- Pour ce qui est du choix des diphones au pitch réduit, je me suis basée sur la règle très générale qui dit que l'intonation à tendance à baisser en fin de phrase en français. J'ai donc baissé le pitch des diphones précédent des virgules ou étant en fin de phrase. Le choix de la hauteur s'est fait de manière assez arbitraire.

- Il a fallu également augmenter la hauteur de certains diphones dans la phrase 4, cette dernière étant une question. Ici, la fin de la phrase ainsi que le verbe interrogatif devaient disposer d'une hauteur plus élevée. Pour cela, j'ai utilisé les mêmes mécanismes que dans la fonction choix_manipulation_duree(). Il a fallu cependant créer une sous condition if quand j'ai voulu donner deux hauteurs différentes à deux diphones identiques. J'ai pour celà utilisé de nouveau les indices : 

```
elif choix_phrase == 4:
        mots_descendants4 = ["uR"]
        mots_interrogatif = ["s@", "Re", "EZ", "dR", "RE", "Es"]
        if diphone in mots_descendants4:
            manipulation_pitch(0.9)
        elif diphone in mots_interrogatif:
            manipulation_pitch(1.1)
        elif diphone == "@R":
            if i == 10:
                manipulation_pitch(1.1)
            elif i == 30:
                manipulation_pitch(1.3)
```

- Cette fonction appelle pour chaque condition la fonction manipulation_pitch() :

    #### manipulation_pitch(hauteur) : 

    Cette fonction prend en argument l'hauteur déterminée par l'utilisateur. 

    - Elle fonctionne de la même manière que la fonction manipulation_duree().



Nous appellons enfin notre fonction main() en fin de code. 

