import argparse
import subprocess
from tmdbv3api import TMDb, Movie
from pymediainfo import MediaInfo
import requests
from bs4 import BeautifulSoup
import iso639

def get_tmdb_details(tmdb_id):
    tmdb = TMDb()
    tmdb.api_key = ''  # Mettre la clef API TMDB ici / Enter your TMDB API key
    movie = Movie()
    tmdb.language = 'fr' # Langue des détailles / lang of details
    details = movie.details(tmdb_id)  # Recupérer les détailles / get details

    # Fetch credits separately
    credits = movie.credits(tmdb_id)

    # Vérifier la disponibilité du poster en français / Check if the French poster is available
    if details.poster_path:
        cover_url = f"https://image.tmdb.org/t/p/w500{details.poster_path}"
    else:
        # Se rabattre sur le poster en Anglais si Français pas dispo / Fallback to English poster if French is not available
        tmdb.language = 'en'
        details_en = movie.details(tmdb_id)
        cover_url = f"https://image.tmdb.org/t/p/w500{details_en.poster_path}"

    director = ", ".join([crew['name'] for crew in credits.crew if crew['job'] == 'Director']) # Récuperer le nom du producteur / get name of Director
    # Récupérer le top 5 des acteurs du film 
    actors = []
    for cast in list(credits.cast)[:5]:
        actor_name = cast['name']
        actor_image = f"https://image.tmdb.org/t/p/w138_and_h175_face{cast['profile_path']}" if cast['profile_path'] else None
        actors.append((actor_name, actor_image))

    genres = ", ".join([genre['name'] for genre in list(details.genres)[:3]])  # Récupérer les genres du film et le limiter à 3 / Get the genres of the movie then limit it to 3
    country_of_origin = ", ".join([country['name'] for country in details.production_countries]) # Récupérer le pays de production / get country of production
    date_of_release = details.release_date # Récupérer la date de sortie / get release date
    runtime = f"{details.runtime // 60}h et {details.runtime % 60}min" # Récupérer la longueur du film / get runtime of movie
    tmdb_link = f"https://www.themoviedb.org/movie/{tmdb_id}" # Générer le lien TMDB / generate TMDB link
    trailer_link = f"https://www.youtube.com/watch?v={details.videos.results[0]['key']}" if details.videos.results else None # Récupérer le trailer si disponible / get movie trailer if available 

    return {
        'cover_url': cover_url,
        'director': director,
        'actors': actors,
        'genres': genres,
        'country_of_origin': country_of_origin,
        'date_of_release': date_of_release,
        'runtime': runtime,
        'tmdb_link': tmdb_link,
        'trailer_link': trailer_link
    }

def get_allocine_synopsis(movie_title):
    base_url = "https://www.allocine.fr"
    search_url = f"{base_url}/rechercher/?q={movie_title}"

    # Faire une requête de recherche / Make a request to the search page
    response = requests.get(search_url)
    movie_soup = BeautifulSoup(response.text, 'html.parser')

    # Récupérer le synopsis et la note spéctateur / Find the synopsis and rating
    synopsis_element = movie_soup.find('div', class_='content-txt')
    rating_element = movie_soup.find('span', class_='stareval-note')

    # Extraire les éléments si possible / Extract text from elements or return None if not found
    synopsis = synopsis_element.get_text(strip=True) if synopsis_element else None
    rating = rating_element.get_text(strip=True) if rating_element else None

    return synopsis, rating

def map_codec(codec_id): # NFO incompréhensible -> termes compréhensible / NFO gibberish -> common words
    codec_mapping = {
        'V_MPEG4/ISO/AVC': 'h264',
        'V_MPEGH/ISO/HEVC': 'h265',
        'V_MPEG2': 'MPEG2',
        'V_MPEG4/ISO/ASP': 'MPEG4',
        'V_MS/VFW/FOURCC': 'FOURCC',
        'V_MS/VFW/FOURCC / DIV3': 'DivX 3',
        'V_MS/VFW/FOURCC / DIVX': 'DivX',
        'V_MS/VFW/FOURCC / DX50': 'DivX 5',
        'V_MS/VFW/FOURCC / XVID': 'Xvid',
        'V_MPEG4/ISO/AP': 'MPEG4 Part 2',
        'V_MJPEG': 'MJPEG',
        'V_MS/VFW/FOURCC / H264': 'h264',
        'V_MS/VFW/FOURCC / X264': 'h264',
        'V_MS/VFW/FOURCC / AVC1': 'h264',
        'V_MS/VFW/FOURCC / H265': 'h265',
        'V_MS/VFW/FOURCC / HEVC': 'h265',
        'V_MS/VFW/FOURCC / x265': 'h265',
        'V_MS/VFW/FOURCC / hev1': 'h265',
        'V_VP8': 'VP8',
        'V_VP9': 'VP9',
        'V_THEORA': 'Theora',
        'V_MPEG1': 'MPEG1',
        'V_MPEG4/ISO/SP': 'MPEG4 Part 2',
        'V_MPEG4/ISO/MP4V-ES': 'MPEG4 Part 2',
        'V_MPEG4/ISO/AVC / MP4V-ES': 'h264',
        'V_MPEG4/ISO/AVC / AVC1': 'h264',
        'V_MPEG4/ISO/AVC / avc1': 'h264',
        'V_MPEG4/ISO/HEVC / HEVC': 'h265',
        'V_MPEG4/ISO/HEVC / hev1': 'h265',
        'V_MPEG4/ISO/HEVC / hevc': 'h265',
        'V_MPEGH/ISO/HEVC / HEVC': 'h265',
        'V_MPEGH/ISO/HEVC / hev1': 'h265',
        'V_MPEGH/ISO/HEVC / hevc': 'h265',
    }
    return codec_mapping.get(codec_id, codec_id)

def map_audio_codec(audio_codec_id): # NFO incompréhensible -> termes compréhensible / NFO gibberish -> common words
    audio_codec_mapping = {
        'A_AAC-2': 'AAC',
        'A_AAC': 'AAC',
        'A_AC3': 'AC3',
        'A_DTS': 'DTS',
        'A_DTS/HD': 'DTS-HD',
        'A_DTS/HDMA': 'DTS-HD MA',
        'A_EAC3': 'EAC3',
        'A_FLAC': 'FLAC',
        'A_MPEG/L3': 'MP3',
        'A_MPEG/L2': 'MP2',
        'A_TRUEHD': 'TrueHD',
        'A_VORBIS': 'Vorbis',
        'A_WAVPACK4': 'WavPack',
        'A_PCM': 'PCM',
        'A_PCM/INT/LIT': 'PCM',
        'A_PCM/INT/BIG': 'PCM',
        'A_PCM/FLOAT/IEEE': 'PCM',
        'A_PCM/FLOAT/IEEE/PLANAR': 'PCM',
        'A_PCM/INT/LIT/BE': 'PCM',
        'A_PCM/INT/BIG/BE': 'PCM',
        'A_PCM/FLOAT/IEEE/BE': 'PCM',
        'A_PCM/FLOAT/IEEE/PLANAR/BE': 'PCM',
        'A_PCM/INT/LIT/LE': 'PCM',
        'A_PCM/INT/BIG/LE': 'PCM',
        'A_PCM/FLOAT/IEEE/LE': 'PCM',
        'A_PCM/FLOAT/IEEE/PLANAR/LE': 'PCM',
    }
    return audio_codec_mapping.get(audio_codec_id, audio_codec_id)

def map_audio_channels(channels): # NFO -> termes plus compréhensible / NFO -> more common words
    channel_mapping = {
        1: 'Mono',
        2: 'Stereo',
        3: '2.1',
        4: '4.0',
        5: '5.0',
        6: '5.1',
        7: '6.1',
        8: '7.1',
    }
    return channel_mapping.get(channels, str(channels))


def parse_nfo(file_path): # Mettre les infos du NFO dans des cases / Parse the NFO...
    media_info = MediaInfo.parse(file_path)

    # Extraire les pistes vidéo / Find the video track
    video_track = None
    for track in media_info.tracks:
        if track.track_type == 'Video':
            video_track = track
            break

    # Extraire les pistes audio / Find the audio tracks
    audio_tracks = []
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            audio_tracks.append(track)

    # Extarire le restes des infos / Extract relevant information
    format = media_info.tracks[0].format
    codec_id = video_track.codec_id if video_track else None
    codec = map_codec(codec_id) if codec_id else None
    video_bitrate = round(video_track.bit_rate / 1000) if video_track and video_track.bit_rate else None
    global_bitrate = round(media_info.general_tracks[0].overall_bit_rate / 1000) if media_info.general_tracks and media_info.general_tracks[0].overall_bit_rate else None
    file_size = media_info.general_tracks[0].file_size if media_info.general_tracks and media_info.general_tracks[0].file_size else None

    audio_details = [] # Récupérer les détails de chaque piste audio
    for audio_track in audio_tracks:
        language = audio_track.language if hasattr(audio_track, 'language') and audio_track.language else "Unknown"
        audio_bitrate = round(audio_track.bit_rate / 1000) if audio_track.bit_rate else None
        audio_codec = map_audio_codec(audio_track.codec_id) if audio_track.codec_id else None
        audio_channels = map_audio_channels(audio_track.channel_s) if audio_track.channel_s else None
        audio_details.append({
            'language': language,
            'audio_bitrate': audio_bitrate,
            'audio_codec': audio_codec,
            'audio_channels': audio_channels
        })

    return {
        'format': format,
        'codec': codec,
        'video_bitrate': video_bitrate,
        'global_bitrate': global_bitrate,
        'file_size': file_size,
        'audio_details': audio_details
    }



def generate_bbcode(movie_title, tmdb_id, nfo_file_path): # Générer le BBCODE grâce à toute les infos
    tmdb_details = get_tmdb_details(tmdb_id)
    synopsis, rating = get_allocine_synopsis(movie_title)
    media_details = parse_nfo(nfo_file_path)

    # Générer une partition de d'étoiles depuis un float de 0 à 5 / Generate star rating image
    star_rating = ""
    clear = str(rating).replace(",", ".")
    if rating:
        full_stars = int(float(clear))
        half_star = float(clear) - full_stars >= 0.5
        empty_stars = 5 - full_stars - (1 if half_star else 0)

        star_rating = "[img]https://zupimages.net/up/24/34/t8al.png[/img]" * full_stars
        if half_star:
            star_rating += "[img]https://zupimages.net/up/24/34/gniq.png[/img]"
        star_rating += "[img]https://zupimages.net/up/24/34/60bv.png[/img]" * empty_stars

    # Récupérer les liens vers les images des acteurs / Get actor images
    actor_images = ""
    actor_names = []
    for actor_name, actor_image in tmdb_details['actors']:
        if actor_image:
            actor_images += f"[img]{actor_image}[/img] "
        actor_names.append(actor_name)

    # Générer les langues / Generate language details !!!TODO!!!: make map like audio; video etc, with a fully fletched function for it. Or find lib 
    language_details = ""
    language_mapping = {
        'fr': ('fr', 'Français (VFF)'),
        'en': ('us', 'Anglais')
    }
    # Générer des joli drapeau pour les langues etc / Generate cool flags next to lang
    for audio in media_details['audio_details']:
        language_code = audio['language'].lower() if audio['language'] != "Unknown" else "unknown"
        country_code, language_name = language_mapping.get(language_code, (language_code, audio['language']))
        language_flag = f"https://flagcdn.com/20x15/{country_code}.png"
        language_details += f"[img]{language_flag}[/img] {language_name} [{audio['audio_channels']}] | {audio['audio_codec']} à {audio['audio_bitrate']} kb/s\n"

    # Convertir la taille des fichier en Go / Convert file size to gigabytes (Go)
    file_size_gb = media_details['file_size'] / (1024 * 1024 * 1024) if media_details['file_size'] else None
    file_size_str = f"{file_size_gb:.2f} Go" if file_size_gb else "Unknown"
    
    # Utlitmate build !!
    bbcode = f"""
    [center][size=29][color=#aa0000][b]{movie_title}[/b][/color][/size]

    [img]{tmdb_details['cover_url']}[/img]


    [img]https://zupimages.net/up/24/34/ng5x.png[/img]

    [b]Origine :[/b] {tmdb_details['country_of_origin']}
    [b]Sortie :[/b] {tmdb_details['date_of_release']}
    [b]Titre original :[/b] {movie_title}
    [b]Durée :[/b] {tmdb_details['runtime']}

    [b]Réalisateur :[/b] {tmdb_details['director']}

    [b]Acteurs :[/b]
    {", ".join(actor_names)}

    [b]Genres :[/b]
    {tmdb_details['genres']}

    {star_rating} {rating}

    [img]https://zupimages.net/up/21/03/mxao.png[/img][url={tmdb_details['tmdb_link']}]Fiche du film[/url]
    [img]https://www.zupimages.net/up/21/02/ogot.png[/img][url={tmdb_details['trailer_link']}]Bande annonce[/url]

    [img]https://zupimages.net/up/24/34/534l.png[/img]

    {synopsis}

    {actor_images}


    [img]https://zupimages.net/up/24/34/xlqf.png[/img]

    [b]Qualité :[/b]
    [b]Format :[/b] {media_details['format']}
    [b]Codec Vidéo :[/b] {media_details['codec']}
    [b]Débit Vidéo :[/b] {media_details['video_bitrate']} kb/s

    [b]Langue(s) :[/b]
    {language_details}

    [b]Débit Global :[/b] {media_details['global_bitrate']} kb/s

    [b]Source :[/b]
    [b]Nombre de fichier(s) :[/b] 1
    [b]Poids Total :[/b] {file_size_str}[/center]
    [url=https://github.com/calabazza1337/DrawMeAPrez]Prez construit avec DMAP[/url][/center]
    """

    return bbcode


def generate_nfo(file_path): # all in the name
    command = f"mediainfo {file_path} > {file_path}.nfo" # forgot to say in readme but have to install mediainfo thingy, find lib instead ? # Talked with OG, lib he tested was dead, TODO when lib gets better :(
    subprocess.run(command, shell=True)

def generate_torrent(file_path, tracker_url): # Gen .torrent
    output_torrent_path = f"{file_path}.torrent"
    command = f"mktorrent -a {tracker_url} -p -o {output_torrent_path} {file_path}" # forgot to ask to install in readme, maybe find lib ?
    subprocess.run(command, shell=True)

def main(args):
    bbcode = generate_bbcode(args.movie_title, args.tmdb_id, args.nfo_file_path)
    print(bbcode)

    generate_nfo(args.nfo_file_path)

    if args.tracker_url:
        generate_torrent(args.nfo_file_path, args.tracker_url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate BBCODE and .nfo file for a movie.")
    parser.add_argument("movie_title", type=str, help="The title of the movie.")
    parser.add_argument("tmdb_id", type=str, help="The TMDB ID of the movie.")
    parser.add_argument("nfo_file_path", type=str, help="The path to the .nfo file.")
    parser.add_argument("--tracker_url", type=str, help="The tracker URL for the torrent.")

    args = parser.parse_args()
    main(args)

