#!/usr/bin/env python3
"""QUELLE v0 — tirer des octets, déclarer la source. Pas de photon inventé."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SOURCES = ("os", "qrng", "qkd")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def tirer(n: int = 32, source: str = "os") -> dict:
    source = (source or "os").strip().lower()
    if source not in SOURCES:
        raise SystemExit("source : os | qrng | qkd")
    if source != "os":
        raise SystemExit(
            f"source={source} refusée : pas d'appareil détecté. "
            "v0 n'écrit qrng/qkd que branché. Relance avec --source os."
        )
    brut = secrets.token_bytes(n)
    carte = {
        "format": "quelle.v0",
        "id": "QL-" + uuid.uuid4().hex[:12],
        "source": "os",
        "simule": True,
        "appareil": None,
        "n_octets": n,
        "sha256": hashlib.sha256(brut).hexdigest(),
        "tire_at": _now(),
        "note": "os.urandom / secrets — pas un photon",
    }
    return {"carte": carte, "octets_hex": brut.hex()}


def lire(chemin: str) -> dict:
    p = Path(chemin).expanduser()
    carte = json.loads(p.read_text(encoding="utf-8"))
    if carte.get("format") != "quelle.v0":
        raise SystemExit("pas une carte quelle.v0")
    if carte.get("source") != "os" and not carte.get("simule") and not carte.get("appareil"):
        raise SystemExit("carte mensongère : source non-os sans appareil")
    return carte


def voir(carte: dict, registre: str = "vues.quelle.json") -> dict:
    sha = carte.get("sha256")
    if not sha:
        raise SystemExit("refus : pas de sha256")
    path = Path(registre).expanduser()
    mem = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {"sha256": []}
    vues = list(mem.get("sha256") or [])
    if sha in vues:
        raise SystemExit("refus : fraîcheur. empreinte déjà vue")
    vues.append(sha)
    mem["sha256"] = vues
    mem["vue_at"] = _now()
    path.write_text(json.dumps(mem, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"ok": True, "sha256": sha, "n_vues": len(vues), "registre": str(path)}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="quelle")
    sub = p.add_subparsers(dest="cmd", required=True)
    pt = sub.add_parser("tirer")
    pt.add_argument("--octets", type=int, default=32)
    pt.add_argument("--source", default="os")
    pt.add_argument("--vers", default="carte.quelle.json")
    pl = sub.add_parser("lire")
    pl.add_argument("fichier")
    pv = sub.add_parser("voir")
    pv.add_argument("fichier")
    pv.add_argument("--registre", default="vues.quelle.json")
    args = p.parse_args(argv)
    if args.cmd == "tirer":
        rec = tirer(args.octets, args.source)
        Path(args.vers).write_text(json.dumps(rec["carte"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out = dict(rec["carte"])
        out["octets_hex"] = rec["octets_hex"]
        out["fichier"] = args.vers
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.cmd == "lire":
        print(json.dumps(lire(args.fichier), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(voir(lire(args.fichier), args.registre), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
