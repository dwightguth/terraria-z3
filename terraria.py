from z3 import *
npcs = []
biomes = []

class npc(object):
  def __init__(self, name):
    self.name = name
    self.sells = True
    self.guide = False
    self._loves = []
    self._likes = []
    self._dislikes = []
    self._hates = []
    self.near = {}
    npcs.append(self)

  def loves(self, *loves):
    self._loves = loves
  def likes(self, *likes):
    self._likes = likes
  def dislikes(self, *dislikes):
    self._dislikes = dislikes
  def hates(self, *hates):
    self._hates = hates

guide = npc("Guide")
merchant = npc("Merchant")
zoologist = npc("Zoologist")
golfer = npc("Golfer")
nurse = npc("Nurse")
tavernkeep = npc("Tavernkeep")
party_girl = npc("Party girl")
wizard = npc("Wizard")
demolitionist = npc("Demolitionist")
goblin_tinkerer = npc("Goblin tinkerer")
clothier = npc("Clothier")
dye_trader = npc("Dye trader")
arms_dealer = npc("Arms dealer")
steampunker = npc("Steampunker")
dryad = npc("Dryad")
painter = npc("Painter")
witch_doctor = npc("Witch doctor")
stylist = npc("Stylist")
angler = npc("Angler")
pirate = npc("Pirate")
mechanic = npc("Mechanic")
tax_collector = npc("Tax collector")
cyborg = npc("Cyborg")
#santa = npc("Santa claus")
truffle = npc("Truffle")

class biome(object):
  def __init__(self, name):
    self.name = name
    biomes.append(self)

forest = biome("Forest")
hallow = biome("Hallow")
underground = biome("Underground")
desert = biome("Desert")
jungle = biome("Jungle")
ocean = biome("Ocean")
snow = biome("Snow")
mushroom = biome("Mushroom")

guide.likes(forest, clothier, zoologist)
guide.dislikes(ocean, steampunker)
guide.hates(painter)
guide.sells = False
guide.guide = True

merchant.likes(forest, golfer, nurse)
merchant.dislikes(desert, tax_collector)
merchant.hates(angler)

zoologist.loves(witch_doctor)
zoologist.likes(forest, golfer)
zoologist.dislikes(desert, angler)
zoologist.hates(arms_dealer)

golfer.loves(angler)
golfer.likes(forest, painter, zoologist)
golfer.dislikes(underground, pirate)
golfer.hates(merchant)

nurse.loves(arms_dealer)
nurse.likes(hallow, wizard)
nurse.dislikes(snow, dryad, party_girl)
nurse.hates(zoologist)
nurse.sells = False

tavernkeep.loves(demolitionist)
tavernkeep.likes(hallow, goblin_tinkerer)
tavernkeep.dislikes(snow, guide)
tavernkeep.hates(dye_trader)

party_girl.loves(wizard, zoologist)
party_girl.likes(hallow, stylist)
party_girl.dislikes(underground, merchant)
party_girl.hates(tax_collector)

wizard.loves(golfer)
wizard.likes(hallow, merchant)
wizard.dislikes(ocean, witch_doctor)
wizard.hates(cyborg)

demolitionist.loves(tavernkeep)
demolitionist.likes(underground, mechanic)
demolitionist.dislikes(ocean, arms_dealer, goblin_tinkerer)

goblin_tinkerer.loves(mechanic)
goblin_tinkerer.likes(underground, dye_trader)
goblin_tinkerer.dislikes(jungle, clothier)
goblin_tinkerer.hates(stylist)

clothier.loves(truffle)
clothier.likes(underground, tax_collector)
clothier.dislikes(hallow, nurse)
clothier.hates(mechanic)

dye_trader.likes(desert, arms_dealer, painter)
dye_trader.dislikes(forest, steampunker)
dye_trader.hates(pirate)

arms_dealer.loves(nurse)
arms_dealer.likes(desert, steampunker)
arms_dealer.dislikes(snow, golfer)
arms_dealer.hates(demolitionist)

steampunker.loves(cyborg)
steampunker.likes(desert, painter)
steampunker.dislikes(jungle, dryad, wizard, party_girl)

dryad.likes(jungle, witch_doctor, truffle)
dryad.dislikes(desert, angler)
dryad.hates(golfer)

painter.loves(dryad)
painter.likes(jungle, party_girl)
painter.dislikes(forest, truffle, cyborg)

witch_doctor.likes(jungle, dryad, guide)
witch_doctor.dislikes(hallow, nurse)
witch_doctor.hates(truffle)

stylist.loves(dye_trader)
stylist.likes(ocean, pirate)
stylist.dislikes(snow, tavernkeep)
stylist.hates(goblin_tinkerer)

angler.likes(ocean, demolitionist, party_girl, tax_collector)
angler.hates(tavernkeep)
angler.sells = False

pirate.loves(angler)
pirate.likes(ocean, tavernkeep)
pirate.dislikes(underground, stylist)
pirate.hates(guide)

mechanic.loves(goblin_tinkerer)
mechanic.likes(snow, cyborg)
mechanic.dislikes(underground, arms_dealer)
mechanic.hates(clothier)

tax_collector.loves(merchant)
tax_collector.likes(snow, party_girl)
tax_collector.dislikes(hallow, demolitionist, mechanic)
#tax_collector.hates(santa)
tax_collector.sells = False

cyborg.likes(snow, steampunker,  pirate, stylist)
cyborg.dislikes(jungle, zoologist)
cyborg.hates(wizard)

#santa.loves(snow)
#santa.hates(desert, tax_collector)

truffle.loves(guide)
truffle.likes(dryad)
truffle.dislikes(clothier)
truffle.hates(witch_doctor)

NPC = Datatype("NPC")
for n in npcs:
  NPC.declare(n.name) 
NPC = NPC.create()
for n in npcs:
  n.ctr = getattr(NPC, n.name)

Biome = Datatype("Biome")
for b in biomes:
  Biome.declare(b.name)
Biome = Biome.create()
for b in biomes:
  b.ctr = getattr(Biome, b.name)

for n in npcs:
  n.biome = Const(n.name + "_biome", Biome)
  n.near = {}

for i in range(len(npcs)):
  for j in range(i+1, len(npcs)):
     near = Bool("near_" + npcs[i].name + "_" + npcs[j].name)
     npcs[i].near[npcs[j].name] = near
     npcs[j].near[npcs[i].name] = near

r = RealVal

def modifier(l, n, mod, result):
  if isinstance(l, biome):
    return result + If(l.ctr == n.biome, mod, 0)
  elif isinstance(l, npc):
    return result + If(n.near[l.name], mod, 0)
  else:
      raise

def happiness(npc):
  result = 95
  for l in npc._loves:
    result = modifier(l, npc, -12, result)
  for l in npc._likes:
    result = modifier(l, npc, -6, result)
  for l in npc._dislikes:
    result = modifier(l, npc, 6, result)
  for l in npc._hates:
    result = modifier(l, npc, 12, result)
  return If(result < 80, 0,
         If(result < 86, 1,
         If(result < 92, 2,
         If(result < 98, 3,
         If(result < 98, 4,
         If(result < 104, 5,
         If(result < 110, 6,
         If(result < 116, 7,
         If(result < 122, 8,
         If(result < 128, 9,
         If(result < 134, 10,
         If(result < 140, 11,
         If(result < 146, 12,
         13)))))))))))))

total = 0
for n in npcs:
  if not n.guide:
    n.happiness = happiness(n)
    total += n.happiness

o = Optimize()
o.add(truffle.biome == mushroom.ctr)
o.add(goblin_tinkerer.happiness == 0)
o.add(tax_collector.happiness == 0)
o.add(angler.happiness == 0)
for n in npcs:
  nnear = 0
  for n2 in npcs:
    if n.name != n2.name:
      o.add(Implies(n.near[n2.name], n.biome == n2.biome))
      nnear += If(n.near[n2.name], 1, 0)
  o.add(nnear < 3)

o.minimize(total)
print(o.check())
m = o.model()
print(m.eval(total))
for n in npcs:
  print(n.name, ":", m[n.biome], "=", str(m.eval(happiness(n)).as_long() * 5 + 75) + "%", end=' ')
  near=False
  for n2 in npcs:
    if n.name != n2.name:
      if m[n.near[n2.name]]:
        near=True
  if near:
    print("near", end=' ')
  for n2 in npcs:
    if n.name != n2.name:
      if m[n.near[n2.name]]:
        print(n2.name, end=' ')
  print()
