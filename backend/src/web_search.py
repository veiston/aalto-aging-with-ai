"""
Web Search + Local Lookup
Find nearby events and activities for elderly person
"""
# from geopy import distance
# import requests

def search_local_events(location: tuple, query: str, radius_km: float = 5) -> list:
    """
    Find events near elderly person
    location: (latitude, longitude)
    Returns: list of nearby activities
    """
    # events_api = requests.get(
    #     f"https://events-api.com/search?lat={location[0]}&lon={location[1]}&q={query}"
    # )
    
    # Placeholder: mock events
    events = [
        {"name": "Yoga class", "distance": 1.2, "time": "14:00"},
        {"name": "Swimming", "distance": 2.1, "time": "15:00"},
        {"name": "Book club", "distance": 0.8, "time": "16:00"}
    ]
    
    return [e for e in events if e["distance"] <= radius_km]

def web_search(query: str) -> list:
    """
    General web search for answers
    """
    # results = requests.get(
    #     f"https://api.search.com/search?q={query}"
    # )
    
    # Placeholder
    return [
        {"title": "What is paddle tennis", "snippet": "A racquet sport..."},
        {"title": "Paddle clubs near me", "snippet": "Find local clubs..."}
    ]

if __name__ == "__main__":
    # Test: find events
    elderly_location = (60.1695, 24.9354)  # Helsinki
    events = search_local_events(elderly_location, "yoga")
    print("Nearby yoga events:", events)
    
    # Test: web search
    results = web_search("What is paddle tennis")
    print("Search results:", results[0]["title"])
