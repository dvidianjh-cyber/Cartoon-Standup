# Stand-Up — Bible

James does stand-up. Each episode is one short routine (under five minutes)
performed at the mic on a comedy club stage, cut between a wide, a medium and
a close shot. The words are James's own routine, kept as close to verbatim as
the TTS allows.

## Look
- Faceted low-poly flat art (the `geometric` puppet style in `show/skeleton.yaml`):
  angular shapes, flat shading in two or three tones per surface, realistic
  proportions. 1280x720, 30 fps.
- The stage is drawn once by `art/make_stage.py` and cropped into three
  framings, so every cut matches.

## Characters
- **James**: the comic. Dry, warm, quietly exasperated by modern life; tells stories about his mate Tom. Dark navy zip jacket, blue dotted shirt, jeans, spiky brown hair. Body: adult. Voice: Algieba.

## Locations (backdrops)
- **stage_wide / stage_mid / stage_close**: a small comedy club stage. Exposed
  brick wall lit by a spotlight, a pink and gold LIVE COMEDY neon sign, red
  curtains, a bar stool with a pint of water. The three are the same picture
  at zoom 1, 2 and 3. Where James stands in each is at the top of
  `art/make_stage.py` and in every episode's `script.yaml`.

## Set pieces
- **mic**: mic on a stand, drawn over James (`layer: front`). Same x and scale
  as James, `y` 20 puppet units below his feet.
- **audience**: front row of heads in silhouette; wide shot only, at (640, 720).

## Props

## Running gags
- Granddad's 400 vinyl records and the three trips in the estate car.
- Tom, the well-meaning, highly efficient executor who makes everything worse.
