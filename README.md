# Paper Video Production

A reusable Codex skill for creating and refining research videos from papers, slides, diagrams, and experiment footage. Instructions are written in Chinese; video language and style are chosen per project.

It covers evidence-linked storyboards, visual design constraints, narration cues and captions, continuous figure navigation, layered scientific animations, qualitative comparisons, render-and-review repair loops, verified project lessons, and end-to-end delivery checks. It contains no paper-specific assets, model settings, project history, or fixed visual template.

Rendering frameworks are selected per project. The skill incorporates methods from the ten projects and papers listed in [reviewed sources](references/rendering-backends.md#参考来源与采用边界); it does not install every framework or require every video to use all of them.

## Install

Clone into your Codex skills directory, using the skill name as the folder name:

```bash
git clone https://github.com/LV-Robotics-Lab/paper-video-production.git ~/.codex/skills/paper-video-production
```

If that directory already exists, preserve and compare your local changes before replacing it. For a custom Codex home, use its `skills/` directory instead.

Invoke `$paper-video-production` with your paper, available assets, and desired output. The skill provides workflow guidance; rendering, voice generation, and hosting use the tools available in your environment.

## Contents

- [SKILL.md](SKILL.md): entry point and production workflow.
- [Storyboard and design](references/storyboard-design.md): learning goals, evidence-linked shots, visual constraints, and representative renders.
- [Rendering backends](references/rendering-backends.md): task-based selection, compatibility checks, deterministic rendering, and reviewed sources.
- [Review and repair](references/review-loop.md): frame/object-specific feedback, bounded repairs, and verified project-level lessons.
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
