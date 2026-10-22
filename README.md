# WTL Championship 2026 Rulebook

Static site for the [We Teach League](https://weteachleague.com) WTL Championship 2026:

- **Rulebook** – transcribed from the [official Google Doc](https://docs.google.com/document/d/1Qu6pscRUl_iEMHQSeYPh40HkourK8NhKNg7LbW2ugCQ/edit?tab=t.0)
- **SLOPE Evaluations** – summary of [SLOPE.pdf](https://drive.google.com/file/d/1ss4DqESf0VN2vPcBvnPUsJRWD0nqzJhL/view) by WD Maverick
- **SLOPE Calculator** – a JavaScript port of the [Colab POC](https://colab.research.google.com/drive/115SeCJfrsuFeppZrprDW_tJcKFyIaOHo?usp=sharing), plus point values and a team TPE checker

## Editing

Edit `src/page.html`, then run `./build.sh` to regenerate `index.html` (the file GitHub Pages serves). No other build step or dependencies.

## Keeping it in sync

When WTL updates the rulebook doc, or WD Maverick sends a new calculator (save it as `temp/slope_calculator.html`), open Claude Code in this folder and ask it to re-review and update the page (or run `/update-rulebook`). The steps are in `.claude/skills/update-rulebook/SKILL.md`.

Manual checks:

```sh
scripts/fetch-doc.sh                  # download the doc and diff against sources/rulebook.txt (last synced)
python3 -I scripts/check-rules.py     # every rule ID in the doc is on the page, and none are stale
./build.sh && node scripts/check-calc.js   # formula and point values match the reference calculators
```
