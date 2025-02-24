# Pokémon Fetcher 🏆

A Python script to fetch Pokémon data from the PokéAPI, including types, abilities, and other relevant details.

## 📌 Features

- Fetch a list of Pokémon with details like type, abilities, sprite, base stats, and other
- Retrieve details of a **specific Pokémon** by name or ID
- Categorize Pokémon by type
- Fetch data efficiently with multithreading

## 🔧 Requirements

- Python 3.x
- `requests` library (install with `pip install -r requirements.txt`)

## 🚀 Installation & Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/ajlorans/pokemon-fetcher.git

   cd pokemon-fetcher
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run The Script**

   **📜 Fetch all Pokémon (default 150)**

   ```bash
   python pokemon-fetcher.py
   ```

   **📜 Fetch Pokémon using multiple threads (faster)**

   ```bash
   python pokemon-fetcher.py --limit 300 --threads 40
   ```

   **📜 Example Output**

   ```yaml
   ✅ Successfully fetched 10 Pokémon.

   📂 Pokémon Categorized by Type:

   🐞  Type: Bug
   ➔  Caterpie (ID: 10 | Abilities: Shield-dust, Run-away | Base Exp: 39)

   🔥  Type: Fire
   ➔  Charmander (ID: 4 | Abilities: Blaze, Solar-power | Base Exp: 62)
   ➔  Charmeleon (ID: 5 | Abilities: Blaze, Solar-power | Base Exp: 142)
   ```

   **📜 Fetch a specific Pokémon (by name or ID)**

   ```bash
   python pokemon-fetcher.py --pokemon blastoise
   ```

   ```bash
   python pokemon-fetcher.py --pokemon 9 # Blastoise's ID
   ```

   **📜 Example Output**

   ```yaml
   🔹 Name: Blastoise
   🔹 ID: 9
   🔹 Types: Water
   🔹 Abilities: Torrent, Rain-dish
   🔹 Base Experience: 265, Height: 16, Weight: 855
   🔹 Sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png
   🔹 Base Stats:
     ➔ HP: 79
     ➔ Attack: 83
     ➔ Defense: 100
     ➔ Special Attack: 85
     ➔ Special Defense: 105
     ➔ Speed: 78
   ```
