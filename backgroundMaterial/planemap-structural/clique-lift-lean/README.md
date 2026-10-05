# Clique-component and protected filling-path composition

Math canonical sources mirror the live Lean checkout. The whole-component theorem allows the hole on the separator; the filling-path theorem requires every side hole strictly interior and preserves this invariant at every global intermediate state. No planarity, finiteness, degree or palette-size assumption is made. `SideKempeStep` explicitly excludes artificial exterior isolates from the ambient spanning side graph.

A first fresh audit rebuilt the accepted 95 sources plus `VacancyCliqueLift` and its test (97 sources). A second rebuilt those plus `VacancyProtectedLift` and its test (99). Exact source hashes, source stability, search paths and module lists are in audit97/audit99. Both exclude cached custom artifacts. Exact standard-axiom guards and printed statements are in the corresponding MathlibTest logs.

Rebuild scripts are `longtable/audit/clique_lift_source_audit.py` and `protected_lift_source_audit.py`; use matching baseline source versions and fresh ROOT folders. Snapshots are committed here; original baseline snapshots are in the short-fill, three-move and belt artifact directories. ARTIFACT-SHA256SUMS binds this package and the associated reports/messages from repository root.

The topology establishing a spherical separator, legal-fan transfer, and VH_C reduction are accepted hand arguments, not part of the new compiled theorem. VH_C and VH∃ remain open.
