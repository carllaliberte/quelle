# QUELLE

**D'où vient ce bit.**

QUELLE is an origin certificate for entropy. A draw carries one label: `os`, `qrng`, or `qkd`. Never invent a photon.

On a phone without a dongle, the label is `os`. That is honest. After [famille juge.v0](https://github.com/carllaliberte/famille/blob/main/schema/juge.v0.json) and [mode-protocol `5e4518b`](https://github.com/carllaliberte/mode-protocol/commit/5e4518bb9c8d683dad1b2420609ff53b3fe6d2d1), `quelle: os` is classique, not quantique. This rail does not mint `quantique`.

This repository is version 0. Phone + Python. MIT. Zéro token. See [INTERDIT.md](INTERDIT.md).

Ce n'est pas UNFORGE (sceau de fichier).  
Ce n'est pas SITUS (droit sur un lieu).  
Ce n'est pas QUANTUM le nœud (sas local).  
Ce n'est pas un ordinateur quantique dans ta poche.

## Three sources

```
source déclarée  +  octets  +  empreinte  →  carte .quelle.json
```

| Source | When you may write it |
|---|---|
| `os` | `secrets` / urandom. Always true on a phone. Classique. |
| `qrng` | A real USB/PCIe QRNG answers. Webcam noise is not qrng. Otherwise: refuse. |
| `qkd` | A hardware QKD session. IBM Job / IonQ / software BB84 is not qkd. Otherwise: refuse. |

`simule: true` only if a presented software protocol (BB84, CHSH in software) claims it. Honest `os` is not a simulation. Do not stamp `simule` on every `os` card.

## Physics locks (this rail)

- Origin certificate only: `os` \| `qrng` \| `qkd`. Never invent a photon.
- `os` is phone entropy (`secrets` / urandom). Always honest on a phone. `quelle: os` is classique, not quantique. This rail does not mint `quantique`.
- `qrng` / `qkd` only if real hardware answers. Webcam noise is not qrng. IBM Job / IonQ / software BB84 is not qkd.
- `simule: true` only if a presented software protocol claims it. Honest `os` is not a simulation.
- QUANTUM signs later. Keys stay off Git. This repo is not a QUANTUM seal and not the QUANTUM node.
- No token, L1, or cloud QUELLE.

Judgment = Carl: `python3 quelle.py tirer|lire`.

## How to run

```bash
python3 quelle.py tirer --octets 32
python3 quelle.py lire carte.quelle.json
```

Sans dongle : source = `os`. C'est correct. Ce n'est pas honteux.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

Tests lock the rows below. Nothing in this repository is a theorem. Nothing here is a QUANTUM seal.

| Claim | Status |
|---|---|
| default `tirer` → `os` | **verified** by tests on this rail |
| `os` card is not quantique and not a photon | **verified** |
| `qrng` / `qkd` refused without a hardware path | **verified** |
| honest `os` is not stamped `simule: true` | **verified** |
| JSON card is not a QUANTUM seal | **verified** |
| webcam / IBM Job / IonQ / software BB84 as qrng or qkd | **refused** |
| QUANTUM signature | **later** — keys off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| `os` → `quantique` | **refused** — phone entropy stays classique |

## What v0 refuses

See [INTERDIT.md](INTERDIT.md). In short:

- se dire photon / IBM Job / IonQ sans preuve matérielle
- écrire `qrng` parce que le webcam a du bruit
- tamponner `simule: true` sur un `os` honnête
- un agent « quantum AI »
- un token, un L1, un cloud QUELLE
- frapper `quantique` sur cette rail

Mentir est le seul bug.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |
| [MODE](https://github.com/carllaliberte/mode-protocol) | le collapse des quatre |

`unforge-check` peut *lire* une carte QUELLE (`--quelle`). Il ne signe pas.  
MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`JUGE.md`](JUGE.md) — cette rail nomme la source, ne frappe pas `quantique`
- [`schema/carte.v0.json`](schema/carte.v0.json)
- [`quelle.py`](quelle.py) — `python3 quelle.py tirer` / `lire`
- [`examples/os-32.quelle.json`](examples/os-32.quelle.json) — téléphone sans dongle
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
