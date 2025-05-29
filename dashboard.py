import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DOSYA_ADI = "data.json"
RENK_ARKA = "#2C3E50"
RENK_KUTU = "#34495E"
YAZI_RENGİ = "#ECF0F1"
RENK_BUTON = "#1ABC9C"

def load_data():
    if not os.path.exists(DOSYA_ADI):
        return []
    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def open_dashboard():
    data = load_data()
    sirala_azalan = {"Tür": False, "Ad": False, "Not": False, "Puan": True}

    def listeyi_guncelle(filtre=None, sirala=None):
        liste.delete(*liste.get_children())
        liste_data = data[:]
        if filtre:
            filtre_lower = filtre.lower()
            liste_data = [item for item in liste_data if any(filtre_lower in str(v).lower() for v in item.values())]
        if sirala:
            key, ters = sirala
            if key == "Puan":
                liste_data.sort(key=lambda x: x.get('puan', 0), reverse=ters)
            elif key == "Tür":
                liste_data.sort(key=lambda x: x.get('tür', '').lower(), reverse=ters)
            elif key == "Ad":
                liste_data.sort(key=lambda x: x.get('ad', '').lower(), reverse=ters)
            elif key == "Not":
                liste_data.sort(key=lambda x: x.get('not', '').lower(), reverse=ters)
        for i, item in enumerate(liste_data):
            if isinstance(item, dict) and 'tür' in item and 'ad' in item and 'not' in item and 'puan' in item:
                liste.insert("", "end", iid=i, values=(item['tür'], item['ad'], item['not'], item['puan']))

    def arama_yap():
        filtre = arama_entry.get()
        listeyi_guncelle(filtre=filtre)

    def baslika_tiklandi(event):
        col = liste.identify_column(event.x)
        col_index = int(col.replace('#', '')) - 1
        columns = ["Tür", "Ad", "Not", "Puan"]
        if col_index < 0 or col_index >= len(columns):
            return
        secilen_sutun = columns[col_index]
        sirala_azalan[secilen_sutun] = not sirala_azalan[secilen_sutun]
        listeyi_guncelle(sirala=(secilen_sutun, sirala_azalan[secilen_sutun]))

    def icerik_ekle():
        def kaydet():
            try:
                puan = float(entry_puan.get())
                if not (1 <= puan <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Geçersiz Puan", "Puan 1 ile 10 arasında bir sayı olmalı.")
                return
            yeni = {
                "tür": combo_tur.get(),
                "ad": entry_ad.get(),
                "not": entry_not.get("1.0", "end").strip(),
                "puan": puan
            }
            data.append(yeni)
            save_data(data)
            listeyi_guncelle()
            pencere.destroy()

        pencere = tk.Toplevel(dash)
        pencere.title("İçerik Ekle")
        pencere.configure(bg=RENK_KUTU)
        tk.Label(pencere, text="Tür", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        combo_tur = ttk.Combobox(pencere, values=["Film", "Dizi", "Sitcom"])
        combo_tur.pack()
        tk.Label(pencere, text="Ad", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        entry_ad = tk.Entry(pencere)
        entry_ad.pack()
        tk.Label(pencere, text="Not", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        entry_not = tk.Text(pencere, height=4)
        entry_not.pack()
        tk.Label(pencere, text="Puan (1-10)", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        entry_puan = tk.Entry(pencere)
        entry_puan.pack()
        tk.Button(pencere, text="Kaydet", command=kaydet, bg=RENK_BUTON, fg="white").pack(pady=5)

    def sil():
        secilen = liste.focus()
        if secilen:
            try:
                index = int(secilen)
                data.pop(index)
                save_data(data)
                listeyi_guncelle()
            except:
                messagebox.showerror("Hata", "Silme işlemi başarısız oldu.")

    def duzenle():
        secilen = liste.focus()
        if not secilen:
            return
        eski = data[int(secilen)]

        def kaydet():
            try:
                puan = float(entry_puan.get())
                if not (1 <= puan <= 10):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Geçersiz Puan", "Puan 1 ile 10 arasında bir sayı olmalı.")
                return
            yeni = {
                "tür": combo_tur.get(),
                "ad": entry_ad.get(),
                "not": entry_not.get("1.0", "end").strip(),
                "puan": puan
            }
            data[int(secilen)] = yeni
            save_data(data)
            listeyi_guncelle()
            pencere.destroy()

        pencere = tk.Toplevel(dash)
        pencere.title("İçeriği Düzenle")
        pencere.configure(bg=RENK_KUTU)
        tk.Label(pencere, text="Tür", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        combo_tur = ttk.Combobox(pencere, values=["Film", "Dizi", "Sitcom"])
        combo_tur.set(eski['tür'])
        combo_tur.pack()
        tk.Label(pencere, text="Ad", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        entry_ad = tk.Entry(pencere)
        entry_ad.insert(0, eski['ad'])
        entry_ad.pack()
        tk.Label(pencere, text="Not", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        entry_not = tk.Text(pencere, height=4)
        entry_not.insert("1.0", eski['not'])
        entry_not.pack()
        tk.Label(pencere, text="Puan (1-10)", bg=RENK_KUTU, fg=YAZI_RENGİ).pack()
        entry_puan = tk.Entry(pencere)
        entry_puan.insert(0, eski['puan'])
        entry_puan.pack()
        tk.Button(pencere, text="Kaydet", command=kaydet, bg=RENK_BUTON, fg="white").pack(pady=5)

    global dash
    dash = tk.Tk()
    dash.title("Filminyo Dashboard")
    dash.geometry("900x550")
    dash.configure(bg=RENK_ARKA)
    tk.Label(dash, text="Hoş geldin sadıç 👊", font=("Segoe UI", 16), bg=RENK_ARKA, fg=YAZI_RENGİ).pack(pady=10)
    arama_frame = tk.Frame(dash, bg=RENK_ARKA)
    arama_frame.pack(pady=5)
    arama_entry = tk.Entry(arama_frame, font=("Segoe UI", 10), bg=RENK_KUTU, fg=YAZI_RENGİ, insertbackground=YAZI_RENGİ, width=40)
    arama_entry.pack(side="left", padx=5)
    tk.Button(arama_frame, text="Ara", command=arama_yap, bg=RENK_BUTON, fg="white").pack(side="left")
    liste = ttk.Treeview(dash, columns=("Tür", "Ad", "Not", "Puan"), show="headings")
    for col in ("Tür", "Ad", "Not", "Puan"):
        liste.heading(col, text=col)
        liste.column(col, width=180 if col == "Not" else 100, anchor="center")
    liste.pack(pady=10, fill="both", expand=True)
    liste.bind("<Button-1>", baslika_tiklandi)
    btn_frame = tk.Frame(dash, bg=RENK_ARKA)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Ekle", command=icerik_ekle, width=15, bg=RENK_KUTU, fg=YAZI_RENGİ).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Düzenle", command=duzenle, width=15, bg=RENK_KUTU, fg=YAZI_RENGİ).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Sil", command=sil, width=15, bg=RENK_KUTU, fg=YAZI_RENGİ).grid(row=0, column=2, padx=5)
    listeyi_guncelle()
    dash.mainloop()
