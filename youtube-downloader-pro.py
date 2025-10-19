import os
import re
import threading
import time
import queue
from datetime import datetime
from io import BytesIO

import yt_dlp
import customtkinter as ctk
from tkinter import filedialog, messagebox, Text, DISABLED, NORMAL, END, NW
from PIL import Image, ImageTk
import requests
import random

# -------------------- Utility --------------------
def sanitize_filename(title):
    """Menghilangkan karakter ilegal dari nama file."""
    return re.sub(r'[\\/*?:"<>|]', "", title).strip()

def log_download(title, path):
    """Mencatat riwayat download ke file."""
    with open("riwayat_download.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {title} -> {path}\n")

# -------------------- Colors  --------------------
BG_MAIN = "#061018"        
PANEL = "#0b1820"          
ACCENT = "#fdfdfd"          
ACCENT2 = "#000000"         
TEXT_SOFT = "#c9f0ef"      
MUTED = "#97b3b7"       

# -------------------- App Config --------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

APP_W = 980
APP_H = 640

# Thread-safe queue to receive progress_hook events
progress_queue = queue.Queue()

# -------------------- Main Window --------------------
app = ctk.CTk()
app.title("┌─[ S N E I J D E R • SOFT-HACK ]─┐")
app.geometry(f"{APP_W}x{APP_H}")
app.resizable(False, False)

# Using Canvas for gentle animated background
bg_canvas = ctk.CTkCanvas(app, width=APP_W, height=APP_H, highlightthickness=0, bg=BG_MAIN)
bg_canvas.place(x=0, y=0)

# Main frame (slightly translucent look)
main_frame = ctk.CTkFrame(app, corner_radius=12, fg_color=PANEL)
main_frame.place(relx=0.02, rely=0.03, relwidth=0.96, relheight=0.94)

# -------------------- Left Column (controls) --------------------
left_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#07121a")
left_frame.place(relx=0.02, rely=0.02, relwidth=0.56, relheight=0.96)

# Title area
title_label = ctk.CTkLabel(left_frame, text="SNEIJDERLINO • YOU TUBE DOWNLOADER", 
                        font=("Consolas", 20, "bold"), text_color=ACCENT)
title_label.pack(pady=(12,4))

subtitle = ctk.CTkLabel(left_frame, text="Sneijderlino Ghost • GUI terminal", 
                        font=("Consolas", 10), text_color=MUTED)
subtitle.pack(pady=(0,12))

# URL input
ctk.CTkLabel(left_frame, text="▶ URL YouTube:", anchor="w", font=("Consolas", 11), text_color=TEXT_SOFT).pack(padx=16, pady=(6,2), fill="x")
url_var = ctk.StringVar()
url_entry = ctk.CTkEntry(left_frame, textvariable=url_var, width=480, placeholder_text="https://youtube.com/...", 
                        fg_color="#061821", text_color=TEXT_SOFT, corner_radius=6)
url_entry.pack(padx=16, pady=(0,10), fill="x")

# Playlist checkbox
playlist_var = ctk.BooleanVar(value=False)
playlist_chk = ctk.CTkCheckBox(left_frame, text="Playlist (multi)", variable=playlist_var, 
                            fg_color="#103235", text_color=MUTED)
playlist_chk.pack(padx=16, pady=(0,8), anchor="w")

# Type radio (audio / video)
ctk.CTkLabel(left_frame, text="▶ Mode:", anchor="w", font=("Consolas", 11), text_color=TEXT_SOFT).pack(padx=16, pady=(6,2), fill="x")
jenis_var = ctk.StringVar(value="audio")
frame_radio = ctk.CTkFrame(left_frame, fg_color="#07121a", corner_radius=6)
frame_radio.pack(padx=16, pady=(0,8), fill="x")
ctk.CTkRadioButton(frame_radio, text="Audio", variable=jenis_var, value="audio", 
                   text_color=TEXT_SOFT, fg_color="#103235", height=24).pack(side="left", padx=12, pady=8)
ctk.CTkRadioButton(frame_radio, text="Video", variable=jenis_var, value="video", 
                   text_color=TEXT_SOFT, fg_color="#103235", height=24).pack(side="left", padx=12, pady=8)

# Format menu
ctk.CTkLabel(left_frame, text="▶ Format:", anchor="w", font=("Consolas", 11), text_color=TEXT_SOFT).pack(padx=16, pady=(6,2), fill="x")
format_var = ctk.StringVar(value="mp3")
format_menu = ctk.CTkOptionMenu(left_frame, values=["mp3","wav","m4a","mp4","mkv","webm"], variable=format_var,
                                fg_color="#061821", button_color="#11363a", text_color=TEXT_SOFT)
format_menu.pack(padx=16, pady=(0,8), fill="x")

# Resolution menu (video)
ctk.CTkLabel(left_frame, text="▶ Resolusi (Video):", anchor="w", font=("Consolas", 11), text_color=TEXT_SOFT).pack(padx=16, pady=(6,2), fill="x")
res_var = ctk.StringVar(value="best")
res_menu = ctk.CTkOptionMenu(left_frame, values=["best"], variable=res_var,
                            fg_color="#061821", button_color="#11363a", text_color=TEXT_SOFT)
res_menu.pack(padx=16, pady=(0,8), fill="x")

# Folder chooser
# Lokasi Hasil download default
output_folder_var = ctk.StringVar(value=r"D:\SNEIJDERLINO\DATABASE APLIKASI SNEIJDERLINO\DATABASE_YOUTUBE_DOWNLOAD")

def pilih_folder():
    f = filedialog.askdirectory()
    if f:
        output_folder_var.set(f)
        folder_label.configure(text=f"📁 {f}", text_color=MUTED)

ctk.CTkButton(left_frame, text="Pick Save Folder", command=pilih_folder, 
            fg_color=ACCENT2, hover_color="#e8c79f").pack(padx=16, pady=(6,6), anchor="w")
folder_label = ctk.CTkLabel(left_frame, text=f"📁 {output_folder_var.get()}", anchor="w", font=("Consolas",9), text_color=MUTED)
folder_label.pack(padx=16, pady=(0,12), fill="x")

# Buttons row
btn_frame = ctk.CTkFrame(left_frame, fg_color="#07121a")
btn_frame.pack(padx=16, pady=(6,12), fill="x")
def on_ambil():
    threading.Thread(target=ambil_resolusi_preview, daemon=True).start()
ctk.CTkButton(btn_frame, text="● FETCH INFO", command=on_ambil, fg_color=ACCENT, hover_color="#5bd0d6").pack(side="left", padx=8, pady=8, ipadx=6)
def on_start():
    threading.Thread(target=mulai_download_thread, daemon=True).start()
ctk.CTkButton(btn_frame, text="▶ START", command=on_start, fg_color=ACCENT2, hover_color="#e8c79f").pack(side="left", padx=8, pady=8, ipadx=12)

# -------------------- Right Column (preview + logs) --------------------
right_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="#041216")
right_frame.place(relx=0.60, rely=0.02, relwidth=0.38, relheight=0.96)

# Preview card (thumbnail + title)
preview_card = ctk.CTkFrame(right_frame, corner_radius=8, fg_color="#071a1c")
preview_card.pack(padx=12, pady=12, fill="x")

thumbnail_placeholder = ctk.CTkLabel(preview_card, text="No Preview", width=360, height=180, 
                                     fg_color="#031314", text_color=MUTED, corner_radius=6)
thumbnail_placeholder.pack(padx=12, pady=10)

title_var = ctk.StringVar(value="—")
title_preview = ctk.CTkLabel(preview_card, textvariable=title_var, text_color=TEXT_SOFT, 
                             font=("Consolas", 12, "bold"), wraplength=260, anchor=NW)
title_preview.pack(padx=12, pady=(0,12), fill="x")

# Progress visible numeric + bar (soft accents)
progress_frame = ctk.CTkFrame(right_frame, fg_color="#041216")
progress_frame.pack(padx=12, pady=(0,8), fill="x")

progress_label_var = ctk.StringVar(value="Progress: 0.0%")
progress_label = ctk.CTkLabel(progress_frame, textvariable=progress_label_var, text_color=TEXT_SOFT, font=("Consolas",10))
progress_label.pack(padx=10, pady=(8,6), anchor="w")

progress_bar = ctk.CTkProgressBar(progress_frame, width=300, height=18, mode="determinate")
progress_bar.set(0)
progress_bar.pack(padx=10, pady=(0,12))

# Speed & ETA
speed_var = ctk.StringVar(value="Speed: 0 KB/s")
eta_var = ctk.StringVar(value="ETA: --:--")
ctk.CTkLabel(progress_frame, textvariable=speed_var, text_color=MUTED, font=("Consolas",9)).pack(padx=10, anchor="w")
ctk.CTkLabel(progress_frame, textvariable=eta_var, text_color=MUTED, font=("Consolas",9)).pack(padx=10, pady=(0,8), anchor="w")

# Terminal log (softer green text)
log_frame = ctk.CTkFrame(right_frame, fg_color="#021216")
log_frame.pack(padx=12, pady=6, fill="both", expand=True)
terminal = Text(log_frame, bg="#021216", fg="#A7FFE6", insertbackground="#A7FFE6", 
                font=("Consolas", 10), wrap="word", bd=0, highlightthickness=0)
terminal.pack(fill="both", expand=True, padx=6, pady=6)
terminal.insert(END, ">> Ready. Paste URL then [● FETCH INFO] → [▶ START]\n")
terminal.configure(state=DISABLED)

# -------------------- Gentle matrix-effect background --------------------
class GentleMatrix:
    def __init__(self, canvas, width, height, cols=80):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.cols = cols
        self.font_size = max(9, int(width/cols))
        self.drops = [random.randint(-300, 0) for _ in range(cols)]
        self.chars = "01░▒▗▖▝▘"
        self.running = True
        self._tick()

    def _tick(self):
        if not self.running:
            return
        self.canvas.delete("matrix")
        for i in range(self.cols):
            x = i * (self.font_size + 2)
            y = self.drops[i] * (self.font_size + 1)
            ch = random.choice(self.chars)
            # faint trail (very soft, amber)
            self.canvas.create_text(x, y, text=ch, anchor="nw", font=("Consolas", self.font_size),
                                    fill="#2a1b12", tag="matrix")
            # gentle head (soft-cyan)
            self.canvas.create_text(x, y, text=ch, anchor="nw", font=("Consolas", self.font_size),
                                    fill=ACCENT, tag="matrix")
            if y > self.height and random.random() > 0.986:
                self.drops[i] = random.randint(-12, 0)
            self.drops[i] += 1
        self.canvas.after(90, self._tick)

matrix = GentleMatrix(bg_canvas, APP_W, APP_H, cols=80)

# -------------------- Helper functions --------------------
def log(msg, newline=True):
    ts = datetime.now().strftime("%H:%M:%S")
    text = f"[{ts}] {msg}"
    def _append():
        terminal.configure(state=NORMAL)
        terminal.insert(END, text + ("\n" if newline else ""))
        terminal.see(END)
        terminal.configure(state=DISABLED)
    app.after(0, _append)

def progress_hook(d):
    progress_queue.put(d)

# Process queue and update UI
last_download_n = 0
last_time = None
def process_progress_queue():
    global last_download_n, last_time
    try:
        while True:
            d = progress_queue.get_nowait()
            status = d.get("status", "")
            if status == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
                downloaded = d.get("downloaded_bytes") or 0
                now = time.time()
                if last_time is None:
                    last_time = now
                    last_download_n = downloaded
                    speed = 0.0
                else:
                    dt = now - last_time if (now - last_time) > 0 else 1
                    speed = (downloaded - last_download_n) / dt
                    last_time = now
                    last_download_n = downloaded
                percent = (downloaded / total) if total else 0
                progress_bar.set(percent)
                progress_label_var.set(f"Progress: {percent*100:.2f}%")
                speed_kb = speed / 1024.0
                speed_var.set(f"Speed: {speed_kb:.1f} KB/s")
                eta = "--:--"
                if speed > 50 and total and downloaded < total:
                    secs = (total - downloaded) / speed
                    eta = time.strftime("%H:%M:%S", time.gmtime(secs))
                eta_var.set(f"ETA: {eta}")
                if int(percent*100) % 5 == 0:
                    log(f"downloading... {percent*100:.2f}%")
            elif status == "finished":
                progress_bar.set(1.0)
                progress_label_var.set("Progress: 100.00%")
                speed_var.set("Speed: 0 KB/s")
                eta_var.set("ETA: 00:00:00")
                log("Download finished, processing file...")
                app.after(0, lambda: messagebox.showinfo("Selesai", "Download complete"))
            elif status == "error":
                log("ERROR: " + str(d.get("error", "unknown")))
            else:
                log(f"status: {status}")
    except queue.Empty:
        pass
    app.after(250, process_progress_queue)

app.after(250, process_progress_queue)

# -------------------- Fetch info & preview --------------------
def ambil_resolusi_preview_sync(url):
    info_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

def ambil_resolusi_preview():
    url = url_var.get().strip()
    if not url:
        messagebox.showwarning("No URL", "Masukkan URL dulu.")
        return
    try:
        log("Fetching video info...")
        info = ambil_resolusi_preview_sync(url)
        formats = [f for f in info.get('formats', []) if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
        available_res = []
        for f in formats:
            res = f.get('format_note') or f.get('height')
            if res and str(res) not in available_res:
                available_res.append(str(res))
        if "best" not in available_res:
            available_res.append("best")
        def set_res():
            res_menu.configure(values=available_res)
            res_var.set("best")
        app.after(0, set_res)
        title = info.get("title", "Unknown")
        app.after(0, lambda: title_var.set(title))
        thumb = info.get("thumbnail")
        if thumb:
            try:
                r = requests.get(thumb, timeout=10)
                img = Image.open(BytesIO(r.content)).convert("RGBA")
                img.thumbnail((360, 200))
                tkimg = ImageTk.PhotoImage(img)
                def set_thumb():
                    thumbnail_placeholder.configure(image=tkimg, text="")
                    thumbnail_placeholder.image = tkimg
                app.after(0, set_thumb)
            except Exception as e:
                log(f"Failed to fetch thumbnail: {e}")
        log(f"Fetched info: {title}")
    except Exception as e:
        log(f"Failed to fetch info: {e}")
        messagebox.showerror("Fetch failed", f"Gagal ambil info: {e}")

# -------------------- Download logic (thread) --------------------
def build_ydl_opts(jenis, fmt, output_folder, playlist_mode, resolution):
    """Membangun opsi yt-dlp berdasarkan pilihan GUI."""
    opts = {
        # output_folder digunakan di sini
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'quiet': True,
        'noplaylist': not playlist_mode,
        'no_warnings': True,
    }
    if jenis == "audio":
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': fmt,
                'preferredquality': '192',
            }],
        })
    else:
        if resolution == "best":
            opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': fmt
            })
        else:
            try:
                h = int(resolution)
                opts.update({
                    'format': f'bestvideo[height<={h}]+bestaudio/best',
                    'merge_output_format': fmt
                })
            except:
                opts.update({
                    'format': f'bestvideo+bestaudio/best',
                    'merge_output_format': fmt
                })
    return opts

def mulai_download_thread():
    url = url_var.get().strip()
    if not url:
        messagebox.showwarning("Missing URL", "Masukkan URL terlebih dahulu.")
        return
    
    # Pastikan folder target ada sebelum memulai download
    output_folder = output_folder_var.get()
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        log(f"Error creating folder {output_folder}: {e}")
        app.after(0, lambda: messagebox.showerror("Folder Error", f"Gagal membuat folder: {e}"))
        return
        
    jenis = jenis_var.get()
    fmt = format_var.get()
    playlist_mode = playlist_var.get()
    resolution = res_var.get()
    log(f"Start: jenis={jenis} format={fmt} playlist={playlist_mode} res={resolution}")

    def run():
        try:
            opts = build_ydl_opts(jenis, fmt, output_folder, playlist_mode, resolution)
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Cek apakah folder output_folder_var.get() ada
                final_output_path = output_folder_var.get()
                if not os.path.exists(final_output_path):
                    raise FileNotFoundError(f"Folder penyimpanan tidak ditemukan: {final_output_path}")

                ydl.download([url])
                
            log(f"Saved to: {output_folder}")
            try:
                # Log download ke riwayat file
                info = ambil_resolusi_preview_sync(url)
                title = sanitize_filename(info.get("title", "video"))
                log_download(title, output_folder)
            except Exception:
                pass
        except Exception as e:
            log(f"Download error: {e}")
            app.after(0, lambda: messagebox.showerror("Download Error", str(e)))

    threading.Thread(target=run, daemon=True).start()

# -------------------- Finalization --------------------
def on_close():
    matrix.running = False
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)

log("Soft Hacker UI ready.")
app.mainloop()
