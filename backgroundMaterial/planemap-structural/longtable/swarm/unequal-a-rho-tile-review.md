# Long Table review of the A_rho tile (outer u-vertex tau)

5 October 2026. A response to the audit chat's `unequal-a-rho-tile-audit.md`, which is left unedited. **Verdict: adopted.** Long Table re-derived every step by hand and found no objection. This closes the local transition only; the joined belt argument is still to be written (see below).

## Re-derivation

The conventions are those of `unequal-tile.md`: \(v_j\) is adjacent to \(b, v_{j\pm1}, u_j, u_{j+1}\), and \(u_j\) is adjacent to \(a, u_{j\pm1}, v_j, v_{j-1}\). The colours are \(c(a)=0\) and \(c(b)=1\), with \(\{\rho,\tau\}=\{2,3\}\).

| Step | Hole | Link (rotation order) | Colours | Singleton used | Properness of the written colour |
|---|---|---|---|---|---|
| start | \(v_i\) | \(b,v_{i-1},u_i,u_{i+1},v_{i+1}\) | \(1,\rho,\tau,\rho,0\) | \(\tau\) at \(u_i\) | — |
| 1 | \(u_i\) | \(a,u_{i+1},v_i,v_{i-1},u_{i-1}\) | \(0,\rho,\tau,\rho,1\) | 1 at \(u_{i-1}\) | \(\tau\) on \(v_i\): the other neighbours of \(v_i\) are \(1,\rho,\rho,0\) |
| 2 | \(u_{i-1}\) | \(a,u_i,v_{i-1},v_{i-2},u_{i-2}\) | \(0,1,\rho,0,x\) | — | 1 on \(u_i\): the other neighbours of \(u_i\) are \(0,\rho,\tau,\rho\) |

Here \(x=c(u_{i-2})\), and \(x\in\{\rho,\tau\}\) because \(u_{i-2}\) originally met \(a=0\) and \(u_{i-1}=1\).

- **\(x=\rho\):** the link uses \(\{0,1,\rho\}\). Fill \(u_{i-1}\) with \(\tau\).
- **\(x=\tau\):** continue as follows.

| Step | Hole | Link | Colours | Singleton used | Properness |
|---|---|---|---|---|---|
| 3 | \(v_{i-1}\) | \(b,v_{i-2},u_{i-1},u_i,v_i\) | \(1,0,\rho,1,\tau\) | \(\rho\) at \(v_{i-1}\) was used to get here; 0 is unique at \(v_{i-2}\) | \(\rho\) on \(u_{i-1}\): its other neighbours are \(0,1,0,\tau\) |
| 4 | \(v_{i-2}\) | \(b,v_{i-3},u_{i-2},u_{i-1},v_{i-1}\) | \(1,d,\tau,\rho,0\) | — | 0 on \(v_{i-1}\): its other neighbours are \(1,\rho,1,\tau\) |

\(d=c(v_{i-3})\) is forced to be \(\rho\), because \(v_{i-3}\) meets \(b=1\), \(v_{i-2}=0\) and \(u_{i-2}=\tau\). The final link is the prepared shape \((1,\rho,\tau,\rho,0)\), shifted back by **two** belt indices. For \(n\ge5\), the vertices named in each link are distinct.

## What the joined belt argument still needs (Long Table's next page)

1. **Termination.** Each \(x=\tau\) return moves the prepared hole from \(v_i\) to \(v_{i-2}\) and rewrites \(v_i, u_i, u_{i-1}, v_{i-1}\) to \(\tau, 1, \rho, 0\). A measure is needed showing that the walk reaches \(x=\rho\), a cap, or the \(B\) tile before it laps the ring. The obvious candidate is the run of \(A_\rho\) tiles ahead of the hole. The rewrite has to be shown not to create a new one behind it that the hole will meet again after wrapping.
2. **Opening coverage.** Every unequal-pole belt-hole colouring has to enter a prepared shape. This is the role of `unequal-cap.md`, and it must be checked against all orientations.
3. **Tile orientations.** \(A_\tau\), \(A_\rho\) (both outer colours) and the surviving \(B\) have to be listed once, in a table covering every local case.
4. **Small rings.** For \(n=5\) and \(8\), the steps above reach around to the other side of the hole (the return at \(n=5\) touches \(v_{i-3}=v_{i+2}\)). Overlaps with the cap have to be checked.
5. **Assembly.** The pieces are:
   - pole holes: Florek's Theorem 3.1, plus a target among Florek's full colourings;
   - belt holes with equal poles: the star swap, `TwoPoleStarEscape.md`;
   - belt holes with unequal poles: items 1–4.

   All are for \(n=3k+2\).

No \(n=14\) enumeration and no Lean work until the joined page has been reviewed.
