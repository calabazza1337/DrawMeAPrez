# French
# DrawMeAPrez
Ce script génère du BBCode et/grâce à un fichier NFO pour un film en utilisant des données TMDB. Il propose également la possibilité de générer un fichier torrent avec une URL de serveur tracker spécifiée.

Le BBCode est généré à l'aide du titre de film fourni, de l'ID TMDB et d'autres détails récoltés via l'API TMDB. Le fichier NFO est créé en exécutant la commande `mediainfo` sur le chemin du fichier vidéo 
spécifié. Si l'option `--tracker_url` est fournie, un fichier torrent sera généré à l'aide de l'URL de serveur tracker spécifiée.

# SVP CONTRIBUEZ ! N'en faite pas des versions privées, partagez, s'il vous plaît :)
## Installation
1. Cloner le repo.
```bash
git clone https://github.com/calabazza1337/DrawMeAPrez && cd DrawMeAPrez
```
2. Installez les paquets requis.
```bash
pip install -r requirements.txt
```

## Utilisation
```bash
python generate_bbcode.py "Titre du Film" id-tmdb /chemin/vers/le/film.mkv --tracker_url http://tracker.exemple.com
```
Le fichier NFO est crée dans le même répertoire que le film

## Obtenir une clé API TMDB
Créez un compte TMDB puis allez sur https://www.themoviedb.org/settings/api

# English
# DrawMeAPrez
This script generates a BBCode and/from an NFO file for a movie using TMDB data. It also provides options to generate a torrent file with a specified tracker URL.

The BBCode is generated using the provided movie title, TMDB ID, and some other details fetched from TMDB API. The NFO file is created by running `mediainfo` command on the given video file path. If the 
`--tracker_url` option is specified, a torrent file will be generated using the specified tracker URL.
# PLEASE CONTRIBUTE ! Do NOT make private versions, share them, pls :)
## Install
1. Clone repo.
```bash
git clone https://github.com/calabazza1337/DrawMeAPrez && cd DrawMeAPrez
```
2. Install the required packages.
```bash
pip install -r requirements.txt
```

## Usage
```bash
python generate_bbcode.py "Movie Title" tmdb-id /path/to/movie.mkv --tracker_url http://tracker.example.com
```
NFO is saved in the same folder as the movie

## Get TMDB api key
Create TMDB account then go https://www.themoviedb.org/settings/api
