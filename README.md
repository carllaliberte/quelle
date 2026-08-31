# QUELLE

**D'où vient ce bit.**

QUELLE est un certificat d'origine d'entropie. Un tirage porte une étiquette : `os`, `qrng` ou `qkd`. Si le matériel n'est pas là, l'étiquette dit `os`. Mentir est le seul bug.

Ce n'est pas UNFORGE (sceau de fichier).  
Ce n'est pas SITUS (droit sur un lieu).  
Ce n'est pas QUANTUM le nœud (sas local).  
Ce n'est pas un ordinateur quantique dans ta poche.

Open source MIT. Téléphone + Python. Zéro token.

## Primitive

```
source déclarée  +  octets  +  empreinte  →  carte .quelle.json
```

| Source | Quand tu as le droit de l'écrire |
|---|---|
| `os` | `secrets` / urandom. Toujours vrai sur un cellulaire. |
| `qrng` | Un QRNG USB/PCIe réel répond. Sinon : interdiction. |
| `qkd` | Une session QKD matérielle. Sinon : interdiction. |

`simule: true` sur tout protocole (BB84, CHSH) tourné en logiciel.

## v0 au cellulaire

```bash
python3 quelle.py tirer --octets 32
python3 quelle.py lire carte.quelle.json
```

Sans dongle : source = `os`. C'est correct. Ce n'est pas honteux.

## Ce que v0 refuse

- se dire photon / IBM Job / IonQ sans preuve matérielle
- un agent « quantum AI »
- un token, un L1, un cloud QUELLE
- écrire `qrng` parce que le webcam a du bruit (voir [INTERDIT.md](INTERDIT.md))

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |

`unforge-check` peut *lire* une carte QUELLE (`--quelle`). Il ne signe pas.  
MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe. Les clés restent hors Git.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`schema/carte.v0.json`](schema/carte.v0.json)
- [`quelle.py`](quelle.py) — tirer + lire
- [`examples/os-32.quelle.json`](examples/os-32.quelle.json)
