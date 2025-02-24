# Pokémon Fetcher 🏆

A Python script to fetch Pokémon data from the PokéAPI, including types, abilities, and other relevant details.

## 📌 Features

- Fetch a list of Pokémon with details like type, abilities, height, and weight
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
   python pokemon_fetcher.py --limit 150
   ```

   **📜 Fetch a specific Pokémon (by name or ID)**

   ```bash
   python pokemon_fetcher.py --pokemon charizard
   ```

   ```bash
   python pokemon_fetcher.py --pokemon 6 # Charizard's ID
   ```

   **📜 Fetch Pokémon using multiple threads (faster)**

   ```bash
   python pokemon_fetcher.py --limit 300 --threads 20
   ```

   **📜 Example Output**

   ```yaml
   🔹 Name: Charizard
   🔹 Types: Fire, Flying
   🔹 Abilities: Blaze, Solar-power
   🔹 Base Experience: 240, Height: 17, Weight: 905
   ```
