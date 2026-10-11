// Islands Free: the Islands art on a board with no walls. The three far regions become tiles like the rest and the
// whole map spreads out and settles like soft bubbles; links may cross, nothing is held in place. Same renderer as
// Islands (board/island.js), another configuration. The numbers start from the dev-panel values (home and bridge
// springs 0, damping .53, swing .38, link pull .065) and were tuned over every level and screen size with
// tools/free_check.js: bubble push 2.5 (settles in ~270 steps instead of ~600), bubble size 1.15 (a hexagonal packing
// that fills about the whole island; the layout settles offline before the first frame, so the island opens at rest).
FTH_SKINS.register(FTH_SKINS.extend('islands', {
  id: 'islands-free', name: 'Islands Free', ic: '🫧', blurb: 'no walls: tiles drift like bubbles',
  look: 'islands',                    // chrome CSS scope: the Islands rules apply as they are
  board: { free: true, guard: false, live: { kH: 0, kB: 0, damp: .53, cap: .38, rep: 5, fk: .065, fr: 2.5, fl: 1.15 } },
}));
