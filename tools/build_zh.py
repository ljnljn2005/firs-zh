"""Build src/grf/lang/schinese.toml for the FIRS 5.2.0 Chinese translation.

Reads the upstream English TOML, applies the translation JSON files in this
directory, validates that every English string is translated and that no
NewGRF string control code was dropped or invented, then writes the Chinese
TOML (grflangid 0x56 = Chinese Simplified).
"""

import json
import os
import re
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
REL = os.path.join("src", "grf", "lang", "english.toml")


def find_source():
    """Prefer the FIRS checkout in the current directory, else ./firs-main next to this file."""
    for base in (os.getcwd(), os.path.join(HERE, "firs-main")):
        candidate = os.path.join(base, REL)
        if os.path.isfile(candidate):
            return candidate
    raise SystemExit("cannot find src/grf/lang/english.toml (run inside a FIRS checkout)")


SRC = find_source()
DST = os.path.join(os.path.dirname(SRC), "schinese.toml")

CODE_RE = re.compile(r"\{[^{}]*\}")


def load_json(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fp:
        return json.load(fp)


def codes(text):
    """Multiset of control codes, ignoring the plural marker which Chinese drops."""
    out = {}
    for match in CODE_RE.findall(text):
        if match.startswith("{P "):
            continue
        out[match] = out.get(match, 0) + 1
    return out


def main():
    with open(SRC, "rb") as fp:
        english = tomllib.load(fp)

    cargo = load_json("zh_cargo.json")
    ind = load_json("zh_ind.json")
    station = load_json("zh_station.json")
    misc = load_json("zh_misc.json")

    translated = {}
    problems = []

    for key, fields in english.items():
        if key == "GLOBAL_PRAGMA":
            continue
        new_fields = {}
        for sub, value in fields.items():
            if sub == "cid":
                new_fields[sub] = value
                continue
            text = None
            if key.startswith("STR_CARGO_") and sub in ("name", "cargo_unit"):
                cid = key[len("STR_CARGO_"):]
                entry = cargo.get(cid)
                if entry is None:
                    problems.append(f"missing cargo translation: {cid}")
                else:
                    if sub == "name":
                        text = entry[0]
                    elif sub == "cargo_unit":
                        text = entry[1]
                    elif sub == "base":
                        text = misc.get(key)
            elif key.startswith("STR_CARGO_"):
                text = misc.get(key)
                if text is None:
                    problems.append(f"missing translation: {key}")
            elif key.startswith("STR_IND_"):
                iid = key[len("STR_IND_"):]
                text = ind.get(iid)
                if text is None:
                    problems.append(f"missing industry translation: {iid}")
            elif key.startswith("STR_STATION_"):
                sid = key[len("STR_STATION_"):]
                text = station.get(sid)
                if text is None:
                    problems.append(f"missing station translation: {sid}")
            else:
                text = misc.get(key)
                if text is None:
                    problems.append(f"missing translation: {key}")

            if text is None:
                text = value  # keep English as a visible fallback

            if codes(value) != codes(text):
                problems.append(
                    f"control code mismatch in {key}.{sub}: {sorted(codes(value))} vs {sorted(codes(text))}"
                )
            if text.strip() == value.strip() and key not in ("STR_TOWN", "STR_STATION"):
                problems.append(f"untranslated: {key}.{sub}")

            new_fields[sub] = text
        translated[key] = new_fields

    # unused translation entries are almost always a typo in an id
    for cid in cargo:
        if f"STR_CARGO_{cid}" not in english:
            problems.append(f"unused cargo id: {cid}")
    for iid in ind:
        if f"STR_IND_{iid}" not in english:
            problems.append(f"unused industry id: {iid}")
    for sid in station:
        if f"STR_STATION_{sid}" not in english:
            problems.append(f"unused station id: {sid}")
    for key in misc:
        if key not in english:
            problems.append(f"unused misc key: {key}")

    if problems:
        for p in problems:
            print("PROBLEM:", p, file=sys.stderr)
        print(f"{len(problems)} problem(s), aborting", file=sys.stderr)
        return 1

    def escape(value):
        return value.replace("\\", "\\\\").replace('"', '\\"')

    lines = [
        "[GLOBAL_PRAGMA]",
        'grflangid = "0x56"',
        'plural = "0"',
        "",
    ]
    for key, fields in translated.items():
        lines.append(f"[{key}]")
        for sub, value in fields.items():
            lines.append(f'{sub} = "{escape(value)}"')
        lines.append("")

    with open(DST, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("\n".join(lines))

    print(f"wrote {DST}: {len(translated)} strings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
