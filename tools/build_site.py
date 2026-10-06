#!/usr/bin/env python3
"""Bangun situs GitHub Pages "Dashboard ISA" dari file HTML artifact claude.ai.

Pakai (dari folder repo):
  python3 tools/build_site.py --pimpinan A.html --cpu B.html --pembelian C.html --gaji D.html

Setiap file adalah halaman artifact apa adanya (hasil Artifact read). Skrip ini:
  - menyalin tiap halaman ke foldernya (pimpinan/, produksi-cpu/, pembelian/, gaji-harian/),
  - menambahkan bar navigasi antar halaman dan meta noindex,
  - memberi cadangan unduhan CSV biasa di Dashboard Pembelian,
  - memperbarui tanggal data di halaman menu (index.html, di antara penanda ASOF).
Argumen yang tidak diberikan dilewati, jadi satu dashboard bisa diperbarui sendiri.
"""
import argparse, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    ('pimpinan', 'pimpinan', 'Pimpinan'),
    ('cpu', 'produksi-cpu', 'Produksi CPU'),
    ('pembelian', 'pembelian', 'Pembelian'),
    ('gaji', 'gaji-harian', 'Gaji Harian'),
]
ABSENSI = 'https://script.google.com/macros/s/AKfycbxP97nMJzQncOaqQW48dLaUP78PRFDgGwmjU3X4b8qvZI9eTSqAyTmK7IWO8bn-7zKQ/exec'

NAV_CSS = """<style id="isa-nav-css">
.isa-nav{--n-bg:#1b2130;--n-ink:#e7eaf0;--n-mute:#9aa3b5;--n-on:#ffffff;--n-pill:#2c3445;
  background:var(--n-bg);color:var(--n-ink);font:600 13px/1.3 "Figtree","Segoe UI",system-ui,sans-serif;
  padding:8px 16px;padding-top:calc(8px + env(safe-area-inset-top,0px));display:flex;flex-wrap:wrap;align-items:center;gap:6px 14px}
.isa-nav a{color:var(--n-mute);text-decoration:none;padding:4px 10px;border-radius:999px;white-space:nowrap}
.isa-nav a:hover{color:var(--n-on);background:var(--n-pill)}
.isa-nav a:focus-visible{outline:2px solid var(--n-on);outline-offset:2px}
.isa-nav a[aria-current="page"]{color:var(--n-on);background:var(--n-pill)}
.isa-nav .home{color:var(--n-on);padding-left:0;font-weight:700;letter-spacing:.02em}
.isa-nav .home:hover{background:none;text-decoration:underline;text-underline-offset:3px}
.isa-nav .links{display:flex;flex-wrap:wrap;gap:4px}
@media (max-width:600px){.isa-nav{font-size:12px}.isa-nav a{padding:4px 8px}}
</style>"""


def nav(current):
    cur = ' aria-current="page"'
    links = ''.join(
        '<a href="../%s/"%s>%s</a>' % (slug, cur if slug == current else '', label)
        for _, slug, label in PAGES)
    return (f'<nav class="isa-nav" aria-label="Dashboard ISA"><a class="home" href="../">← Dashboard ISA</a>'
            f'<span class="links">{links}<a href="{ABSENSI}" target="_blank" rel="noopener">Absensi ↗</a></span></nav>')


def patch(html, slug):
    head = '<meta name="robots" content="noindex,nofollow">' + NAV_CSS
    if slug == 'gaji-harian':  # body halaman ini ber-padding 20px 16px; tarik bar ke tepi
        head += '<style>.isa-nav{margin:-20px -16px 16px}</style>'
    i = html.find('<head>')
    if i < 0:
        sys.exit(f'{slug}: tag <head> tidak ditemukan')
    html = html[:i + 6] + head + html[i + 6:]
    j = html.find('<body>')
    if j < 0:
        sys.exit(f'{slug}: tag <body> tidak ditemukan')
    html = html[:j + 6] + nav(slug) + html[j + 6:]
    if slug == 'pembelian':
        old = "const dl=await getDl();const btn=document.getElementById('itCsv');if(!dl){btn.hidden=true;return}"
        new = ("const dl=await getDl();const btn=document.getElementById('itCsv');"
               "if(!dl){const u=URL.createObjectURL(new Blob(['\\ufeff'+lines.join('\\r\\n')],{type:'text/csv;charset=utf-8'}));"
               "const a=document.createElement('a');a.href=u;a.download=`pembelian_${it[0]}.csv`;document.body.appendChild(a);a.click();a.remove();"
               "setTimeout(()=>URL.revokeObjectURL(u),2000);return}")
        if old in html:
            html = html.replace(old, new)
        else:
            print('peringatan: kode CSV Pembelian tidak dikenali, cadangan unduhan tidak dipasang', file=sys.stderr)
    return html


def asof(key, html):
    pats = {
        'pimpinan': r'const ASOF="([^"]+)"',
        'cpu': r'const META=\{[^}]*?"asof":\s*"([^"]+)"',
        'pembelian': r'const SNAP=\{"ASOF":"([^"]+)"',
        'gaji': r'const SNAP = \{"at":"([^"]+)"',
    }
    m = re.search(pats[key], html)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    for key, _, _ in PAGES:
        ap.add_argument('--' + key)
    a = ap.parse_args()
    idx_path = os.path.join(ROOT, 'index.html')
    idx = open(idx_path, encoding='utf-8').read()
    done = 0
    for key, slug, label in PAGES:
        src = getattr(a, key)
        if not src:
            continue
        html = open(src, encoding='utf-8').read()
        d = asof(key, html)
        out = os.path.join(ROOT, slug)
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(patch(html, slug))
        if d:
            idx = re.sub(r'(<!--ASOF:%s-->).*?(<!--/ASOF-->)' % key, lambda m: m.group(1) + d + m.group(2), idx)
        print(f'OK {slug}: {len(html):,} byte, data {d or "?"}')
        done += 1
    open(idx_path, 'w', encoding='utf-8').write(idx)
    if not done:
        print('Tidak ada halaman yang diberikan.')


if __name__ == '__main__':
    main()
