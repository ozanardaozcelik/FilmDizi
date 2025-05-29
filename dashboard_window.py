import tkinter as tk
from tkinter import messagebox
from dashboard import open_dashboard

DOĞRU_ŞİFRE = "dostinyo"
RENK_ARKA = "#2C3E50"
RENK_KUTU = "#34495E"
YAZI_RENGİ = "#ECF0F1"
RENK_BUTON = "#1ABC9C"

def giris_ekrani():
    def check_password():
        if sifre_entry.get() == DOĞRU_ŞİFRE:
            giris.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Şifre Hatalı", "Yanlış şifre dostinyo 👀")

    giris = tk.Tk()
    giris.title("FILMINYO | Giriş")
    giris.geometry("400x250")
    giris.configure(bg=RENK_ARKA)

    frame = tk.Frame(giris, bg=RENK_KUTU, bd=2, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=180)

    tk.Label(frame, text="Şifreyi Gir Dostinyo", font=("Segoe UI", 13, "bold"), fg=YAZI_RENGİ, bg=RENK_KUTU).pack(pady=12)
    sifre_entry = tk.Entry(frame, show="*", font=("Segoe UI", 12), justify="center", bg=RENK_ARKA, fg=YAZI_RENGİ, insertbackground=YAZI_RENGİ, relief="flat")
    sifre_entry.pack(ipady=6, ipadx=10, pady=8)
    tk.Button(frame, text="Giriş Yap", command=check_password, font=("Segoe UI", 11), bg=RENK_BUTON, fg="white", relief="flat", width=20).pack(pady=10)

    giris.mainloop()
