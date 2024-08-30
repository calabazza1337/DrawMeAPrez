# French
# DrawMeAPrez
Ce script génère du BBCode et/grâce à un fichier NFO pour un film en utilisant des données TMDB. Il propose également la possibilité de générer un fichier torrent avec une URL de serveur tracker spécifiée.

Le BBCode est généré à l'aide du titre de film fourni, de l'ID TMDB et d'autres détails récoltés via l'API TMDB. Le fichier NFO est créé en exécutant la commande `mediainfo` sur le chemin du fichier vidéo 
spécifié. Si l'option `--tracker_url` est fournie, un fichier torrent sera généré à l'aide de l'URL de serveur tracker spécifiée.

# SVP CONTRIBUEZ ! N'en fais pas des versions privées, les partagez, s'il vous plaît :)
## Installation
Voici une brève explication sur comment utiliser ce script :

1. Installez les paquets requis (par exemple, `argparse`, `subprocess`).
2. Enregistrez ce script sous le nom de `generate_bbcode.py`.
3. Exécutez le script en ligne de commande en fournissant les arguments nécessaires :

## Utilisation
```bash
python generate_bbcode.py "Titre du Film" id-tmdb /chemin/vers/le/film.mkv --tracker_url http://tracker.exemple.com
```
Le fichier NFO est écrit dans le même répertoire que le film

## Obtenir une clé API TMDB
Créez un compte TMDB puis allez sur https://www.themoviedb.org/settings/api

# English
# DrawMeAPrez
This script generates a BBCode and/from an NFO file for a movie using TMDB data. It also provides options to generate a torrent file with a specified tracker URL.

The BBCode is generated using the provided movie title, TMDB ID, and some other details fetched from TMDB API. The NFO file is created by running `mediainfo` command on the given video file path. If the 
`--tracker_url` option is specified, a torrent file will be generated using the specified tracker URL.
# PLEASE CONTRIBUTE ! Do NOT make private versions, share them, pls :)
## Install
Here's a brief explanation of how to use this script:

1. Install the required packages (e.g., `argparse`, `subprocess`).
2. Save this script as `generate_bbcode.py`.
3. Run the script using the command line, providing the necessary arguments:

## Usage
```bash
python generate_bbcode.py "Movie Title" tmdb-id /path/to/movie.mkv --tracker_url http://tracker.example.com
```
NFO is written in the same folder as the movie

## Get TMDB api key
Create TMDB account then go https://www.themoviedb.org/settings/api
