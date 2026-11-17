import os
import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "laporan_xdof.db"
DEFAULT_IMPLEMENTOR = "Rachmat Trisnanto"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS laporan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            jenis TEXT,
            implementor TEXT,
            nama_partner TEXT,
            partname TEXT,
            sales TEXT,
            device TEXT,
            kode TEXT,
            sdcard_lama TEXT,
            sdcard_baru TEXT,
            kelengkapan TEXT,
            status TEXT,
            alasan TEXT,
            teks_wa TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salin_ke_clipboard(teks):
    try:
        import pyperclip
        pyperclip.copy(teks)
        print("\n[INFO] Teks berhasil disalin ke clipboard HP! Tinggal Paste di WhatsApp.")
    except:
        print("\n[INFO] Modul pyperclip belum aktif, silakan copy manual teks di bawah.")

def tambah_data(data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO laporan (tanggal, jenis, implementor, nama_partner, partname, sales, device, kode, sdcard_lama, sdcard_baru, kelengkapan, status, alasan, teks_wa)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('tanggal'), data.get('jenis'), data.get('implementor'),
        data.get('nama_partner'), data.get('partname'), data.get('sales'),
        data.get('device'), data.get('kode'), data.get('sdcard_lama'),
        data.get('sdcard_baru'), data.get('kelengkapan'), data.get('status'),
        data.get('alasan'), data.get('teks_wa')
    ))
    conn.commit()
    conn.close()

def ambil_semua_data():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laporan")
    rows = cursor.fetchall()
    conn.close()
    return rows

def hapus_data_by_id(data_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM laporan WHERE id = ?", (data_id,))
    conn.commit()
    conn.close()

def reset_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS laporan")
    conn.commit()
    conn.close()
    init_db()

def get_default_tanggal():
    bulan_indo = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
        7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }
    now = datetime.now()
    return f"{now.day} {bulan_indo[now.month]} {now.year}"

def input_status_pilihan():
    print("\nPilih Status:")
    print("1. Done✅")
    print("2. Reschedule")
    print("3. CANCEL ❌")
    print("4. Status Lainnya (Ketik Manual)")
    pilih = input("Pilih (1-4): ").strip()
    
    if pilih == '1':
        return "Done✅"
    elif pilih == '2':
        keterangan = input("Masukkan keterangan reschedule (cth: sedang di luar kota): ").strip()
        if keterangan:
            return f"Reschedule ({keterangan})"
        return "Reschedule"
    elif pilih == '3':
        keterangan = input("Masukkan alasan cancel (cth: mitra sudah tidak ada respon): ").strip()
        if keterangan:
            return f"CANCEL ❌ ({keterangan})"
        return "CANCEL ❌"
    else:
        return input("Masukkan status manual: ").strip()

def menu_input_laporan():
    os.system('clear')
    print("========================================")
    print("         PILIH JENIS LAPORAN            ")
    print("========================================")
    print("1. Hand Over")
    print("2. Take Over")
    print("3. Switch Device")
    print("4. Switch SD Card")
    print("5. Kembali ke Menu Utama")
    
    pilihan = input("\nPilih (1-5): ").strip()
    if pilihan not in ['1', '2', '3', '4']:
        return

    default_tgl = get_default_tanggal()
    input_tgl = input(f"Tanggal [{default_tgl}] (Tekan Enter jika sesuai): ").strip()
    tanggal = input_tgl if input_tgl else default_tgl

    input_impl = input(f"Nama Implementor [{DEFAULT_IMPLEMENTOR}] (Tekan Enter jika sesuai): ").strip()
    implementor = input_impl if input_impl else DEFAULT_IMPLEMENTOR

    if pilihan in ['1', '2', '3']:
        nama = input("Nama Partner: ")
        partname = input("Partname: ")
        
        if pilihan in ['1', '2']:
            jenis_str = "Hand Over" if pilihan == '1' else "Take Over"
            sales = input("Sales: ")
            device = input("Device (kosongkan jika tidak ada): ")
            kode = input("Kode (kosongkan jika tidak ada): ")
            kelengkapan = input("Kelengkapan: ")
            status = input_status_pilihan()
            
            teks_wa = f"Rekap {jenis_str} {tanggal}\nImplementor : {implementor}\n\nNama Partner : {nama}\n- partname : {partname}\n- Sales : {sales}\n- Device : {device}\n- Kode : {kode}\n- Kelengkapan : {kelengkapan}\n- Status : {status}\n____________________________________________"
            
            tambah_data({
                "tanggal": tanggal, "jenis": jenis_str, "implementor": implementor,
                "nama_partner": nama, "partname": partname, "sales": sales,
                "device": device, "kode": kode, "sdcard_lama": "", "sdcard_baru": "",
                "kelengkapan": kelengkapan, "status": status, "alasan": "", "teks_wa": teks_wa
            })
            
        elif pilihan == '3': # Switch Device
            alasan = input("Alasan Switch (cth: device bermasalah kameranya): ")
            device = input("Device (cth: dscap-mini To ego-dscap): ")
            kelengkapan = input("Kelengkapan: ")
            status = input_status_pilihan()
            
            teks_wa = f"Rekap SWITCH DEVICE {tanggal}\nImplementor : {implementor}\n\n- Nama Partner : {nama}\n- partname : {partname}\n- Switch karna ({alasan})\n- Device : {device}\n- Kelengkapan : {kelengkapan}\n- Status : {status}\n____________________________________________"
            
            tambah_data({
                "tanggal": tanggal, "jenis": "Switch Device", "implementor": implementor,
                "nama_partner": nama, "partname": partname, "sales": "",
                "device": device, "kode": "", "sdcard_lama": "", "sdcard_baru": "",
                "kelengkapan": kelengkapan, "status": status, "alasan": alasan, "teks_wa": teks_wa
            })

    elif pilihan == '4': # Switch SD Card
        list_sd = []
        while True:
            print(f"\n[ Partner SD Card ke-{len(list_sd) + 1} ]")
            nama_partner = input("Nama Partner: ")
            partname_sd = input("Partname: ")
            sd_lama = input("SDcard lama: ")
            sd_baru = input("SDcard Baru: ")
            status_sd = input_status_pilihan()
            
            list_sd.append({
                "nama": nama_partner, 
                "partname": partname_sd, 
                "sd_lama": sd_lama, 
                "sd_baru": sd_baru, 
                "status": status_sd
            })
            if input("Tambah partner SD Card lagi? (y/n): ").strip().lower() != 'y':
                break
        
        teks_wa = f"Rekap Switch SD CARD {tanggal}\nImplementor : {implementor}\n"
        for s in list_sd:
            teks_wa += f"\n- Nama patner : {s['nama']}\n- Patrname : {s['partname']}\n- SDcard lama : {s['sd_lama']}\n- SDcard Baru : {s['sd_baru']}\n- Status : {s['status']}\n"
        
        for s in list_sd:
            tambah_data({
                "tanggal": tanggal, "jenis": "Switch SD Card", "implementor": implementor,
                "nama_partner": s['nama'], "partname": s['partname'], "sales": "",
                "device": "", "kode": "", "sdcard_lama": s['sd_lama'], "sdcard_baru": s['sd_baru'],
                "kelengkapan": "", "status": s['status'], "alasan": "", "teks_wa": teks_wa if s == list_sd[0] else ""
            })

    input("\n[Sukses] Data berhasil disimpan ke Database SQLite! Tekan Enter...")

def lihat_dan_finalisasi():
    rows = ambil_semua_data()
    if not rows:
        input("\n[Peringatan] Belum ada data tersimpan! Tekan Enter...")
        return

    tgl_filter = input(f"\nMasukkan tanggal yang ingin ditampilkan (Tekan Enter untuk tanggal hari ini [{get_default_tanggal()}], atau ketik 'ALL' untuk semua): ").strip()
    
    if tgl_filter == '':
        tgl_filter = get_default_tanggal()
    elif tgl_filter.upper() == 'ALL':
        tgl_filter = ''

    list_teks = []
    filtered_rows = [r for r in rows if not tgl_filter or tgl_filter.lower() in r['tanggal'].lower()]

    if not filtered_rows:
        input("\n[Info] Tidak ada data pada tanggal tersebut. Tekan Enter...")
        return

    for r in filtered_rows:
        if r['jenis'] == 'Switch SD Card':
            list_teks.append(f"Rekap Switch SD CARD {r['tanggal']}\nImplementor : {r['implementor']}\n\n- Nama patner : {r['nama_partner']}\n- Patrname : {r['partname']}\n- SDcard lama : {r['sdcard_lama']}\n- SDcard Baru : {r['sdcard_baru']}\n- Status : {r['status']}")
        else:
            list_teks.append(r['teks_wa'])

    total_partner = len(filtered_rows)
    done_count = sum(1 for r in filtered_rows if "DONE" in r['status'].upper() or "DONE✅" in r['status'].replace(" ", "").upper())
    
    ringkasan_footer = f"\n\n📊 **Ringkasan Hari Ini:**\n- Total Kunjungan: {total_partner}\n- Done: {done_count} ✅\n- Lainnya: {total_partner - done_count}\n\nIzin cc pak"
    
    rekap_final = "\n\n".join(list_teks) + ringkasan_footer
    
    os.system('clear')
    print("========================================")
    print("      REKAP SIAP KIRIM KE WHATSAPP      ")
    print("========================================")
    print(rekap_final)
    print("========================================")
    
    salin_ke_clipboard(rekap_final)
    input("\nTekan Enter untuk kembali ke menu...")

def export_excel():
    rows = ambil_semua_data()
    if not rows:
        input("\n[Peringatan] Belum ada data untuk diexport! Tekan Enter...")
        return

    nama_file = input("\nMasukkan nama file Excel (cth: Rekap_November_2026.xlsx): ").strip()
    if not nama_file.endswith(".xlsx"):
        nama_file += ".xlsx"

    data_ho, data_to, data_switch, data_sd = [], [], [], []

    for r in rows:
        item = dict(r)
        jns = item.get("jenis")
        if jns == "Hand Over": data_ho.append(item)
        elif jns == "Take Over": data_to.append(item)
        elif jns == "Switch Device": data_switch.append(item)
        elif jns == "Switch SD Card": data_sd.append(item)

    try:
        with pd.ExcelWriter(nama_file, engine='openpyxl') as writer:
            if data_ho: pd.DataFrame(data_ho).drop(columns=["id", "teks_wa", "alasan", "sdcard_lama", "sdcard_baru"], errors="ignore").to_excel(writer, sheet_name="Hand Over", index=False)
            if data_to: pd.DataFrame(data_to).drop(columns=["id", "teks_wa", "alasan", "sdcard_lama", "sdcard_baru"], errors="ignore").to_excel(writer, sheet_name="Take Over", index=False)
            if data_switch: pd.DataFrame(data_switch).drop(columns=["id", "teks_wa", "sdcard_lama", "sdcard_baru"], errors="ignore").to_excel(writer, sheet_name="Switch Device", index=False)
            if data_sd: pd.DataFrame(data_sd).drop(columns=["id", "teks_wa", "alasan", "sales", "device", "kode", "kelengkapan"], errors="ignore").to_excel(writer, sheet_name="Switch SD Card", index=False)

        print(f"\n[SUKSES] File Excel berhasil dibuat dengan sheet terpisah: {nama_file}")
    except Exception as e:
        print(f"\n[GAGAL] Terjadi kesalahan: {e}")

    input("\nTekan Enter untuk kembali ke menu...")

def kelola_hapus_data():
    rows = ambil_semua_data()
    if not rows:
        input("\n[Peringatan] Database kosong! Tekan Enter...")
        return

    os.system('clear')
    print("========================================")
    print("          KELOLA / HAPUS DATA           ")
    print("========================================")
    for r in rows:
        print(f"ID: {r['id']} | Tgl: {r['tanggal']} | Jenis: {r['jenis']} | Partner: {r['nama_partner']} | Status: {r['status']}")
    print("========================================")
    
    id_hapus = input("\nMasukkan ID data yang ingin dihapus (atau ketik 0 untuk batal): ").strip()
    if id_hapus.isdigit() and int(id_hapus) > 0:
        hapus_data_by_id(int(id_hapus))
        input(f"\n[Sukses] Data dengan ID {id_hapus} berhasil dihapus! Tekan Enter...")

def main():
    init_db()
    while True:
        os.system('clear')
        rows = ambil_semua_data()
        
        print("========================================")
        print("     XDOF REPORT SYSTEM (SQLITE)        ")
        print("========================================")
        print(f"📌 [STATUS] {len(rows)} total entri tersimpan di database.")
        print("========================================")
        print("1. Tambah Laporan Baru (HO/TO/Switch/SD)")
        print("2. Lihat & Finalisasi Rekap WhatsApp")
        print("3. Export Rekap ke Excel (Sheet Terpisah)")
        print("4. Hapus Data Tertentu (Per-Item)")
        print("5. Reset / Kosongkan Seluruh Database")
        print("6. Keluar")
        
        pilihan = input("\nPilih menu (1-6): ").strip()
        
        if pilihan == '1':
            menu_input_laporan()
        elif pilihan == '2':
            lihat_dan_finalisasi()
        elif pilihan == '3':
            export_excel()
        elif pilihan == '4':
            kelola_hapus_data()
        elif pilihan == '5':
            konfirmasi = input("Yakin ingin menghapus SELURUH database? (y/n): ").strip().lower()
            if konfirmasi == 'y':
                reset_database()
                input("\nDatabase berhasil dikosongkan! Tekan Enter...")
        elif pilihan == '6':
            print("\nProgram ditutup. Data Anda aman tersimpan di SQLite.")
            break

if __name__ == "__main__":
    main()