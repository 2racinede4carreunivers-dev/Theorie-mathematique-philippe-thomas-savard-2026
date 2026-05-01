# Audio cache TTS (shimmer FR)

Ce dossier contient les **29 fichiers MP3** de narration audio pre-generes par
OpenAI TTS (modele `tts-1-hd`, voix `shimmer`, vitesse 0.95) via l'Emergent LLM
Key.

## Pourquoi commit ces MP3 dans le repo ?

Le workflow GitHub Actions `generate-animation.yml` et `generate-video.yml`
s'execute sur un compte Emergent **Free Tier** : l'Universal Key retourne
alors une erreur `403: Free users can only use Universal Key from within
Emergent platform.`

Pour contourner cette limite, la generation TTS est effectuee **localement** (ou
depuis l'environnement Emergent Pod) puis les MP3 sont commit dans ce dossier.
Le script `scripts/generate_animation.py` detecte automatiquement ce cache
et l'utilise **en priorite** avant tout appel a l'API TTS distante.

## Convention de nommage

```
scene_{NNN}_{HASH8}.mp3
```

Ou :
- `NNN` = numero de scene sur 3 chiffres (001 a 029)
- `HASH8` = 8 premiers caracteres du MD5 du texte narre
  (`hashlib.md5(text[:4000].encode()).hexdigest()[:8]`)

Si le texte narre d'une scene change dans `src/SCRIPT_NARRATIF_VP.md`, le hash
change : il faut alors regenerer localement puis re-commiter le nouveau MP3.

## Regeneration locale

```bash
export EMERGENT_LLM_KEY="sk-emergent-..."
export ENABLE_TTS=true
python3 scripts/generate_animation.py
cp animation_output/audio/*.mp3 assets/audio_cache/
```

## Taille

~94 MB total (29 fichiers, ~3 MB chacun).
