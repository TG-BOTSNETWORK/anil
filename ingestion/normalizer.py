from datetime import datetime

def normalize_entry(entry):
    # Get URL (link or guid)
    url = entry.get("link") or entry.get("guid")
    
    # Get title
    title = entry.get("title") or "No Title"

    # Get summary: RSS often uses 'description', Atom uses 'summary'
    summary = entry.get("summary") or entry.get("description") or ""

    # Author (optional)
    author = entry.get("author", "Unknown")

    # Parse published date
    published_at = parse_date(entry)

    return {
        "title": title,
        "summary": summary,
        "author": author,
        "url": url,
        "published_at": published_at
    }


def parse_date(entry):
    # Try Atom/RSS parsed date
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])
    else:
        # Sometimes feeds only have string dates
        for key in ["published", "pubDate", "updated"]:
            if key in entry:
                try:
                    return datetime.strptime(entry[key], "%a, %d %b %Y %H:%M:%S %Z")
                except:
                    continue
    return None