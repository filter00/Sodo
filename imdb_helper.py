import re
import requests
from spellchecker import SpellChecker

spell = SpellChecker()

def check_spelling_and_get_imdb_info(movie_name):
    """Spelling check karta hai aur IMDB se information deta hai agar spelling galat hai."""
    words = re.findall(r'\w+', movie_name.lower())
    misspelled = spell.unknown(words)

    if misspelled:
        suggestions_text = "\n".join([f"  - {word}: {spell.candidates(word)}" for word in misspelled])
        message = f"Spelling galat hai. Suggestions:\n{suggestions_text}\n\nIMDB se information:"
        imdb_info = get_imdb_info(movie_name)
        if imdb_info:
            return message + "\n" + imdb_info
        else:
            return message + "\nKoi information nahi mili."
    else:
        return "Spelling sahi hai."

def get_imdb_info(movie_name):
    """IMDB se movie information retrieve karta hai."""
    try:
        search_url = f"https://www.imdb.com/find?q={movie_name}&s=tt&exact=true&ref_=fn_al_tt_ex"
        response = requests.get(search_url)
        response.raise_for_status()

        match = re.search(r'<a href="(/title/tt\d+/)">', response.text)
        if not match:
            return None

        movie_url = "https://www.imdb.com" + match.group(1)
        movie_response = requests.get(movie_url)
        movie_response.raise_for_status()

        title_match = re.search(r'<title>(.*?) \((\d{4})\) - IMDb<\/title>', movie_response.text)
        if not title_match:
            return None
        title = title_match.group(1)
        year = title_match.group(2)

        plot_match = re.search(r'<span data-testid="plot-xl">(.*?)<\/span>', movie_response.text)
        if plot_match:
            plot = plot_match.group(1)
        else:
            plot = "Plot summary available nahi hai."

        return f"Title: {title}\nYear: {year}\nPlot: {plot}\nURL: {movie_url}"

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Parsing error: {e}")
        return None
