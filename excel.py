# excel.py
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment
from urllib.parse import quote

def read_resi_list(file_path):
    """Membaca daftar resi dari file excel input"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} tidak ditemukan!")
    
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
        
    resi_list = df["RESI"].dropna().astype(str).str.strip().tolist()
    return resi_list

def save_to_excel(data_list, output_path):
    """Menyimpan list of dictionary hasil tracking ke Excel dengan hyperlink WhatsApp"""
    if not data_list:
        print("Tidak ada data untuk disimpan.")
        return

    df = pd.DataFrame(data_list)
    
    # Pastikan kolom "Pesan WA" ada
    if "Pesan WA" not in df.columns:
        df["Pesan WA"] = ""

    df.to_excel(output_path, index=False, engine='openpyxl')
    
    wb = load_workbook(output_path)
    ws = wb.active

    # Cari posisi kolom HP dan Pesan WA
    hp_col = None
    pesan_col = None
    for col_idx, col_name in enumerate(ws[1], 1):
        if col_name.value == "HP":
            hp_col = col_idx
        elif col_name.value == "Pesan WA":
            pesan_col = col_idx

    # Jika ada kolom HP dan Pesan WA, tambahkan kolom "Link WA"
    if hp_col is not None and pesan_col is not None:
        # Sisipkan kolom baru setelah Pesan WA
        link_col = pesan_col + 1
        ws.insert_cols(link_col)
        ws.cell(row=1, column=link_col, value="Link WA")

        for row in range(2, ws.max_row + 1):
            hp_cell = ws.cell(row=row, column=hp_col)
            pesan_cell = ws.cell(row=row, column=pesan_col)
            hp_value = hp_cell.value
            pesan_value = pesan_cell.value if pesan_cell.value else ""

            if hp_value and str(hp_value).strip():
                # Bersihkan nomor
                phone = ''.join(filter(str.isdigit, str(hp_value)))
                if phone:
                    if phone.startswith('0'):
                        phone = '62' + phone[1:]
                    # Encode pesan
                    encoded_msg = quote(pesan_value)
                    wa_url = f"https://wa.me/{phone}?text={encoded_msg}"
                    
                    link_cell = ws.cell(row=row, column=link_col)
                    link_cell.value = "Klik WhatsApp"
                    link_cell.hyperlink = wa_url
                    link_cell.font = Font(color="0000FF", underline="single")
                    link_cell.alignment = Alignment(horizontal='center')

        # Lebarkan kolom Link WA
        ws.column_dimensions[get_column_letter(link_col)].width = 18

    # Lebarkan kolom lain
    for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        ws.column_dimensions[col].width = 25

    wb.save(output_path)
    print(f"\n[+] Berhasil menyimpan {len(data_list)} data ke {output_path} dengan link WhatsApp.")