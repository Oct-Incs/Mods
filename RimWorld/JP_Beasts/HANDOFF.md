# JP_Beasts - 開発引き継ぎドキュメント (HANDOFF)

このファイルは、次の担当(後継のClaudeセッション)がクリーンな状態からでもこの続きを
スムーズに開発できるようにするための引き継ぎ資料です。**あなたはこのMOD開発における
私(前任)と同じ役割を担います** — つまり、ユーザーの日本語での要望・バグ報告を正確に
理解し、憶測で修正せず実際に原因を調査してから直し、変更のたびに検証・コミット・
プッシュ・変更点のみの配布まで一貫して行う担当者です。

このドキュメントは長いですが、読み飛ばさず全体に目を通してください。特に
「確立した開発方針」と「これまでに解決した不具合」は、同じ調査を繰り返さないために
必須です。

## 1. このMODについて

**JP_Beasts (和ノ獣譚)** は RimWorld 1.6 向けの XML のみで構成されたコンテンツMODで、
自然出現する野生/敵対クリーチャーを23体追加します:

- **妖怪型 (8体)**: Nekomata(猫又) / Youko(妖狐) / Yukionna(雪女) /
  Zashikiwarashi(座敷童) / Tengu(天狗) / Oni(鬼人) / Dragonkin(竜人) /
  Jorogumo(女郎蜘蛛) — いずれも `body=Human` + `intelligence=Animal` の
  人型ボディを持つ動物として実装
- **古代獣型 (8体)**: JapaneseWolf(ニホンオオカミ) / EzoWolf(エゾオオカミ) /
  Mammoth(マンモス) / Mazotairos(マゾタイロス) / AdamantiteBeast(アダマンタイト) /
  WoollyRhino(ケナガサイ) / IrishElk(オオツノジカ) / Smilodon(サーベルタイガー)
- **古代昆虫型 (7体)**: Meganeura(メガネウラ) / Titanoptera(ティタノプテラ) /
  Arthropleura(アースロプレウラ) / Pulmonoscorpius(プルモノスコルピウス) /
  Megarachne(メガラクネ) / Titanomyrma(タイタノミルマ) / Archimylacris(アーキミラクリス)

リポジトリ: **`Oct-Incs/Mods`**(GitHubの表示名。旧名 `Oct-Incs/i` からリネーム
済みで、旧URLへのアクセスは自動的にリダイレクトされる — ただし git remote の
URLはリネーム後の名称に変更すると push が403で失敗することを確認済みなので、
`origin` のURL文字列自体は古い名称のままにしておくこと。詳細はリポジトリ
ルートの `README.md` を参照)。このMODはリポジトリの直下ではなく
**`RimWorld/JP_Beasts/`** 配下にある(このリポジトリは複数ゲームのMODを
格納する前提の構成になった。ルートの `README.md` に構成ルールがある)。
開発は `main` ブランチが常に最新。以前は
`claude/rimworld-mod-characters-enemies-q47qgd` というフィーチャーブランチで
長期間作業しており、それが `main` に一度もマージされていなかったために
別セッションがこのMODの存在に気づけない事故が起きた。今後は作業が一段落する
たびに `main` へマージすること。

ユーザーは日本語話者で、RimWorldにかなり詳しく、こちらの推測や説明の甘さを鋭く
指摘してきます。生半可な回答は許されないと思って調査してください。

## 2. 確立した開発方針 (最重要)

このMODの開発を通じて、何度も痛い目を見て確立した鉄則です。**必ず守ってください**。

### 2.1 絶対に憶測でXMLを直さない。必ず実際のソース/データで裏取りする

このセッションで繰り返し起きたパターン: 「たぶんこのフィールドが原因だろう」と
憶測で直す → ユーザーが実際にテストして「直ってません」「本当にそれが原因ですか?
調査が必要じゃないですか?」と鋭く指摘される → 実際に調べたら全く別の原因だった。

対処法:
- RimWorld 1.6のC#ソースはクローズドソースだが、デコンパイル済みリポジトリが
  GitHub上に複数存在する。`add_repo` ツールで一時的にクローンして直接読むこと。
  - `josh-m/RW-Decompile` — このセッションで実際に使用。ただし**古いバージョン
    (1.0〜1.1相当)**なので、Biotech以降に追加/変更された機能(妊娠システム等)は
    載っていない点に注意。それでも `Pawn_MindState.cs`・`FoodUtility.cs`・
    `RaceProperties.cs` 等の基本的なAI/繁殖ロジックの構造は現行版でも大枠は
    変わっていないことが多く、非常に有用だった。
  - クローン例: `add_repo(owner="josh-m", repo="RW-Decompile", access="read")` の
    案内に従い `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 ...` を実行。
- XML定義そのもの(バニラCoreのDefs)は公式リポジトリが存在しないため、実際の
  vanillaの挙動やフィールド名は「信頼できる翻訳リポジトリ」経由で裏取りするのが
  最も確実だった: `Ludeon/RimWorld-Finnish` などの公式言語リポジトリの
  `DefInjected/` 以下には、バニラの実際のXMLに存在するフィールド名が
  `<DefName.fieldpath>` という形でそのまま現れる。例:
  `Megaspider.race.meatLabel` というキーの存在自体が「Megaspiderのrace blockに
  meatLabelフィールドが実在する」ことの動かぬ証拠になる。
- 参照実績のあるMOD (`Alpha Animals`) がスクラッチパッドにクローン済み:
  `/tmp/claude-0/.../scratchpad/AlphaAnimals/1.6/` (パスはセッションごとに変わる
  可能性があるので、無ければ `add_repo` で再取得するか、Steam Workshop ID
  `1541721856` から探す)。「このMODで動いている実例と1フィールドずつ突き合わせる」
  手法で `gestationPeriodDays` の欠落や `meatDef` vs `meatLabel` の違いなど、
  複数の重大なバグを特定できた。**新しいXMLフィールドを使う前に、まずAlpha
  Animalsの該当箇所を`grep`で確認する癖をつけること。**
- `rimworldwiki.com` / `rimworld.fandom.com` / `rimworldhub.com` / `ludeon.com` は
  このセッションのネットワークプロキシで**アクセスブロックされている**
  (`EGRESS_BLOCKED`)。WebFetchで直接開こうとしても失敗するので、WebSearchの
  スニペット経由、または上記のGitHub系リポジトリ経由で情報を得ること。

### 2.2 検証 → コミット → プッシュ → 配布、の型を毎回崩さない

1. XML編集後は必ず `python3 Scripts/validate.py` を実行する
   (旧パスは `/tmp/.../scratchpad/validate.py` だったが、今回**リポジトリ内の
   `Scripts/validate.py` に正式に移設した**。今後はこちらを使うこと)。
2. `git add` で変更ファイルのみをステージし、詳細な理由(何が起きていたか・
   根本原因・裏取りに使った証拠)を書いたコミットメッセージを作成する。
   フッターは毎回:
   ```
   Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_01Hxjmer8pd3V7oq4ENEZsyu
   ```
   (このセッションIDは前任のものなので、新しいセッションでは自分の
   Claude-Session URLに置き換えること。システムリマインダーで都度指示される。)
3. `git push -u origin claude/rimworld-mod-characters-enemies-q47qgd`
4. ユーザーへのファイル配布は **`SendUserFile`** で行う。
   - **原則、変更があったファイルのみを個別に送る**。ユーザーは自分でテクスチャを
     差し替え済みの場合があるため、MOD全体のZIPを送ると上書きしてしまう恐れが
     ある、という理由で個別配布が既定の方針だった。
   - ただし、ユーザーが明示的に「ZIPでまとめて出力して」と頼んだ場合は、
     `zip -r -q <出力先> JP_Beasts -x "*.git*"` で作成して送ってよい
     (このセッション後半では変更が多岐にわたったため、毎回ZIP送付に切り替えた)。
     どちらのスタイルを使うかは直近のユーザーの指示に従うこと。

### 2.3 設定シート (`Patches/Patch_CreatureSettings.xml`) は手で編集しない

出現頻度・基本肉量・基本革量・基本毛量・drawSize (見た目サイズ) は
`Scripts/gen_settings_patch.py` の `CREATURES` テーブルで一元管理している。
**このファイルを直接手編集すると、次にスクリプトを再実行したときに上書きされて
消える。** 変更する際は必ずスクリプトのテーブルを編集 →
`python3 Scripts/gen_settings_patch.py` を実行 → 生成結果を確認、の順で行うこと。

それ以外のパラメータ(攻撃性・捕食者フラグ・肉アイテムの種類・妊娠日数・産卵設定・
テクスチャ・サウンド・ラベル等)は `Defs/ThingDefs_Races/*.xml` に直接書かれており、
設定シートの対象外。

### 2.4 XML一括編集にはPythonスクリプトを使う

23体に同じ種類の変更を加える場合(例: 全個体に `gestationPeriodDays` を追加、
特定グループだけ `predator` を書き換える等)、`Edit` ツールで1体ずつ処理すると
`old_string` の重複(同じ値が複数箇所にある)で失敗しやすい。このセッションでは
`defName` でThingDefブロックを正規表現分割し、対象defNameのブロックだけ
置換・挿入する使い捨てPythonスクリプトを都度
`/tmp/.../scratchpad/fix_*.py` に書いて実行する手法を多用した。今後も
同様のパターンを推奨する(スクリプト自体は使い捨てでよく、リポジトリに残す
必要はない)。

### 2.5 Textures/ 配下の画像ファイルには絶対に触れない(2026-09-21〜、恒久ルール)

**ユーザーが今回の会話の中で明示的に「この画像を差し替えて」「このテクスチャを
変更して」と指示しない限り、`Textures/` 配下のいかなる画像ファイル(PNG)も
作成・変更・削除・上書き・リサイズ・再生成してはならない。** 新しいセッションが
始まっても引き継がれる恒久的なルール。詳細と経緯は同フォルダの `CLAUDE.md` を
参照(セッション開始時に自動で読み込まれる)。

- 触ってよいのは画像の“表示サイズ”を制御するXML側の数値(`drawSize`等)のみ。
  画像ファイル自体のバイト列・ピクセル内容には触れないこと。
- ユーザーはこのMODの画像を自分で描き直し、GitHubの`main`ブランチに直接
  アップロードする運用を自分で確立させた(この方法にたどり着くまで、
  「GitHub Web UIにUpload filesが無い」という誤った決めつけをしてユーザーを
  怒らせた経緯がある。§8参照)。
- 作業前に必ず `git fetch`/`git pull` して、ユーザーが直接pushした最新の
  テクスチャを取り込むこと。取り込まずに作業を続けると、次に出力するZIPが
  古い画像のままになり、ユーザーの差し替え作業を無に帰してしまう(実際に
  このセッションで、ブランチが分岐したまま気づかず作業を続けていたら
  発生していたところだった)。

## 3. これまでに発生した不具合と解決策 (時系列)

このセクションが最も重要です。**同じ調査を繰り返さないために、必ず目を通してください。**

### 3.1 Config エラー: 重複thingCategory・間違ったbody-part group名
`AnimalThingBase` が既に `<thingCategories><li>Animals</li></thingCategories>` を
継承提供しているのに、子ThingDef側でも再宣言していて重複エラー。また
`QuadrupedAnimalWithPawsAndTail` ボディの前脚パーツグループ名は
`FrontLeftLeg`/`FrontRightLeg` ではなく `FrontLeftPaw`/`FrontRightPaw` が正しい
(Alpha Animalsの `Races_ArcticLion.xml` と突き合わせて確認)。→ 両方削除・修正済み。

### 3.2 昆虫8体がテイム不可だった
`fleshType: Insectoid` (バニラ組み込みのenum値) を設定すると、C#側で
未特定の副作用(おそらく蜂の巣/昆虫特有のAI・テイム制限)が発生することが判明。
`meatLabel`/`meatColor` で見た目の「虫肉」フレーバーは保ったまま
`fleshType` そのものを削除して解決(→後で3.8で meatLabel 自体が別の不具合の
原因と判明し、`meatDef` 方式に置き換えることになる)。

### 3.3 妖怪全体が突然テイム不可になった (重大な回帰)
`intelligence: Animal` を明示追加する、という最初の仮説はユーザーに
「だめですね。変わりません。」と一蹴された。実際にデコンパイル済みソース
(`RimWorld/TameUtility.cs`)を読んだところ:
```csharp
public static bool CanTame(Pawn pawn)
{
    if (pawn.AnimalOrWildMan() && ... && pawn.GetStatValue(StatDefOf.Wildness) < 1f && ...)
        return !pawn.health.hediffSet.HasHediff(HediffDefOf.Scaria);
    return false;
}
```
**`Wildness` が厳密に `1.0` 未満でなければならない**。全妖怪+AdamantiteBeastが
ちょうど `1.0` になっていたことが根本原因だった。`0.985` 等に変更して解決。
その後ユーザーの要望で、妖怪+AdamantiteBeast=0.985(バニラThrumbo相当=最高)、
マンモス+昆虫=0.96、他の古代哺乳類=0.93、と3段階に再設計した。

### 3.4 「10時間プレイしても一切自然スポーンしない」+ 時々クラッシュ (重大)
このセッション最大のデバッグ案件。段階を追うと:
1. 最初は出現頻度(commonality)の数値そのものが低すぎるのではと考え、
   4倍→さらに3倍(実質12倍)に引き上げたが直らなかった。
2. drawSize(見た目サイズ)が大きすぎてキャラクターエディタの描画処理が
   クラッシュしているのではという仮説でMammoth/AdamantiteBeastのdrawSizeを
   下げたが、ユーザーに「小型の妖怪まで一切スポーンしない理由になっていない」と
   的確に指摘された。
3. 実際のPlayer.logを提供してもらい確認したところ、`Biomes_Cold.xml` 等の
   ロード中に `ArgumentNullException` が発生し、本来ロードされるべき
   vanilla BiomeDefが破損して13個しかロードされておらず、Tundra/Desert等への
   何百件もの参照解決エラーが連鎖していることが判明。
4. 根本原因は**2段階の誤り**だった:
   - まず、使っていたXPathが `Defs/BiomeDef[...]/animalCommonalities` だったが、
     **RimWorld 1.6のBiomeDefにそのようなフィールドは存在しない**。実際の
     フィールド名は `wildAnimals` (`RimWorld/BiomeDef.cs` の
     `private List<BiomeAnimalRecord> wildAnimals` を確認)。
   - フィールド名を直しても、今度は要素の書き方が間違っていた。
     `<li><animal>X</animal><commonality>Y</commonality></li>` という
     直感的な形式を使っていたが、`BiomeAnimalRecord.LoadDataFromXmlCustom` と
     `DirectXmlCrossRefLoader.RegisterObjectWantsCrossRef` の実装を読むと、
     **正しい形式は `<{defName}>{数値}</{defName}>`** (タグ名自体が
     クロスリファレンス先のdefName、テキスト内容が数値) だと判明。
     この誤ったXML構造が実際に稼働中のvanilla BiomeDefを壊しており、
     おそらくこれがクラッシュの真の原因だった(drawSizeの仮説ではなかった)。
   - 修正後、ユーザーが「完全に直りました」と確認。

**この一件の教訓**: XMLが「一見正しそう」でも動かない場合、必ずC#側の実装
(特にカスタムXMLローダーを持つクラスの `LoadDataFromXmlCustom` や
`DirectXmlCrossRefLoader` の呼び出しパターン)を確認すること。

### 3.5 3段階の攻撃性システム設計 (テイム失敗時反撃・被弾時反撃)
ユーザー要望: 草食性の古代哺乳類+一部妖怪=アイベックス相当(反撃0%)、
他の妖怪+小型昆虫+オオカミ系=バニラ肉食獣相当、アダマンタイト+大型昆虫=
バニラ野生昆虫相当。`predator`/`maxPreyBodySize`/`manhunterOnDamageChance`/
`manhunterOnTameFailChance` を調整。詳細は3.6・3.7で述べる通り、この初回の
調整だけでは不十分で、複数回の追加修正が必要だった。

### 3.6 「オオカミ・女郎蜘蛛が入植者を勝手に襲ってくる」(最重大バグの一つ)
最初は「populationが多すぎるせいで遭遇頻度が上がっているだけ」と誤った説明を
してしまい、ユーザーに「本当にそれが原因ですか?調査が必要じゃないですか?」と
指摘された。実際にデコンパイル済みソースを読み直すと:
- `RimWorld/JobDriver_PredatorHunt.cs` の `CheckWarnPlayer()` が、まさに
  ユーザーが見た「◯◯は入植者〜を獲物として襲っている」という
  `"LetterPredatorHuntingColonist"` メッセージそのものだと判明。つまり
  マンハンター化ではなく、**正規の「捕食者が獲物を狩る」AIそのもの**が
  入植者を対象にしていた。
- 原因は `RimWorld/DifficultyDef.cs` の `public bool predatorsHuntHumanlikes = true;`
  — **バニラのデフォルトでtrue**。`FoodUtility.IsAcceptablePreyFor()` は
  `prey.BodySize > predator.RaceProps.maxPreyBodySize` の場合のみ人間を除外する。
  成人入植者(体格1.0)は`maxPreyBodySize`(0.45〜0.8程度に設定していた)を
  上回るので通常は除外されるはずだが、**Biotech DLCの幼児/子供コロニストは
  体格が0.2〜0.7程度まで下がる**ため、それらの値でも「妥当な獲物」と
  判定されてしまっていた。
- 子供の正確な体格やXenotypeによる変動を完全に把握しきれないため、
  数値の微調整では確実な安全と言えないと判断し、**全23体の`predator: true`を
  falseに統一**して捕食AIの発動経路そのものを排除した(`maxPreyBodySize`も
  合わせて削除)。既に一部の草食系個体で`predator: false`が機能実績済みだった
  ことも判断材料にした。

**この一件の教訓**: 「マンハンター化」と「捕食者が獲物として狙う」は
全く別のC#メカニズムで、どちらも「入植者を攻撃する」という見た目の結果は
同じだが、原因も手紙(通知)の有無も全く異なる。ユーザーの報告に具体的な
メッセージ文言が含まれている場合は、それをそのままソース内でgrepして
特定すること。

### 3.7 manhunterOnTameFailChance の見落とし
3.5で `manhunterOnDamageChance`(被弾時反撃)だけ調整し、
`manhunterOnTameFailChance`(テイム失敗時に襲われる確率)を未調整のまま
放置していた。ユーザーに「テイムを試みただけで30%の確率で襲ってくる」と
指摘されて気づいた。同じ3段階(0% / 12% / 28%)で再調整。

### 3.8 出現頻度(commonality)の調整履歴が複雑
3.4のデバッグ中に誤って4倍→3倍(実質12倍)に積み増した値がバグ修正後も
そのまま残っており、狼系・猫又が過剰にスポーンする一方でマンモス等の
レア設定個体がほぼ出現しない状態になっていた。2回に分けて全面的に
作り直した:
1. 1回目: 各モンスターの説明文中のレア度表現(「ごく稀に目撃される」等)に
   基づき5段階(普通2.0-2.6 / やや珍しい0.75-1.6 / レア0.3-0.65 /
   かなりレア0.12-0.2 / 伝説級0.03)で再設計。
2. ユーザーから「普通:約2〜3、伝説級:約0.1〜0.5」という具体的な範囲指定を
   もらい、幅を圧縮して再設計(現在の値)。

**現在の設定は `Scripts/gen_settings_patch.py` の `CREATURES` テーブルに
反映済み。今後さらに調整する場合はこのファイルを編集すること。**

### 3.9 昆虫の肉が「メガスパイダー等バニラの虫肉のように統一されない」
これも最初は「バニラと同じ`meatLabel`方式だから問題ない」と誤って説明し、
ユーザーに「モンスターごとに別々の『インセクトミート』として認識されている」と
具体的に指摘されて再調査した。判明した内部メカニズム:
- `meatDef` を明示せず `meatLabel`/`meatColor` だけ設定すると、RimWorldは
  `ThingDefGenerator_Meat` 経由で**モンスターごとに別々の暗黙のアイテムを
  自動生成**する。ラベルが同じ「insect meat」でも内部的には別アイテムとして
  扱われ、スタックがマージされない。
- バニラのMegaspider/Megascarab/Spelopedeが全て「虫肉」として統一されるのは、
  3種とも`meatDef`で**同じ1つの実在アイテムを明示的に共有指定**している
  ためだと判明。
- 妖怪7体(Meat_Human使用)がこの不具合に引っかからなかった理由もこれで説明が
  つく: 最初から`meatDef`で実在の共有アイテムを直接指定していたため。
- **修正**: 既存の`JP_Meat_*`アイテム群と同じ`ParentName="OrganicProductBase"`
  方式で、8体(古代昆虫7種+女郎蜘蛛)共有の実在アイテム`JP_Meat_Insect`を
  新規作成し(`Defs/ThingDefs_Items/Meats.xml`)、対象8体を`meatDef`で
  そこに直接紐付けた。`meatLabel`/`meatColor`は削除。

### 3.10 虫肉を食べても忌避ムードが一切発生しない
3.9の修正(スタックのマージ)だけでは不十分だった。RimWorldの
`IngestibleProperties`には`specialThoughtDirect`/`specialThoughtAsIngredient`
という専用フィールドがあり、これが「このアイテムを食べた時に発生させる
ThoughtDef」を直接指定する。バニラの虫肉はここに`AteInsectMeatDirect`/
`AteInsectMeatAsIngredient`(実在のバニラThoughtDef)を設定している。
`JP_Meat_Insect`にこれが欠けていたため追加した。

### 3.11 Ideology DLCの「虫肉を好む信条」に反応しない
3.10で設定した`specialThoughtDirect`は通常の忌避ムードのみを制御しており、
Ideology DLCの食の好み信条(例:「Insect Meat: Loved」で忌避ムードが+6の
好意ムードに反転する)は**別レイヤーの独立した仕組み**で判定されている。
ThingDefのルート階層に以下を追加することで対応:
```xml
<mergeCompatibilityTags MayRequire="Ludeon.RimWorld.Ideology">
  <li MayRequire="Ludeon.RimWorld.Ideology">InsectMeat</li>
</mergeCompatibilityTags>
```
`MayRequire`属性により、Ideology DLCを持たない環境でも安全(この属性は
DLC条件付きフィールドの標準的なXMLパターン)。

**→ 3.15で訂正: 上記のXML配置(ThingDefのルート直下)は実際には間違っていた
(実機のPlayer.logで確認済み)。詳細は3.15を参照。**

### 3.12 妖怪が妊娠しない・古代昆虫が産卵しない
最初は「野生(未テイム)動物はRimWorld仕様上繁殖しない
(`ThinkNode_ConditionalHasFaction`によりブロックされる)」という説明をしたが、
ユーザーが「テイム済みの個体でも孕娠・産卵しない」と確認したため、これは
説明として不十分だった(ただしこの仕様自体は事実であり、他の文脈では
正しい知識として有用)。
実際にAlpha Animalsと全23体のXMLを1フィールドずつ突き合わせたところ、
**`gestationPeriodDays`というフィールドが、このMOD全23体のどれにも
一つも設定されていない**ことが判明。Alpha Animalsでは人型ボディ・四足ボディを
問わずあらゆる個体にこのフィールドが明示的に設定されている。念のため
(卵生個体の繁殖判定にも共通のゲートが影響する可能性を考慮し)卵生の8体にも
防御的に追加した。

### 3.13 繁殖・産卵の「頻度」がバニラと比べて遅すぎた
3.12で追加した`gestationPeriodDays`の値は、「大きい生物ほど妊娠期間が長い」
という現実の生物学的な思い込みで10〜30日という幅で設定してしまっていたが、
ユーザーから「一般的なバニラ生物と同じような一般的な頻度で繁殖するように」と
指摘され、実際のバニラ数値を複数の情報源から調査した。判明した事実:
Cow/Alpaca=6.66日、Goat=5.61日、Husky/Labrador/Yorkie=10日、Warg=10日、
Wild boar=5.661日、バニラGrizzly Bear/Cougar=10日 — **体格に関わらず、
ほとんどのバニラ動物が5.6〜10日という狭い範囲に集中**しており、唯一の例外が
Thrumbo(20日、伝説級)。この実データに基づき、通常個体は6〜12日に圧縮し、
このMOD内で最も伝説級の生体繁殖個体(Mammoth・Dragonkin)のみThrumbo同様
18日に据え置いた。産卵組(古代昆虫7種)の`eggLayIntervalDays`も、バニラの
鶏(2日)・アヒル(1日)等と比較して3〜12日だった値を2〜6日に短縮した
(AdamantiteBeastは伝説枠として20日のまま意図的に変更なし)。

**この修正はこのHANDOFF作成時点でまだユーザーによるゲーム内確認が
取れていない。次に会話が続く場合、最初に確認すること。**

### 3.14 README.md/About.xmlが虫肉の実装について古い(既に修正済みの)説明のまま残っていた
ユーザーからの「技術的な異常・不具合がないか確認してほしい」という依頼を受けての全体レビューで
発覚。3.9〜3.11で`meatDef`省略+`fleshType`/`meatLabel`方式から`JP_Meat_Insect`という実在の
共有アイテムを明示参照する方式に切り替えたにもかかわらず、`README.md`と`About.xml`(ゲーム内
Mod一覧・Steam Workshopページに表示される説明文)の複数箇所が「虫肉はバニラ標準のアイテムを
`fleshType`+`meatLabel`で流用しているだけ」という**修正前の(実際にバグがあった)実装**の説明の
ままになっていた。実際のXML(`Meats.xml`)と食い違っており、ユーザーが誤った前提で在庫管理や
他MODとの互換性を判断してしまう恐れがあったため、該当箇所を全て現状の実装に合わせて修正した。
コード自体に不具合はなく、ドキュメントの記述漏れ(実装変更時にREADME/Aboutの更新が漏れていた)
が原因。

### 3.15 `mergeCompatibilityTags`のXML配置が間違っており、起動のたびにXMLエラーが出ていた(3.11の訂正)
3.14の全体レビュー後、ユーザーが実機でMODを起動したPlayer.logを提供してくれたことで発覚した、
**実際に起動時エラーとして再現していた不具合**。ログの実際のエラー内容:

```
XML error: <mergeCompatibilityTags MayRequire="Ludeon.RimWorld.Ideology">...</mergeCompatibilityTags>
doesn't correspond to any field in type ThingDef. Context: <ThingDef ...><defName>JP_Meat_Insect</defName>...
```

3.11で「ThingDefのルート階層に`mergeCompatibilityTags`を追加すればIdeologyの信条が反応する」と
記録していたが、**このXML配置自体が誤りだった**。`mergeCompatibilityTags`は`ThingDef`直下の
フィールドではなく、`<ingredient>`ブロック(`IngredientProperties`)の中に置く必要がある。
実際のバニラのエラーメッセージ("doesn't correspond to any field in type ThingDef")がまさに
この誤りを示しており、3.11時点でこれを「デコンパイル済みソースで検証済み」としていたのは
不正確だった(おそらく検証が不十分だった)。

このタグはXMLパース時に無効な位置にあったため黙って無視されるだけで、ゲームがクラッシュしたり
他の項目の読み込みが壊れたりすることはなかったが、(1) 起動のたびにログにエラーが出続ける、
(2) Ideologyの「Insect Meat: Loved/Despised」信条が`JP_Meat_Insect`を対象として一切認識しない
(タグ自体が読み込まれていないため)、という二重の実害があった。

正しい配置(RimWorldコミュニティの実例で確認- Hardcore Foods等の既存MODが同じ手法を使用):
```xml
<ingredient>
  <mergeCompatibilityTags MayRequire="Ludeon.RimWorld.Ideology">
    <li MayRequire="Ludeon.RimWorld.Ideology">InsectMeat</li>
  </mergeCompatibilityTags>
</ingredient>
```
`Defs/ThingDefs_Items/Meats.xml`の`JP_Meat_Insect`をこの形式に修正し、`validate.py`で
XML整形式チェック済み。**この修正はまだユーザーによるPlayer.logでの再確認が取れていない。
次回、起動ログに同じXMLエラーが再発していないか、また該当の信条を持つ入植者が実際に
`JP_Meat_Insect`を食べてIdeologyの好意ムードが正しく発生するかを確認すること。**

**教訓**: 「デコンパイル済みソースで検証した」という過去セッションの記述であっても、
実際に実機のログで再現するまでは鵜呑みにしない。今回のように、フィールド名自体は
正しくてもXML上の配置(親要素)を間違えるケースは、静かに無視されるだけでエラーにすら
気づきにくい。

### 3.16 食性の雑食化、肉・革産出量+20%、卵生種の産卵頻度短縮(ユーザー要望によるバランス調整)
ユーザーから3点の要望: (1) 女郎蜘蛛など現在`foodType: CarnivoreAnimal`になっている
モンスターを`OmnivoreAnimal`に変更、(2) 肉・革の産出量が以前より減っている気がするので
調整、(3) 卵を産む頻度も以前より減っている気がするので調整。

(2)(3)については、実際に減ったのかをこのリポジトリのgit履歴で確認しようとしたが、
`Scripts/gen_settings_patch.py`・`Defs/ThingDefs_Races/*.xml`とも**リポジトリ統合時
(`630466c`/`6f3b128`)の1スナップショットしか記録がなく**、それ以前の長期セッションでの
反復調整はコミット単位で残っていないため、実際に数値が下がったのかは確認できなかった。
ただし設定シートはまさにこの種の再調整のために存在するので、実害の有無に関わらず
ユーザーの要望通り引き上げた。

実施内容:
- **食性**: `foodType: CarnivoreAnimal`だった12体
  (JapaneseWolf/EzoWolf/AdamantiteBeast/Meganeura/Titanoptera/Smilodon/
  Pulmonoscorpius/Megarachne/Nekomata/Yukionna/Dragonkin/Jorogumo)を
  全て`OmnivoreAnimal`に変更。`Defs/ThingDefs_Races/*.xml`に直接記載。
  残り11体(元からOmnivore 7体+Vegetarian 4体: Mammoth/WoollyRhino/
  IrishElk/Arthropleura)は変更なし。これで23体中`CarnivoreAnimal`は0体。
- **肉量・革量**: `Scripts/gen_settings_patch.py`の`CREATURES`テーブルの
  MeatAmount/LeatherAmountを全23体一律+20%(四捨五入)。`python3
  Scripts/gen_settings_patch.py`で`Patch_CreatureSettings.xml`に反映済み。
  wool量・drawSizeは変更していない。
- **産卵頻度**: 卵生8体の`eggLayIntervalDays`(`Defs/ThingDefs_Races/*.xml`に
  直接記載、設定シートの対象外)を約20%短縮: AdamantiteBeast 20→16、
  Meganeura 3→2.5、Titanoptera 5→4、Arthropleura 6→5、
  Pulmonoscorpius 5→4、Megarachne 4→3、Titanomyrma 3→2.5、
  Archimylacris 2→1.5。`hatcherDaystoHatch`(孵化日数、`Eggs.xml`/
  `Eggs_Insects.xml`)は今回の要望が「産卵頻度」のみだったため変更していない
  (元々ほとんどの個体で孵化日数 > 産卵間隔なので、間隔を縮めても孵化前に
  次の卵を産む状態になるだけで矛盾はない)。

`validate.py`で検証済み、既知の1件(Shearable 16 vs 16)以外の問題なし。

## 4. 現在の各パラメータの状態 (要点)

詳細な数値は各ファイルを直接参照。ここでは「どのロジックで決めたか」の
要点のみ記す。

- **出現頻度・肉量・革量・毛量・drawSize**: `Scripts/gen_settings_patch.py`の
  `CREATURES`テーブルが正。3.8参照。肉量・革量は3.16で全23体+20%済み。
- **foodType**: 23体中`CarnivoreAnimal`は0体(3.16で全て`OmnivoreAnimal`化)。
  `VegetarianAnimal`はMammoth/WoollyRhino/IrishElk/Arthropleuraの4体、
  残り19体は`OmnivoreAnimal`。
- **Wildness**: 妖怪+AdamantiteBeast=0.985(Thrumbo相当)、Mammoth+昆虫類=0.96、
  他の古代哺乳類=0.93。3.3参照。
- **predator**: 全23体`false`。3.6参照(入植者の子供を誤って襲う不具合の
  根本対策)。
- **manhunterOnDamageChance** (被弾時反撃): Tier A(草食獣+穏健妖怪)=0%、
  Tier B(他妖怪+小型昆虫+オオカミ系)=35%、Tier C(Adamantite+大型昆虫)=100%。
  3.5参照。
- **manhunterOnTameFailChance** (テイム失敗時反撃): Tier A=0%、Tier B=12%、
  Tier C=28%。3.7参照。
- **肉アイテムの種類**: 妖怪7体(Nekomata/Youko/Yukionna/Zashikiwarashi/
  Tengu/Oni/Dragonkin)=`Meat_Human`(バニラ実在アイテム)。虫系8体
  (古代昆虫7種+Jorogumo)=`JP_Meat_Insect`(このMOD独自の共有アイテム、
  `Defs/ThingDefs_Items/Meats.xml`)。他の古代獣は各自専用の`JP_Meat_*`。
  3.9〜3.11参照。
- **gestationPeriodDays / eggLayIntervalDays**: 3.12・3.13参照。値は
  `Defs/ThingDefs_Races/*.xml` に直接記載。eggLayIntervalDaysは3.16で
  卵生8体を約20%短縮済み。

## 5. ファイル構成マップ

パスはリポジトリルートから見て `RimWorld/JP_Beasts/` 配下(§1参照)。

```
RimWorld/JP_Beasts/
  About/                          MOD メタデータ (About.xml)
  Defs/
    ThingDefs_Races/              23体の本体定義 (最重要・頻繁に編集)
      Races_Yokai.xml             妖怪8体
      Races_Ancient.xml           古代獣5体(狼2+マンモス+マゾタイロス+アダマンタイト)+昆虫2体(メガネウラ+ティタノプテラ)
      Races_AncientMammals.xml    古代哺乳類3体(ケナガサイ+オオツノジカ+サーベルタイガー)
      Races_Insects.xml           古代昆虫5体(アースロプレウラ+プルモノスコルピウス+メガラクネ+タイタノミルマ+アーキミラクリス)
    ThingDefs_Items/
      Meats.xml                   各種専用肉アイテム + 共有JP_Meat_Insect
      Eggs.xml / Eggs_Insects.xml 卵アイテム(Hatcher comp)
      (その他: 革・毛・素材アイテム)
    PawnKindDefs/                 PawnKindDef (ライフステージのdrawSize等)
    RecipeDefs/
  Languages/Japanese/DefInjected/ 日本語ラベル翻訳(自動翻訳MOD誤訳対策)
  Patches/
    Patch_CreatureSettings.xml    生成物。手編集禁止(§2.3参照)
  Scripts/                        ★このセッションでリポジトリに正式移設
    gen_settings_patch.py         設定シート生成スクリプト
    validate.py                   コミット前チェックスクリプト
  Textures/                       画像アセット(ユーザーが独自差し替え済みの
                                   ものがあるため、フルZIP配布時は要注意)
  README.md                       ユーザー向けMOD説明
  HANDOFF.md                      このファイル
```

## 6. 開発ワークフローの型 (毎回このサイクルで進める)

1. ユーザーの日本語報告を正確に読む。曖昧な場合、AskUserQuestionで確認する
   (このセッションでも「テイム済みでも繁殖しないか」等、要所で確認を挟んで
   いる)。
2. 憶測で直さない。§2.1の手順で実際に原因を調べる。
3. 修正を実装(1体の変更ならEdit、23体一括ならPythonスクリプト§2.4)。
4. `python3 Scripts/validate.py` で検証。
5. `git add <変更ファイルのみ>` → 詳細なコミットメッセージ(背景・根本原因・
   裏取りの証拠を含める) → `git push`。
6. `SendUserFile`で変更点を配布(個別ファイル、またはユーザー指示があれば
   ZIP)。
7. 何を直したか・なぜそれが原因だったかを日本語で簡潔に説明する。

## 7. 引き継ぎ時点で未確認・要フォローアップの項目

- **3.13の繁殖頻度調整**: 実装・検証・プッシュ・配布まで完了しているが、
  ユーザーによるゲーム内での実際の繁殖頻度確認はまだ取れていない。
  次のやり取りで最初にフォローアップすること。
- ~~`validate.py`のチェック5(Shearable comp数16 vs 設定シートのwool patch数17)~~
  → **解決済み**。原因はMODの不具合ではなく`validate.py`自身の数え方だった:
  設定シート冒頭の使い方コメント(`4) 基本毛量 woolAmount タグの数値...`)にも
  たまたま「基本毛量」という文字列が含まれており、これも1件としてカウント
  されていたため恒常的に+1されていた。検索文字列を「基本毛量(」(直後の
  括弧まで含める)に変更し、実際の毛刈り個体ブロックのコメントだけを
  拾うよう修正した結果、16 vs 16で一致することを確認した(2026-09-18)。

## 8. その他の実務上の注意

- ユーザーのメールアドレス(`base@oct-inks.com`)は作者情報等の識別にのみ使い、
  外部サービスへの送信には使わないこと。
- コミットメッセージ・PR等にモデル識別子(Sonnet 5等)を含めないこと
  (チャット上の返答でのみ言及可)。
- `Textures/`配下の画像ファイルには絶対に触れないこと。§2.5(恒久ルール)参照。
- **GitHubのWeb UIについて、確認せず断定した情報を話して信頼を失った事例
  (2026-09-21)**: ユーザーから「画像を直接リポジトリに反映するにはどうすれば
  いいか」と聞かれた際、「GitHubのWeb UIには"Add file"→"Upload files"という
  ボタンがある」と一般論を確認なしに断定して伝えた。実際にはユーザーは
  正しいアカウント(`Oct-Incs`、このセッションのGitHub連携と同一アカウント。
  `get_me`/`list_repository_collaborators`で確認済み)でログイン済みだったが、
  それでも該当ボタンが見当たらず、「噓をつくな」と厳しく指摘された。
  原因は、(1) GitHubの画面デザインが近年何度も変わっており、最新のUIでの
  正確なボタンの位置を確認せずに言い切ったこと、(2) 最初の失敗の後も
  「アカウントの権限不一致では」という別の未検証の仮説を重ねてしまったこと。
  最終的にユーザー自身が「フォルダ一覧でのドラッグ&ドロップ」または
  「`github.dev`(URLの`github.com`を`github.dev`に変えるとVS Code風の
  ブラウザエディタが開く)」という、UIの細部に依存しない確実な方法で
  画像をリポジトリの`main`ブランチに直接アップロードする運用を確立した。
  **教訓**: GitHubのUI要素の有無・場所のような、外部サービスの現在の見た目に
  関する主張は、自分の知識だけで断定しない。確認できない場合は「不確かだが」
  と明言し、UIの変更に左右されない代替手段(ドラッグ&ドロップ、`github.dev`
  等)を優先して案内する。
