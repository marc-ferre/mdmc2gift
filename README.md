# mdmc2gift

Convertisseur de fichiers `.mdmc` vers le format GIFT de Moodle.

Le script principal s'appelle `mdmc2gift` et produit un fichier `.gift` prêt à importer dans Moodle.

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

Le script accepte aussi l'ancien format AMC inspiré de `questionmult`/`reponses`.

## Utilisation

```bash
python3 mdmc2gift mon_qcm.mdmc
```

Cela crée `mon_qcm.gift` dans le même dossier.

Pour écrire sur la sortie standard :

```bash
cat mon_qcm.mdmc | python3 mdmc2gift > mon_qcm.gift
```

## Dépendances

- Python 3.10+
- Pandoc, si vous voulez une normalisation plus fidèle des fragments Markdown/LaTeX. Le script fonctionne aussi sans Pandoc, en mode dégradé.

## Tests

```bash
python3 tests/test_mdmc2gift.py
```
