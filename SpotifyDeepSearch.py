import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageOps
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import requests
from io import BytesIO

# .envファイルの読み込み
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )
)


def search_tracks():
    query = entry_query.get()
    artist = entry_artist.get()
    genre = entry_genre.get()
    limit = int(entry_limit.get())

    if not query:
        messagebox.showerror("エラー", "検索キーワードを入力してください。")
        return

    search_params = {"q": query, "type": "track", "limit": limit}
    if artist:
        search_params["q"] += f" artist:{artist}"
    if genre:
        search_params["q"] += f" genre:{genre}"

    results = sp.search(**search_params)

    listbox_results.delete(0, tk.END)
    global track_data
    track_data = results["tracks"]["items"]
    for idx, track in enumerate(track_data):
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        listbox_results.insert(tk.END, f"{idx + 1}. {track_name} - {artist_name}")


def make_rounded_image(image, size, radius):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + size, radius=radius, fill=255)
    output = ImageOps.fit(image, size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output


def show_album_art(event):
    selected_index = listbox_results.curselection()
    if selected_index:
        track = track_data[selected_index[0]]

        # アルバムジャケットの取得と表示
        album_url = track["album"]["images"][0]["url"]
        response = requests.get(album_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((200, 200), Image.LANCZOS)
        img = make_rounded_image(img, (200, 200), radius=10)  # 角丸の半径を10に設定
        img_tk = ImageTk.PhotoImage(img)
        label_album_art.config(image=img_tk)
        label_album_art.image = img_tk

        # アーティストアイコンの取得と表示
        artist_id = track["artists"][0]["id"]
        artist = sp.artist(artist_id)
        if artist["images"]:
            artist_url = artist["images"][0]["url"]
            response = requests.get(artist_url)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.LANCZOS)
            img = make_rounded_image(
                img, (100, 100), radius=50
            )  # 完全に丸くするために半径を50に設定
            img_tk = ImageTk.PhotoImage(img)
            label_artist_icon.config(image=img_tk)
            label_artist_icon.image = img_tk
        else:
            label_artist_icon.config(image="")  # 画像がない場合はラベルをクリア


# UI作成
root = tk.Tk()
root.title("Spotify 曲検索")
root.geometry("950x600")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# ラベルとエントリー
ttk.Label(frame, text="検索キーワード:").grid(row=0, column=0, sticky=tk.W)
entry_query = ttk.Entry(frame, width=40)
entry_query.grid(row=0, column=1)

ttk.Label(frame, text="アーティスト:").grid(row=1, column=0, sticky=tk.W)
entry_artist = ttk.Entry(frame, width=40)
entry_artist.grid(row=1, column=1)

ttk.Label(frame, text="ジャンル:").grid(row=2, column=0, sticky=tk.W)
entry_genre = ttk.Entry(frame, width=40)
entry_genre.grid(row=2, column=1)

ttk.Label(frame, text="検索結果数:").grid(row=3, column=0, sticky=tk.W)
entry_limit = ttk.Entry(frame, width=5)
entry_limit.insert(0, "10")
entry_limit.grid(row=3, column=1, sticky=tk.W)

# ttk.Scale
ttk.Label(frame, text="danceability:").grid(row=4, column=0, sticky=tk.W)
var_scale_ttk = tk.DoubleVar()
var_scale_ttk.set(0.3)
scale_ttk = ttk.Scale(
    frame,
    variable=var_scale_ttk,
    length=100,
)
scale_ttk.grid(row=4, column=1, sticky=tk.W)

# 検索ボタン
btn_search = ttk.Button(frame, text="検索", command=search_tracks)
btn_search.grid(row=5, columnspan=2, pady=10)

# リストボックス
listbox_results = tk.Listbox(frame, width=60, height=10)
listbox_results.grid(row=6, columnspan=2)
listbox_results.bind("<<ListboxSelect>>", show_album_art)

# アルバムジャケット表示用ラベル
label_album_art = tk.Label(frame)
label_album_art.grid(row=0, column=2, rowspan=6, padx=10, pady=10)
ttk.Label(frame, text="").grid(row=0, column=3, sticky=tk.W)

# アーティストアイコン表示用ラベルの追加
label_artist_icon = tk.Label(frame)
label_artist_icon.grid(row=6, column=2, padx=10, pady=10)


root.mainloop()
