# Dashboard ISA

Situs GitHub Pages yang menggabungkan dashboard PT. Inti Selera Asia dalam satu link:

| Halaman | Folder | Sumber (artifact claude.ai) |
|---|---|---|
| Menu | `index.html` | – |
| Dashboard Pimpinan | `pimpinan/` | https://claude.ai/artifact/4jTCwC5zA6pjcxgkeKES1K |
| Produksi CPU | `produksi-cpu/` | https://claude.ai/artifact/53KNxmb2Cf75vbjb8rQZZM |
| Pembelian | `pembelian/` | https://claude.ai/artifact/CoXN6FbQReHPH17x6A55gF |
| Gaji Harian | `gaji-harian/` | https://claude.ai/artifact/FwqpoE8LSkw8bjQjumMtbk |
| Absensi Outlet | tautan keluar | Google Apps Script web app |

## Penting
- Situs GitHub Pages bisa dibuka siapa pun yang tahu link-nya. `robots.txt` dan meta `noindex` hanya meminta mesin pencari tidak mengindeks, bukan pengaman.
- Halaman di sini adalah salinan statis. Pengambilan data langsung dari Google Drive/Sheets dan tombol "Refresh data" hanya berjalan di versi claude.ai.

## Memperbarui data
1. Perbarui dashboard di claude.ai seperti biasa.
2. Ambil HTML terbaru tiap artifact (Artifact `read`), simpan sebagai file.
3. Jalankan dari folder repo (argumen yang tidak diberikan dilewati):
   ```
   python3 tools/build_site.py --pimpinan pimpinan.html --cpu cpu.html --pembelian pembelian.html --gaji gaji.html
   ```
   Skrip menambahkan bar navigasi, meta noindex, cadangan unduhan CSV di Pembelian, dan memperbarui tanggal data di menu.
4. Commit dan push ke branch `main`. GitHub Pages memperbarui situs dalam 1–2 menit.
