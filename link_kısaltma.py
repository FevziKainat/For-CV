import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pyperclip
import threading

class URLShortener:
    def __init__(self, master):
        self.master = master
        master.title("Gelişmiş Link Kısaltıcı")
        master.geometry("400x300")
        master.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Link Kısaltıcı", font=('Helvetica', 16, 'bold')).pack(pady=10)

        ttk.Label(main_frame, text="Uzun Linki Giriniz:").pack(pady=5)
        self.entry = ttk.Entry(main_frame, width=50)
        self.entry.pack(pady=5)

        self.shorten_button = ttk.Button(main_frame, text="Kısalt", command=self.shorten_url)
        self.shorten_button.pack(pady=10)

        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.pack(fill=tk.X, pady=10)

        self.result_label = ttk.Label(self.result_frame, text="", wraplength=350)
        self.result_label.pack(side=tk.LEFT, padx=(0, 10))

        self.copy_button = ttk.Button(self.result_frame, text="Kopyala", command=self.copy_to_clipboard, state=tk.DISABLED)
        self.copy_button.pack(side=tk.RIGHT)

        self.status_label = ttk.Label(main_frame, text="")
        self.status_label.pack(pady=5)

    def shorten_url(self):
        self.status_label.config(text="İşleniyor...")
        self.shorten_button.config(state=tk.DISABLED)
        threading.Thread(target=self._shorten_url, daemon=True).start()

    def _shorten_url(self):
        long_url = self.entry.get()
        try:
            response = requests.get(f'http://tinyurl.com/api-create.php?url={long_url}')
            response.raise_for_status()
            short_url = response.text
            self.result_label.config(text=f'Kısaltılmış Link: {short_url}')
            self.copy_button.config(state=tk.NORMAL)
            self.status_label.config(text="Başarıyla kısaltıldı!")
        except requests.RequestException as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")
            self.status_label.config(text="Hata oluştu")
        finally:
            self.shorten_button.config(state=tk.NORMAL)

    def copy_to_clipboard(self):
        short_url = self.result_label.cget("text").split(": ")[1]
        pyperclip.copy(short_url)
        self.status_label.config(text="Kısa URL kopyalandı!")

if __name__ == "__main__":
    root = tk.Tk()
    app = URLShortener(root)
    root.mainloop()







app.mainloop()


