import re


def normalize_show_title(primary_title):
    title = re.sub(r"[^a-zA-Z0-9]", "", primary_title)
    title = title.lower()
    return title
