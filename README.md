# Kit vidéo biblique — « Enracinée avec Adeline Nana »

Ce dépôt contient un skill Claude Code qui monte les vidéos bibliques d'Adeline :
- tu donnes le texte, l'audio ElevenLabs (`.mp3`) et la vidéo HeyGen (`.mp4`) ;
- Claude propose un plan, puis une planche d'aperçu, puis rend la vidéo finale en 4K ;
- il ajoute les animations, les versets, les peintures, les sous-titres, le logo, la musique et les petits sons, et fait la miniature.

## Installation (une seule fois)

1. Installe [Claude Code](https://claude.com/claude-code) et connecte-toi.
2. Dans le Terminal :
   ```bash
   git clone https://github.com/jhmesseroux/bible-avatar-video-kit.git ~/bible-avatar-video-kit
   cd ~/bible-avatar-video-kit
   claude
   ```
3. Dis à Claude : **« installe tout pour commencer »**. Il lit `CLAUDE.md`, lance `./install.sh` et t'explique ce qu'il te reste à faire. C'est souvent seulement Google Chrome et la connexion à Codex pour les peintures.
4. Ferme puis relance Claude Code.

## Faire une vidéo

Dans Claude Code, tape :

```
/bible-avatar-video
texte : <ton texte>
audio : <chemin du .mp3>
vidéo : <chemin du .mp4>
```

Astuce : tu peux glisser les fichiers depuis le Finder dans le Terminal pour coller leur chemin.

Claude te montre d'abord le plan, puis les visuels. Il ne lance le rendu 4K que quand tu dis « go ». Pour la miniature, demande-lui « fais la miniature ».

## Mettre à jour

```bash
cd ~/bible-avatar-video-kit && git pull
```

Puis relance Claude Code.

## Contenu

- `skills/bible-avatar-video/` : le skill. Il contient la méthode (`SKILL.md`), le logo, les polices, les musiques, les sons, deux vidéos d'exemple et les scripts.
- `install.sh` : l'installation (outils, skill, skills HyperFrames).
- `CLAUDE.md` : les instructions que Claude lit en ouvrant ce dossier.

Les polices sont sous licence SIL Open Font License. La musique et les sons appartiennent à la chaîne. Ce dépôt est privé : ne le partage pas.
