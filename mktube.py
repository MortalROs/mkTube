import argparse
import pytube
import os
from pathlib import Path


def read_music_links(download_location):
    music_file_path = os.path.join(download_location, 'music.txt')

    # Check if the file exists
    if os.path.exists(music_file_path):
        # Read the links from the music.txt file
        with open(music_file_path, 'r') as file:
            music_links = [line.strip() for line in file.readlines()]
        return music_links
    else:
        return None


def download_music_from_links(links, destination):
    for link in links:
        try:
            yt = pytube.YouTube(link)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=destination)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print(f"{yt.title} has been successfully downloaded to {destination}")
        except Exception as e:
            print(f"An error occurred while downloading {link}: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link', help='Youtube link')
    parser.add_argument('-o', '--out', help='Download Location')
    parser.add_argument('-m', '--music', action='store_true', help='Read links from music.txt')
    args = parser.parse_args()

    if args.link:
        links = [args.link]
    elif args.music:
        if args.out:
            links = read_music_links(args.out)
        else:
            desktop_path = Path.home() / 'Desktop'
            destination = desktop_path / 'mktube'
            # Check if the folder exists, otherwise create it
            if not os.path.exists(destination):
                os.makedirs(destination)
                print(f"Folder '{destination}' has been created.")
            links = read_music_links(destination)
            if links is None:
                # Create an empty music.txt file in the mktube folder on the desktop
                music_file_path = os.path.join(destination, 'music.txt')
                with open(music_file_path, 'w') as file:
                    pass
                links = []
                print("music.txt has been created!")
    else:
        print("No link to download!")
        return

    destination = Path(args.out).expanduser().resolve() if args.out else (Path.home() / 'Desktop' / 'mktube')
    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)

    download_music_from_links(links, destination)


if __name__ == '__main__':
    main()