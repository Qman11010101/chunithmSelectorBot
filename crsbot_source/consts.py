import json

with open("setting.json", "r", encoding="UTF-8_sig") as s:
    setting = json.load(s)

# URL
URL_chunirec = "https://reiwa.f5.si/chunirec_all.json"
URL_ONGEKI = "https://ongeki.sega.jp/assets/json/music/music.json"
URL_MAIMAI = "https://maimai.sega.jp/data/DXsongs.json"

URL_WACCA = "https://reiwa.f5.si/wacca_all.json"
URL_ARCAEA = "https://reiwa.f5.si/arcaea_all.json"
URL_PHIGROS = "https://reiwa.f5.si/phigros_all.json"

# トークン
CHUNIREC_TOKEN = setting["token"]["chunirec"]
DISCORD_TOKEN = setting["token"]["discord"]

# API関係
API_LIFETIME = int(setting["misc"]["api_lifetime"])

# logger関係
tz = setting["misc"]["timezone"]
is_logging = setting["logging"]["logging"]
loglevel_stdio = setting["logging"]["loglevel_stdio"]
loglevel_file = setting["logging"]["loglevel_file"]
log_filename = setting["logging"]["log_filename"]

# その他
MAX_MUSICS = setting["misc"]["max_musics"]
CMDPREF = setting["misc"]["command_prefix"]
APP_VERSION = "2.0"
CHANNEL_NAME = "選曲bot"

# ヘルプメッセージ
DECLARATION_NAME = f"**CHUNITHM Random Selector bot v{APP_VERSION}** by キューマン・エノビクト"
HIGHLOW = f"""※`(:high/low)`がついているパラメータは、後ろに『:high』もしくは『:low』を付け足すことで『以上』『以下』を表すことができます。
`:up/:down`や`:big/:small`でも可能です。"""

HELPMES_CHUNITHM = f"""
{DECLARATION_NAME}

【コマンド文字列】
`{CMDPREF}random [曲数] [レベル(:high/low)] [ジャンル] [アーティスト] [ノーツ数(:high/low)] [BPM(:high/low)] [難易度]`
`{CMDPREF}search [レベル(:high/low)] [ジャンル] [アーティスト] [ノーツ数(:high/low)] [BPM(:high/low)] [難易度]`
{HIGHLOW}

【パラメータ】
指定しないパラメータは、`-`もしくは`none`と入力してください。

**曲数**
> 表示する曲数を指定します。最大{MAX_MUSICS}曲まで表示できます。
> それ以上の数字を入力した場合、ランダム選曲コマンドにおいては{MAX_MUSICS}曲として扱われ、検索コマンドではエラー扱いになります。
> 指定されなかった場合、3曲として扱われます。
> 半角数字で入力してください。

**レベル**
>  楽曲のレベルを指定します。
> 『10』『13+』のようなレベル表記形式、もしくは『12.6』『13.7』のような譜面定数形式で入力してください。

**ジャンル**
> 楽曲が属するジャンルを指定します。
> 『ORIGINAL』『POPS&ANIME』『niconico』『東方Project』『VARIETY』『イロドリミドリ』『ゲキマイ』から1つ選んで入力してください。

**アーティスト**
> 楽曲のアーティスト名を指定します。
> アーティスト名を入力してください。
> 大文字・小文字および全角・半角を考慮しない部分一致で検索されます。

**ノーツ数**
> 楽曲のノーツ数を指定します。
> 半角数字で入力してください。

**BPM**
> 楽曲のBPMを指定します。
> 半角数字で入力してください。

**難易度**
> 楽曲の難易度を指定します。EXPERTのみもしくはMASTERのみの検索をする場合に使用します。
> 指定する場合、『exp』もしくは『mas』と指定してください。
> 指定されないか、不正な値を指定した場合は自動的にEXPERTとMASTERの両方から検索します。
> レベルもしくはノーツ数が指定されたときのみ機能します。

【コマンド例】
`{CMDPREF}random`: 全楽曲の中からランダムに3曲選びます。
`{CMDPREF}random 5 13+:up`: レベル13+以上の楽曲の中からランダムに5曲選びます。
`{CMDPREF}random - 13 - - - - exp`: レベル13のEXPERTの楽曲をランダムに3曲選びます。
`{CMDPREF}search none 東方Project none 1000:low`: 東方Projectの楽曲の中からノーツ数が1000以下の楽曲を検索します。
`{CMDPREF}search - - - - 300:high`: 全楽曲の中からBPM300以上の楽曲を検索します。

【注意点】
- ジャンルは1つのみ指定可能です。
- WORLD'S ENDには対応していません。
- 一部の値が未登録になっている場合があります。

**オンゲキ楽曲も検索可能です！`{CMDPREF}help_ongeki`もしくは`{CMDPREF}hgeki`でヘルプを呼び出せます！**
"""

HELPMES_ONGEKI = f"""
{DECLARATION_NAME}

【コマンド文字列】
`{CMDPREF}random_ongeki [曲数] [レベル(:high/low)] [ジャンル] [アーティスト] [難易度]` (`{CMDPREF}rgeki`でも可)
`{CMDPREF}search_ongeki [レベル(:high/low)] [ジャンル] [アーティスト] [難易度]` (`{CMDPREF}sgeki`でも可)
{HIGHLOW}

【パラメータ】
指定しないパラメータは、`-`もしくは`none`と入力してください。

**曲数**
> 表示する曲数を指定します。最大{MAX_MUSICS}曲まで表示できます。
> それ以上の数字を入力した場合、ランダム選曲コマンドにおいては{MAX_MUSICS}曲として扱われ、検索コマンドではエラー扱いになります。
> 指定されなかった場合、3曲として扱われます。
> 半角数字で入力してください。

**レベル**
>  楽曲のレベルを指定します。
> 『10』『13+』のようなレベル表記形式で入力してください。
> 譜面定数は使えません。

**ジャンル**
> 楽曲が属するジャンルを指定します。
> 『オンゲキ』『POPS&ANIME』『niconico』『東方Project』『VARIETY』『チュウマイ』から1つ選んで入力してください。

**アーティスト**
> 楽曲のアーティスト名を指定します。
> アーティスト名を入力してください。
> 大文字・小文字および全角・半角を考慮しない部分一致で検索されます。

**難易度**
> 楽曲の難易度を指定します。EXPERTのみもしくはMASTERのみの検索をする場合に使用します。
> 指定する場合、『exp』もしくは『mas』と指定してください。
> 指定されないか、不正な値を指定した場合は自動的にEXPERTとMASTERの両方から検索します。
> レベルが指定されたときのみ機能します。

【コマンド例】
`{CMDPREF}random_ongeki`: 全楽曲の中からランダムに3曲選びます。
`{CMDPREF}random_ongeki 5 13+:up`: レベル13+以上の楽曲の中からランダムに5曲選びます。
`{CMDPREF}random_ongeki - 13 - - - - exp`: レベル13のEXPERTの楽曲をランダムに3曲選びます。
`{CMDPREF}search_ongeki 14 東方Project`: 東方Projectの楽曲の中からレベル14の曲を検索します。

【注意点】
- ジャンルは1つのみ指定可能です。
- LUNATICおよびボーナストラックには対応していません。
"""

HELPMES_WACCA = f"""
{DECLARATION_NAME}

【コマンド文字列】
`{CMDPREF}random [曲数] [レベル(:high/low)] [ジャンル] [アーティスト] [難易度]`
`{CMDPREF}search [レベル(:high/low)] [ジャンル] [アーティスト] [難易度]`
{HIGHLOW}

【パラメータ】
指定しないパラメータは、`-`もしくは`none`と入力してください。

**曲数**
> 表示する曲数を指定します。最大{MAX_MUSICS}曲まで表示できます。
> それ以上の数字を入力した場合、ランダム選曲コマンドにおいては{MAX_MUSICS}曲として扱われ、検索コマンドではエラー扱いになります。
> 指定されなかった場合、3曲として扱われます。
> 半角数字で入力してください。

**レベル**
>  楽曲のレベルを指定します。
> 『10』『13+』のようなレベル表記形式で入力してください。
> 譜面定数は使えません。

**ジャンル**
> 楽曲が属するジャンルを指定します。
> 『アニメ／ＰＯＰ』『ボカロ』『東方アレンジ』『2.5次元』『バラエティ』『オリジナル』『TANO\\*C』『TANO\\*C（オリジナル）』から1つ選んで入力してください。

**アーティスト**
> 楽曲のアーティスト名を指定します。
> アーティスト名を入力してください。
> 大文字・小文字および全角・半角を考慮しない部分一致で検索されます。

**難易度**
> 楽曲の難易度を指定します。EXPERTのみもしくはINFERNOのみの検索をする場合に使用します。
> 指定する場合、『exp』もしくは『inf』と指定してください。
> 指定されないか、不正な値を指定した場合は自動的にEXPERTとINFERNOの両方から検索します。
> レベルが指定されたときのみ機能します。
"""
