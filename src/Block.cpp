#include "Block.h"
using namespace std;

Block* Block::BlockList[5000] = {0};

Block::Block(int _id)
{
	BlockList[_id] = this;
	id = _id;
	renderType = NORMAL;
	transparent = 0;
}

int Block::getColor(Section* section,int x,int y,int z)
{
	return 16777215;
}

string Block::getTexName(int face,int meta)
{
	return mTexName[face];
}

Air::Air(int id):
Block(id)
{
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
}

Stone::Stone(int id):
Block(id)
{
	mTexName.push_back("stone");
	mTexName.push_back("stone");
	mTexName.push_back("stone");
	mTexName.push_back("stone");
	mTexName.push_back("stone");
	mTexName.push_back("stone");
}

GrassBlock::GrassBlock(int id):
Block(id)
{
	mTexName.push_back("grass_top");
	mTexName.push_back("dirt");
	mTexName.push_back("grass_side");
	mTexName.push_back("grass_side");
	mTexName.push_back("grass_side");
	mTexName.push_back("grass_side");
}

Dirt::Dirt(int id):
Block(id)
{
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
}

Cobblestone::Cobblestone(int id):
Block(id)
{
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
}

WoodPlanks::WoodPlanks(int id):
Block(id)
{
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
}

Saplings::Saplings(int id):
Block(id)
{
	mTexName.push_back("sapling");
	mTexName.push_back("sapling_spruce");
	mTexName.push_back("sapling_birch");
	mTexName.push_back("sapling_jungle");
	renderType = FLOWER;
	transparent = 1;
}
string Saplings::getTexName(int face,int meta)
{
	return mTexName[meta&0x3];
}

Bedrock::Bedrock(int id):
Block(id)
{
	mTexName.push_back("bedrock");
	mTexName.push_back("bedrock");
	mTexName.push_back("bedrock");
	mTexName.push_back("bedrock");
	mTexName.push_back("bedrock");
	mTexName.push_back("bedrock");
}

Water::Water(int id):
Block(id)
{
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	transparent = 1;
}

Stationarywater::Stationarywater(int id):
Block(id)
{
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	mTexName.push_back("water");
	transparent = 1;
}

Lava::Lava(int id):
Block(id)
{
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
}

Stationarylava::Stationarylava(int id):
Block(id)
{
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
	mTexName.push_back("lava");
}

Sand::Sand(int id):
Block(id)
{
	mTexName.push_back("sand");
	mTexName.push_back("sand");
	mTexName.push_back("sand");
	mTexName.push_back("sand");
	mTexName.push_back("sand");
	mTexName.push_back("sand");
}

Gravel::Gravel(int id):
Block(id)
{
	mTexName.push_back("gravel");
	mTexName.push_back("gravel");
	mTexName.push_back("gravel");
	mTexName.push_back("gravel");
	mTexName.push_back("gravel");
	mTexName.push_back("gravel");
}

GoldOre::GoldOre(int id):
Block(id)
{
	mTexName.push_back("oreGold");
	mTexName.push_back("oreGold");
	mTexName.push_back("oreGold");
	mTexName.push_back("oreGold");
	mTexName.push_back("oreGold");
	mTexName.push_back("oreGold");
}

IronOre::IronOre(int id):
Block(id)
{
	mTexName.push_back("oreIron");
	mTexName.push_back("oreIron");
	mTexName.push_back("oreIron");
	mTexName.push_back("oreIron");
	mTexName.push_back("oreIron");
	mTexName.push_back("oreIron");
}

CoalOre::CoalOre(int id):
Block(id)
{
	mTexName.push_back("oreCoal");
	mTexName.push_back("oreCoal");
	mTexName.push_back("oreCoal");
	mTexName.push_back("oreCoal");
	mTexName.push_back("oreCoal");
	mTexName.push_back("oreCoal");
}

Wood::Wood(int id):
Block(id)
{
	mTexName.push_back("tree_top");
	mTexName.push_back("tree_top");
	mTexName.push_back("tree_side");
	mTexName.push_back("tree_side");
	mTexName.push_back("tree_side");
	mTexName.push_back("tree_side");
}

Leaves::Leaves(int id):
Block(id)
{
	mTexName.push_back("leaves_spruce");
	mTexName.push_back("leaves_spruce");
	mTexName.push_back("leaves_spruce");
	mTexName.push_back("leaves_spruce");
	mTexName.push_back("leaves_spruce");
	mTexName.push_back("leaves_spruce");
	transparent = 1;
}

Sponge::Sponge(int id):
Block(id)
{
	mTexName.push_back("sponge");
	mTexName.push_back("sponge");
	mTexName.push_back("sponge");
	mTexName.push_back("sponge");
	mTexName.push_back("sponge");
	mTexName.push_back("sponge");
}

Glass::Glass(int id):
Block(id)
{
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	transparent = 1;
}

LapisLazuliOre::LapisLazuliOre(int id):
Block(id)
{
	mTexName.push_back("oreLapis");
	mTexName.push_back("oreLapis");
	mTexName.push_back("oreLapis");
	mTexName.push_back("oreLapis");
	mTexName.push_back("oreLapis");
	mTexName.push_back("oreLapis");
}

LapisLazuliBlock::LapisLazuliBlock(int id):
Block(id)
{
	mTexName.push_back("blockLapis");
	mTexName.push_back("blockLapis");
	mTexName.push_back("blockLapis");
	mTexName.push_back("blockLapis");
	mTexName.push_back("blockLapis");
	mTexName.push_back("blockLapis");
}

Dispenser::Dispenser(int id):
Block(id)
{
	mTexName.push_back("furnace_top");
	mTexName.push_back("furnace_top");
	mTexName.push_back("dispenser_front");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
}

Sandstone::Sandstone(int id):
Block(id)
{
	mTexName.push_back("sandstone_top");
	mTexName.push_back("sandstone_bottom");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
}

NoteBlock::NoteBlock(int id):
Block(id)
{
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
}

Bed::Bed(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

PoweredRail::PoweredRail(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

DetectorRail::DetectorRail(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

StickyPiston::StickyPiston(int id):
Block(id)
{
	mTexName.push_back("piston_top_sticky");
	mTexName.push_back("piston_bottom");
	mTexName.push_back("piston_side");
	mTexName.push_back("piston_side");
	mTexName.push_back("piston_side");
	mTexName.push_back("piston_side");
}

Cobweb::Cobweb(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

Grass::Grass(int id):
Block(id)
{
	mTexName.push_back("tallgrass");
	mTexName.push_back("tallgrass");
	mTexName.push_back("tallgrass");
	mTexName.push_back("tallgrass");
	mTexName.push_back("tallgrass");
	mTexName.push_back("tallgrass");
	renderType = FLOWER;
	transparent = 1;
}

int Grass::getColor(Section* section,int x,int y,int z)
{
	return -7226023;
}

DeadBush::DeadBush(int id):
Block(id)
{
	mTexName.push_back("deadbush");
	mTexName.push_back("deadbush");
	mTexName.push_back("deadbush");
	mTexName.push_back("deadbush");
	mTexName.push_back("deadbush");
	mTexName.push_back("deadbush");
	renderType = FLOWER;
	transparent = 1;
}

Piston::Piston(int id):
Block(id)
{
	mTexName.push_back("piston_top");
	mTexName.push_back("piston_bottom");
	mTexName.push_back("piston_side");
	mTexName.push_back("piston_side");
	mTexName.push_back("piston_side");
	mTexName.push_back("piston_side");
}

PistonExtension::PistonExtension(int id):
Block(id)
{
	mTexName.push_back("piston_top");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");

	renderType = NO;
	transparent = 1;
}

Wool::Wool(int id):
Block(id)
{
	mTexName.push_back("cloth_0");
	mTexName.push_back("cloth_1");
	mTexName.push_back("cloth_2");
	mTexName.push_back("cloth_3");
	mTexName.push_back("cloth_4");
	mTexName.push_back("cloth_5");
	mTexName.push_back("cloth_6");
	mTexName.push_back("cloth_7");
	mTexName.push_back("cloth_8");
	mTexName.push_back("cloth_9");
	mTexName.push_back("cloth_10");
	mTexName.push_back("cloth_11");
	mTexName.push_back("cloth_12");
	mTexName.push_back("cloth_13");
	mTexName.push_back("cloth_14");
	mTexName.push_back("cloth_15");
}
string Wool::getTexName(int face,int meta)
{
	return mTexName[meta&0xf];
}

BlockmovedbyPiston::BlockmovedbyPiston(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

Dandelion::Dandelion(int id):
Block(id)
{
	mTexName.push_back("flower");
	mTexName.push_back("flower");
	mTexName.push_back("flower");
	mTexName.push_back("flower");
	mTexName.push_back("flower");
	mTexName.push_back("flower");
	renderType = FLOWER;
	transparent = 1;
}

Rose::Rose(int id):
Block(id)
{
	mTexName.push_back("rose");
	mTexName.push_back("rose");
	mTexName.push_back("rose");
	mTexName.push_back("rose");
	mTexName.push_back("rose");
	mTexName.push_back("rose");
	renderType = FLOWER;
	transparent = 1;
}

BrownMushroom::BrownMushroom(int id):
Block(id)
{
	mTexName.push_back("mushroom_brown");
	mTexName.push_back("mushroom_brown");
	mTexName.push_back("mushroom_brown");
	mTexName.push_back("mushroom_brown");
	mTexName.push_back("mushroom_brown");
	mTexName.push_back("mushroom_brown");
	renderType = FLOWER;
	transparent = 1;
}

RedMushroom::RedMushroom(int id):
Block(id)
{
	mTexName.push_back("mushroom_red");
	mTexName.push_back("mushroom_red");
	mTexName.push_back("mushroom_red");
	mTexName.push_back("mushroom_red");
	mTexName.push_back("mushroom_red");
	mTexName.push_back("mushroom_red");
	renderType = FLOWER;
	transparent = 1;
}

BlockofGold::BlockofGold(int id):
Block(id)
{
	mTexName.push_back("blockGold");
	mTexName.push_back("blockGold");
	mTexName.push_back("blockGold");
	mTexName.push_back("blockGold");
	mTexName.push_back("blockGold");
	mTexName.push_back("blockGold");
}

BlockofIron::BlockofIron(int id):
Block(id)
{
	mTexName.push_back("blockIron");
	mTexName.push_back("blockIron");
	mTexName.push_back("blockIron");
	mTexName.push_back("blockIron");
	mTexName.push_back("blockIron");
	mTexName.push_back("blockIron");
}

DoubleSlabs::DoubleSlabs(int id):
Block(id)
{
	mTexName.push_back("stoneslab_top");
	mTexName.push_back("stoneslab_top");
	mTexName.push_back("stoneslab_side");
	mTexName.push_back("stoneslab_side");
	mTexName.push_back("stoneslab_side");
	mTexName.push_back("stoneslab_side");
}

Slabs::Slabs(int id):
Block(id)
{
	mTexName.push_back("stoneslab_top");
	mTexName.push_back("stoneslab_top");
	mTexName.push_back("stoneslab_side");
	mTexName.push_back("stoneslab_side");
	mTexName.push_back("stoneslab_side");
	mTexName.push_back("stoneslab_side");
}

Bricks::Bricks(int id):
Block(id)
{
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
}

TNT::TNT(int id):
Block(id)
{
	mTexName.push_back("tnt_top");
	mTexName.push_back("tnt_bottom");
	mTexName.push_back("tnt_side");
	mTexName.push_back("tnt_side");
	mTexName.push_back("tnt_side");
	mTexName.push_back("tnt_side");
}

Bookshelf::Bookshelf(int id):
Block(id)
{
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("bookshelf");
	mTexName.push_back("bookshelf");
	mTexName.push_back("bookshelf");
	mTexName.push_back("bookshelf");
}

MossStone::MossStone(int id):
Block(id)
{
	mTexName.push_back("stoneMoss");
	mTexName.push_back("stoneMoss");
	mTexName.push_back("stoneMoss");
	mTexName.push_back("stoneMoss");
	mTexName.push_back("stoneMoss");
	mTexName.push_back("stoneMoss");
}

Obsidian::Obsidian(int id):
Block(id)
{
	mTexName.push_back("obsidian");
	mTexName.push_back("obsidian");
	mTexName.push_back("obsidian");
	mTexName.push_back("obsidian");
	mTexName.push_back("obsidian");
	mTexName.push_back("obsidian");
}

Torch::Torch(int id):
Block(id)
{
	mTexName.push_back("torch");
	mTexName.push_back("torch");
	mTexName.push_back("torch");
	mTexName.push_back("torch");
	mTexName.push_back("torch");
	mTexName.push_back("torch");
	renderType = TORCH;
	transparent = 1;
}

Fire::Fire(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

MonsterSpawner::MonsterSpawner(int id):
Block(id)
{
	mTexName.push_back("mobSpawner");
	mTexName.push_back("mobSpawner");
	mTexName.push_back("mobSpawner");
	mTexName.push_back("mobSpawner");
	mTexName.push_back("mobSpawner");
	mTexName.push_back("mobSpawner");
	transparent = 1;
}

OakWoodStairs::OakWoodStairs(int id):
Stairs(id)
{
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
}

Chest::Chest(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

RedstoneWire::RedstoneWire(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

DiamondOre::DiamondOre(int id):
Block(id)
{
	mTexName.push_back("oreDiamond");
	mTexName.push_back("oreDiamond");
	mTexName.push_back("oreDiamond");
	mTexName.push_back("oreDiamond");
	mTexName.push_back("oreDiamond");
	mTexName.push_back("oreDiamond");
}

BlockofDiamond::BlockofDiamond(int id):
Block(id)
{
	mTexName.push_back("blockDiamond");
	mTexName.push_back("blockDiamond");
	mTexName.push_back("blockDiamond");
	mTexName.push_back("blockDiamond");
	mTexName.push_back("blockDiamond");
	mTexName.push_back("blockDiamond");
}

CraftingTable::CraftingTable(int id):
Block(id)
{
	mTexName.push_back("workbench_top");
	mTexName.push_back("wood");
	mTexName.push_back("workbench_front");
	mTexName.push_back("workbench_front");
	mTexName.push_back("workbench_side");
	mTexName.push_back("workbench_side");
}

Wheat::Wheat(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Farmland::Farmland(int id):
Block(id)
{
	mTexName.push_back("farmland_dry");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
	mTexName.push_back("dirt");
}

Furnace::Furnace(int id):
Block(id)
{
	mTexName.push_back("furnace_top");
	mTexName.push_back("furnace_top");
	mTexName.push_back("furnace_front");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
}

BurningFurnace::BurningFurnace(int id):
Block(id)
{
	mTexName.push_back("furnace_top");
	mTexName.push_back("furnace_top");
	mTexName.push_back("furnace_front_lit");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
}

SignPost::SignPost(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

WoodenDoor::WoodenDoor(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = DOOR;
	transparent = 1;
}

Ladders::Ladders(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Rail::Rail(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

CobblestoneStairs::CobblestoneStairs(int id):
Stairs(id)
{
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
}

WallSign::WallSign(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

Lever::Lever(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

StonePressurePlate::StonePressurePlate(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

IronDoor::IronDoor(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = DOOR;
	transparent = 1;
}

WoodenPressurePlate::WoodenPressurePlate(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

RedstoneOre::RedstoneOre(int id):
Block(id)
{
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
}

GlowingRedstoneOre::GlowingRedstoneOre(int id):
Block(id)
{
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
	mTexName.push_back("oreRedstone");
}

RedstoneTorchinactive::RedstoneTorchinactive(int id):
Block(id)
{
	mTexName.push_back("redtorch");
	mTexName.push_back("redtorch");
	mTexName.push_back("redtorch");
	mTexName.push_back("redtorch");
	mTexName.push_back("redtorch");
	mTexName.push_back("redtorch");
	renderType = TORCH;
}

RedstoneTorchactive::RedstoneTorchactive(int id):
Block(id)
{
	mTexName.push_back("redtorch_lit");
	mTexName.push_back("redtorch_lit");
	mTexName.push_back("redtorch_lit");
	mTexName.push_back("redtorch_lit");
	mTexName.push_back("redtorch_lit");
	mTexName.push_back("redtorch_lit");
	renderType = TORCH;
}

StoneButton::StoneButton(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Snow::Snow(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

Ice::Ice(int id):
Block(id)
{
	mTexName.push_back("ice");
	mTexName.push_back("ice");
	mTexName.push_back("ice");
	mTexName.push_back("ice");
	mTexName.push_back("ice");
	mTexName.push_back("ice");
	transparent = 1;
}

SnowBlock::SnowBlock(int id):
Block(id)
{
	mTexName.push_back("snow");
	mTexName.push_back("snow");
	mTexName.push_back("snow");
	mTexName.push_back("snow");
	mTexName.push_back("snow");
	mTexName.push_back("snow");
}

Cactus::Cactus(int id):
Block(id)
{
	mTexName.push_back("cactus_top");
	mTexName.push_back("cactus_bottom");
	mTexName.push_back("cactus_side");
	mTexName.push_back("cactus_side");
	mTexName.push_back("cactus_side");
	mTexName.push_back("cactus_side");
	transparent = 1;
}

Clay::Clay(int id):
Block(id)
{
	mTexName.push_back("clay");
	mTexName.push_back("clay");
	mTexName.push_back("clay");
	mTexName.push_back("clay");
	mTexName.push_back("clay");
	mTexName.push_back("clay");
}

SugarCane::SugarCane(int id):
Block(id)
{
	mTexName.push_back("reeds");
	mTexName.push_back("reeds");
	mTexName.push_back("reeds");
	mTexName.push_back("reeds");
	mTexName.push_back("reeds");
	mTexName.push_back("reeds");
	renderType = FLOWER;
	transparent = 1;
}

Jukebox::Jukebox(int id):
Block(id)
{
	mTexName.push_back("jukebox_top");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
	mTexName.push_back("musicBlock");
}

Fence::Fence(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Pumpkin::Pumpkin(int id):
Block(id)
{
	mTexName.push_back("pumpkin_top");
	mTexName.push_back("pumpkin_top");
	mTexName.push_back("pumpkin_face");
	mTexName.push_back("pumpkin_side");
	mTexName.push_back("pumpkin_side");
	mTexName.push_back("pumpkin_side");
}

Netherrack::Netherrack(int id):
Block(id)
{
	mTexName.push_back("hellrock");
	mTexName.push_back("hellrock");
	mTexName.push_back("hellrock");
	mTexName.push_back("hellrock");
	mTexName.push_back("hellrock");
	mTexName.push_back("hellrock");
}

SoulSand::SoulSand(int id):
Block(id)
{
	mTexName.push_back("hellsand");
	mTexName.push_back("hellsand");
	mTexName.push_back("hellsand");
	mTexName.push_back("hellsand");
	mTexName.push_back("hellsand");
	mTexName.push_back("hellsand");
}

Glowstone::Glowstone(int id):
Block(id)
{
	mTexName.push_back("lightgem");
	mTexName.push_back("lightgem");
	mTexName.push_back("lightgem");
	mTexName.push_back("lightgem");
	mTexName.push_back("lightgem");
	mTexName.push_back("lightgem");
}

NetherPortal::NetherPortal(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

JackLantern::JackLantern(int id):
Block(id)
{
	mTexName.push_back("pumpkin_top");
	mTexName.push_back("pumpkin_top");
	mTexName.push_back("pumpkin_jack");
	mTexName.push_back("pumpkin_side");
	mTexName.push_back("pumpkin_side");
	mTexName.push_back("pumpkin_side");
}

CakeBlock::CakeBlock(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

RedstoneRepeaterinactive::RedstoneRepeaterinactive(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

RedstoneRepeateractive::RedstoneRepeateractive(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

LockedChest::LockedChest(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Trapdoor::Trapdoor(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = DOOR;
	transparent = 1;
}

MonsterEgg::MonsterEgg(int id):
Block(id)
{
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
	mTexName.push_back("stonebrick");
}

StoneBricks::StoneBricks(int id):
Block(id)
{
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
}

HugeBrownMushroom::HugeBrownMushroom(int id):
Block(id)
{
	mTexName.push_back("mushroom_skin_brown");
	mTexName.push_back("mushroom_skin_brown");
	mTexName.push_back("mushroom_skin_brown");
	mTexName.push_back("mushroom_skin_brown");
	mTexName.push_back("mushroom_skin_brown");
	mTexName.push_back("mushroom_skin_brown");
}

HugeRedMushroom::HugeRedMushroom(int id):
Block(id)
{
	mTexName.push_back("mushroom_skin_red");
	mTexName.push_back("mushroom_skin_red");
	mTexName.push_back("mushroom_skin_red");
	mTexName.push_back("mushroom_skin_red");
	mTexName.push_back("mushroom_skin_red");
	mTexName.push_back("mushroom_skin_red");
}

IronBars::IronBars(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

GlassPane::GlassPane(int id):
Block(id)
{
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	mTexName.push_back("glass");
	transparent = 1;
}

Melon::Melon(int id):
Block(id)
{
	mTexName.push_back("melon_top");
	mTexName.push_back("melon_top");
	mTexName.push_back("melon_side");
	mTexName.push_back("melon_side");
	mTexName.push_back("melon_side");
	mTexName.push_back("melon_side");
}

PumpkinStem::PumpkinStem(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

MelonStem::MelonStem(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Vines::Vines(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

FenceGate::FenceGate(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

BrickStairs::BrickStairs(int id):
Stairs(id)
{
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
	mTexName.push_back("brick");
}

StoneBrickStairs::StoneBrickStairs(int id):
Stairs(id)
{
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
	mTexName.push_back("stonebricksmooth");
}

Mycelium::Mycelium(int id):
Block(id)
{
	mTexName.push_back("mycel_top");
	mTexName.push_back("dirt");
	mTexName.push_back("mycel_side");
	mTexName.push_back("mycel_side");
	mTexName.push_back("mycel_side");
	mTexName.push_back("mycel_side");
}

LilyPad::LilyPad(int id):
Block(id)
{
	mTexName.push_back("waterlily");
	mTexName.push_back("waterlily");
	mTexName.push_back("waterlily");
	mTexName.push_back("waterlily");
	mTexName.push_back("waterlily");
	mTexName.push_back("waterlily");
	renderType = LILYPAD;
}

NetherBrick::NetherBrick(int id):
Block(id)
{
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
}

NetherBrickFence::NetherBrickFence(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

NetherBrickStairs::NetherBrickStairs(int id):
Stairs(id)
{
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
	mTexName.push_back("netherBrick");
}

NetherWart::NetherWart(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Enchantmentable::Enchantmentable(int id):
Block(id)
{
	mTexName.push_back("enchantment_top");
	mTexName.push_back("enchantment_bottom");
	mTexName.push_back("enchantment_side");
	mTexName.push_back("enchantment_side");
	mTexName.push_back("enchantment_side");
	mTexName.push_back("enchantment_side");
	transparent = 1;
}

BrewingStand::BrewingStand(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Cauldron::Cauldron(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

EndPortal::EndPortal(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

EndPortalBlock::EndPortalBlock(int id):
Block(id)
{
	mTexName.push_back("endframe_top");
	mTexName.push_back("whiteStone");
	mTexName.push_back("endframe_side");
	mTexName.push_back("endframe_side");
	mTexName.push_back("endframe_side");
	mTexName.push_back("endframe_side");
}

EndStone::EndStone(int id):
Block(id)
{
	mTexName.push_back("whiteStone");
	mTexName.push_back("whiteStone");
	mTexName.push_back("whiteStone");
	mTexName.push_back("whiteStone");
	mTexName.push_back("whiteStone");
	mTexName.push_back("whiteStone");
}

DragonEgg::DragonEgg(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

RedstoneLamp::RedstoneLamp(int id):
Block(id)
{
	mTexName.push_back("redstoneLight");
	mTexName.push_back("redstoneLight");
	mTexName.push_back("redstoneLight");
	mTexName.push_back("redstoneLight");
	mTexName.push_back("redstoneLight");
	mTexName.push_back("redstoneLight");
}

RedstoneLampOn::RedstoneLampOn(int id):
Block(id)
{
	mTexName.push_back("redstoneLight_lit");
	mTexName.push_back("redstoneLight_lit");
	mTexName.push_back("redstoneLight_lit");
	mTexName.push_back("redstoneLight_lit");
	mTexName.push_back("redstoneLight_lit");
	mTexName.push_back("redstoneLight_lit");
}

WoodenDoubleSlab::WoodenDoubleSlab(int id):
Block(id)
{
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
}

WoodenSlab::WoodenSlab(int id):
Block(id)
{
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
	mTexName.push_back("wood");
}

Cocoa::Cocoa(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

SandstoneStairs::SandstoneStairs(int id):
Stairs(id)
{
	mTexName.push_back("sandstone_top");
	mTexName.push_back("sandstone_bottom");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
	mTexName.push_back("sandstone_side");
}

EmeraldOre::EmeraldOre(int id):
Block(id)
{
	mTexName.push_back("oreemerald");
	mTexName.push_back("oreemerald");
	mTexName.push_back("oreemerald");
	mTexName.push_back("oreemerald");
	mTexName.push_back("oreemerald");
	mTexName.push_back("oreemerald");
}

EnderChest::EnderChest(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

TripwireHook::TripwireHook(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Tripwire::Tripwire(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

BlockofEmeral::BlockofEmeral(int id):
Block(id)
{
	mTexName.push_back("blockemerald");
	mTexName.push_back("blockemerald");
	mTexName.push_back("blockemerald");
	mTexName.push_back("blockemerald");
	mTexName.push_back("blockemerald");
	mTexName.push_back("blockemerald");
}

SpruceWoodStairs::SpruceWoodStairs(int id):
Stairs(id)
{
	mTexName.push_back("wood_spruce");
	mTexName.push_back("wood_spruce");
	mTexName.push_back("wood_spruce");
	mTexName.push_back("wood_spruce");
	mTexName.push_back("wood_spruce");
	mTexName.push_back("wood_spruce");
}

BirchWoodStairs::BirchWoodStairs(int id):
Stairs(id)
{
	mTexName.push_back("wood_birch");
	mTexName.push_back("wood_birch");
	mTexName.push_back("wood_birch");
	mTexName.push_back("wood_birch");
	mTexName.push_back("wood_birch");
	mTexName.push_back("wood_birch");
}

JungleWoodStairs::JungleWoodStairs(int id):
Stairs(id)
{
	mTexName.push_back("wood_jungle");
	mTexName.push_back("wood_jungle");
	mTexName.push_back("wood_jungle");
	mTexName.push_back("wood_jungle");
	mTexName.push_back("wood_jungle");
	mTexName.push_back("wood_jungle");
}

CommandBlock::CommandBlock(int id):
Block(id)
{
	mTexName.push_back("commandBlock");
	mTexName.push_back("commandBlock");
	mTexName.push_back("commandBlock");
	mTexName.push_back("commandBlock");
	mTexName.push_back("commandBlock");
	mTexName.push_back("commandBlock");
}

Beacon::Beacon(int id):
Block(id)
{
	mTexName.push_back("beacon");
	mTexName.push_back("beacon");
	mTexName.push_back("beacon");
	mTexName.push_back("beacon");
	mTexName.push_back("beacon");
	mTexName.push_back("beacon");
}

CobblestoneWall::CobblestoneWall(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

FlowerPot::FlowerPot(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Carrots::Carrots(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Potatoes::Potatoes(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

WoodenButton::WoodenButton(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

MobHead::MobHead(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Anvil::Anvil(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

TrappedChest::TrappedChest(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

WeightedPressurePlateLight::WeightedPressurePlateLight(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

WeightedPressurePlateHeavy::WeightedPressurePlateHeavy(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	renderType = NO;
	transparent = 1;
}

RedstoneComparator::RedstoneComparator(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

RedstoneComparatorOn::RedstoneComparatorOn(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

DaylightSensor::DaylightSensor(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

BlockofRedstone::BlockofRedstone(int id):
Block(id)
{
	mTexName.push_back("blockRedstone");
	mTexName.push_back("blockRedstone");
	mTexName.push_back("blockRedstone");
	mTexName.push_back("blockRedstone");
	mTexName.push_back("blockRedstone");
	mTexName.push_back("blockRedstone");
}

NetherQuartzOre::NetherQuartzOre(int id):
Block(id)
{
	mTexName.push_back("netherquartz");
	mTexName.push_back("netherquartz");
	mTexName.push_back("netherquartz");
	mTexName.push_back("netherquartz");
	mTexName.push_back("netherquartz");
	mTexName.push_back("netherquartz");
}

Hopper::Hopper(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

BlockofQuartz::BlockofQuartz(int id):
Block(id)
{
	mTexName.push_back("quartzBlock");
	mTexName.push_back("quartzBlock");
	mTexName.push_back("quartzBlock");
	mTexName.push_back("quartzBlock");
	mTexName.push_back("quartzBlock");
	mTexName.push_back("quartzBlock");
}

QuartzStairs::QuartzStairs(int id):
Stairs(id)
{
	mTexName.push_back("quartzblock_top");
	mTexName.push_back("quartzblock_bottom");
	mTexName.push_back("quartzblock_side");
	mTexName.push_back("quartzblock_side");
	mTexName.push_back("quartzblock_side");
	mTexName.push_back("quartzblock_side");
}

ActivatorRail::ActivatorRail(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Dropper::Dropper(int id):
Block(id)
{
	mTexName.push_back("furnace_top");
	mTexName.push_back("furnace_top");
	mTexName.push_back("dropper_front");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
	mTexName.push_back("furnace_side");
}

StainedClay::StainedClay(int id):
Block(id)
{
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
	mTexName.push_back("missingno");
}

Block* Block::air = new Air(0);
Block* Block::stone = new Stone(1);
Block* Block::grassblock = new GrassBlock(2);
Block* Block::dirt = new Dirt(3);
Block* Block::cobblestone = new Cobblestone(4);
Block* Block::woodplanks = new WoodPlanks(5);
Block* Block::saplings = new Saplings(6);
Block* Block::bedrock = new Bedrock(7);
Block* Block::water = new Water(8);
Block* Block::stationarywater = new Stationarywater(9);
Block* Block::lava = new Lava(10);
Block* Block::stationarylava = new Stationarylava(11);
Block* Block::sand = new Sand(12);
Block* Block::gravel = new Gravel(13);
Block* Block::goldore = new GoldOre(14);
Block* Block::ironore = new IronOre(15);
Block* Block::coalore = new CoalOre(16);
Block* Block::wood = new Wood(17);
Block* Block::leaves = new Leaves(18);
Block* Block::sponge = new Sponge(19);
Block* Block::glass = new Glass(20);
Block* Block::lapislazuliore = new LapisLazuliOre(21);
Block* Block::lapislazuliblock = new LapisLazuliBlock(22);
Block* Block::dispenser = new Dispenser(23);
Block* Block::sandstone = new Sandstone(24);
Block* Block::noteblock = new NoteBlock(25);
Block* Block::bed = new Bed(26);
Block* Block::poweredrail = new PoweredRail(27);
Block* Block::detectorrail = new DetectorRail(28);
Block* Block::stickypiston = new StickyPiston(29);
Block* Block::cobweb = new Cobweb(30);
Block* Block::grass = new Grass(31);
Block* Block::deadbush = new DeadBush(32);
Block* Block::piston = new Piston(33);
Block* Block::pistonextension = new PistonExtension(34);
Block* Block::wool = new Wool(35);
Block* Block::blockmovedbypiston = new BlockmovedbyPiston(36);
Block* Block::dandelion = new Dandelion(37);
Block* Block::rose = new Rose(38);
Block* Block::brownmushroom = new BrownMushroom(39);
Block* Block::redmushroom = new RedMushroom(40);
Block* Block::blockofgold = new BlockofGold(41);
Block* Block::blockofiron = new BlockofIron(42);
Block* Block::doubleslabs = new DoubleSlabs(43);
Block* Block::slabs = new Slabs(44);
Block* Block::bricks = new Bricks(45);
Block* Block::tnt = new TNT(46);
Block* Block::bookshelf = new Bookshelf(47);
Block* Block::mossstone = new MossStone(48);
Block* Block::obsidian = new Obsidian(49);
Block* Block::torch = new Torch(50);
Block* Block::fire = new Fire(51);
Block* Block::monsterspawner = new MonsterSpawner(52);
Block* Block::oakwoodstairs = new OakWoodStairs(53);
Block* Block::chest = new Chest(54);
Block* Block::redstonewire = new RedstoneWire(55);
Block* Block::diamondore = new DiamondOre(56);
Block* Block::blockofdiamond = new BlockofDiamond(57);
Block* Block::craftingtable = new CraftingTable(58);
Block* Block::wheat = new Wheat(59);
Block* Block::farmland = new Farmland(60);
Block* Block::furnace = new Furnace(61);
Block* Block::burningfurnace = new BurningFurnace(62);
Block* Block::signpost = new SignPost(63);
Block* Block::woodendoor = new WoodenDoor(64);
Block* Block::ladders = new Ladders(65);
Block* Block::rail = new Rail(66);
Block* Block::cobblestonestairs = new CobblestoneStairs(67);
Block* Block::wallsign = new WallSign(68);
Block* Block::lever = new Lever(69);
Block* Block::stonepressureplate = new StonePressurePlate(70);
Block* Block::irondoor = new IronDoor(71);
Block* Block::woodenpressureplate = new WoodenPressurePlate(72);
Block* Block::redstoneore = new RedstoneOre(73);
Block* Block::glowingredstoneore = new GlowingRedstoneOre(74);
Block* Block::redstonetorchinactive = new RedstoneTorchinactive(75);
Block* Block::redstonetorchactive = new RedstoneTorchactive(76);
Block* Block::stonebutton = new StoneButton(77);
Block* Block::snow = new Snow(78);
Block* Block::ice = new Ice(79);
Block* Block::snowblock = new SnowBlock(80);
Block* Block::cactus = new Cactus(81);
Block* Block::clay = new Clay(82);
Block* Block::sugarcane = new SugarCane(83);
Block* Block::jukebox = new Jukebox(84);
Block* Block::fence = new Fence(85);
Block* Block::pumpkin = new Pumpkin(86);
Block* Block::netherrack = new Netherrack(87);
Block* Block::soulsand = new SoulSand(88);
Block* Block::glowstone = new Glowstone(89);
Block* Block::netherportal = new NetherPortal(90);
Block* Block::jacklantern = new JackLantern(91);
Block* Block::cakeblock = new CakeBlock(92);
Block* Block::redstonerepeaterinactive = new RedstoneRepeaterinactive(93);
Block* Block::redstonerepeateractive = new RedstoneRepeateractive(94);
Block* Block::lockedchest = new LockedChest(95);
Block* Block::trapdoor = new Trapdoor(96);
Block* Block::monsteregg = new MonsterEgg(97);
Block* Block::stonebricks = new StoneBricks(98);
Block* Block::hugebrownmushroom = new HugeBrownMushroom(99);
Block* Block::hugeredmushroom = new HugeRedMushroom(100);
Block* Block::ironbars = new IronBars(101);
Block* Block::glasspane = new GlassPane(102);
Block* Block::melon = new Melon(103);
Block* Block::pumpkinstem = new PumpkinStem(104);
Block* Block::melonstem = new MelonStem(105);
Block* Block::vines = new Vines(106);
Block* Block::fencegate = new FenceGate(107);
Block* Block::brickstairs = new BrickStairs(108);
Block* Block::stonebrickstairs = new StoneBrickStairs(109);
Block* Block::mycelium = new Mycelium(110);
Block* Block::lilypad = new LilyPad(111);
Block* Block::netherbrick = new NetherBrick(112);
Block* Block::netherbrickfence = new NetherBrickFence(113);
Block* Block::netherbrickstairs = new NetherBrickStairs(114);
Block* Block::netherwart = new NetherWart(115);
Block* Block::enchantmentable = new Enchantmentable(116);
Block* Block::brewingstand = new BrewingStand(117);
Block* Block::cauldron = new Cauldron(118);
Block* Block::endportal = new EndPortal(119);
Block* Block::endportalblock = new EndPortalBlock(120);
Block* Block::endstone = new EndStone(121);
Block* Block::dragonegg = new DragonEgg(122);
Block* Block::redstonelamp = new RedstoneLamp(123);
Block* Block::redstonelampon = new RedstoneLampOn(124);
Block* Block::woodendoubleslab = new WoodenDoubleSlab(125);
Block* Block::woodenslab = new WoodenSlab(126);
Block* Block::cocoa = new Cocoa(127);
Block* Block::sandstonestairs = new SandstoneStairs(128);
Block* Block::emeraldore = new EmeraldOre(129);
Block* Block::enderchest = new EnderChest(130);
Block* Block::tripwirehook = new TripwireHook(131);
Block* Block::tripwire = new Tripwire(132);
Block* Block::blockofemeral = new BlockofEmeral(133);
Block* Block::sprucewoodstairs = new SpruceWoodStairs(134);
Block* Block::birchwoodstairs = new BirchWoodStairs(135);
Block* Block::junglewoodstairs = new JungleWoodStairs(136);
Block* Block::commandblock = new CommandBlock(137);
Block* Block::beacon = new Beacon(138);
Block* Block::cobblestonewall = new CobblestoneWall(139);
Block* Block::flowerpot = new FlowerPot(140);
Block* Block::carrots = new Carrots(141);
Block* Block::potatoes = new Potatoes(142);
Block* Block::woodenbutton = new WoodenButton(143);
Block* Block::mobhead = new MobHead(144);
Block* Block::anvil = new Anvil(145);
Block* Block::trappedchest = new TrappedChest(146);
Block* Block::weightedpressureplatelight = new WeightedPressurePlateLight(147);
Block* Block::weightedpressureplateheavy = new WeightedPressurePlateHeavy(148);
Block* Block::redstonecomparator = new RedstoneComparator(149);
Block* Block::redstonecomparatoron = new RedstoneComparatorOn(150);
Block* Block::daylightsensor = new DaylightSensor(151);
Block* Block::blockofredstone = new BlockofRedstone(152);
Block* Block::netherquartzore = new NetherQuartzOre(153);
Block* Block::hopper = new Hopper(154);
Block* Block::blockofquartz = new BlockofQuartz(155);
Block* Block::quartzstairs = new QuartzStairs(156);
Block* Block::activatorrail = new ActivatorRail(157);
Block* Block::dropper = new Dropper(158);
Block* Block::stainedclay = new StainedClay(159);
