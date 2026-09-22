"""Regenerate dark_mode.svg / light_mode.svg with live GitHub stats.

Neofetch-style profile. Stdlib only, no dependencies.
"""
import calendar
import html
import json
import os
import urllib.request
from datetime import date, datetime, timezone

USER = "soominn"
ACCOUNT_YEAR = 2021
W = 56  # info column width in characters

ART = r"""
                .,,.  .
           .;: ,;+++;,.,.:.     ,.
        .;%?@+ .;:?*?,,;,;,,?*: ..
      :%S#@**  .;,,:..... .,,::,,+?: ..
    .?@@#@?+, ,:;;,. .;*?*;. ....,:;:::;:.
   .%@###S+; ,**:. :+?##?,,.....   .:;;;**,
  ,%#####++  :%; +S#@#%?+;,,,.  ..   ,::, ?,
 ,%#####?;, ,?, ?@###S##?++,   .    ...,:. +.
 *###@#S;;  :+ +@########?++**;    ...  :,:?,
,?S####+;. :%,.%#########S##@S;..,:. . ,:,*+.
;S####?;: .;;,.S#######%:?##S%?+:;:. ,,S;,....
*#?%S%;;  ;%?: %@#@@@##%.?%*?%##S?+.,,*S,,
;?++?+:. .,,:: ,#@#####%;?SSSSSSS%: ..?:,.
      ..:,:,,,: :#@@@@##@#%%%%??+   ,:,,.
 ..,:,.,;..., .. .*SS##@@#%*+;:,   .;,. ...
  :::;,,:,.    ... .,:+?S##?.    ..,..:,:;,
  ,?*,:::;:....,..;:. .,,:;++:;++;,  ??;?:.
   .:.,:+?;,,,;::+:,,;+:,;,,.,,.    :%?%?,
      ,::,.,.:?+:+:,;;;,,.,          *SS:
      .:;:,........,:,.,.,;,       .,??:
        .::;;;::,... .. .;:.     .;;,.
            ..,::::::,. .,,
                   .,.
""".strip(
    "\n"
)

ART_FONT = 11
ART_LH = 13
ART_CHAR_W = 7.0  # Consolas/Menlo @ 11px
INFO_MIN_X = 460
INFO_Y0 = 40
INFO_LH = 21
SVG_PAD = 24
PANEL_GAP = 20

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("ACCESS_TOKEN") or ""
PRIV_TOKEN = os.environ.get("ACCESS_TOKEN") or TOKEN


def gh(url, payload=None, token=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers={
            "Authorization": f"Bearer {token or TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "soominn-profile",
        },
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.loads(r.read() or "{}")


def graphql(query, variables=None, token=None):
    _, resp = gh(
        "https://api.github.com/graphql",
        {"query": query, "variables": variables or {}},
        token,
    )
    if resp.get("errors"):
        raise RuntimeError(resp["errors"])
    return resp["data"]


def age(b, t):
    years = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
    months = (t.month - b.month - (t.day < b.day)) % 12
    if t.day >= b.day:
        days = t.day - b.day
    else:
        pm_year, pm = (t.year, t.month - 1) if t.month > 1 else (t.year - 1, 12)
        days = calendar.monthrange(pm_year, pm)[1] - b.day + t.day
    return years, months, days


def first_contribution_date():
    for y in range(ACCOUNT_YEAR, datetime.now(timezone.utc).year + 1):
        data = graphql(
            f"""
            query {{
              user(login: "{USER}") {{
                contributionsCollection(
                  from: "{y}-01-01T00:00:00Z",
                  to: "{y + 1}-01-01T00:00:00Z"
                ) {{
                  contributionCalendar {{
                    weeks {{
                      contributionDays {{ date contributionCount }}
                    }}
                  }}
                }}
              }}
            }}"""
        )["user"]["contributionsCollection"]["contributionCalendar"]
        for week in data["weeks"]:
            for day in week["contributionDays"]:
                if day["contributionCount"] > 0:
                    return date.fromisoformat(day["date"])
    return date(ACCOUNT_YEAR, 4, 22)


def fetch_stats():
    yr_aliases = "\n".join(
        f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y + 1}-01-01T00:00:00Z")'
        " { totalCommitContributions restrictedContributionsCount }"
        for y in range(ACCOUNT_YEAR, datetime.now(timezone.utc).year + 1)
    )
    contrib = graphql(f'query {{ user(login: "{USER}") {{ {yr_aliases} }} }}')["user"]
    commits = sum(
        v["totalCommitContributions"] + v["restrictedContributionsCount"]
        for v in contrib.values()
    )
    u = graphql(
        f"""
    query {{
      user(login: "{USER}") {{
        id
        followers {{ totalCount }}
        repositories(first: 100, ownerAffiliations: OWNER) {{
          totalCount
          nodes {{ name stargazerCount isFork }}
        }}
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) {{
          totalCount
        }}
      }}
    }}""",
        token=PRIV_TOKEN,
    )["user"]
    stats = {
        "followers": u["followers"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "contributed": u["repositoriesContributedTo"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "commits": commits,
        "first_contrib": first_contribution_date(),
    }
    stats.update(
        loc([n["name"] for n in u["repositories"]["nodes"] if not n["isFork"]], u["id"])
    )
    return stats


LOC_QUERY = """
query($owner: String!, $name: String!, $id: ID!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef { target { ... on Commit {
      history(first: 100, author: {id: $id}, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { additions deletions }
      }
    } } }
  }
}"""


def loc(repo_names, user_id):
    add = rem = 0
    for name in repo_names:
        cursor = None
        try:
            while True:
                ref = graphql(
                    LOC_QUERY,
                    {"owner": USER, "name": name, "id": user_id, "cursor": cursor},
                    token=PRIV_TOKEN,
                )["repository"]["defaultBranchRef"]
                if ref is None:
                    break
                h = ref["target"]["history"]
                add += sum(n["additions"] for n in h["nodes"])
                rem += sum(n["deletions"] for n in h["nodes"])
                if not h["pageInfo"]["hasNextPage"]:
                    break
                cursor = h["pageInfo"]["endCursor"]
        except Exception as e:
            print(f"loc {name}: {e}")
    return {"loc_add": add, "loc_del": rem, "loc": add - rem}


PALETTES = {
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "art": "#8b949e",
        "h": "#58a6ff",
        "k": "#ffa657",
        "v": "#c9d1d9",
        "d": "#484f58",
        "g": "#3fb950",
        "r": "#f85149",
    },
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "art": "#57606a",
        "h": "#0969da",
        "k": "#953800",
        "v": "#24292f",
        "d": "#afb8c1",
        "g": "#1a7f37",
        "r": "#cf222e",
    },
}


def kv(key, val, width=W):
    dots = "." * max(width - len(key) - len(str(val)) - 3, 1)
    return [(f"{key}: ", "k"), (dots + " ", "d"), (str(val), "v")]


def kv2(k1, v1, k2, v2):
    left = kv(k1, v1, 30)
    return left + [(" | ", "d")] + kv(k2, v2, 23)


def rule(title=""):
    label = f"─ {title} " if title else ""
    return [(label, "h"), ("─" * (W - len(label)), "d")]


def info_lines(s):
    y, m, d = age(s["first_contrib"], date.today())
    n = lambda x: f"{x:,}"
    return [
        [(f"{USER}@github ", "h"), ("─" * (W - len(USER) - 8), "d")],
        [],
        kv("OS", "Windows, macOS"),
        kv("Uptime", f"{y} years, {m} months, {d} days"),
        kv("Location", "Incheon"),
        kv("Kernel", "Software Engineer"),
        kv("IDE", "Cursor, VS Code"),
        [],
        kv("Languages.Programming", "Python, TypeScript, Java"),
        kv("Languages.Real", "Korean, English"),
        kv("Hobbies", "Gaming"),
        [],
        rule("Contact"),
        kv("Email", "chosm0129@naver.com"),
        kv("Blog", "som-ethi-ng.tistory.com"),
        [],
        rule("GitHub Stats"),
        kv2("Repos", f"{s['repos']} {{Contributed: {s['contributed']}}}", "Stars", n(s["stars"])),
        kv2("Commits", n(s["commits"]), "Followers", n(s["followers"])),
        [
            ("Lines of Code: ", "k"),
            (n(s["loc"]), "v"),
            (" ( ", "d"),
            (n(s["loc_add"]) + "++", "g"),
            (", ", "d"),
            (n(s["loc_del"]) + "--", "r"),
            (" )", "d"),
        ],
    ]


def normalize_art(raw: str) -> list[str]:
    """Equal-width rows so the circle can be positioned as one block."""
    lines = [ln.rstrip("\n") for ln in raw.split("\n")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    width = max((len(ln.rstrip(" ")) for ln in lines), default=0)
    return [ln.rstrip(" ").ljust(width) for ln in lines]


def canvas_size(info_count, art_lines):
    art_cols = max((len(ln) for ln in art_lines), default=0)
    art_w = art_cols * ART_CHAR_W
    art_h = len(art_lines) * ART_LH
    info_h = INFO_Y0 + info_count * INFO_LH
    h = max(int(art_h + 2 * SVG_PAD), info_h + SVG_PAD) + SVG_PAD
    info_x = INFO_MIN_X
    w = info_x + 16 + W * 8 + SVG_PAD
    return w, h, info_x, art_w, art_h


def render(mode, stats):
    p = PALETTES[mode]
    art_lines = normalize_art(ART)
    lines = info_lines(stats)
    w, h, info_x, art_w, art_h = canvas_size(len(lines), art_lines)

    # Center the whole ASCII block in the left panel (no text-anchor — GitHub-safe)
    panel_left = SVG_PAD
    panel_right = info_x - PANEL_GAP
    panel_cx = (panel_left + panel_right) / 2
    art_x = panel_cx - art_w / 2
    art_y0 = (h - art_h) / 2 + ART_LH
    text_len = art_w  # force exact rendered width

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'font-family="Consolas, Menlo, monospace">',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{p["bg"]}" stroke="{p["border"]}"/>',
    ]
    for i, line in enumerate(art_lines):
        out.append(
            f'<text x="{art_x:.1f}" y="{art_y0 + i * ART_LH:.1f}" fill="{p["art"]}" '
            f'font-size="{ART_FONT}px" textLength="{text_len:.1f}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve">{html.escape(line)}</text>'
        )
    for i, segs in enumerate(lines):
        if not segs:
            continue
        spans = "".join(f'<tspan fill="{p[c]}">{html.escape(t)}</tspan>' for t, c in segs)
        out.append(
            f'<text x="{info_x}" y="{INFO_Y0 + i * INFO_LH}" font-size="13px" '
            f'xml:space="preserve">{spans}</text>'
        )
    out.append("</svg>")
    return "\n".join(out)


def selfcheck():
    assert age(date(2021, 4, 22), date(2026, 9, 22)) == (5, 5, 0)
    assert len("".join(t for t, _ in kv("OS", "Windows, macOS"))) == W
    assert len(ART.split("\n")) >= 1


if __name__ == "__main__":
    selfcheck()
    stats = fetch_stats()
    print("stats:", {k: (str(v) if k == "first_contrib" else v) for k, v in stats.items()})
    for mode in PALETTES:
        with open(f"{mode}_mode.svg", "w", encoding="utf-8") as f:
            f.write(render(mode, stats))
    print("wrote dark_mode.svg, light_mode.svg")
