// Islands 3D: the Islands art as a three.js scene you can tilt and spin (lab/islands3d.html, built on lab/core.js). It
// builds its layout from the level's graph, so every level plays; without WebGL it posts an error and the shell
// plays the level on the island board instead.
FTH_SKINS.register(FTH_SKINS.extend('islands', {
  id: 'islands-3d', name: 'Islands 3D', ic: '🧊', blurb: 'tilt and spin a floating island',
  look: 'islands',
  src: 'lab/islands3d.html',
  board: null,
}));
