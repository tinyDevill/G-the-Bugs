# G-THE BUGS

![Imej G-THE BUGS Gameplay](https://placehold.co/800x400/1a1d24/a9dfd8?text=G-THE+BUGS&font=cinzel)

Selamat datang ke dunia "G-THE BUGS", sebuah game platformer 2D yang penuh aksi dan petualangan. Kendalikan seorang ksatria serangga yang gagah berani dalam perjalanannya melalui dunia yang misterius dan berbahaya untuk menghadapi kegelapan yang mengancam.

---

## 📜 Cerita

Di sebuah dunia kecil yang dihuni oleh berbagai jenis serangga, kedamaian telah hancur oleh entitas jahat yang dikenal sebagai **The Void**. Kegelapan ini merayap ke seluruh negeri, merusak pikiran dan jiwa para penghuninya, mengubah mereka menjadi makhluk tanpa pikiran yang ganas.

Di tengah kekacauan ini, muncullah seorang pahlawan—seorang ksatria serangga yang tak kenal takut. Berbekal pedang dan keberanian, dia memulai misi berbahaya untuk melakukan perjalanan ke jantung kegelapan, menghadapi para pengikut The Void yang rusak, dan akhirnya mengalahkan sumber dari segala kejahatan itu sendiri. Akankah sang ksatria berhasil mengembalikan cahaya ke dunianya, atau akankah dia juga ditelan oleh kehampaan abadi?

---

## ✨ Fitur Utama

-   **Eksplorasi Platformer Klasik:** Lompat, lari, dan berjuang melewati berbagai level yang dirancang dengan cermat, masing-masing dengan tantangan dan musuh yang unik.
-   **Sistem Pertarungan Cepat:** Gunakan serangan pedang cepat untuk mengalahkan berbagai musuh yang menghalangi jalan Anda.
-   **Dunia Multi-Scene:** Jelajahi 5 scene atau level yang berbeda, mulai dari kuil kuno hingga gua-gua gelap, masing-masing dengan latar belakang dan atmosfernya sendiri.
-   **Interaksi dengan NPC:** Temui berbagai karakter Non-Playable (NPC) di sepanjang perjalanan Anda. Bicaralah dengan mereka untuk mengungkap pengetahuan, mendapatkan petunjuk, atau bahkan memicu peristiwa unik.
-   **Sistem Progresi Cerita:** Kemajuan Anda dipengaruhi oleh interaksi dengan NPC dan mengalahkan musuh, membuka jalan baru dan kelanjutan cerita.
-   **Musuh yang Menantang:** Hadapi musuh standar dan bos mini seperti "Witcher" yang dapat menembakkan proyektil.
-   **Mekanik Penyembuhan:** Pulihkan kesehatan secara otomatis setelah beberapa saat tidak menerima kerusakan, mendorong permainan yang strategis.

---

## ⌨️ Kontrol

-   **Gerak Kiri:** Tombol Panah Kiri
-   **Gerak Kanan:** Tombol Panah Kanan
-   **Lompat:** Tombol Spasi
-   **Serang:** Tombol Z
-   **Berinteraksi dengan NPC:** Tombol E
-   **Jeda Permainan:** Tombol ESC

---

## 🛠️ Teknologi yang Digunakan

-   **Bahasa:** Python 3
-   **Library:** Pygame

---

## 🚀 Cara Menjalankan Game

Untuk memainkan "G-THE BUGS" di komputer Anda, ikuti langkah-langkah berikut:

### 1. Prasyarat

Pastikan Anda telah menginstal **Python 3** di sistem Anda. Anda juga memerlukan library **Pygame**.

### 2. Instalasi

1.  **Clone repositori ini (atau unduh file ZIP):**
    ```bash
    git clone [https://github.com/NAMA_USER_ANDA/NAMA_REPOSITORI_ANDA.git](https://github.com/NAMA_USER_ANDA/NAMA_REPOSITORI_ANDA.git)
    cd NAMA_REPOSITORI_ANDA
    ```

2.  **Instal Pygame:**
    Buka terminal atau command prompt Anda dan jalankan perintah berikut:
    ```bash
    pip install pygame
    ```

3.  **Pastikan Aset Tersedia:**
    Game ini memerlukan folder `assets/image/` di direktori yang sama dengan file `.py`. Pastikan semua gambar yang diperlukan ada di dalam folder ini dengan struktur yang benar.

### 3. Menjalankan Game

Setelah instalasi selesai, jalankan game dengan mengeksekusi file `main.py`:
```bash
python main.py
```

---

## 📂 Struktur Proyek

Proyek ini diorganisir ke dalam beberapa file Python untuk menjaga agar kode tetap bersih dan terkelola:

-   `main.py`: Titik masuk utama untuk memulai permainan.
-   `game.py`: Berisi loop permainan utama, manajemen state (menu, bermain, jeda), penanganan input, dan orkestrasi semua elemen game.
-   `character.py`: Mendefinisikan kelas `Player`, menangani gerakan, serangan, animasi, dan status pemain.
-   `enemy.py`: Mendefinisikan kelas `Enemy`, mengontrol perilaku patroli, serangan, dan status musuh.
-   `npc.py`: Mendefinisikan kelas `NPC` dan bos mini `WitcherNPC`, mengelola dialog dan interaksi khusus.
-   `gameobject.py`: Berisi kelas dasar seperti `GameObject`, `Platform`, `Animation`, dan `Projectile`.
-   `scene_config.py`: Mengkonfigurasi setiap level/scene, termasuk layout platform, penempatan NPC dan musuh, serta pemicu transisi.
-   `screen.py`: Menangani pemuatan aset, manajemen kamera, dan fungsi-fungsi rendering seperti menggambar objek dan latar belakang.
-   `animation.py`: Kelas sederhana untuk mengelola animasi berbasis frame.
