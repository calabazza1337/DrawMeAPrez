# DrawMeAPrez
This script generates BBCode and an NFO file for a movie using TMDB data. It also provides options to generate a torrent file with a specified tracker URL.

The BBCode is generated using the provided movie title, TMDB ID, and some other details fetched from TMDB API. The NFO file is created by running `mediainfo` command on the given video file path. If the 
`--tracker_url` option is specified, a torrent file will be generated using the specified tracker URL.

## Install
Here's a brief explanation of how to use this script:

1. Install the required packages (e.g., `argparse`, `subprocess`).
2. Save this script as `generate_bbcode.py`.
3. Run the script using the command line, providing the necessary arguments:

## Usage
```bash
python generate_bbcode.py "Movie Title" tmdb-id /path/to/nfo_file.nfo --tracker_url http://tracker.example.com
```
