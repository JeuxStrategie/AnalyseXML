Le script Python "lecture_fichiersXML_ElementTree" a pour objet de lire un fichier XML pour le convertir en fichier structuré csv lisible par IDEA
Le script est une ébauche, il ne traite pas tous les champs.
Il a pour intérêt d'utiliser directement la structure du fichier XML grâce à la bibliotheque elementtree.
Il est donc plus facilement réutilisable dans le cas d'un autre fichier XML avec d'autres noms de balises.
Il est nécessaires d'avoir installé les bibliotheques python pandas et elementtrees.

Un traitement intermédiaire est effectué (ajout de la balise "root" en début et fin de chaque fichier XML) car elementtree a besoin d'un fichier XML qui soit encadré et conclu par une balise.

Pour être exécuté, le script a besoin d'un dossier EXEMPLE4_0 qui contiendra lui-même les 4 dossiers suivants:
fichiers_source: contient les fichiers source XML
fichiers_passage: vide
fichiers_entete: vide
fichiers_detail: vide

 