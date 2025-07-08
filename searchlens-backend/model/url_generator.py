import urllib.parse

def build_walmart_url(category: str, attributes: list[str]) -> str:
    base_url = "https://www.walmart.com/search"
    query = f"?q={urllib.parse.quote_plus(category.strip())}"

    facet_parts = []
    for attr in attributes:
        if ':' not in attr:
            continue
        key, value = attr.split(':', 1)
        facet_key = key.strip().lower().replace(" ", "_")
        facet_value = value.strip().title()
        facet_string = f"{facet_key}:{facet_value}"
        facet_parts.append(facet_string)

    # Join facet parts with '||' and encode the entire facet string
    if facet_parts:
        raw_facet = "||".join(facet_parts)
        encoded_facet = urllib.parse.quote(raw_facet, safe='')
        query += f"&facet={encoded_facet}"

    return base_url + query
