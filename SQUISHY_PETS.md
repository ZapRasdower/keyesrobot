# 🥟 Squishy Pets

A cozy, single-file unboxing & idle collector. Open themed blind boxes, squish
what pops out to earn Dough, and fill your shelf with all **48 collectible
pets** — dumplings, sushi, mochi, critters, fruit, and sea creatures, each with
its own soft-body shape.

## How to play

1. **Tap the box** (or press **Open Box**) to unbox a random squishy pet.
2. **Squish** the pet — tap and hold to keep squishing — to earn 🥟 Dough.
   Squishing fast builds a **combo** multiplier; max it out (with Fever Time
   unlocked) to trigger 🔥 **FEVER** for a timed earnings boost.
3. Watch for the **✨ Golden Box** — every minute or so the box turns gold:
   that open is **free** and guarantees a **Rare or better** pet.
4. Any pull can come out **✨ Shiny** — a gold-rimmed, sparkling variant worth
   **×5 Dough** per squish. Shinies are marked in your shelf.
5. Spend Dough in the **🛒 Upgrade Shop** and unlock new box themes from the
   bottom strip.
6. Check **🏆 Achievements** for Dough rewards, and browse the **📖 Pet Shelf**
   to bring any collected pet back out (shinies come out shiny).

## Boxes

| Box | Theme | Unlock |
|---|---|---|
| 🥟 Dumpling Steamer | squishy dumplings & buns | free |
| 🍣 Sushi Bar | nigiri & rolls | 220 |
| 🍡 Sweet Shop | mochi & desserts | 750 |
| 🐾 Critter Cove | animal friends | 1,900 |
| 🍓 Fruit Stand | fruity pals | 4,200 |
| 🪼 Ocean Drift | jellies & sea buddies | 9,000 |

## Shapes

Pets aren't all round anymore — the soft-body sim supports **round, tall, wide
(loaf), star, heart, square, pear, and jellyfish-bell** silhouettes, all fully
squishable.

## Upgrades

- **💪 Squishy Power** — more Dough per squish
- **🤲 Helper Hands** — passive Dough/sec (even while away, capped at 4h)
- **🔥 Combo Master** — higher combo cap & slower decay
- **🍀 Lucky Charm** — better odds for rare pets
- **✨ Golden Touch** — chance for a ×10 squish
- **🖐️ Big Hands** — bigger squish zone
- **🏷️ Bargain Hunter** — cheaper boxes
- **🌟 Shiny Hunter** — better ✨Shiny odds
- **⚡ Fever Time** — unlock & strengthen FEVER mode

## Rarities

Common → Uncommon → Rare → Epic → Legendary. Rarer pets are worth far more
Dough per squish, and Epic/Legendary/Shiny pulls come with extra confetti and a
screen flash.

## Running it

It's a single self-contained `index.html` — no build step, no dependencies.

- Open `index.html` in any modern browser, or
- Serve it locally: `python3 -m http.server` then visit `http://localhost:8000`.

It's mobile-first (touch friendly) and scales to any screen.

## Saving

Progress saves automatically when a host `window.storage` API is available
(with offline idle earnings, capped at 4 hours). Old v2 saves migrate
automatically. Without the API, the game still runs fully — just without
persistence.
