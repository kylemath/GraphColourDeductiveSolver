// 4square skin registry: each skins/<id>.js calls FTH_SKINS.register(spec). See SKIN-SPEC.md.
(function () {
  const list = [];
  window.FTH_SKINS = {
    list,
    register(spec) {
      if (!spec || !spec.id || !spec.name) throw new Error('skin spec needs id and name');
      const i = list.findIndex(s => s.id === spec.id);
      if (i >= 0) list[i] = spec; else list.push(spec);
    },
    get(id) { return list.find(s => s.id === id) || list[0]; },
    // a skin derived from an already registered one: extend('islands', { id, name, ic, blurb, ... }). Plain-object fields
    // (theme, words, map, bonus, levelMap, title, board) are merged one level deep, everything else is replaced.
    extend(baseId, over) {
      const b = list.find(s => s.id === baseId); if (!b) throw new Error('extend: unknown skin ' + baseId);
      const out = Object.assign({}, b, over), plain = v => v && typeof v === 'object' && !Array.isArray(v);
      for (const k in over) if (plain(b[k]) && plain(over[k])) out[k] = Object.assign({}, b[k], over[k]);
      return out;
    },
  };
})();
