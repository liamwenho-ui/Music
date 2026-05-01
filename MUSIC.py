import flet as ft
import flet_audio as fta

def main(page: ft.Page):
    page.title = "Music Player"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    playlist = [
        {"title": "Never Gonna Give You Up", "artist": "Rick Astley", "album": "Whenever You Need Somebody", "file": "audio/LOL.mp3"},
        {"title": "No Pole", "artist": "Don Toliver", "album": "Love Sick", "file": "audio/nopole.mp3"},
        {"title": "Timeless", "artist": "The Weeknd & Playboi Carti", "album": "Timeless", "file": "audio/timeless.mp3"},
        {"title": "Que Pasaría", "artist": "Rauw Alejandro & Bad Bunny", "album": "Saturno", "file": "audio/Quep.mp3"},
        {"title": "Revolú", "artist": "Rauw Alejandro & Feid", "album": "Playa Saturno", "file": "audio/revo.mp3"},
    ]

    current_index = 0
    is_playing = False
    has_started = False

    # UI
    title_text = ft.Text(size=20, weight="bold")
    artist_text = ft.Text()
    album_text = ft.Text()
    position_text = ft.Text("00:00")

    progress = ft.Slider(min=0, max=100, value=0, expand=True)
    volume_slider = ft.Slider(min=0, max=100, value=100)

    # Audio
    audio = fta.Audio(
        src=playlist[current_index]["file"],
        volume=1.0,
    )

    # Load song
    def load_song(index):
        nonlocal current_index, has_started, is_playing
        current_index = index
        song = playlist[current_index]

        audio.src = song["file"]

        title_text.value = song["title"]
        artist_text.value = f"Artist: {song['artist']}"
        album_text.value = f"Album: {song['album']}"

        has_started = False
        is_playing = False
        play_btn.text = "Play"

        page.update()

    
    async def play_pause(e):
        nonlocal is_playing, has_started

        if is_playing:
            await audio.pause()
            is_playing = False
            play_btn.text = "Play"
        else:
            if not has_started:
                await audio.play()
                has_started = True
            else:
                await audio.resume()

            is_playing = True
            play_btn.text = "Pause"

        page.update()

    
    async def next_song(e):
        index = (current_index + 1) % len(playlist)
        load_song(index)
        await audio.play()

    # Previous
    async def prev_song(e):
        index = (current_index - 1) % len(playlist)
        load_song(index)
        await audio.play()

   
    def change_volume(e):
        audio.volume = volume_slider.value / 100

    
    async def update_position(e):
        pos = await audio.get_current_position()
        dur = await audio.get_duration()

        if dur > 0:
            progress.value = (pos / dur) * 100

        position_text.value = f"{pos.minutes:02}:{pos.seconds:02}"
        page.update()

    audio.on_position_change = update_position

   
    play_btn = ft.ElevatedButton("Play", on_click=play_pause)
    next_btn = ft.ElevatedButton("Next", on_click=next_song)
    prev_btn = ft.ElevatedButton("Previous", on_click=prev_song)

   
    page.add(
        title_text,
        artist_text,
        album_text,
        position_text,
        progress,
        ft.Row([prev_btn, play_btn, next_btn], alignment="center"),
        ft.Text("Volume"),
        volume_slider,
    )

    load_song(0)

ft.run(main=main, assets_dir="assets")