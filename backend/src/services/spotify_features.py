def spotify_features_to_text(features: dict) -> str:
    desc = []

    d = features.get("danceability", 0)
    e = features.get("energy", 0)
    v = features.get("valence", 0)
    t = features.get("tempo", 0)
    a = features.get("acousticness", 0)
    i = features.get("instrumentalness", 0)
    l = features.get("liveness", 0)
    s = features.get("speechiness", 0)

    # Danceability
    if d > 0.75:
        desc.append("very danceable")
    elif d > 0.5:
        desc.append("danceable")
    else:
        desc.append("not very danceable")

    # Energy
    if e > 0.75:
        desc.append("highly energetic")
    elif e > 0.4:
        desc.append("moderately energetic")
    else:
        desc.append("low energy")

    # Valence (mood)
    if v > 0.75:
        desc.append("happy and upbeat")
    elif v > 0.4:
        desc.append("somewhat positive")
    else:
        desc.append("sad or serious")

    # Tempo
    if t > 120:
        desc.append(f"fast tempo at {int(t)} BPM")
    elif t > 90:
        desc.append(f"moderate tempo at {int(t)} BPM")
    else:
        desc.append(f"slow tempo at {int(t)} BPM")

    # Acousticness
    if a > 0.7:
        desc.append("acoustic sound")
    elif a > 0.3:
        desc.append("some acoustic elements")
    else:
        desc.append("mostly electronic sound")

    # Instrumentalness
    if i > 0.5:
        desc.append("instrumental")
    else:
        desc.append("vocal")

    # Liveness
    if l > 0.5:
        desc.append("live performance feel")
    else:
        desc.append("studio recording")

    # Speechiness
    if s > 0.3:
        desc.append("contains a lot of speech or rap")
    elif s > 0.1:
        desc.append("some spoken words")
    else:
        desc.append("mostly singing")

    return "This song is " + ", ".join(desc) + "."
