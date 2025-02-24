import requests
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_pokemon_list(limit=150):
    """
    Fetch a list of Pokémon from the PokéAPI.

    Args:
        limit (int): Number of Pokémon to fetch from the API.

    Returns:
        list: A list of dictionaries, each containing a Pokémon's name and details URL.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print(f"Requesting Pokémon list from: {url}")  # Debug print
    
    try:
        response = requests.get(url, headers=headers, timeout=10)  # Set a timeout to prevent hanging
        response.raise_for_status()  # Raise an error for HTTP response codes 4xx/5xx
        data = response.json()
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"Error fetching Pokémon list: {e}")
        return []

def fetch_pokemon_details(url):
    """
    Fetch detailed data for a given Pokémon.

    Args:
        url (str): The API URL for the Pokémon details.

    Returns:
        dict: A dictionary containing Pokémon details or None if an error occurs.
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching details from {url}: {e}")
        return None

def fetch_pokemon(pokemon_name_or_id):
    """
    Fetch detailed information about a specific Pokémon using its name or ID.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()  # Returns Pokémon details as JSON
    except requests.RequestException as e:
        print(f"Error: Pokémon '{pokemon_name_or_id}' not found. {e}")
        return None

def categorize_pokemon(pokemon_details_list):
    """
    Categorize Pokémon based on their types.

    Args:
        pokemon_details_list (list): A list of Pokémon detail dictionaries.

    Returns:
        dict: A dictionary where keys are type names and values are lists of Pokémon details.
    """
    categories = {}

    for details in pokemon_details_list:
        if details is None:
            continue
        
        types = [t["type"]["name"] for t in details.get("types", [])]

        for t in types:
            if t not in categories:
                categories[t] = []
            categories[t].append(details)

    return categories

def display_pokemon_details(details):
    """
    Display the details of a single Pokémon.

    Args:
        details (dict): Pokémon detail dictionary.
    """
    if not details:
        print("No Pokémon details available.")
        return
    
    name = details.get("name", "N/A").capitalize()
    types = ", ".join([t["type"]["name"].capitalize() for t in details.get("types", [])])
    abilities = ", ".join([a["ability"]["name"].capitalize() for a in details.get("abilities", [])])
    base_exp = details.get("base_experience", "N/A")
    height = details.get("height", "N/A")
    weight = details.get("weight", "N/A")

    print(f"🔹 Name: {name}")
    print(f"🔹 Types: {types}")
    print(f"🔹 Abilities: {abilities}")
    print(f"🔹 Base Experience: {base_exp}, Height: {height}, Weight: {weight}")
    print()

def display_results(categories):
    """
    Display the categorized Pokémon along with relevant details.

    Args:
        categories (dict): A dictionary containing Pokémon data grouped by type.
    """
    for type_name, pokemons in categories.items():
        print(f"🔹 Type: {type_name.capitalize()}")
        for details in pokemons:
            display_pokemon_details(details)

def parse_args():
    """
    Parse command-line arguments to customize the script execution.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Fetch and categorize Pokémon using the PokéAPI.")
    parser.add_argument('--pokemon', type=str, help="Fetch details of a specific Pokémon by name or ID")
    parser.add_argument('--limit', type=int, default=150, help="Number of Pokémon to fetch (default: 150)")
    parser.add_argument('--threads', type=int, default=10, help="Number of threads to use for concurrent fetching (default: 10)")
    return parser.parse_args()

def main():
    """
    Main function to orchestrate fetching, processing, and displaying Pokémon data.
    """
    args = parse_args()

    if args.pokemon:
        # Fetch a single Pokémon if the user specifies one
        details = fetch_pokemon(args.pokemon)
        display_pokemon_details(details)
        return

    # Step 1: Fetch a list of Pokémon with the specified limit
    pokemon_list = fetch_pokemon_list(limit=args.limit)

    # Step 2: Retrieve Pokémon details concurrently using ThreadPoolExecutor
    pokemon_details_list = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_pokemon = {executor.submit(fetch_pokemon_details, pokemon["url"]): pokemon for pokemon in pokemon_list}
        
        for future in as_completed(future_to_pokemon):
            data = future.result()
            if data:
                pokemon_details_list.append(data)

    # Step 3: Categorize Pokémon by type
    categorized_pokemon = categorize_pokemon(pokemon_details_list)

    # Step 4: Display the categorized results
    display_results(categorized_pokemon)

if __name__ == "__main__":
    main()
