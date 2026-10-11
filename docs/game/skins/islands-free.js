// Islands Free: the Islands art on a board with no walls. The three far regions become tiles like the rest and the
// whole map spreads out and settles like soft bubbles; links may cross, nothing is held in place. Same renderer as
// Islands (board/island.js), another configuration. Numbers tuned over every level with tools/free_check.js.
FTH_SKINS.register(FTH_SKINS.extend('islands', {
  id: 'islands-free', name: 'Islands Free', ic: '🫧', blurb: 'no walls: tiles drift like bubbles',
  look: 'islands',                    // chrome CSS scope: the Islands rules apply as they are
  board: { free: true, guard: false, live: { kH: 0, kB: 0, damp: .53, cap: .38, rep: 5, fk: .065, fr: 1.55, fl: 1.08 } },
}));
