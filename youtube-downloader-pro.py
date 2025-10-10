import os
import re
import yt_dlp
from colorama import Fore, Style, init
from tqdm import tqdm


init(autoreset=True)

def sanitize_filename(title):

    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def pilih_jenis():
    while True:
        print(Fore.MAGENTA + "\nPilih jenis download:")
        print("1. Audio saja 🎵")
        print("2. Video lengkap 🎬")
        print("0. Kembali / Batal ❌")
        pilihan = input(Fore.YELLOW + "Masukkan pilihan (0/1/2): ").strip()
        if pilihan in ['1', '2']:
            return pilihan
        elif pilihan == '0':
            return None
        else:
            print(Fore.RED + "❌ Pilihan tidak valid, coba lagi.")

def pilih_format_audio():

    while True:
        print(Fore.MAGENTA + "\nPilih format audio:")
        print("1. MP3")
        print("2. WAV")
        print("3. M4A")
        print("0. Kembali 🔙")
        f_choice = input(Fore.YELLOW + "Masukkan pilihan (0/1/2/3): ").strip()
        if f_choice == '0':
            return None
        if f_choice in ['1', '2', '3']:
            return {'1': 'mp3', '2': 'wav', '3': 'm4a'}[f_choice]
        print(Fore.RED + "❌ Pilihan tidak valid, coba lagi.")

def pilih_format_video():

    while True:
        print(Fore.MAGENTA + "\nPilih format video:")
        print("1. MP4")
        print("2. MKV")
        print("3. WebM")
        print("0. Kembali 🔙")
        f_choice = input(Fore.YELLOW + "Masukkan pilihan (0/1/2/3): ").strip()
        if f_choice == '0':
            return None
        if f_choice in ['1', '2', '3']:
            return {'1': 'mp4', '2': 'mkv', '3': 'webm'}[f_choice]
        print(Fore.RED + "❌ Pilihan tidak valid, coba lagi.")

def pilih_resolusi(info):

    print(Fore.MAGENTA + "\n📺 Daftar resolusi yang tersedia:")
    formats = [
        f for f in info['formats']
        if f.get('vcodec') != 'none' and f.get('acodec') != 'none'
    ]
    available_res = []
    for f in formats:
        res = f.get('format_note') or f.get('height')
        if res and str(res) not in available_res:
            available_res.append(str(res))

    for i, r in enumerate(available_res, 1):
        print(f"{i}. {r}")
    print("0. Kembali 🔙")

    while True:
        choice = input(Fore.YELLOW + "Pilih resolusi (nomor): ").strip()
        if choice == '0':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(available_res):
            return available_res[int(choice)-1]
        print(Fore.RED + "❌ Pilihan tidak valid, coba lagi.")

def progress_hook(d):

    global progress_bar
    if d['status'] == 'downloading':
        if progress_bar is None:
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            progress_bar = tqdm(total=total, unit='B', unit_scale=True, desc="📥 Mengunduh")
        progress_bar.update(d.get('downloaded_bytes', 0) - progress_bar.n)
    elif d['status'] == 'finished':
        if progress_bar:
            progress_bar.close()
            print(Fore.GREEN + "✅ Unduhan selesai, memproses file...")


print(Fore.CYAN + "🚀 YouTube Downloader Sneijderlino")
print(Fore.CYAN + "===================================================")

url = input(Fore.YELLOW + "Masukkan link YouTube: ").strip()
if not url:
    print(Fore.RED + "❌ URL tidak boleh kosong.")
    exit()


while True:
    jenis = pilih_jenis()
    if jenis is None:
        print(Fore.RED + "❌ Proses dibatalkan oleh pengguna.")
        exit()

    if jenis == '1':  
        fmt = pilih_format_audio()
        if fmt is None:
            continue
        download_type = 'audio'
    else:  # Video
        fmt = pilih_format_video()
        if fmt is None:
            continue
        download_type = 'video'
    break


output_folder = input(Fore.YELLOW + "\nMasukkan folder tujuan (kosongkan untuk folder ini): ").strip()
if not output_folder:
    output_folder = os.getcwd()
else:
    os.makedirs(output_folder, exist_ok=True)


info_opts = {'quiet': True}
with yt_dlp.YoutubeDL(info_opts) as ydl:
    info = ydl.extract_info(url, download=False)

judul = sanitize_filename(info.get('title', 'video'))
print(Fore.CYAN + f"\n🎧 Judul: {judul}")


if download_type == 'video':
    resolution = pilih_resolusi(info)
    if resolution is None:
        print(Fore.RED + "🔙 Kembali ke menu utama.")
        exit()
else:
    resolution = None


progress_bar = None


if download_type == 'audio':
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, f"{judul}.%(ext)s"),
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': fmt,
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True
    }
else:
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best' if resolution != 'best' else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_folder, f"{judul}.%(ext)s"),
        'progress_hooks': [progress_hook],
        'merge_output_format': fmt,
        'noplaylist': True,
        'quiet': True
    }


try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(Fore.GREEN + f"\n🎉 Selesai! File tersimpan di: {output_folder}")
except Exception as e:
    print(Fore.RED + f"\n❌ Terjadi kesalahan: {e}")

print(Style.RESET_ALL + "\n💎 Terima kasih telah menggunakan YouTube Downloader Sneijderlino 💎")