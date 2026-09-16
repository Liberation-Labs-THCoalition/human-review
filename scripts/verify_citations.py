#!/usr/bin/env python3
"""Verify every arXiv citation in a .bib against the arXiv API.

Opened as a program-wide action item 2026-08-29: 13 of 29 references in the
consequentiality working draft had wrong first authors, years, or titles --
including arXiv:2506.04909, which is Wang, K. and was cited as Shi, L. Lyra had
already flagged the same class on logit-bias-confab ("refs.bib cross-scrambles
citations"). Two papers is a pattern, not an accident, and nothing in the
pipeline checks it.

Batches IDs into one query per paper (arXiv supports a comma-separated id_list)
and backs off on 429 rather than hammering. Reports MISMATCH, not just missing:
a citation that resolves to a real paper with the wrong author is the failure
mode that matters, and a presence check cannot see it.

    python3 verify_citations.py ../temporal-boundary/references.bib [more.bib ...]
"""
import re, sys, time, urllib.parse, urllib.request

API = "https://export.arxiv.org/api/query"
ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def id_is_wellformed(aid):
    """arXiv IDs are YYMM.NNNNN. A month outside 01-12 cannot exist, so the ID
    was invented rather than mistyped -- worth separating from 'the API did not
    return it', which can just mean a withdrawn paper or a network hiccup."""
    mm = int(aid[2:4])
    return 1 <= mm <= 12


def entries(path):
    """(key, fields) per @entry, brace-aware enough for these files."""
    txt = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", txt):
        start = m.end()
        depth, i = 1, txt.find("{", m.start())
        i += 1
        while i < len(txt) and depth:
            depth += (txt[i] == "{") - (txt[i] == "}")
            i += 1
        body = txt[start:i - 1]
        f = {}
        for fm in re.finditer(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\w+\s*=|$)",
                              body, re.S):
            f[fm.group(1).lower()] = " ".join(fm.group(2).split())
        out.append((m.group(2).strip(), f))
    return out


def arxiv_id(f):
    """An arXiv ID, ONLY where the field actually denotes one.

    The first version scanned the `doi` field too, and a Frontiers DOI --
    10.3389/fpsyg.2015.00500 -- matches \\d{4}\\.\\d{4,5} as "2015.00500". It then
    reported a correct reference as a fabricated identifier. A verifier that
    invents findings is worse than no verifier: it spends the reader's trust on
    noise. Only `eprint` (with an arXiv archivePrefix) or a field that literally
    says arXiv counts.
    """
    ep = f.get("eprint", "").strip()
    if ep and ID_RE.fullmatch(ep):
        return ID_RE.fullmatch(ep).group(1)
    for k in ("journal", "url", "note", "howpublished", "eprint", "doi"):
        v = f.get(k, "")
        if "arxiv" not in v.lower():
            continue                     # a non-arXiv DOI is not an arXiv ID
        m = re.search(r"arxiv[:\s/.]*(\d{4}\.\d{4,5})", v, re.I)
        if m:
            return m.group(1)
        m = ID_RE.search(v)
        if m:
            return m.group(1)
    return None


def fetch(ids, tries=6):
    q = f"{API}?id_list={','.join(ids)}&max_results={len(ids)}"
    delay = 5
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(q, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            code = getattr(e, "code", None)
            if attempt == tries - 1:
                print(f"  ! arXiv fetch failed after {tries}: {e}")
                return None
            print(f"  . arXiv {code or e}; backing off {delay}s", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 120)
    return None


def parse_feed(xml):
    out = {}
    for chunk in xml.split("<entry>")[1:]:
        idm = ID_RE.search(re.search(r"<id>(.*?)</id>", chunk, re.S).group(1))
        if not idm:
            continue
        title = " ".join(re.search(r"<title>(.*?)</title>", chunk, re.S).group(1).split())
        names = re.findall(r"<name>(.*?)</name>", chunk)
        pub = re.search(r"<published>(\d{4})", chunk)
        out[idm.group(1)] = {"title": title,
                             "first": names[0] if names else "",
                             "year": pub.group(1) if pub else ""}
    return out


def surname(s):
    s = s.strip().strip("{}").strip()      # {OpenAI} and OpenAI are the same author
    if "," in s:
        return s.split(",")[0].strip().lower()
    return s.split()[-1].lower() if s.split() else ""


def given_initial(s):
    """First letter of the given name, for 'Surname, Given' or 'Given Surname'."""
    s = s.strip().strip("{}").strip()
    if "," in s:
        rest = s.split(",", 1)[1].strip()
        return rest[0].lower() if rest else ""
    parts = s.split()
    return parts[0][0].lower() if len(parts) > 1 else ""


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def main(paths):
    bad = 0
    for path in paths:
        es = entries(path)
        want = {}
        for key, f in es:
            aid = arxiv_id(f)
            if aid:
                want[aid] = (key, f)
        print(f"\n=== {path}  ({len(es)} entries, {len(want)} with arXiv IDs) ===")
        if not want:
            continue
        xml = fetch(sorted(want))
        if not xml:
            bad += 1
            continue
        got = parse_feed(xml)
        for aid, (key, f) in sorted(want.items()):
            if not id_is_wellformed(aid):
                print(f"  BAD ID    {key:28s} arXiv:{aid} — month {aid[2:4]} does not "
                      f"exist; this identifier is fabricated, not mistyped")
                bad += 1
                continue
            g = got.get(aid)
            if not g:
                print(f"  UNRESOLVED {key:28s} arXiv:{aid} — not returned by the API")
                bad += 1
                continue
            probs = []
            cited_first = f.get("author", "").split(" and ")[0]
            if cited_first and surname(cited_first) != surname(g["first"]):
                probs.append(f"first author: cited {surname(cited_first)!r}, "
                             f"arXiv {surname(g['first'])!r}")
            elif cited_first:
                # Surname alone is not enough. 'Fu, Yuxin' for Tianyu Fu and
                # 'Kim, Seungone' for Junsol Kim both passed a surname check
                # while naming the wrong person (found 2026-09-15 in
                # oracle-harness/papers/references.bib).
                gi, ai = given_initial(cited_first), given_initial(g["first"])
                if gi and ai and gi != ai:
                    probs.append(f"first author given name: cited "
                                 f"{cited_first.strip()!r}, arXiv {g['first']!r}")
            cy = f.get("year", "")
            # arXiv year is the PREPRINT year; a citation may legitimately carry
            # the later conference/journal year. Only flag a gap that convention
            # cannot explain.
            if cy and g["year"] and abs(int(cy) - int(g["year"])) > 1:
                probs.append(f"year: cited {cy}, arXiv {g['year']} "
                             f"(>1yr apart, not a preprint/publication gap)")
            ct = norm(f.get("title", ""))
            if ct and norm(g["title"]) and ct != norm(g["title"]):
                a, b = set(ct.split()), set(norm(g["title"]).split())
                if len(a & b) / max(1, len(a | b)) < 0.7:
                    probs.append(f"title: cited {f.get('title','')[:45]!r} vs "
                                 f"arXiv {g['title'][:45]!r}")
            if probs:
                bad += 1
                print(f"  MISMATCH  {key:28s} arXiv:{aid}")
                for p in probs:
                    print(f"              - {p}")
            else:
                print(f"  ok        {key:28s} arXiv:{aid}")
        time.sleep(4)          # arXiv asks for spacing between queries
    print(f"\n{'ALL CLEAN' if not bad else str(bad) + ' PROBLEM(S)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
