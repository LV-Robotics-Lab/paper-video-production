# Paper Video Production

A reusable Codex skill for creating and refining research videos from papers, slides, diagrams, and experiment footage. Instructions are written in Chinese; video language and style are chosen per project.

It covers narrative planning, narration and captions, continuous figure navigation, layered scientific animations, qualitative comparisons, and end-to-end delivery checks. It contains no paper-specific assets, model settings, project history, or fixed visual template.

## Install

Clone into your Codex skills directory, using the skill name as the folder name:

```bash
git clone https://github.com/LV-Robotics-Lab/paper-video-production.git ~/.codex/skills/paper-video-production
```

If that directory already exists, preserve and compare your local changes before replacing it. For a custom Codex home, use its `skills/` directory instead.

Invoke `$paper-video-production` with your paper, available assets, and desired output. The skill provides workflow guidance; rendering, voice generation, and hosting use the tools available in your environment.

## Contents

- [SKILL.md](SKILL.md): entry point and production workflow.
- [Audio and captions](references/audio-captions.md): narration alignment, terminology, subtitles, and mixing.
- [Motion](references/motion.md): continuous figure navigation and numerical chart animations.
- [Scientific diagrams](references/diagram-animation.md): faithful layered redraws and mechanism animations.
- [Qualitative comparisons](references/qualitative-comparisons.md): experimental conditions, synchronization, annotations, and layout changes.
- [Delivery](references/delivery.md): revision tracking, media checks, and authorized anonymous/public publishing.
- [Caption checker](scripts/check_captions.py): read-only validation of single-line SRT files.

## Caption checks

The checker requires Python 3. Font-width checks additionally require Pillow and the actual font used for rendering. Without a font, it checks structure and timing only.

```bash
python3 scripts/check_captions.py captions.srt --duration 180
python3 scripts/check_captions.py captions.srt --duration 180 \
  --font /path/to/font.ttf --font-size 34 --max-width 1500
```

It exits with status 1 for errors. Reading-speed warnings require review. These checks do not replace visual inspection or listening to the finished video.
