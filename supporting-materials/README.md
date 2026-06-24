# Supporting Materials

Upload-ready files for the Sentient Foundation Open Source AGI Grant application.

Recommended upload:

1. `Open_Agent_Safety_Kit_Grant_Deck_Final.pdf` — polished grant deck (recommended)
2. `Open_Agent_Safety_Kit_Grant_Deck_Elegant.pdf` — backup deck
3. `Open_Agent_Safety_Kit_Grant_Deck.pdf` — simple backup deck
4. `Open_Agent_Safety_Kit_One_Pager.pdf` — optional short summary

The Markdown source docs remain in `docs/`, but the Typeform upload should use the PDF deck because reviewers expect a file, not only repository notes.

Regenerate locally:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install reportlab
python scripts/generate_supporting_materials.py
```
