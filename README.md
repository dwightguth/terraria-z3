# Terraria NPC Happiness Algorithm

This algorithm is designed to be a customizable constraint solver for computing various permutations of NPC happiness in the video game Terraria. For more information, see the [Terraria Wiki](https://terraria.fandom.com/wiki/NPCs#Happiness).

The algorithm makes the following assumptions by default:

1. Each biome contains at most 4 NPCs
2. Each NPC is near at most 2 other NPCs
3. Each biome contains an NPC that sells a Pylon
4. Two NPCs that are near each other must be in the same biome
5. NPC nearness is transitive
6. You want the Goblin Tinkerer to be as cheap as possible
7. After optimizing the Goblin Tinkerer, you also want the Tax Collector and Angler to give as much money as possible.
8. All other NPCs should be as happy as possible.

Each of these assumptions can be tweaked by modifying the script. Look for lines that say `o.add` to see the individual constraints that are being placed on the solver.
