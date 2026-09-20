"""Regenerate Patches/Patch_CreatureSettings.xml - the consolidated settings sheet.

This is the canonical source for every creature's:
  - wild spawn commonality per biome
  - base meat/leather amounts
  - base wool amount (wool-bearing creatures only)
  - adult drawSize (visual size only, no gameplay effect)

DO NOT hand-edit Patches/Patch_CreatureSettings.xml directly - it is fully
generated output. Edit the CREATURES table below, then run:

    python3 Scripts/gen_settings_patch.py

from the JP_Beasts repo root (or anywhere - the script locates the repo via
its own file path). Then run Scripts/validate.py before committing.

Whatever is NOT in this file (aggression/predator/manhunter stats, meat
item identity, gestationPeriodDays, egg-laying config, textures, sounds,
labels) lives directly in Defs/ThingDefs_Races/*.xml and is NOT touched by
this script.
"""
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

# (defName, jp_label, [(biome, commonality), ...], meat_amount, leather_amount, wool_amount_or_None, adult_draw_size)
#
# Rarity rebalance note: commonality is set on a 5-tier scale between two
# user-specified endpoints (common ~2-3, legendary ~0.1-0.5), matching each
# creature's own in-mod flavor text (many yokai/beast descriptions
# explicitly say "ごく稀に目撃される" / "滅多に人前に姿を現さない" /
# "極めて稀" etc):
#   Common    (small/swarm insects):        ~2.0-3.0
#   Uncommon  (wolves, mid-size insects):    ~1.1-2.0
#   Rare      (megafauna, most yokai):       ~0.45-1.45
#   Very rare (Tengu, Oni):                  ~0.3-0.5
#   Legendary (AdamantiteBeast, Dragonkin):  ~0.2
#
# History: these commonality numbers went through several revisions -
# see HANDOFF.md for the full story of why they are NOT close to their
# original design values. Short version: an earlier debugging session
# (chasing a "zero spawns ever" bug that turned out to be an unrelated XML
# bug, not a commonality problem) inflated these ~10x, and it took two
# follow-up rebalance passes plus a set of grounded reference points from
# the user (common~2-3, legendary~0.1-0.5) to land here.
#
# MeatAmount/LeatherAmount: all 23 raised +20% from the values that shipped
# when Scripts/ was first added to the repo, per user request (perceived
# drop in yield - the repo's git history only has one squashed snapshot of
# these values, so an actual prior regression could not be confirmed, but
# this is exactly what this sheet exists to retune). See HANDOFF.md.
CREATURES = [
    # ---- Ancient type (beasts) ----
    ("JP_JapaneseWolf", "ニホンオオカミ",
     [("TemperateForest", 1.45), ("BorealForest", 2.0), ("Tundra", 1.15)],
     256, 90, 44, 2.88),
    ("JP_EzoWolf", "エゾオオカミ",
     [("BorealForest", 1.75), ("Tundra", 1.45)],
     270, 96, 57, 3.15),
    ("JP_Mammoth", "マンモス",
     [("Tundra", 0.9), ("BorealForest", 0.7), ("ExtremeDesert", 0.55)],
     330, 120, 163, 5.78),
    ("JP_Mazotairos", "マゾタイロス",
     [("AridShrubland", 0.8), ("Desert", 0.65), ("TropicalRainforest", 0.65)],
     316, 114, 88, 4.2),
    ("JP_AdamantiteBeast", "アダマンタイト",
     [("ExtremeDesert", 0.2), ("Tundra", 0.2)],
     300, 136, 20, 5.1),
    ("JP_WoollyRhino", "ケナガサイ",
     [("Tundra", 1.1), ("BorealForest", 0.7)],
     286, 114, 138, 3.6),
    ("JP_IrishElk", "オオツノジカ",
     [("TemperateForest", 1.45), ("BorealForest", 1.15), ("Tundra", 0.7)],
     226, 78, 66, 2.55),
    ("JP_Smilodon", "サーベルタイガー",
     [("AridShrubland", 0.8), ("TemperateForest", 0.7), ("Desert", 0.7)],
     210, 72, 53, 2.4),
    # ---- Ancient type (insects) ----
    ("JP_Meganeura", "メガネウラ",
     [("TropicalSwamp", 2.76), ("TemperateSwamp", 2.3), ("TropicalRainforest", 1.84)],
     136, 46, None, 1.05),
    ("JP_Titanoptera", "ティタノプテラ",
     [("TropicalRainforest", 1.6), ("TropicalSwamp", 1.6), ("AridShrubland", 1.1)],
     196, 66, None, 2.25),
    ("JP_Arthropleura", "アースロプレウラ",
     [("TropicalRainforest", 1.6), ("TemperateForest", 1.4), ("TemperateSwamp", 1.4)],
     196, 76, None, 2.85),
    ("JP_Pulmonoscorpius", "プルモノスコルピウス",
     [("AridShrubland", 1.4), ("Desert", 1.6), ("ExtremeDesert", 1.1)],
     180, 66, None, 2.55),
    ("JP_Megarachne", "メガラクネ",
     [("TropicalRainforest", 1.6), ("TemperateForest", 1.3)],
     166, 54, None, 1.95),
    ("JP_Titanomyrma", "タイタノミルマ",
     [("TropicalRainforest", 2.76), ("TropicalSwamp", 2.42), ("AridShrubland", 1.73)],
     106, 36, None, 1.35),
    ("JP_Archimylacris", "アーキミラクリス",
     [("TemperateForest", 2.99), ("TemperateSwamp", 2.76), ("TropicalRainforest", 2.99), ("TropicalSwamp", 2.76)],
     60, 24, None, 0.9),
    # ---- Yokai type ----
    ("JP_Nekomata", "猫又",
     [("TemperateForest", 0.8), ("TemperateSwamp", 0.8), ("TropicalRainforest", 0.7)],
     240, 84, 50, 1.3),
    ("JP_Youko", "妖狐",
     [("TemperateForest", 0.7), ("AridShrubland", 0.8), ("Desert", 0.7)],
     234, 82, 44, 1.3),
    ("JP_Yukionna", "雪女",
     [("Tundra", 0.8), ("BorealForest", 0.65)],
     240, 84, 44, 1.3),
    ("JP_Zashikiwarashi", "座敷童",
     [("TemperateForest", 0.65), ("BorealForest", 0.45)],
     180, 60, 30, 0.9),
    ("JP_Tengu", "天狗",
     [("BorealForest", 0.45), ("TemperateForest", 0.45), ("Tundra", 0.3)],
     256, 90, 50, 1.5),
    ("JP_Oni", "鬼人",
     [("AridShrubland", 0.4), ("ExtremeDesert", 0.5), ("Tundra", 0.4)],
     286, 106, 60, 2),
    ("JP_Dragonkin", "竜人",
     [("TropicalRainforest", 0.2), ("ExtremeDesert", 0.2), ("Tundra", 0.2), ("BorealForest", 0.2)],
     300, 120, 56, 1.9),
    ("JP_Jorogumo", "女郎蜘蛛",
     [("TemperateForest", 0.7), ("TropicalRainforest", 0.7), ("TemperateSwamp", 0.55)],
     166, 72, 48, 1.3),
]

def fmt(v):
    s = f"{v:.3f}".rstrip('0').rstrip('.')
    return s

lines = []
lines.append('<?xml version="1.0" encoding="utf-8"?>')
lines.append('<Patch>')
lines.append('')
lines.append('  <!-- ============================================================')
lines.append('       JP_Beasts 設定シート (Creature Settings Sheet)')
lines.append('       ============================================================')
lines.append('       このファイル1つで、モンスターごとの下記パラメータを編集できます:')
lines.append('         1) 出現頻度 commonality タグの数値 - バイオームごとの野生出現の重み')
lines.append('         2) 基本肉量 MeatAmount タグの数値  - 屠殺で得られる肉の基礎量')
lines.append('         3) 基本革量 LeatherAmount タグの数値 - 屠殺で得られる革の基礎量')
lines.append('         4) 基本毛量 woolAmount タグの数値  - テイム後の毛刈りで得られる毛の量')
lines.append('         5) 見た目の大きさ drawSize タグの数値 - 成体になったときの描画サイズ')
lines.append('')
lines.append('       【出現を完全にOFFにしたい場合】')
lines.append('       対象モンスターの「出現頻度」ブロック全体(見出しコメントから')
lines.append('       次の見出しコメントの手前まで)を削除するか、XMLコメントで囲んで')
lines.append('       ください。それだけでそのモンスターは一切自然出現しなくなります')
lines.append('       (テイムして繁殖させることは引き続き可能です)。')
lines.append('')
lines.append('       【数値だけ変えたい場合】')
lines.append('       各タグの数値部分だけを書き換えて保存すれば、次回ゲーム起動時から')
lines.append('       反映されます。commonality/MeatAmount/LeatherAmount/woolAmountは')
lines.append('       他MODとの相対的な重みなので上限はありません。自由に増減してください。')
lines.append('')
lines.append('       【肉/革の仕組みについて】')
lines.append('       MeatAmount/LeatherAmount は「体格1.0あたりの基礎量」で、実際の量は')
lines.append('       個体の体格(baseBodySize)を掛けた値になります(体格はDefs/ThingDefs_Races/')
lines.append('       内で定義・バニラのAnimalThingBaseの既定値は肉90・革30相当)。')
lines.append('')
lines.append('       【見た目の大きさについて】')
lines.append('       drawSize は成体(3段階のライフステージのうち最後の段階)の描画倍率です。')
lines.append('       1.0がおおよそ人間1体分の大きさに相当します。幼体・若齢個体の大きさは')
lines.append('       PawnKindDefs側に元々定義された比率のまま変わりません。個体の当たり判定')
lines.append('       や戦闘力には影響しない、純粋な見た目のみの調整項目です。')
lines.append('       ============================================================ -->')
lines.append('')

for defname, jp, biomes, meat, leather, wool, draw_size in CREATURES:
    lines.append(f'  <!-- ==================== {jp} ({defname}) - 出現頻度 ==================== -->')
    for biome, comm in biomes:
        lines.append('  <Operation Class="PatchOperationConditional">')
        lines.append(f'    <xpath>Defs/BiomeDef[defName="{biome}"]/wildAnimals</xpath>')
        lines.append('    <match Class="PatchOperationAdd">')
        lines.append(f'      <xpath>Defs/BiomeDef[defName="{biome}"]/wildAnimals</xpath>')
        lines.append(f'      <value><{defname}>{fmt(comm)}</{defname}></value>')
        lines.append('    </match>')
        lines.append('  </Operation>')
    lines.append('')
    lines.append(f'  <!-- 基本肉量・革量: {jp} -->')
    lines.append('  <Operation Class="PatchOperationConditional">')
    lines.append(f'    <xpath>Defs/ThingDef[defName="{defname}"]/statBases</xpath>')
    lines.append('    <match Class="PatchOperationAdd">')
    lines.append(f'      <xpath>Defs/ThingDef[defName="{defname}"]/statBases</xpath>')
    lines.append(f'      <value>')
    lines.append(f'        <MeatAmount>{meat}</MeatAmount>')
    lines.append(f'        <LeatherAmount>{leather}</LeatherAmount>')
    lines.append(f'      </value>')
    lines.append('    </match>')
    lines.append('  </Operation>')
    if wool is not None:
        lines.append('')
        lines.append(f'  <!-- 基本毛量(テイム後の毛刈り): {jp} -->')
        lines.append('  <Operation Class="PatchOperationConditional">')
        lines.append(f'    <xpath>Defs/ThingDef[defName="{defname}"]/comps/li[@Class="CompProperties_Shearable"]/woolAmount</xpath>')
        lines.append('    <match Class="PatchOperationReplace">')
        lines.append(f'      <xpath>Defs/ThingDef[defName="{defname}"]/comps/li[@Class="CompProperties_Shearable"]/woolAmount</xpath>')
        lines.append(f'      <value><woolAmount>{wool}</woolAmount></value>')
        lines.append('    </match>')
        lines.append('  </Operation>')
    lines.append('')
    lines.append(f'  <!-- 見た目の大きさ(成体): {jp} -->')
    lines.append('  <Operation Class="PatchOperationConditional">')
    lines.append(f'    <xpath>Defs/PawnKindDef[defName="{defname}"]/lifeStages/li[3]/bodyGraphicData/drawSize</xpath>')
    lines.append('    <match Class="PatchOperationReplace">')
    lines.append(f'      <xpath>Defs/PawnKindDef[defName="{defname}"]/lifeStages/li[3]/bodyGraphicData/drawSize</xpath>')
    lines.append(f'      <value><drawSize>{fmt(draw_size)}</drawSize></value>')
    lines.append('    </match>')
    lines.append('  </Operation>')
    lines.append('')

lines.append('</Patch>')

content = '\n'.join(lines) + '\n'
path = BASE_DIR / "Patches" / "Patch_CreatureSettings.xml"
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("wrote", path, len(content), "bytes", len(CREATURES), "creatures")
