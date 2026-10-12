# Frozen link patterns

**NOT FORCED.** No multiplicity pattern of a frozen link forces an unlocking Kempe swap. For every proper colouring of a cycle of length \(d\ge 8\) that uses all four colours at least twice, the sorted multiplicities admit some proper colouring of that same sorted type, and some planar extension of it, in which every Kempe component that meets the link leaves every link colour with multiplicity at least \(2\). The \(21\)-vertex link is one such colouring, not a type: the same cyclic word has a chordal extension that stays frozen, so the obstruction in the witness lives in the interior.

An arrangement can still force the swap. The repetition \((0,1,2,3,0,1,2,3)\) does, by a separation argument that uses only the cycle. It has multiplicities \((2,2,2,2)\), and a second colouring of that same multiplicity stays frozen. The positive case is an arrangement, not a multiplicity pattern.

## What is being tested

Colours are \(\{0,1,2,3\}\). A link of length \(d\) is frozen when its colouring is proper, every colour appears at least twice, and therefore the deleted vertex neither fills nor slides. For \(d\le 7\) this is impossible: a proper colouring that uses all four colours has at least \(8-d\) colours appearing once. The patterns below are the other side of that count.

A multiplicity pattern is a sorted tuple \(m_1\ge m_2\ge m_3\ge m_4\ge 2\) with \(m_1+m_2+m_3+m_4=d\) and \(m_1\le m_2+m_3+m_4\). The inequality is exactly the condition under which some proper colouring of a \(d\)-cycle realises those counts. If the largest part exceeds the sum of the other three, two vertices of that colour are adjacent and the colouring is not proper.

A Kempe component of colours \(\{a,b\}\) meets the link in some of the link vertices of those colours. If it contains \(n_a\) link vertices of colour \(a\) and \(n_b\) of colour \(b\), the swap changes only those two link counts:
\[
m_a' = m_a-n_a+n_b, \qquad m_b' = m_b-n_b+n_a.
\]
The other two counts stay. The swap makes a link colour unique precisely when \(m_a'=1\) or \(m_b'=1\). It leaves the link frozen when both new counts are at least \(2\). A global exchange, \(n_a=m_a\) and \(n_b=m_b\), only swaps the two multiplicities, so a frozen link stays frozen.

On the cycle itself the \(\{a,b\}\) vertices form alternating paths, the boundary chains, separated by the other two colours. A chain is one component until the interior joins chains. Joins of a complementary pair cannot cross. The interior is otherwise unknown: an extension may add vertices and edges inside the cycle, and it may add none.

## Arrangements the cycle does force

The colouring \((0,1,2,3,0,1,2,3)\) has multiplicities \((2,2,2,2)\). For the complementary pairs \(\{0,2\}\) and \(\{1,3\}\) every boundary chain is a single vertex, in the order
\[
0,\;1,\;2,\;3,\;0,\;1,\;2,\;3.
\]
Both colours of either pair have multiplicity \(2\), so a component is safe only when its link footprint is balanced: equally many of each colour. The safe partitions of the four \(\{0,2\}\) vertices are one component of type \((2,2)\), or two components of type \((1,1)\).

One component containing every \(\{0,2\}\) vertex separates the four \(\{1,3\}\) vertices from each other. Each of those is a singleton of a colour of multiplicity \(2\), and swapping it leaves that colour once.

Two balanced components are a non-crossing pairing of the cyclic word \(0,2,0,2\). Each pair occupies adjacent positions in that word, so the arc between them contains exactly one \(\{1,3\}\) vertex. Any interior \(\{0,2\}\) path realising the pair separates that vertex from the other three. Its \(\{1,3\}\) component is a singleton, and the swap leaves a unique colour. The other adjacent pairing isolates one of the remaining two. The diameter pairing joins colour to the same colour, so it is not balanced, and the two diameters cross.

Every planar extension therefore has a Kempe component whose swap makes a link colour unique. The same holds, by the same separation, for any colouring obtained from this one by rotating the colours.

This does not make the multiplicity \((2,2,2,2)\) a forcing pattern. The next section gives another colouring with the same counts that stays frozen.

## Multiplicities at least \(3\)

Suppose every multiplicity is at least \(3\). Colour the cycle and add nothing inside it. The Kempe components that meet the link are the boundary chains. An alternating chain has footprint differing by at most one, so the swap changes each of the two counts by at most one. Each new count is therefore at least \(m-1\ge 2\). No link colour becomes unique.

So every arrangement with all four multiplicities at least \(3\), and not merely some arrangement of that pattern, has a freezing extension. The extension is the cycle alone. Patterns with \(m_4\ge 3\) are not forcing.

## A frozen extension of multiplicities \((2,2,2,2)\)

Let the link, in order, with positions numbered from \(0\), be
\[
(0,1,2,0,3,2,1,3).
\]
Each colour appears twice. Add four interior vertices, in this order, each into the interior face that still contains its neighbours:

| Vertex | Colour | Adjacent to |
| --- | --- | --- |
| \(X\) | \(0\) | positions \(5\) and \(6\) |
| \(Y\) | \(2\) | positions \(7\) and \(0\), and to \(X\) |
| \(A\) | \(3\) | positions \(1\) and \(2\), and to \(Y\) |
| \(Z\) | \(1\) | positions \(3\) and \(4\), and to \(X\) and \(A\) |

Reading the link from position \(0\), the link neighbours are coloured \(2,1\), then \(3,0\), then \(1,2\), then \(0,3\). Each new vertex is placed in a face whose walk already contains every listed neighbour, so the edges do not cross. The resulting components that meet the link, and the counts after the swap, are:

| Pair | Link vertices in each component | Counts after the swap |
| --- | --- | --- |
| \(\{0,1\}\) | \(\{0,1\}\) and \(\{3,6\}\) | \((2,2)\) and \((2,2)\) |
| \(\{0,2\}\) | \(\{0,5\}\) and \(\{2,3\}\) | \((2,2)\) and \((2,2)\) |
| \(\{0,3\}\) | \(\{0,7\}\) and \(\{3,4\}\) | \((2,2)\) and \((2,2)\) |
| \(\{1,2\}\) | \(\{1,2\}\) and \(\{5,6\}\) | \((2,2)\) and \((2,2)\) |
| \(\{1,3\}\) | \(\{1,4\}\) and \(\{6,7\}\) | \((2,2)\) and \((2,2)\) |
| \(\{2,3\}\) | \(\{2,7\}\) and \(\{4,5\}\) | \((2,2)\) and \((2,2)\) |

Every swap preserves both multiplicities. This kills \((2,2,2,2)\) as a forcing pattern: the repetition forces, and this second colouring of the same multiplicities does not.

## Two operations that keep a frozen disk frozen

Both operations edit the boundary and keep the colouring proper and planar.

**Paired expansion.** On a boundary edge \(uv\) with colours \(a\) and \(b\), replace the edge by the path \(u,x,y,v\) with \(x\) coloured \(b\) and \(y\) coloured \(a\). The new vertices lie on the \(\{a,b\}\) path through \(u\) and \(v\), so that component gains one \(a\) and one \(b\). Both of its updated counts increase by one. Every other \(\{a,b\}\) component is unchanged while the two multiplicities increase by one, so its updated counts also increase by one. For a third colour \(p\), the new vertex of colour \(a\) has both neighbours coloured \(b\), so it is a singleton of the pair \(\{a,p\}\). Swapping it leaves colour \(a\) with its old multiplicity, which is at least \(2\), and increases the multiplicity of \(p\). The same holds for the new vertex of colour \(b\). The two colours outside \(\{a,b\}\) are untouched. The link stays frozen.

**Heavy insertion.** Suppose colour \(c\) already appears at least three times, and \(uv\) is a boundary edge whose colours are not \(c\). Put a new boundary vertex \(w\) coloured \(c\) between \(u\) and \(v\), and keep the edge \(uv\) as a chord of the triangle \(uvw\). Pairs that do not use \(c\) are unchanged. In the pair \(\{c,a\}\), where \(a\) is the colour of \(u\), the vertex \(w\) joins the component of \(u\) and contributes one extra \(c\). The updated count of \(c\) on that component equals the old updated count, and the updated count of \(a\) increases by one. The same holds for the colour of \(v\). Against the fourth colour, \(w\) is a singleton: the swap leaves colour \(c\) with its old multiplicity, at least \(3\). The link stays frozen.

As long as a colour appears strictly fewer times than the sum of the other three, some boundary edge avoids it, so heavy insertion can still be applied. A proper cycle always has such an edge under that inequality, and both operations preserve properness.

## Every pattern with a \(2\) has a freezing extension

The seed of the previous section realises \((2,2,2,2)\), and every colour pair appears on its boundary. Paired expansion on a pair keeps a boundary edge of that same pair.

The \(21\)-vertex link realises \((3,2,2,2)\). In cyclic order it is
\[
(0,2,3,0,1,2,0,3,1).
\]
Colour \(0\) appears three times and the others twice. The six chords
\[
0\!-\!4,\ 0\!-\!5,\ 1\!-\!4,\ 2\!-\!4,\ 5\!-\!7,\ 5\!-\!8,
\]
with vertices numbered from \(0\), are non-crossing and together with the cycle give \(15\) edges, so they triangulate the \(9\)-gon. The components that meet the link are:

| Pair | Link footprints \((n_a,n_b)\) | Counts after each swap |
| --- | --- | --- |
| \(\{0,1\}\) | \((2,2),\ (1,0)\) | \((3,2),\ (2,3)\) |
| \(\{0,2\}\) | \((2,2),\ (1,0)\) | \((3,2),\ (2,3)\) |
| \(\{0,3\}\) | \((1,0),\ (1,1),\ (1,1)\) | \((2,3),\ (3,2),\ (3,2)\) |
| \(\{1,2\}\) | \((2,2)\) | \((2,2)\) |
| \(\{1,3\}\) | \((1,1),\ (1,1)\) | \((2,2),\ (2,2)\) |
| \(\{2,3\}\) | \((1,1),\ (1,1)\) | \((2,2),\ (2,2)\) |

No swap makes a count of \(1\). This is a second abstract colouring of the same link. The witness interior is one frozen extension; the chords are another. Neither is forced by the cyclic word, and the multiplicity \((3,2,2,2)\) is not a forcing type.

From this chordal disk, heavy insertion on colour \(0\) can be repeated while that colour appears at most five times. The three edges among colours \(1,2,3\) supply the insertions. The resulting links realise every tuple \((k,2,2,2)\) with \(3\le k\le 6\). For \(k>6\) the tuple is not a pattern: colour \(0\) would exceed the sum of the other three.

The remaining patterns are reached as follows.

- Two parts equal to \(2\), and the other two at least \(3\). Expand the seed once on the pair of colours that should grow. Both of those colours then appear three times. Heavy insertion raises either of them. While a coordinate is still below a realisable target, some coordinate that still needs to grow is strictly below the sum of the others, so the insertion applies.
- One part equal to \(2\), and the other three at least \(3\). On the chordal link, expand the boundary edge joining the two colours among \(\{1,2,3\}\) that should become heavy. All three edges \(1\!-\!2\), \(2\!-\!3\) and \(3\!-\!1\) occur. The result is some labelling of \((3,3,3,2)\). Heavy insertion then raises the three colours that are already at least \(3\).

Every pattern with a part equal to \(2\) therefore has a freezing planar extension. Together with the chordless case, no multiplicity pattern forces an unlocking swap.

## What this does not say

The separation argument still stands for \((0,1,2,3,0,1,2,3)\). A frozen link of multiplicity \((2,2,2,2)\) may or may not unlock, according to the circular word. The same is true of \((3,2,2,2)\): the chordal \(9\)-gon stays frozen, and other words of those counts have a complementary matching with no safe non-crossing partition. The test that sees the difference is the footprint of the chains after every non-crossing join, not the sorted tuple.

The \(21\)-vertex colouring is one interior whose footprints all stay at least \(2\). It is not the only one, and it is not determined by the link.

Feasibility of classifying frozen links by multiplicity: **Low**.

## Next step

On a frozen link, record the boundary chains of each complementary matching and test whether any non-crossing join leaves a footprint with a new count of \(1\). That is a property of the circular word. Use it on the chordal \(9\)-gon and on the witness interior separately: both pass, so a descent from the witness has to leave this link, not unlock it in place.
