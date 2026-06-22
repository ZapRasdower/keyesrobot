# 🥟 Squishy Pets

A cozy, single-file unboxing & idle collector. Open the **Dumpling Steamer** box
to unbox a squishy dumpling, then **squish it** to earn Dough. Spend Dough on
upgrades, unlock new themed boxes (Sushi Bar, Sweet Shop, Critter Cove), and
fill your shelf with all 32 collectible pets.

## How to play

1. **Tap the box** (or press **Open Box**) to unbox a random squishy pet.
2. **Squish** the pet — tap and hold to keep squishing — to earn 🥟 Dough.
   Squishing fast builds a **combo** multiplier.
3. Open the **🛒 Upgrade Shop** to buy:
   - **Squishy Power** — more Dough per squish
   - **Helper Hands** — passive Dough/sec (even while away)
   - **Combo Master** — higher combo cap & slower decay
   - **Lucky Charm** — better odds for rare pets
   - **Golden Touch** — chance for a ×10 squish
4. Spend Dough to **unlock new box themes** from the bottom strip.
5. Browse the **📖 Pet Shelf** to see everything you've collected, and tap any
   owned pet to bring it back out and squish it for free.

## Rarities

Common → Uncommon → Rare → Epic → Legendary. Rarer pets are worth far more Dough
per squish, and Epic/Legendary pulls come with extra confetti and a screen flash.

## Running it

It's a single self-contained `index.html` — no build step, no dependencies.

- Open `index.html` in any modern browser, or
- Serve it locally: `python3 -m http.server` then visit `http://localhost:8000`.

It's mobile-first (touch friendly) and scales to any screen.

## Saving

Progress saves automatically when a host `window.storage` API is available
(with offline idle earnings, capped at 4 hours). Without it, the game still runs
fully — just without persistence.
