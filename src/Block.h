#ifndef _BLOCKS_H_
#define _BLOCKS_H_

#include "CommonInc.h"
#include "Section.h"

class Block
{
public:
	enum RenderType {
		NORMAL,
		FLOWER,
		TORCH,
		FIRE,
		LIQUID,
		REDSTONEWIRE,
		CROPS,
		DOOR,
		LADDER,
		MINECARTTRCK,
		STAIRS,
		FENCE,
		LEVER,
		CACTUS,
		BED,
		REPEATER,
		PISTONBASE,
		PISTONEXT,
		PANE,
		STEM,
		VINE,
		FENCEGATE,
		LILYPAD,
		CAULDRON,
		BREWINGSTAND,
		ENDPORTALFRAME,
		DRAGONEGG,
		COCOA,
		TRIPWIRESOURCE,
		TRIPWIRE,
		TREE,
		WALL,
		FLOWERPOT,
		BEACON,
		ANVIL,
		RESTONELOGIC,
		COMPARATOR,
		HOPPER,
		QUARTZ,
		NO,
	};
	static Block* BlockList[5000];
	static Block* air;
	static Block* stone;
	static Block* grassblock;
	static Block* dirt;
	static Block* cobblestone;
	static Block* woodplanks;
	static Block* saplings;
	static Block* bedrock;
	static Block* water;
	static Block* stationarywater;
	static Block* lava;
	static Block* stationarylava;
	static Block* sand;
	static Block* gravel;
	static Block* goldore;
	static Block* ironore;
	static Block* coalore;
	static Block* wood;
	static Block* leaves;
	static Block* sponge;
	static Block* glass;
	static Block* lapislazuliore;
	static Block* lapislazuliblock;
	static Block* dispenser;
	static Block* sandstone;
	static Block* noteblock;
	static Block* bed;
	static Block* poweredrail;
	static Block* detectorrail;
	static Block* stickypiston;
	static Block* cobweb;
	static Block* grass;
	static Block* deadbush;
	static Block* piston;
	static Block* pistonextension;
	static Block* wool;
	static Block* blockmovedbypiston;
	static Block* dandelion;
	static Block* rose;
	static Block* brownmushroom;
	static Block* redmushroom;
	static Block* blockofgold;
	static Block* blockofiron;
	static Block* doubleslabs;
	static Block* slabs;
	static Block* bricks;
	static Block* tnt;
	static Block* bookshelf;
	static Block* mossstone;
	static Block* obsidian;
	static Block* torch;
	static Block* fire;
	static Block* monsterspawner;
	static Block* oakwoodstairs;
	static Block* chest;
	static Block* redstonewire;
	static Block* diamondore;
	static Block* blockofdiamond;
	static Block* craftingtable;
	static Block* wheat;
	static Block* farmland;
	static Block* furnace;
	static Block* burningfurnace;
	static Block* signpost;
	static Block* woodendoor;
	static Block* ladders;
	static Block* rail;
	static Block* cobblestonestairs;
	static Block* wallsign;
	static Block* lever;
	static Block* stonepressureplate;
	static Block* irondoor;
	static Block* woodenpressureplate;
	static Block* redstoneore;
	static Block* glowingredstoneore;
	static Block* redstonetorchinactive;
	static Block* redstonetorchactive;
	static Block* stonebutton;
	static Block* snow;
	static Block* ice;
	static Block* snowblock;
	static Block* cactus;
	static Block* clay;
	static Block* sugarcane;
	static Block* jukebox;
	static Block* fence;
	static Block* pumpkin;
	static Block* netherrack;
	static Block* soulsand;
	static Block* glowstone;
	static Block* netherportal;
	static Block* jacklantern;
	static Block* cakeblock;
	static Block* redstonerepeaterinactive;
	static Block* redstonerepeateractive;
	static Block* lockedchest;
	static Block* trapdoor;
	static Block* monsteregg;
	static Block* stonebricks;
	static Block* hugebrownmushroom;
	static Block* hugeredmushroom;
	static Block* ironbars;
	static Block* glasspane;
	static Block* melon;
	static Block* pumpkinstem;
	static Block* melonstem;
	static Block* vines;
	static Block* fencegate;
	static Block* brickstairs;
	static Block* stonebrickstairs;
	static Block* mycelium;
	static Block* lilypad;
	static Block* netherbrick;
	static Block* netherbrickfence;
	static Block* netherbrickstairs;
	static Block* netherwart;
	static Block* enchantmentable;
	static Block* brewingstand;
	static Block* cauldron;
	static Block* endportal;
	static Block* endportalblock;
	static Block* endstone;
	static Block* dragonegg;
	static Block* redstonelamp;
	static Block* redstonelampon;
	static Block* woodendoubleslab;
	static Block* woodenslab;
	static Block* cocoa;
	static Block* sandstonestairs;
	static Block* emeraldore;
	static Block* enderchest;
	static Block* tripwirehook;
	static Block* tripwire;
	static Block* blockofemeral;
	static Block* sprucewoodstairs;
	static Block* birchwoodstairs;
	static Block* junglewoodstairs;
	static Block* commandblock;
	static Block* beacon;
	static Block* cobblestonewall;
	static Block* flowerpot;
	static Block* carrots;
	static Block* potatoes;
	static Block* woodenbutton;
	static Block* mobhead;
	static Block* anvil;
	static Block* trappedchest;
	static Block* weightedpressureplatelight;
	static Block* weightedpressureplateheavy;
	static Block* redstonecomparator;
	static Block* redstonecomparatoron;
	static Block* daylightsensor;
	static Block* blockofredstone;
	static Block* netherquartzore;
	static Block* hopper;
	static Block* blockofquartz;
	static Block* quartzstairs;
	static Block* activatorrail;
	static Block* dropper;
	static Block* stainedclay;

	Block(int id);

	virtual int getColor(Section*,int,int,int);
	virtual std::string getTexName(int,int);

	int id;
	int renderType;
	std::vector<std::string> mTexName;
	int color;
	bool transparent;
};

class Stairs: public Block
{
public:
	Stairs(int id):Block(id)
	{
		renderType = STAIRS;
		transparent = 1;
	}
};

class Air : public Block
{
public:
	Air(int id);
};

class Stone : public Block
{
public:
	Stone(int id);
};

class GrassBlock : public Block
{
public:
	GrassBlock(int id);
};

class Dirt : public Block
{
public:
	Dirt(int id);
};

class Cobblestone : public Block
{
public:
	Cobblestone(int id);
};

class WoodPlanks : public Block
{
public:
	WoodPlanks(int id);
};

class Saplings : public Block
{
public:
	Saplings(int id);

	std::string getTexName(int face,int meta);
};

class Bedrock : public Block
{
public:
	Bedrock(int id);
};

class Water : public Block
{
public:
	Water(int id);
};

class Stationarywater : public Block
{
public:
	Stationarywater(int id);
};

class Lava : public Block
{
public:
	Lava(int id);
};

class Stationarylava : public Block
{
public:
	Stationarylava(int id);
};

class Sand : public Block
{
public:
	Sand(int id);
};

class Gravel : public Block
{
public:
	Gravel(int id);
};

class GoldOre : public Block
{
public:
	GoldOre(int id);
};

class IronOre : public Block
{
public:
	IronOre(int id);
};

class CoalOre : public Block
{
public:
	CoalOre(int id);
};

class Wood : public Block
{
public:
	Wood(int id);
};

class Leaves : public Block
{
public:
	Leaves(int id);
};

class Sponge : public Block
{
public:
	Sponge(int id);
};

class Glass : public Block
{
public:
	Glass(int id);
};

class LapisLazuliOre : public Block
{
public:
	LapisLazuliOre(int id);
};

class LapisLazuliBlock : public Block
{
public:
	LapisLazuliBlock(int id);
};

class Dispenser : public Block
{
public:
	Dispenser(int id);
};

class Sandstone : public Block
{
public:
	Sandstone(int id);
};

class NoteBlock : public Block
{
public:
	NoteBlock(int id);
};

class Bed : public Block
{
public:
	Bed(int id);
};

class PoweredRail : public Block
{
public:
	PoweredRail(int id);
};

class DetectorRail : public Block
{
public:
	DetectorRail(int id);
};

class StickyPiston : public Block
{
public:
	StickyPiston(int id);
};

class Cobweb : public Block
{
public:
	Cobweb(int id);
};

class Grass : public Block
{
public:
	Grass(int id);
	int getColor(Section*,int,int,int);
};

class DeadBush : public Block
{
public:
	DeadBush(int id);
};

class Piston : public Block
{
public:
	Piston(int id);
};

class PistonExtension : public Block
{
public:
	PistonExtension(int id);
};

class Wool : public Block
{
public:
	Wool(int id);

	std::string getTexName(int face,int meta);
};

class BlockmovedbyPiston : public Block
{
public:
	BlockmovedbyPiston(int id);
};

class Dandelion : public Block
{
public:
	Dandelion(int id);
};

class Rose : public Block
{
public:
	Rose(int id);
};

class BrownMushroom : public Block
{
public:
	BrownMushroom(int id);
};

class RedMushroom : public Block
{
public:
	RedMushroom(int id);
};

class BlockofGold : public Block
{
public:
	BlockofGold(int id);
};

class BlockofIron : public Block
{
public:
	BlockofIron(int id);
};

class DoubleSlabs : public Block
{
public:
	DoubleSlabs(int id);
};

class Slabs : public Block
{
public:
	Slabs(int id);
};

class Bricks : public Block
{
public:
	Bricks(int id);
};

class TNT : public Block
{
public:
	TNT(int id);
};

class Bookshelf : public Block
{
public:
	Bookshelf(int id);
};

class MossStone : public Block
{
public:
	MossStone(int id);
};

class Obsidian : public Block
{
public:
	Obsidian(int id);
};

class Torch : public Block
{
public:
	Torch(int id);
};

class Fire : public Block
{
public:
	Fire(int id);
};

class MonsterSpawner : public Block
{
public:
	MonsterSpawner(int id);
};

class OakWoodStairs : public Stairs
{
public:
	OakWoodStairs(int id);
};

class Chest : public Block
{
public:
	Chest(int id);
};

class RedstoneWire : public Block
{
public:
	RedstoneWire(int id);
};

class DiamondOre : public Block
{
public:
	DiamondOre(int id);
};

class BlockofDiamond : public Block
{
public:
	BlockofDiamond(int id);
};

class CraftingTable : public Block
{
public:
	CraftingTable(int id);
};

class Wheat : public Block
{
public:
	Wheat(int id);
};

class Farmland : public Block
{
public:
	Farmland(int id);
};

class Furnace : public Block
{
public:
	Furnace(int id);
};

class BurningFurnace : public Block
{
public:
	BurningFurnace(int id);
};

class SignPost : public Block
{
public:
	SignPost(int id);
};

class WoodenDoor : public Block
{
public:
	WoodenDoor(int id);
};

class Ladders : public Block
{
public:
	Ladders(int id);
};

class Rail : public Block
{
public:
	Rail(int id);
};

class CobblestoneStairs : public Stairs
{
public:
	CobblestoneStairs(int id);
};

class WallSign : public Block
{
public:
	WallSign(int id);
};

class Lever : public Block
{
public:
	Lever(int id);
};

class StonePressurePlate : public Block
{
public:
	StonePressurePlate(int id);
};

class IronDoor : public Block
{
public:
	IronDoor(int id);
};

class WoodenPressurePlate : public Block
{
public:
	WoodenPressurePlate(int id);
};

class RedstoneOre : public Block
{
public:
	RedstoneOre(int id);
};

class GlowingRedstoneOre : public Block
{
public:
	GlowingRedstoneOre(int id);
};

class RedstoneTorchinactive : public Block
{
public:
	RedstoneTorchinactive(int id);
};

class RedstoneTorchactive : public Block
{
public:
	RedstoneTorchactive(int id);
};

class StoneButton : public Block
{
public:
	StoneButton(int id);
};

class Snow : public Block
{
public:
	Snow(int id);
};

class Ice : public Block
{
public:
	Ice(int id);
};

class SnowBlock : public Block
{
public:
	SnowBlock(int id);
};

class Cactus : public Block
{
public:
	Cactus(int id);
};

class Clay : public Block
{
public:
	Clay(int id);
};

class SugarCane : public Block
{
public:
	SugarCane(int id);
};

class Jukebox : public Block
{
public:
	Jukebox(int id);
};

class Fence : public Block
{
public:
	Fence(int id);
};

class Pumpkin : public Block
{
public:
	Pumpkin(int id);
};

class Netherrack : public Block
{
public:
	Netherrack(int id);
};

class SoulSand : public Block
{
public:
	SoulSand(int id);
};

class Glowstone : public Block
{
public:
	Glowstone(int id);
};

class NetherPortal : public Block
{
public:
	NetherPortal(int id);
};

class JackLantern : public Block
{
public:
	JackLantern(int id);
};

class CakeBlock : public Block
{
public:
	CakeBlock(int id);
};

class RedstoneRepeaterinactive : public Block
{
public:
	RedstoneRepeaterinactive(int id);
};

class RedstoneRepeateractive : public Block
{
public:
	RedstoneRepeateractive(int id);
};

class LockedChest : public Block
{
public:
	LockedChest(int id);
};

class Trapdoor : public Block
{
public:
	Trapdoor(int id);
};

class MonsterEgg : public Block
{
public:
	MonsterEgg(int id);
};

class StoneBricks : public Block
{
public:
	StoneBricks(int id);
};

class HugeBrownMushroom : public Block
{
public:
	HugeBrownMushroom(int id);
};

class HugeRedMushroom : public Block
{
public:
	HugeRedMushroom(int id);
};

class IronBars : public Block
{
public:
	IronBars(int id);
};

class GlassPane : public Block
{
public:
	GlassPane(int id);
};

class Melon : public Block
{
public:
	Melon(int id);
};

class PumpkinStem : public Block
{
public:
	PumpkinStem(int id);
};

class MelonStem : public Block
{
public:
	MelonStem(int id);
};

class Vines : public Block
{
public:
	Vines(int id);
};

class FenceGate : public Block
{
public:
	FenceGate(int id);
};

class BrickStairs : public Stairs
{
public:
	BrickStairs(int id);
};

class StoneBrickStairs : public Stairs
{
public:
	StoneBrickStairs(int id);
};

class Mycelium : public Block
{
public:
	Mycelium(int id);
};

class LilyPad : public Block
{
public:
	LilyPad(int id);
};

class NetherBrick : public Block
{
public:
	NetherBrick(int id);
};

class NetherBrickFence : public Block
{
public:
	NetherBrickFence(int id);
};

class NetherBrickStairs : public Stairs
{
public:
	NetherBrickStairs(int id);
};

class NetherWart : public Block
{
public:
	NetherWart(int id);
};

class Enchantmentable : public Block
{
public:
	Enchantmentable(int id);
};

class BrewingStand : public Block
{
public:
	BrewingStand(int id);
};

class Cauldron : public Block
{
public:
	Cauldron(int id);
};

class EndPortal : public Block
{
public:
	EndPortal(int id);
};

class EndPortalBlock : public Block
{
public:
	EndPortalBlock(int id);
};

class EndStone : public Block
{
public:
	EndStone(int id);
};

class DragonEgg : public Block
{
public:
	DragonEgg(int id);
};

class RedstoneLamp : public Block
{
public:
	RedstoneLamp(int id);
};

class RedstoneLampOn : public Block
{
public:
	RedstoneLampOn(int id);
};

class WoodenDoubleSlab : public Block
{
public:
	WoodenDoubleSlab(int id);
};

class WoodenSlab : public Block
{
public:
	WoodenSlab(int id);
};

class Cocoa : public Block
{
public:
	Cocoa(int id);
};

class SandstoneStairs : public Stairs
{
public:
	SandstoneStairs(int id);
};

class EmeraldOre : public Block
{
public:
	EmeraldOre(int id);
};

class EnderChest : public Block
{
public:
	EnderChest(int id);
};

class TripwireHook : public Block
{
public:
	TripwireHook(int id);
};

class Tripwire : public Block
{
public:
	Tripwire(int id);
};

class BlockofEmeral : public Block
{
public:
	BlockofEmeral(int id);
};

class SpruceWoodStairs : public Stairs
{
public:
	SpruceWoodStairs(int id);
};

class BirchWoodStairs : public Stairs
{
public:
	BirchWoodStairs(int id);
};

class JungleWoodStairs : public Stairs
{
public:
	JungleWoodStairs(int id);
};

class CommandBlock : public Block
{
public:
	CommandBlock(int id);
};

class Beacon : public Block
{
public:
	Beacon(int id);
};

class CobblestoneWall : public Block
{
public:
	CobblestoneWall(int id);
};

class FlowerPot : public Block
{
public:
	FlowerPot(int id);
};

class Carrots : public Block
{
public:
	Carrots(int id);
};

class Potatoes : public Block
{
public:
	Potatoes(int id);
};

class WoodenButton : public Block
{
public:
	WoodenButton(int id);
};

class MobHead : public Block
{
public:
	MobHead(int id);
};

class Anvil : public Block
{
public:
	Anvil(int id);
};

class TrappedChest : public Block
{
public:
	TrappedChest(int id);
};

class WeightedPressurePlateLight : public Block
{
public:
	WeightedPressurePlateLight(int id);
};

class WeightedPressurePlateHeavy : public Block
{
public:
	WeightedPressurePlateHeavy(int id);
};

class RedstoneComparator : public Block
{
public:
	RedstoneComparator(int id);
};

class RedstoneComparatorOn : public Block
{
public:
	RedstoneComparatorOn(int id);
};

class DaylightSensor : public Block
{
public:
	DaylightSensor(int id);
};

class BlockofRedstone : public Block
{
public:
	BlockofRedstone(int id);
};

class NetherQuartzOre : public Block
{
public:
	NetherQuartzOre(int id);
};

class Hopper : public Block
{
public:
	Hopper(int id);
};

class BlockofQuartz : public Block
{
public:
	BlockofQuartz(int id);
};

class QuartzStairs : public Stairs
{
public:
	QuartzStairs(int id);
};

class ActivatorRail : public Block
{
public:
	ActivatorRail(int id);
};

class Dropper : public Block
{
public:
	Dropper(int id);
};

class StainedClay : public Block
{
public:
	StainedClay(int id);
};


#endif