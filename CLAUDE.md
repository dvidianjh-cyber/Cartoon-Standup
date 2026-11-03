# Stand-Up

This repo is one cartoon series made with CartoonEngine. It holds everything
that belongs to the show; the engine that draws, voices and renders it lives
in a separate repo.

## Two repos, one rule

| Repo | What's in it | You may |
|---|---|---|
| `Cartoon-Standup` (this one) | bible, characters, backdrops, sets, props, episodes, renders | read, write, commit, push |
| `cartoonengine` (the engine), cloned next to this one at `../cartoonengine` | renderer, tools, action library, skills | **read and run only** |

Never edit, commit or push to the engine from this project, and never put
anything from this show into the engine repo. If the show needs an engine
change (a new action, outfit, hairstyle or tool fix), write a short
suggestion (what, why, which episode needs it) and give it to James for the
CartoonEngine project. Until it lands, rewrite around what the engine can do.

If the engine isn't at `../cartoonengine`, look for a sibling folder named
`cartoonengine` or `CartoonEngine`. If it isn't there either, stop and ask
for the `cartoonengine` repo to be attached to this project.

## Skills

The skills live in the engine. Before a task, read the one that fits:

- `../cartoonengine/.claude/skills/write-episode/SKILL.md`: a new episode or a rewrite
- `../cartoonengine/.claude/skills/stage-scenes/SKILL.md`: script.yaml, blocking, actions
- `../cartoonengine/.claude/skills/make-character/SKILL.md`: a new or changed character
- `../cartoonengine/.claude/skills/publish-render/SKILL.md`: upload a finished video to `renders/`

In the skills, `<show>` means this repo's `show/` folder and `$ENGINE` means
`../cartoonengine`.

## Layout

```
series.yaml            # marks this as a series repo
show/                  # what the engine reads (its public dir)
  bible.md             # premise, tone, cast, locations, running gags
  characters/<name>/   # look.yaml, puppet.svg, rig.json, voice.json
  backdrops/<name>/    # backdrop.svg (1280x720)
  sets/<piece>/        # piece.svg, piece.json
  props/<name>/        # prop.svg, prop.json
  titles/              # titles.yaml, intro.wav, outro.wav: title and end cards (tools/make_jingle.py)
  episodes/<ep>/       # script.md, script.yaml, timeline.json (audio/, lipsync/, out/ are gitignored)
renders/<ep>.mp4       # finished episodes, stored with Git LFS
out/                   # puppet and action sheets (gitignored)
```

## Running the tools

Run from this repo's top folder. `py` is the engine's Python:
`../cartoonengine/tools/bin/python/python.exe` on James's Windows PC, `python3`
elsewhere (after `pip install -r ../cartoonengine/requirements.txt`).

```
py ../cartoonengine/tools/validate_script.py show/episodes/ep02
py ../cartoonengine/tools/run_episode.py show/episodes/ep02 --no-render   # voices + timeline (needs GEMINI_API_KEY)
py ../cartoonengine/tools/still.py show/episodes/ep02 3.5 12              # PNG frames in show/episodes/ep02/out/
py ../cartoonengine/tools/run_episode.py show/episodes/ep02               # renders renders/ep02.mp4
py ../cartoonengine/tools/make_puppet.py show/characters/<name>
py ../cartoonengine/tools/sheet.py show/characters/<name> [--actions]     # out/<name>_sheet.png
```

## Renders and Git LFS

Finished videos go in `renders/` and are stored with Git LFS (Large File
Storage): GitHub keeps the video file separately and the repo keeps a small
pointer to it, so the repo stays fast. `.gitattributes` already sends
`renders/*.mp4` to LFS; after a one-time `git lfs install` on each computer,
you commit and push videos like any other file.

Re-rendering is free; only committed versions use GitHub's LFS allowance. So
commit an episode's render once it's final, not after every test render.

Claude's cloud sessions can't reach GitHub's LFS server, so episodes are
rendered and their videos pushed from a throwaway clone on James's PC
(`../cartoonengine/.claude/skills/publish-render/SKILL.md`), deleted afterwards.

## Git

This repo is Claude's to run; James steers what goes in it. Claude creates
the branches, commits, pushes, opens the PRs and merges them into `main`
itself when the work is right, without waiting for a review.

Each episode reaches `main` in exactly two commits, each a squash-merged PR:

1. **The script is locked.** The script is drafted with James in a doc, not
   in git. When he says it's final, one commit adds
   `show/episodes/<ep>/script.md` (the readable screenplay he agreed) and
   `show/episodes/<ep>/script.yaml` (the same words staged for the engine,
   validated, with `display_title:`), plus anything new made for them
   (characters, props, sets, backdrops, bible lines).
2. **The render is final.** Rendered from `main` on a branch cut after the
   script commit, one commit adds `renders/<ep>.mp4`, `timeline.json` and
   any `script.yaml` fixes from the render loop. If a fix changes the spoken
   words, `script.md` changes to match in the same commit.

Test renders, re-voicing and still checks are not committed. Always
squash-merge episode PRs. Ask James first only before a step that can't be
undone: a force-push, rewriting `main`, deleting a branch with unmerged
work, or deleting LFS files on GitHub.
