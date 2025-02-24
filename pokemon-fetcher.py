import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

init(autoreset=True)

# Type icons for each type
TYPE_ICONS = {
    "fire": "🔥",
    "water": "🌊",
    "grass": "🍃",
    "electric": "⚡",
    "bug": "🐞",
    "normal": "⚪",
    "psychic": "🧠",
    "fighting": "🥊",
    "poison": "☠️",
    "ghost": "👻",
    "dark": "🌑",
    "dragon": "🐉",
    "fairy": "🧚",
    "steel": "⚙️",
    "ice": "❄️",
    "rock": "🪨",
    "ground": "🌍",
    "flying": "🕊️",
}

# Fetch Pokémon list
def fetch_pokemon_list(limit=150):
    url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get('results', [])
    except requests.RequestException as e:
        print(f"❌ Error fetching Pokémon list: {e}")
        return []

# Fetch Pokémon details
def fetch_pokemon_details(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching details from {url}: {e}")
        return None

# Categorize Pokémon
def categorize_pokemon(pokemon_details_list):
    categories = {}
    for details in pokemon_details_list:
        if details:
            name = details.get("name", "Unknown").capitalize()
            types = [t["type"]["name"].lower() for t in details.get("types", [])]
            abilities = [a["ability"]["name"].capitalize() for a in details.get("abilities", [])]
            base_exp = details.get("base_experience", "N/A")
            id = details.get("id", "N/A")
            pokemon_info = {'id': id, 'name': name, 'abilities': abilities, 'base_experience': base_exp}
            for t in types:
                categories.setdefault(t, []).append(pokemon_info)
    return categories

# Display Pokémon details
def display_pokemon_details(details):
    """
    Display the details of a single Pokémon.
    """
    if not details:
        print("No Pokémon details available.")
        return
    
    name = details.get("name", "N/A").capitalize()
    pokemon_id = details.get("id", "N/A")
    types = [t["type"]["name"].capitalize() for t in details.get("types", [])]
    sprite = details.get("sprites", {}).get("front_default", "No sprite available")

    abilities = ", ".join([a["ability"]["name"].capitalize() for a in details.get("abilities", [])])
    base_exp = details.get("base_experience", "N/A")
    height = details.get("height", "N/A")
    weight = details.get("weight", "N/A")

    # Get base stats
    stats = details.get("stats", [])
    base_stats = {
        "HP": next((stat["base_stat"] for stat in stats if stat["stat"]["name"] == "hp"), "N/A"),
        "Attack": next((stat["base_stat"] for stat in stats if stat["stat"]["name"] == "attack"), "N/A"),
        "Defense": next((stat["base_stat"] for stat in stats if stat["stat"]["name"] == "defense"), "N/A"),
        "Special Attack": next((stat["base_stat"] for stat in stats if stat["stat"]["name"] == "special-attack"), "N/A"),
        "Special Defense": next((stat["base_stat"] for stat in stats if stat["stat"]["name"] == "special-defense"), "N/A"),
        "Speed": next((stat["base_stat"] for stat in stats if stat["stat"]["name"] == "speed"), "N/A"),
    }

    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}Name: {Fore.WHITE}{name}")
    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}ID: {Fore.WHITE}{pokemon_id}")
    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}Types: {Fore.WHITE}{', '.join(types) if types else 'N/A'}")
    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}Abilities: {Fore.WHITE}{abilities}")
    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}Base Experience: {Fore.WHITE}{base_exp}, {Fore.YELLOW}Height: {Fore.WHITE}{height}, {Fore.YELLOW}Weight: {Fore.WHITE}{weight}")
    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}Sprite: {Fore.WHITE}{sprite}")
    
    # Display base stats
    print(f"{Fore.YELLOW}🔹 {Fore.RED}{Style.BRIGHT}Base Stats: ")
    for stat, value in base_stats.items():
        print(f"  {Fore.YELLOW}➔ {Fore.RED}{Style.BRIGHT}{stat}: {Fore.WHITE}{value}")
    
    print(Style.RESET_ALL)


# Display categorized Pokémon
def display_categorized_pokemon(categories):
    print("\n📂 Pokémon Categorized by Type:")
    for type_name, pokemons in sorted(categories.items()):
        type_icon = TYPE_ICONS.get(type_name, type_name.capitalize())
        print(f"\n{type_icon} {Fore.GREEN}{Style.BRIGHT} Type: {Fore.CYAN}{type_name.capitalize()}")
        for pokemon in pokemons:
            abilities = ", ".join(pokemon['abilities'])
            base_exp = pokemon['base_experience']
            print(f"{Fore.YELLOW}➔ {Fore.WHITE}{Style.BRIGHT} {pokemon['name']} {Fore.WHITE}({Fore.GREEN}ID: {Fore.CYAN}{pokemon['id']}{Fore.WHITE} | {Fore.GREEN}Abilities: {Fore.MAGENTA}{abilities}{Fore.WHITE} | {Fore.YELLOW}Base Exp: {Fore.RED}{base_exp}{Fore.WHITE})")

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and categorize Pokémon using the PokéAPI.")
    parser.add_argument('--pokemon', type=str, help="Fetch details of a specific Pokémon by name or ID")
    parser.add_argument('--limit', type=int, default=150, help="Number of Pokémon to fetch (default: 150)")
    parser.add_argument('--threads', type=int, default=10, help="Number of threads to use for concurrent fetching (default: 10)")
    return parser.parse_args()

# Main function
def main():
    args = parse_args()

    if args.pokemon:
        details = fetch_pokemon_details(f"https://pokeapi.co/api/v2/pokemon/{args.pokemon}")
        display_pokemon_details(details)
        return

    pokemon_list = fetch_pokemon_list(args.limit)
    
    if not pokemon_list:
        print("❌ No Pokémon fetched.")
        return

    print(f"✅ Successfully fetched {len(pokemon_list)} Pokémon.")

    pokemon_details_list = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_pokemon = {executor.submit(fetch_pokemon_details, p["url"]): p for p in pokemon_list}
        for future in as_completed(future_to_pokemon):
            pokemon_details_list.append(future.result())

    categories = categorize_pokemon(pokemon_details_list)
    display_categorized_pokemon(categories)

if __name__ == "__main__":
    main()
