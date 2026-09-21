"""Sanity-check the mod's XML before every commit.

Run from anywhere: `python3 Scripts/validate.py` from the JP_Beasts repo
root, or `python3 /path/to/JP_Beasts/Scripts/validate.py` from elsewhere.

Checks:
  1. Every XML file parses (well-formed).
  2. Every JP_-prefixed specificMeatDef/leatherDef/woolDef/hatcherPawn/race
     reference resolves to a defName that actually exists somewhere in the
     mod.
  3. Every <texPath> resolves to a real file under Textures/.
  4. No leftover references to old, now-deleted meat defs (the original
     per-species insect meats, and JP_Meat_Insect itself after 3.19 moved
     all insect-flavored creatures onto vanilla's shared insect meat via
     useMeatFrom).
  5. Shearable comp count vs. settings-sheet wool-patch count (a rough
     parity check, not authoritative).
  6. No <meatDef> tag anywhere in Defs/ThingDefs_Races - see HANDOFF.md 3.19.
     RaceProperties.meatDef is a runtime-computed [Unsaved] field that
     RimWorld's implied-def generator (ThingDefGenerator_Meat) silently
     overwrites regardless of what XML sets it to; the real, XML-authorable
     fields are <specificMeatDef> (point at one explicit existing item) and
     <useMeatFrom> (share generation with another race, e.g. vanilla
     Megaspider). <meatDef> never errors when used - it's a real field on
     the class - so this class of mistake produces no warning anywhere
     except a player noticing the wrong item in-game. If this check ever
     fires again, do not silently rename it back - re-read HANDOFF.md 3.19
     first.
"""
import xml.etree.ElementTree as ET
import glob, os, re, pathlib

BASE = str(pathlib.Path(__file__).resolve().parent.parent)

# 1. XML well-formedness
xml_files = glob.glob(f"{BASE}/**/*.xml", recursive=True)
errors = []
for f in xml_files:
    try:
        ET.parse(f)
    except Exception as e:
        errors.append(f"{f}: {e}")
print(f"Checked {len(xml_files)} XML files.")
if errors:
    print("XML ERRORS:")
    for e in errors:
        print(" ", e)
else:
    print("All XML well-formed.")

# 2. Collect all defNames defined
defnames = set()
for f in xml_files:
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r"<defName>([^<]+)</defName>", txt):
        defnames.add(m.group(1))

# 3. Collect referenced defNames we expect to exist among our own JP_ set
# (specificMeatDef/leatherDef/woolDef/hatcherPawn/race referencing our own
# JP_ prefixed defs - useMeatFrom targets like vanilla "Megaspider" are
# intentionally not JP_-prefixed and can't be checked without vanilla Core,
# so they're outside what this check can verify)
ref_tags = ["specificMeatDef", "leatherDef", "woolDef", "hatcherPawn", "race"]
missing = []
for f in xml_files:
    txt = open(f, encoding="utf-8").read()
    for tag in ref_tags:
        for m in re.finditer(fr"<{tag}>([^<]+)</{tag}>", txt):
            val = m.group(1)
            if val.startswith("JP_") and val not in defnames:
                missing.append(f"{f}: <{tag}>{val}</{tag}> not found as a defName anywhere")

if missing:
    print("MISSING REFERENCES:")
    for m in missing:
        print(" ", m)
else:
    print("All JP_-prefixed specificMeatDef/leatherDef/woolDef/hatcherPawn/race references resolve.")

# 3b. <meatDef> must never appear in Defs/ThingDefs_Races - see docstring
# item 6 and HANDOFF.md 3.19.
meatdef_races = glob.glob(f"{BASE}/Defs/ThingDefs_Races/*.xml")
stray_meatdef = []
for f in meatdef_races:
    txt = open(f, encoding="utf-8").read()
    if "<meatDef>" in txt:
        stray_meatdef.append(f)
if stray_meatdef:
    print("STRAY <meatDef> TAGS (use <specificMeatDef> or <useMeatFrom> instead - see HANDOFF.md 3.19):")
    for f in stray_meatdef:
        print(" ", f)
else:
    print("No stray <meatDef> tags in Defs/ThingDefs_Races (correctly using specificMeatDef/useMeatFrom).")

# 4. texPath -> file existence check
texpaths = set()
for f in xml_files:
    txt = open(f, encoding="utf-8").read()
    for m in re.finditer(r"<texPath>([^<]+)</texPath>", txt):
        texpaths.add(m.group(1))

missing_tex = []
for tp in sorted(texpaths):
    base = f"{BASE}/Textures/{tp}"
    candidates = [base + ".png", base + "_south.png"]
    if not any(os.path.exists(c) for c in candidates):
        missing_tex.append(tp)

print(f"Checked {len(texpaths)} unique texPaths.")
if missing_tex:
    print("MISSING TEXTURES:")
    for t in missing_tex:
        print(" ", t)
else:
    print("All texPaths resolve to an existing file.")

# 5. check no leftover references to deleted JP_Meat_* insect defs
deleted_meats = ["JP_Meat_Meganeura", "JP_Meat_Titanoptera", "JP_Meat_Arthropleura",
                  "JP_Meat_Pulmonoscorpius", "JP_Meat_Megarachne", "JP_Meat_Titanomyrma",
                  "JP_Meat_Archimylacris", "JP_Meat_Insect"]
leftover = []
for f in xml_files:
    txt = open(f, encoding="utf-8").read()
    for dm in deleted_meats:
        if dm in txt:
            leftover.append(f"{f}: still references {dm}")
if leftover:
    print("LEFTOVER REFERENCES TO DELETED MEAT DEFS:")
    for l in leftover:
        print(" ", l)
else:
    print("No leftover references to deleted per-species insect meat defs.")

# 6. Shearable comp count vs settings-sheet wool patch count.
# Match only the per-creature comment ("基本毛量(...)"), not the sheet's
# own header line, which documents the woolAmount tag using the same
# substring ("基本毛量 woolAmount タグの数値") without the parenthesis.
# That header match was previously counted here too, producing a
# permanent 16-vs-17 off-by-one that was never an actual bug in the mod.
shear_count = 0
for f in xml_files:
    if "Patch_CreatureSettings" in f:
        continue
    txt = open(f, encoding="utf-8").read()
    shear_count += txt.count('Class="CompProperties_Shearable"')
patch_txt = open(f"{BASE}/Patches/Patch_CreatureSettings.xml", encoding="utf-8").read()
wool_patch_count = patch_txt.count("基本毛量(")
print(f"Shearable comps in race files: {shear_count}, wool patches in settings sheet: {wool_patch_count}")
if shear_count != wool_patch_count:
    print(f"  MISMATCH: investigate before committing (see gen_settings_patch.py CREATURES table).")
