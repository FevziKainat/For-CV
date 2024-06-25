import instaloader
import tkinter as tk
from tkinter import ttk, messagebox
import os
import re
import threading

class InstagramDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram İndirici")
        self.root.geometry("400x500")
        self.root.configure(bg='#f0f0f0')

        self.download_path = os.path.dirname(os.path.abspath(__file__))

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Instagram İndirici", font=('Helvetica', 16, 'bold')).pack(pady=10)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        profile_frame = ttk.Frame(notebook, padding="10")
        post_frame = ttk.Frame(notebook, padding="10")

        notebook.add(profile_frame, text="Profil İndirme")
        notebook.add(post_frame, text="Gönderi İndirme")

        self.setup_profile_tab(profile_frame)
        self.setup_post_tab(post_frame)

        ttk.Label(main_frame, text=f"İndirme konumu:\n{self.download_path}", 
                  wraplength=380, justify="center").pack(pady=10)

    def setup_profile_tab(self, frame):
        ttk.Label(frame, text="Kullanıcı adı:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Gönderi limiti:").grid(row=1, column=0, sticky='w', pady=5)
        self.limit_entry = ttk.Entry(frame, width=10)
        self.limit_entry.grid(row=1, column=1, sticky='w', pady=5)

        ttk.Button(frame, text="İndir", command=self.download_profile).grid(row=2, column=0, columnspan=2, pady=20)

        self.profile_progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
        self.profile_progress.grid(row=3, column=0, columnspan=2, pady=10)

        self.profile_status = ttk.Label(frame, text="")
        self.profile_status.grid(row=4, column=0, columnspan=2)

    def setup_post_tab(self, frame):
        ttk.Label(frame, text="Gönderi URL:").grid(row=0, column=0, sticky='w', pady=5)
        self.url_entry = ttk.Entry(frame, width=40)
        self.url_entry.grid(row=0, column=1, pady=5)

        ttk.Button(frame, text="İndir", command=self.download_post).grid(row=1, column=0, columnspan=2, pady=20)

        self.post_status = ttk.Label(frame, text="")
        self.post_status.grid(row=2, column=0, columnspan=2)

    def download_profile(self):
        threading.Thread(target=self._download_profile, daemon=True).start()

    def _download_profile(self):
        username = self.username_entry.get()
        limit = self.limit_entry.get()
        
        if not username:
            messagebox.showerror("Hata", "Lütfen bir kullanıcı adı girin.")
            return

        try:
            limit = int(limit) if limit else None
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir sayı girin veya boş bırakın.")
            return

        try:
            bot = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(bot.context, username)
            posts = profile.get_posts()

            total_posts = min(limit, profile.mediacount) if limit else profile.mediacount
            
            self.profile_progress["maximum"] = total_posts
            self.profile_progress["value"] = 0

            for index, post in enumerate(posts, 1):
                if limit and index > limit:
                    break
                
                self.profile_status.config(text=f"İndiriliyor: {index}/{total_posts}")
                self.root.update()

                bot.download_post(post, target=os.path.join(self.download_path, f"{profile.username}_{index}"))
                self.profile_progress["value"] = index
                self.root.update()

            messagebox.showinfo("Başarılı", f"{index-1} gönderi indirildi.\nKonum: {self.download_path}")
            self.profile_status.config(text="İndirme tamamlandı.")

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def download_post(self):
        threading.Thread(target=self._download_post, daemon=True).start()

    def _download_post(self):
        url = self.url_entry.get()
        
        if not url:
            messagebox.showerror("Hata", "Lütfen bir URL girin.")
            return

        try:
            shortcode = self.extract_shortcode(url)
            if not shortcode:
                raise ValueError("Geçersiz Instagram URL'si")

            bot = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(bot.context, shortcode)

            bot.download_post(post, target=os.path.join(self.download_path, f"instagram_{shortcode}"))

            messagebox.showinfo("Başarılı", f"Gönderi başarıyla indirildi.\nKonum: {self.download_path}")
            self.post_status.config(text="İndirme tamamlandı.")

        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def extract_shortcode(self, url):
        pattern = r"(?:https?:\/\/)?(?:www\.)?instagram\.com(?:\/p\/|\/reel\/|\/tv\/)([^\/?]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else None

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramDownloader(root)
    root.mainloop()