init python:
    import os

    def radio_scan_files():
        stations = {}
        base_path = os.path.join(config.gamedir, "audio", "radios")
        print(f"DEBUG: Scanning {base_path}")
        
        if not os.path.exists(base_path):
            print("DEBUG: Base path does not exist")
            return

        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.lower().endswith((".mp3", ".ogg", ".wav")):
                    # Obtenemos la ruta relativa desde audio/radios
                    rel_dir = os.path.relpath(root, base_path)
                    
                    # Si el archivo está directamente en audio/radios, lo ignoramos o ponemos en "Varios"
                    if rel_dir == ".":
                        continue
                    
                    # El nombre de la estación es la primera carpeta
                    station_name = rel_dir.split(os.sep)[0]
                    
                    # Construimos la ruta relativa desde game/ para Ren'Py
                    # Ren'Py espera rutas como "audio/radios/Supreme Lofi/song.mp3"
                    renpy_path = os.path.join("audio", "radios", rel_dir, file).replace(os.sep, "/")
                    
                    if station_name not in stations:
                        stations[station_name] = []
                    stations[station_name].append(renpy_path)
                    print(f"DEBUG: Added {renpy_path} to {station_name}")
        
        # Convertimos a la lista de diccionarios
        store.radio_stations = []
        for name, files in stations.items():
            store.radio_stations.append({'name': name, 'files': files})
        
        store.radio_stations.sort(key=lambda x: x['name'])
        print(f"DEBUG: Stations found: {len(store.radio_stations)}")

    def radio_play():
        if not store.radio_stations:
            return
        
        station = store.radio_stations[store.current_station_index]
        # Reproducimos la lista de archivos de la estación
        renpy.music.play(station['files'], channel='music', loop=True, fadeout=1.0, fadein=1.0)
        store.radio_is_playing = True

    def radio_stop():
        renpy.music.stop(channel='music', fadeout=1.0)
        store.radio_is_playing = False

    def radio_next():
        if not store.radio_stations:
            return
        
        store.current_station_index = (store.current_station_index + 1) % len(store.radio_stations)
        if store.radio_is_playing:
            radio_play()

    def radio_prev():
        if not store.radio_stations:
            return

        store.current_station_index = (store.current_station_index - 1 + len(store.radio_stations)) % len(store.radio_stations)
        if store.radio_is_playing:
            radio_play()

    def radio_toggle():
        if store.radio_is_playing:
            radio_stop()
        else:
            radio_play()

default radio_stations = []
default current_station_index = 0
default radio_is_playing = False
