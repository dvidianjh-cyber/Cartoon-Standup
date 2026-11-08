# Rendered Rants — Bible

James's video diary. Each episode is one short monologue (under five minutes)
that James films himself: hand-held selfie close-ups walking down the street,
the phone propped up at home, or on the dash mount in his estate car. The words
are James's own, kept as close to verbatim as the TTS allows.

## Look
- Faceted low-poly flat art (the `geometric` puppet style in `show/skeleton.yaml`):
  angular shapes, flat shading in two or three tones per surface, realistic
  proportions. Portrait 720x1280 (filmed upright on a phone; `format: portrait`
  in series.yaml), 30 fps.
- Locations are drawn by `art/make_vlog.py` (helpers in `art/lowpoly.py`).
- Framing: close (`x: 360, y: 1840, scale: 1.6`, head and shoulders, eyes at
  about y 520); in the car `x: 240, y: 1760, scale: 1.5`. Tighter shots are a
  scene `zoom: 1.3`, emphasis a line `zoom:` (the whole frame scales about his
  face, never the cast's scale). Walking shots use `[walk, blink, selfie]`
  (gestures with the left hand); propped-phone shots use `[idle, blink]`.

## Characters
- **Pat**, **Dev**, **Maggie**: non-speaking passers-by on the high street (Pat: long red hair, mustard jumper; Dev: crop, beard, green tee; Maggie: grey bun, glasses, plum cardigan). On the far pavement at `y: 712, scale: 0.23, depth: -3`, crossing with `walk_to`.
- **James**: the vlogger. Dry, warm, quietly exasperated by modern life; tells stories about his mate Tom. Dark navy zip jacket, blue dotted shirt, jeans, spiky brown hair. Body: adult. Voice: Algieba.

## Locations (backdrops)
- **street**: terraced street, walking towards camera (depth backdrop: `motion: { type: recede, speed: 0.6, period: 2.0 }`). The houses are drawn self-similar, so the base zoom-loops seamlessly (`zoom` in backdrop.json), and lampposts, trees, bins and parked cars are sprites with `sync: true`, so everything at one depth moves at one speed.
- **high_street**: James stands on the near pavement; behind him the road, the far pavement and the shops across it: Pemberton & Gall solicitors, Fone Doctor (phone unlocking), Spin Cycle records. Static (no scroll). Scene `depth: { y: 0, scale: 0 }`; passers-by on depth -3, traffic on the far lane (`y: 790`, scale 0.9, depth -2, driving right) and near lane (`y: 872`, scale 1.0, depth -1, driving left), as `move:` set pieces.
- **black**: plain black, for the blackout before the end card.
- **lounge**: James's sofa in front of the vinyl shelves and turntable, window on the right.
- **car**: the estate car from the dash mount, right-hand drive: James in the driver's seat on screen-left, the empty passenger seat on screen-right, in one-point perspective down the cabin; crates of records in the boot against the tailgate, rear headrests folded.

## Set pieces
- **hatch_red_l/_r**, **estate_blue_l/_r**, **van_white_l/_r**: cars side-on, driving left / right, for passing traffic on the high street.

## Props

## Running gags
- Granddad's 400 vinyl records and the three trips in the estate car.
- Tom, the well-meaning, highly efficient executor who makes everything worse.
