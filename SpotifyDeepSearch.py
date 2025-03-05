import tkinter as tk
from tkinter import ttk, messagebox
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API認証
CLIENT_ID = "180305ee093346a79c15a31c353bdfe0"
CLIENT_SECRET = "a11d961415334cb4b391f0625a49be57"
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
    for idx, track in enumerate(results["tracks"]["items"]):
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        listbox_results.insert(tk.END, f"{idx + 1}. {track_name} - {artist_name}")


# UI作成
root = tk.Tk()
root.title("Spotify 曲検索")
root.geometry("500x400")

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

# 検索ボタン
btn_search = ttk.Button(frame, text="検索", command=search_tracks)
btn_search.grid(row=4, columnspan=2, pady=10)

# リストボックス
listbox_results = tk.Listbox(frame, width=60, height=10)
listbox_results.grid(row=5, columnspan=2)

root.mainloop()
