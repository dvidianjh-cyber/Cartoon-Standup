# Rendered Rants — Bible

James's video diary. Each episode is one short monologue (under five minutes)
that James films himself: hand-held selfie close-ups walking down the street,
the phone propped up at home, or on the dash mount in his estate car. The words
are James's own, kept as close to verbatim as the TTS allows.

## Look
- Faceted low-poly flat art (the `geometric` puppet style in `show/skeleton.yaml`):
  angular shapes, flat shading in two or three tones per surface, realistic
  proportions. 1280x720, 30 fps.
- Locations are drawn by `art/make_vlog.py` (helpers in `art/lowpoly.py`).
- Framings: close (`y: 1418, scale: 1.4`, head and shoulders) and extreme
  close (`y: 1825, scale: 1.85`). Walking shots use `[walk, blink, selfie]`
  (gestures with the left hand); propped-phone shots use `[idle, blink]`.

## Characters
- **James**: the vlogger. Dry, warm, quietly exasperated by modern life; tells stories about his mate Tom. Dark navy zip jacket, blue dotted shirt, jeans, spiky brown hair. Body: adult. Voice: Algieba.

## Locations (backdrops)
- **street**: terraced street, walking towards camera (depth backdrop: `motion: { type: recede, speed: 0.6, period: 2.0 }`). The houses are drawn self-similar, so the base zoom-loops seamlessly (`zoom` in backdrop.json) while lampposts, trees, bins and parked cars go by as sprites.
- **high_street**: shop fronts side-on for `scroll` (about 110): Fone Doctor (phone unlocking), The Daily Grind café, Pemberton & Gall solicitors, Spin Cycle records.
- **lounge**: James's sofa in front of the vinyl shelves and turntable, window on the right.
- **car**: the estate car from the dash mount, in one-point perspective down the cabin; crates of records in the boot against the tailgate, rear headrests folded.

## Set pieces

## Props

## Running gags
- Granddad's 400 vinyl records and the three trips in the estate car.
- Tom, the well-meaning, highly efficient executor who makes everything worse.
