# Installation Guide

The skill is distributed as a directory (`cocos-creator-dev/`) containing `SKILL.md` and `references/`. `evals/` is development-only and is not installed.

## Prerequisites

- Node.js (for `npx skills`) **or** an agent that imports `.skill` files / reads skills from a directory
- Python 3.8+ only if you rebuild the archive with `package_skill.py`

## Method 1: `skills` CLI (recommended)

```bash
# Interactive: choose scope and agent(s)
npx skills add Dailiduzhou/cocos-creator-dev-skill

# Project scope, all detected agents, copy instead of symlink, no prompts
npx skills add Dailiduzhou/cocos-creator-dev-skill --skill cocos-creator-dev -a '*' --copy -y

# User scope (available in every project). Add -a <agent> to avoid copying into
# every agent directory the CLI detects.
npx skills add Dailiduzhou/cocos-creator-dev-skill -g -a pi -y

# List what the repository exposes without installing
npx skills add Dailiduzhou/cocos-creator-dev-skill --list
```

The skill is installed into the agent's skills directory, for example:

| Agent | Project path | Global path |
| --- | --- | --- |
| Codex, Pi, Cursor, Gemini CLI, Copilot | `.agents/skills/cocos-creator-dev` | `~/.agents/skills/cocos-creator-dev` |
| Claude Code | `.claude/skills/cocos-creator-dev` | `~/.claude/skills/cocos-creator-dev` |
| Others | see `npx skills add --help` / the skills README agent table | |

Update later with `npx skills update`; remove with `npx skills remove cocos-creator-dev`.

## Method 2: prebuilt archive

```bash
python package_skill.py     # rebuild cocos-creator-dev.skill from cocos-creator-dev/
unzip cocos-creator-dev.skill -d ~/.agents/skills/cocos-creator-dev
```

The archive is a plain zip whose root is `SKILL.md` plus `references/`; use it in environments that import `.skill` files or where you prefer to unzip manually.

`skills add` also installs the archive straight from a URL (the extension does not matter, the content is sniffed):

```bash
npx skills add https://raw.githubusercontent.com/Dailiduzhou/cocos-creator-dev-skill/main/cocos-creator-dev.skill -a pi -y
```

Use a tag or commit URL instead of `main` to pin a version.

## Method 3: from a clone (development)

```bash
git clone https://github.com/Dailiduzhou/cocos-creator-dev-skill
npx skills add ./cocos-creator-dev-skill/cocos-creator-dev --copy -y
```

Installing the repository root also works (`npx skills add ./cocos-creator-dev-skill`); discovery finds the single skill inside it.

## Versioned installs

Every `vX.Y.Z` tag is published as a GitHub release with `cocos-creator-dev.skill`, `cocos-creator-dev.zip` and `SHA256SUMS.txt`:

```bash
# whole skill directory at a tag
npx skills add https://github.com/Dailiduzhou/cocos-creator-dev-skill/tree/v1.2.0/cocos-creator-dev -a pi -y

# release archive by URL (zip sniffed, extension irrelevant)
npx skills add https://raw.githubusercontent.com/Dailiduzhou/cocos-creator-dev-skill/v1.2.0/cocos-creator-dev.skill -a pi -y

# verify a downloaded asset
sha256sum -c SHA256SUMS.txt
```

## Verification

```bash
npx skills ls                       # lists cocos-creator-dev and its source
ls .agents/skills/cocos-creator-dev # SKILL.md + references/, no evals/
```

Then ask the agent something that must load a reference, for example:

```
Creator 3.8 里两个面板共用一张头像，关闭一个后另一个变白，怎么修？
```

A working install answers with the shared-`SpriteFrame` ownership explanation and cites the bundled reference guidance. If the agent answers generically or invents APIs, confirm the skill directory is on the agent's skills path and that `SKILL.md` is readable.

## Maintenance

- Source of truth: `cocos-creator-dev/`. The `.skill` archive is generated and must be rebuilt after source changes.
- Evaluation fixtures: `evals/evals.json` (repo root) — never installed.
- `package_skill.py` excludes `evals/`, `__pycache__`, `.git` and `.DS_Store`; after packaging, verify with `diff -r` against the extracted archive.
