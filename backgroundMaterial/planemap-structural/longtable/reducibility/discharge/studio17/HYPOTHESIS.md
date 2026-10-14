# Job 17 pre-registration (written 2026-10-14 15:52 MDT, before the census)

- **H17:** every 5-wheel whose link has no vertex of degree >= 7 is D- or C-reducible. Here C means: some contraction
  X, |X| <= 4, admissible under Gonthier's valid_contract as translated in studio15/cfast.cpp, leaves no unreached ring
  class extendable.
- **Kill:** any such wheel that is neither D- nor C-reducible.
- **Controls:**
  - 2.126 and 122.126 must come out C (they are RSST's own contracts);
  - the 66667 5-wheel must come out neither;
  - the 666666 6-wheel is recorded as "not C under contraction <= 6"; Franklin's reduction identifies ring
    vertices and is out of scope.
- **Scope:** 5-wheels over {5,6,7,8}^5 and 6-wheels over {5,6,7}^6, up to rotation and reflection, ring <= 16 (216 wheels).
