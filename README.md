<p align="center">
  <img src="/img/banner.jpg" alt="YouTube Downloader Pro Banner" width="900"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tool-YouTube%20Downloader-brightgreen?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/github/license/Sneijderlino/youtube-downloader-pro?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python"/>
</p>

---



# 🎬 YouTube Downloader Pro Ultimate Edition

By [Sneijderlino](https://github.com/Sneijderlino)

🚀 Program profesional untuk mengunduh _video & audio YouTube_ langsung dari terminal dengan tampilan interaktif, cepat, dan berwarna.  
Didesain untuk berjalan di _Windows, **Linux (termasuk Kali), dan **Android (Termux), serta mudah dijalankan di \*\*Visual Studio Code_.

---

## ✨ Fitur Utama

- 🎵 Download _audio_ (MP3, WAV, M4A)
- 🎬 Download _video_ (MP4, MKV, WEBM)
- 🎚 Pilih _resolusi & format_ dengan mudah
- 🧾 _Progress bar real-time_
- 💾 Simpan ke _folder custom_
- 🧩 _Cross-platform_ support (Windows / Linux / Termux)
- 🌈 Tampilan terminal _berwarna & interaktif_
- ⚡ Ringan, cepat, tanpa API key
- 🔁 Dapat dijalankan berulang tanpa crash

---

## 🧰 Persyaratan Sistem

| Komponen             | Keterangan                                       |
| -------------------- | ------------------------------------------------ |
| _Python_             | Minimal versi 3.8                                |
| _FFmpeg_             | Diperlukan untuk konversi video/audio            |
| _yt-dlp_             | Engine utama untuk download                      |
| _colorama, tqdm_     | Untuk tampilan warna & progress bar              |
| _VS Code (opsional)_ | Untuk menjalankan proyek dengan antarmuka modern |

---

## 🧩 Instalasi Cepat

### 💻 Windows / Linux / macOS

```bash
git clone https://github.com/Sneijderlino/youtube-downloader-pro.git
cd youtube-downloader-pro
pip install -r requirements.txt
python src/main.py
```
---

### 🐧 Instalasi Di Kali Linux

```bash
sudo apt update && sudo apt install python3 python3-pip ffmpeg git -y
git clone https://github.com/Sneijderlino/youtube-downloader-pro.git
cd youtube-downloader-pro
pip install -r requirements.txt
python3 src/main.py
```

---

### 📱Instalasi Di Termux

```bash
pkg update && pkg install python ffmpeg git -y
git clone https://github.com/Sneijderlino/youtube-downloader-pro.git
cd youtube-downloader-pro
pip install -r requirements.txt
python src/main.py
```

---

### 💻 Jalankan di Visual Studio Code

<h6>1. Buka Project</h6>

```bash
1. Buka Proyek
2. Buka Visual Studio Code
3. Klik File → Open Folder → pilih folder youtube-downloader-pro
```

---

<h6>2. Buka Terminal</h6>

```bash
CTRL + '
#Lalu Jalankan:
py youtube-downloader-pro.py

```

---

<h6>3. Gunakan Virtual Environment (opsional tapi disarankan)</h6>

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

### 💻 Cara Menggunakan

<h6>1. Jalankan Program</h6>

```bash
python src/main.py
```

---

<h6>2. Masukkan URL video YouTube
</h6>

```bash
Masukkan link YouTube:
```

---

<h6>3. Pilih Mode</h6>

```bash
1 → Audio

2 → Video
```

---

<h6>4. Pilih format (MP3, WAV, MP4, dll)
</h6>

```bash
1. MP4
2. MKV
3. WebM
0. Kembali 🔙
```

---

<h6>5. Pilih resolusi (jika video)
</h6>

```bash
📺 Daftar resolusi yang tersedia:
1. 144
2. 240
3. 360
4. 360p
5. 480
6. 720
7. 1080
0. Kembali 🔙
```

---

<h6>6. Tunggu hingga proses selesai ✅
File akan tersimpan di folder downloads/
</h6>

---

## 🖼 Demo / Contoh Output

<p align="center">
  <img src="/img/demo 1.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Demo Script Dijalankan: <code><br>Inputanan Meminta Masukan Url You Tube<pentest_output/</code>.</em>
</p>

---

<p align="center">
  <img src="/img/demo 2.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Url You tube Dimasukan:
</p>

---

<p align="center">
  <img src="/img/demo3.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Pilih Mode :
</p>

---

<p align="center">
  <img src="/img/demo 4.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Pilih Format :
</p>

---

<p align="center">
  <img src="/img/demo 5.png" alt="Contoh output web_scanner_ghost" width="800"/><br>
  <em>Berhasil Mendownlaod Dan mengkonversi ke Format yang Diinginkan:
</p>

---

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python" alt="Python Badge"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status Active"/>
  <img src="https://img.shields.io/github/stars/Sneijderlino/youtube-downloader-pro?style=for-the-badge" alt="GitHub Stars"/>
  <img src="https://img.shields.io/github/forks/Sneijderlino/youtube-downloader-pro?style=for-the-badge" alt="GitHub Forks"/>
</p>

---

<h3 align="center">📜 Lisensi</h3>

<p align="center">
  Proyek ini dilisensikan di bawah <a href="LICENSE">MIT License</a>.<br>
  Bebas digunakan, dimodifikasi, dan dibagikan selama mencantumkan kredit.
</p>

---

<h3 align="center">💬 Dukungan & Kontribusi</h3>

<p align="center">
  💡 Temukan bug atau ingin menambahkan fitur baru?<br>
  Silakan buka <a href="https://github.com/Sneijderlino/youtube-downloader-pro/issues">Issues</a> atau buat <a href="https://github.com/Sneijderlino/youtube-downloader-pro/pulls">Pull Request</a>.<br><br>
  ⭐ Jangan lupa beri bintang jika proyek ini bermanfaat!
</p>

---

<p align="center">
  Dibuat dengan ❤ oleh <a href="https://github.com/Sneijderlino">Sneijderlino</a><br>
  <em>“Code. Create. Conquer.”</em>
</p>
# youtube-downloader-pro
