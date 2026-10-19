# webhook-spammer - Description rapide du programme.
# Copyright (C) 2026 uhqtools-on
# This file is part of webhook-spammer.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/.

import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests
import threading
import time
import os
import sys
import urllib.request

BG_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIhm-Dibz7NvL35FBur8IDrciVmmA0CGP7osJNmHPaNxEt-vrwHv1fITW7&s=10"
IMAGE_PATH = "panel_bg.png"

DEFAULT_WEBHOOK_URL = "https://discord.com/api/webhooks/TON_ID/TOKEN"

class WebhookSpammer:
    def __init__(self, root):
        self.root = root

        self.bg_image_path = IMAGE_PATH
        if not os.path.exists(self.bg_image_path):
            self.download_bg_image()

        try:
            from PIL import Image, ImageTk
            # Ouverture de l'image avec Pillow
            self.original_img = Image.open(self.bg_image_path)

            def resize_image(event):
                new_width = event.width
                new_height = event.height
                h_ratio = new_height / self.original_img.height
                w_ratio = new_width / self.original_img.width
                ratio = min(w_ratio, h_ratio)

                new_size = (int(self.original_img.width * ratio), int(self.original_img.height * ratio))
                self.resized_img = self.original_img.resize(new_size, Image.ANTIALIAS)
                self.tk_img = ImageTk.PhotoImage(self.resized_img)

                self.bg_label.config(image=self.tk_img)

            self.root.bind("<Configure>", resize_image)
        except Exception as e:
            print(f"Erreur chargement image (mode texte activé): {e}")
            self.bg_image_path = None # Désactive l'image si erreur

        self.color_bg_frame = "#f0f0f0"
        self.color_entry = "#ffffff"
        self.color_button = "#4a90e2"
        self.color_text = "#333333"

        self.root.title("Panel UHQ")
        self.root.geometry("500x600")
        self.root.resizable(True, True)

        self.bg_label = tk.Label(root)
        self.bg_label.pack(fill=tk.BOTH, expand=True)

        # Frame principale avec effet "glass" ou translucide
        self.main_frame = tk.Frame(root, bg=self.color_bg_frame, bd=0, highlightthickness=0)
        self.main_frame.place(relx=0.5, rely=0.15, anchor="n", relwidth=0.9, relheight=0.8)


        # Titre
        tk.Label(self.main_frame, text="PANEL UHQ", font=("Helvetica", 24, "bold"),
                 fg=self.color_text, bg=self.color_bg_frame).pack(pady=(10, 5))

        # Zone URL
        tk.Label(self.main_frame, text="URL du Webhook :", font=("Arial", 10),
                 fg=self.color_text, bg=self.color_bg_frame).pack(anchor="w", padx=20)

        self.url_entry = tk.Entry(self.main_frame, width=50, font=("Arial", 11))
        self.url_entry.pack(pady=(0, 10), ipady=5)
        self.url_entry.insert(0, DEFAULT_WEBHOOK_URL)

        # Zone Message
        tk.Label(self.main_frame, text="Message à spammer :", font=("Arial", 10),
                 fg=self.color_text, bg=self.color_bg_frame).pack(anchor="w", padx=20)

        self.msg_entry = tk.Entry(self.main_frame, width=50, font=("Arial", 11))
        self.msg_entry.pack(pady=(0, 10), ipady=5)
        self.msg_entry.insert(0, "Free Israël ! @everyone")

        # Zone Logs (ScrolledText)
        tk.Label(self.main_frame, text="Logs :", font=("Arial", 10),
                 fg=self.color_text, bg=self.color_bg_frame).pack(anchor="w", padx=20, pady=(5,0))

        self.log_area = scrolledtext.ScrolledText(self.main_frame, height=12, width=58,
                                                  font=("Courier New", 9), state=tk.DISABLED)
        self.log_area.pack(pady=(0, 10))

        # Boutons
        btn_frame = tk.Frame(self.main_frame, bg=self.color_bg_frame)
        btn_frame.pack(fill=tk.X, padx=20)

        self.start_btn = tk.Button(btn_frame, text="SPAMMER", command=self.toggle_spam,
                                   bg="#4CAF50", fg="white", font=("Arial", 12), relief=tk.RAISED, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.stop_btn = tk.Button(btn_frame, text="ARRÊTER", command=self.toggle_spam,
                                  bg="#f44336", fg="white", font=("Arial", 12), relief=tk.RAISED, cursor="hand2")
        self.stop_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        # Indicateur d'état
        self.is_spamming = False
        self.status_label = tk.Label(self.main_frame, text="Statut: Arrêté", font=("Arial", 9),
                                     fg=self.color_text, bg=self.color_bg_frame)
        self.status_label.pack(pady=(5,0))

    def log(self, message):
        """Ajoute un message au journal avec horodatage."""
        self.log_area.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n", "info")
        self.log_area.see(tk.END) # Scroll vers le bas
        self.log_area.config(state=tk.DISABLED)

    def toggle_spam(self):
        """Démarre ou arrête le spam."""
        if self.is_spamming:
            self.stop_spam()
        else:
            self.start_spam()

    def start_spam(self):
        url = self.url_entry.get().strip()
        msg = self.msg_entry.get().strip()

        if not url or not msg:
            messagebox.showwarning("Attention", "Veuillez remplir l'URL et le message.")
            return

        self.is_spamming = True
        self.start_btn.config(state=tk.DISABLED, bg="#81C78D") # Vert clair
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Statut: En cours...", fg="green")

        thread = threading.Thread(target=self.spam_loop, args=(url, msg), daemon=True)
        thread.start()

    def stop_spam(self):
        self.is_spamming = False
        self.start_btn.config(state=tk.NORMAL, bg="#4CAF50")
        self.stop_btn.config(state=tk.DISABLED, bg="#E57373") # Rouge clair
        self.status_label.config(text="Statut: Arrêté", fg=self.color_text)

    def spam_loop(self, url, msg):
        """Boucle de spam dans un thread."""
        payload = {"content": f"{msg}"}

        while self.is_spamming:
            try:
                response = requests.post(url, json=payload)

                if response.status_code == 204 or response.status_code == 200:
                    self.log(f"Message envoyé ! ({response.status_code})")
                else:
                    self.log(f"Erreur API : {response.text}")

            except Exception as e:
                self.log(f"Exception : {str(e)}")

            time.sleep(0.5)

    def download_bg_image(self):
        """Télécharge une image de fond par défaut si elle n'existe pas."""
        try:
            urllib.request.urlretrieve(BG_IMAGE_URL, IMAGE_PATH)
            self.log(f"Image téléchargée : {IMAGE_PATH}")
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image : {e}")

def main():
    try:
        import requests
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror("Dépendances manquantes",
                             "Merci d'installer les bibliothèques nécessaires.\n\n"
                             "Exécutez dans votre terminal :\npip install requests Pillow")
        return

    root = tk.Tk()
    app = WebhookSpammer(root)

    if hasattr(app, 'bg_image_path') and app.bg_image_path:
        try:
            from PIL import Image, ImageTk
            app.original_img = Image.open(app.bg_image_path)

            def resize_image(event):
                new_width = event.width
                new_height = event.height
                h_ratio = new_height / app.original_img.height
                w_ratio = new_width / app.original_img.width
                ratio = min(w_ratio, h_ratio)

                new_size = (int(app.original_img.width * ratio), int(app.original_img.height * ratio))
                app.resized_img = app.original_img.resize(new_size, Image.ANTIALIAS)
                app.tk_img = ImageTk.PhotoImage(app.resized_img)

                app.bg_label.config(image=app.tk_img)

            root.bind("<Configure>", resize_image)
        except Exception as e:
            print(f"Erreur init image : {e}")

    root.mainloop()

if __name__ == "__main__":
    main()
