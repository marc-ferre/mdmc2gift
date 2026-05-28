# mdmc2gift

[![Tests](https://github.com/marc-ferre/mdmc2gift/actions/workflows/ci.yml/badge.svg)](https://github.com/marc-ferre/mdmc2gift/actions)
[![License](https://img.shields.io/badge/license-CeCILL%20v2.1-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-yellow.svg)](https://www.python.org/)
[![Pandoc](https://img.shields.io/badge/pandoc-1.12%2B-orange.svg)](https://pandoc.org/)

Convertisseur de fichiers `.mdmc` vers le format GIFT de Moodle.

Le script principal s'appelle `mdmc2gift` et produit un fichier `.gift` directement importable dans Moodle.

## Fonctionnalités

- Conversion `.mdmc` vers GIFT avec questions à choix multiples.
- Compatibilité avec le format Markdown simple utilisé par l’écosystème `mdmc2*`.
- Compatibilité avec l’ancien format AMC `questionmult` / `reponses`.
- Échappement des caractères spéciaux GIFT les plus sensibles.
- Normalisation via Pandoc quand il est disponible.

## Prérequis

- Python 3.10 ou supérieur.
- Pandoc 1.12 ou supérieur, recommandé pour obtenir un rendu plus fidèle des fragments Markdown et LaTeX.

Le script fonctionne aussi sans Pandoc, avec une conversion plus simple.

## Installation

### Utilisation directe

```bash
python3 mdmc2gift mon_qcm.mdmc
```

### Utilisation sur l'entrée standard

```bash
cat mon_qcm.mdmc | python3 mdmc2gift > mon_qcm.gift
```

### Rendu exécutable

```bash
chmod +x mdmc2gift
./mdmc2gift mon_qcm.mdmc
```

## Format attendu

Le format de base reprend les questions déjà utilisées par les autres convertisseurs du même ensemble :

```markdown
## [Q1]
### Quelle est la capitale de la France ?
+ Paris
- Lyon
- Marseille
- Toulouse

## [Q2]
### 2 + 2 = ?
+ 4
- 3
- 5
- 6
```

L’ancien format AMC est également accepté :

```latex
\begin{questionmult}{Capitales}
Quelle est la capitale de la France ?
\begin{reponses}
\bonne{Paris}
\mauvaise{Lyon}
\end{reponses}
\end{questionmult}
```

## Sortie générée

Chaque question est écrite au format GIFT avec une syntaxe du type :

```gift
::Q1:: Quelle est la capitale de la France ? {
=Paris
~Lyon
~Marseille
~Toulouse
}
```

Le fichier de sortie est créé avec la même base de nom que le fichier d’entrée et l’extension `.gift`.

## Tests

```bash
python3 tests/test_mdmc2gift.py
```

Le dépôt contient aussi un exemple minimal dans `examples/sample_valid.mdmc`.

## Dépôt GitHub

Le dépôt public est disponible sur GitHub et suit le même esprit que les convertisseurs voisins `mdmc2docx` et `mdmc2latex`.
