# Rendered Rants — Bible

James's video diary. Each episode is one short monologue (under five minutes)
that James films himself: hand-held selfie close-ups walking down the street,
the phone propped up at home, or on the dash mount in his estate car. The words
are James's own, kept as close to verbatim as the TTS allows.

## Look
**This is the house style for all of James's personal vlog-style cartoons** (set by
Digital Estates, Nov 2026). Every episode, and any vlog brought in from elsewhere, is
drawn and framed this way; the series is still called "the stand-up".

- Faceted low-poly flat art (the `geometric` puppet style in `show/skeleton.yaml`):
  angular shapes, flat shading in two or three tones per surface, realistic
  proportions. Portrait 720x1280 (filmed upright on a phone; `format: portrait`
  in series.yaml), 30 fps.
- Locations are drawn by `art/make_vlog.py` (Digital Estates) and `art/make_rooms.py`
  (ep02, ep03), helpers in `art/lowpoly.py`: faceted fills, flat two- or three-tone
  shading, no outlines, detail kept at the sides and top where his head isn't.
- One voice to camera wherever possible. Other people are heard on a phone (`phone`
  state, `hold: { l: phone }`, the caller off frame at `x: -900`) or seen small behind
  James (the passers-by, the impound attendant), never in a two-shot.
- Every episode ends on a held reaction, then a 0.7 s `black` blackout before the end card.
- Framing: close (`x: 360, y: 1840, scale: 1.6`, head and shoulders, eyes at
  about y 520); in the car `x: 240, y: 1760, scale: 1.5`. Tighter shots are a
  scene `zoom: 1.3`, emphasis a line `zoom:` (the whole frame scales about his
  face, never the cast's scale). Walking shots use `[walk, blink, selfie]`
  (gestures with the left hand); propped-phone shots use `[idle, blink]`.

## Characters
- **Pat**, **Dev**, **Maggie**: non-speaking passers-by on the high street (Pat: long red hair, mustard jumper; Dev: crop, beard, green tee; Maggie: grey bun, glasses, plum cardigan). On the far pavement at `y: 712, scale: 0.23, depth: -3`, crossing with `walk_to`.
- **James in the bath** (`james_bath`): the same James, bare shoulders, sunk to `y: 1960` behind the `bath_tub` foam. Same voice.
- **James**: the vlogger. Dry, warm, quietly exasperated by modern life; tells stories about his mate Tom. Dark navy zip jacket, blue dotted shirt, jeans, spiky brown hair. Body: adult. Voice: Algieba.

## Locations (backdrops)
- **street**: terraced street, walking towards camera (depth backdrop: `motion: { type: recede, speed: 0.6, period: 2.0 }`). The houses are drawn self-similar, so the base zoom-loops seamlessly (`zoom` in backdrop.json), and lampposts, trees, bins and parked cars are sprites with `sync: true`, so everything at one depth moves at one speed.
- **high_street**: James stands on the near pavement; behind him the road, the far pavement and the shops across it: Pemberton & Gall solicitors, Fone Doctor (phone unlocking), Spin Cycle records. Static (no scroll). Scene `depth: { y: 0, scale: 0 }`; passers-by on depth -3, traffic on the far lane (`y: 790`, scale 0.9, depth -2, driving right) and near lane (`y: 872`, scale 1.0, depth -1, driving left), as `move:` set pieces.
- **black**: plain black, for the blackout before the end card.
- **lounge**: James's sofa in front of the vinyl shelves and turntable, window on the right.
- **bath**: tiles, frosted window, striped towel, candles and a rubber duck; with `bath_tub` in front. Phone propped on the edge (`sway: 0.25`).
- **corridor**: the office corridor, walking towards camera (depth backdrop, zoom-looped like the street).
- **office**: behind his desk: city window, pinboard, plant, the clock at half past four. With `monitor` (x 580, y 960, scale 0.8) and `desk_edge`; James at x 300.
- **kitchen**: green cupboards, metro tiles, window, the red kettle steaming on the right (James at x 330).
- **gaming_den**: night, purple LED strip, rocket poster, the red gaming chair behind him; `game_screen` at x 590, y 780, scale 0.75, James at x 300.
- **home_street**: outside number 27 from the road: red brick, bay window, blue door, hedge, wheelie bin. James at `x: 200, scale: 1.45` with `old_estate` behind him (x 480, y 1110, scale 1.3), or `broken_glass` where it was.
- **industrial_road**: the grey road out to the impound lot, chain-link fence and warehouses (depth backdrop, zoom-looped).
- **impound_hatch**: the portakabin, VEHICLE RELEASE sign, opening hours (£125 a night), the hatch on the right.
- **car**: the estate car from the dash mount, right-hand drive: James in the driver's seat on screen-left, the empty passenger seat on screen-right, in one-point perspective down the cabin; crates of records in the boot against the tailgate, rear headrests folded.

## Set pieces
- **hatch_red_l/_r**, **estate_blue_l/_r**, **van_white_l/_r**: cars side-on, driving left / right, for passing traffic on the high street.

- **monitor** (writable: `writing:` rows are the email), **desk_edge** (front), **game_screen**, **bath_tub** (front), **old_estate** (James's car side-on: bin bag on the front window, fingerprint powder), **broken_glass**, **hatch_counter** (front, card machine showing £500).

## Props

## Running gags
- Granddad's 400 vinyl records and the three trips in the estate car.
- James's car is a battered old estate, his "faithful runaround" (ep03: stolen, impounded, returned with a bin bag on the window and fingerprint powder that does not come off).
- The AI agent is never seen or heard: James talks about it, and it quietly gets on with it.
- Tom, the well-meaning, highly efficient executor who makes everything worse.
