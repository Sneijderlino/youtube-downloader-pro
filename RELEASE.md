# Release Process

Panduan singkat merilis versi baru:

1. Update `CHANGELOG.md` dan pindahkan entri `Unreleased` ke versi yang tepat (contoh: `1.1.0`) dan tambahkan tanggal rilis.
2. Update `version.txt` jika diperlukan.
3. Buat tag git: `git tag -a v1.1.0 -m "Release v1.1.0"` lalu `git push origin --tags`.
4. Buat Release di GitHub dari tag tersebut dan isi dengan ringkasan perubahan dari `CHANGELOG.md`.

Catatan: Pastikan CI lulus sebelum membuat rilis.