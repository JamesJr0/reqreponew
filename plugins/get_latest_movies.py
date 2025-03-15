import re

async def get_latest_movies():
    languages = ["Malayalam", "Tamil", "Telugu", "Kannada", "Hindi", "English", "Chinese", "Japanese", "Korean"]
    latest_movies = {lang: [] for lang in languages}

    # Fetch latest 20 movies from multiple databases
    movies1 = await Media1.collection.find().sort("$natural", -1).limit(20).to_list(None)
    movies2 = await Media2.collection.find().sort("$natural", -1).limit(20).to_list(None)
    movies3 = await Media3.collection.find().sort("$natural", -1).limit(20).to_list(None)
    movies4 = await Media4.collection.find().sort("$natural", -1).limit(20).to_list(None)

    all_movies = movies1 + movies2 + movies3 + movies4

    for movie in all_movies:
        file_name = movie.get("file_name", "")
        caption = str(movie.get("caption", ""))  # Ensure caption is always a string

        # Extract movie name and check if it's a series
        match = re.search(r"(.+?)(\d{4})", file_name)
        movie_name = f"{match.group(1).strip()} {match.group(2)}" if match else file_name
        if re.search(r"S\d{2}", file_name, re.IGNORECASE):
            movie_name = re.sub(r"(S\d{2}).*", r"\1", file_name)

        # Identify and store the movie in multiple language categories
        added_to_languages = set()
        for lang in languages:
            if re.search(lang, caption, re.IGNORECASE):
                if movie_name not in latest_movies[lang]:  # Avoid duplicates
                    latest_movies[lang].append(movie_name)
                    added_to_languages.add(lang)  # Track languages added

        # If no language detected, classify as "Unknown"
        if not added_to_languages:
            if "Unknown" not in latest_movies:
                latest_movies["Unknown"] = []
            if movie_name not in latest_movies["Unknown"]:
                latest_movies["Unknown"].append(movie_name)

    # Return movies categorized by multiple languages
    return [{"language": lang, "movies": latest_movies[lang][:5]} for lang in latest_movies]
