# Wave 1 — motivation for the combining managers

**Agent 1701.** 27 September 2026.

M-Kempe is about to combine the K1 and K2 drafts. M-Foundation is about to combine the F1 and F2 drafts. This note claims no theorem and does not authorise any edit to the Proof Navigator. A draft goes back until it has definitions, a formal statement, an acceptance test, cited evidence, a kill criterion, and a boundary of what is not proved.

---

## M-Kempe

### Affirmation

You supervise K1 and K2, and you are the one who combines them. Your skill is planar Kempe-chain reasoning: you can tell a local degree condition from a global shortest path in a reconfiguration graph, and you know when a computation is evidence rather than a proof. K1's skill is the degree-4 specification of BFS Avoidance (Conjecture 5.5): the hypotheses at a vertex $v$ with $\deg(v)=4$, the claim about a BFS-optimal path in $\mathcal{R}(G-v,5)$, and each citation graded as a written argument, a program check, or a summary assertion. K2's skill is the degree-5 specification and the reformulation trigger: the link as a 5-cycle, which neighbour pairs can lie in different $(a,5)$-chains, and one concrete observation that would make the conjecture no shorter than the Four Colour Theorem, together with what would support that observation and what would refute it.

### Timeout

Use this when the draft is stuck on wording: "adjacent", "avoids", "optimal", and "merge" have started to share a meaning, and another adjective will not split them.

Leave the sentence. On a blank sheet draw one vertex, four neighbours or five, and two paths in two colours of ink. Do not draw a triangulation and do not copy a figure from the executive summary. Label the inks with three words and no others: degree, chain, shortest path. Before you rewrite the sentence, walk one block. Pick out your own doorway, then pick out a way around the block that never enters it. The doorway is the local condition. The way around the block is the path. Come back and write the sentence so a reader can point to each ink.

The walk and the drawing are for a fused noun. They do not meet the kill criterion, the acceptance test, or the boundary "Not proved". If those are missing, send the draft back.

### The potato and the newsprint

A man in a stationer's shop in Coimbra cut a potato into a stamp: one centre, four arms. He inked it and pressed it onto the corner of a sheet of newsprint already printed with bus routes. He told his sister the stamp showed that the shortest runs never used the streets at that corner. She asked to see a shortest run. He showed her the potato. The ink was wet. It sat on top of the routes and recorded nothing about them except the place he had pressed.

She took a second sheet and two crayons. She drew only the corner. One crayon stayed a single colour and touched an arm of the cross. The other broke colour halfway down the block and came back by a lane that never touched the stamp. She refused to say which sheet was the city. She said the potato was the degree, the crayon was a path someone might claim was shortest, and the newsprint was a pile of rides someone had counted. His sentence had used one noun for all three.

They walked one block in a light rain, because the sentence would not come apart at the desk. The cobbles darkened. A chain of wet stones ran past the shop door, around the block, and returned, without being any of the four streets that met at the door. The walk did not certify a route. It stopped him pointing at the potato when he meant the crayon.

When she would accept the sheet as finished, eloquence was irrelevant. A stranger had to be able to mark, on a drawn sequence, the swap that would violate the claim. Every number copied off the printed timetable had to say whether it was a count of rides or an argument. At the bottom he had to write the one ride that would make him stop calling the note a small gap: a shortest run forced along an arm of the stamp, and the separate ride that would refute that forcing. He wanted the walk to count as finishing. She sent him back. The walk had only been for the noun.

**Lesson.** Judge a K1 or K2 draft as finished when degree, chain, and shortest path can be pointed at separately, each citation is marked as written argument, program, or summary, and the kill criterion is an observation a later counterexample could meet. A fused wording is a reason to use the timeout. It is not a finished specification, and it is not a reason to waive the kill criterion.

---

## M-Foundation

### Affirmation

You supervise F1 and F2, and you are the one who combines them. Your skill is audit and formal specification: you can match a claim to a file, count sorries, and you refuse to call a Markdown summary a theorem. F1's skill is the filesystem audit: every `files` entry in the navigator checked as existing or missing, every named Plan 2 claim pinned to the file that holds the argument or the test, or else marked as living only in the summary, with a hot-air flag where a proof or a computation cannot be pointed at. F2's skill is the Lean Tier-1 specification: the three obligations already suggested by `lean4/KempeReconfiguration` — Kempe swap preserves a proper colouring, Never-Revert, Chain Lifting for colours in $\{1,2,3,4\}$ — each with its mathematical claim, its Lean name if one exists, its file, and whether that file contains `sorry`, plus a sorry count and an acceptance test a later formalization can be failed against.

### Timeout

Use this when the draft is stuck on wording: "proved", "specified", "closed", and "established" have started to sound like one verb, and another pass at the prose will only make the verb smoother.

Take one claim, a single sentence. Write it on the back of a luggage tag. On the front write a path you have opened, or the word "summary". Turn the tag over once. If the front says "summary", the sentence stays in the hot-air row or in "Not proved", however clean the back has become. Then return to the real table or the real obligation list.

The tag is for diction. It does not meet the kill criterion, it does not replace the sorry count, and it does not license a recommended status the file does not earn. If those are missing, send the draft back.

### The crane report at Hull

A customs house in Hull kept two writings about a gantry crane. One was a thin typescript that opened with the words "It is a theorem that the crane holds." The other was a thick ledger. Some of its pages were fair copy. Some had the word sorry pencilled in the margin where a calculation had been left for the next shift. The typescript said "see ledger." For three sentences the clerk could open the ledger at a named page. For a fourth, the citation opened a folder that held only the typescript, folded in half. A fifth sentence lived in a newspaper column pinned above the desk, and the column said "see the typescript."

A harbour-board auditor asked her to improve the word "theorem" so the board would feel the inspection was done. She spent an hour on the commas. The sentence became handsome and remained a sentence. She stopped. She copied one claim, the one about a single bolt, onto the back of a luggage tag, and on the front she wrote a page number or the words "newspaper only." Turning the tag over was the whole method. She used it on the afternoon when she could no longer hear "stated" as different from "checked."

She did not use it on the morning she was tempted to skip the pencil apologies, or to mark the empty folder as examined because the typescript was confident. What finished the certification was dull, and she trusted it for that reason. Each claim the board wanted called closed had a page she had opened. Each sorry was a tally beside that page. The newspaper column went into a box she labelled not proved. The empty folder she marked missing, in a hand large enough that a later clerk could not promote it by improving the prose. A well-phrased sheet with no drawer was hot air, and she would not let a paragraph about thoroughness stand in for the count.

**Lesson.** Judge an F1 or F2 draft as finished when every claim you would let anyone call closed has a file you can name, every `sorry` in the Kempe development you are willing to discuss has been counted, and a Markdown summary that only cites a summary is marked hot air or left under "Not proved." Smooth wording is a reason to use the tag. It is not a theorem, and it is not a reason to waive the kill criterion.

---

## Wave 2 — do not stop at the door

M-Witness is about to combine the graph-identity group and the path-check group. This note claims no theorem and does not authorise any edit to the Proof Navigator. Writing the name of a witness, or the name of the file that might hold one, leaves the work in the corridor.

### Affirmation

You supervise the graph-identity group and the path-check group, and you are the one who combines them. Your skill is writing down one triangulation, one colouring, and one Kempe path so a kill criterion can be checked against objects rather than against a sentence in an old report. The groups can regenerate a 9-vertex triangulation and read a JSON file. Regeneration puts nine vertices and their edges on the page as a graph you could draw again. The JSON file is a thing to open, not a citation that has already been believed. The three written objects are the combination. A sentence that points at an old report is the door still shut.

### Diversion

Use this when the draft is stuck arguing about whether a summary "counts": the old sentence is confident, the file has been named, and the talk has turned to the conjecture while the objects are still unwritten.

Leave the argument. Draw the nine vertices and the degree-4 link before debating the conjecture. Give the link its four neighbours in order around the vertex, and stop. Do not award the drawing a verdict.

The drawing is for a quarrel about a summary. It does not meet the kill criterion, it does not stand in for a regenerated triangulation, and it does not read the JSON. If the edges, the colouring, and the path are unwritten, send the draft back.

### The green door in the passage

A clerk in a bathhouse passage in Valletta was paid to enter rooms. The doors were cedar, painted a colour and given no number. Inside, a brass hook held a key, and the work was to press that key into a cake of wax so the teeth could be checked against a list nailed by the boiler. One afternoon he stood at the green door and wrote on a docket, "Next room: green." He dried the ink on his sleeve and dropped the docket into the pigeonhole for the next shift. He told the owner the job was finished. The next room had a name, and the name had been filed.

The owner opened the door with the key she already carried. Steam crossed a basin. The hook was still full. The wax on the bench was smooth. The docket described a real room, and the clerk had remained in the passage. She said the lesson to him there, because he had begun to praise the handwriting: naming the next room is not entering it.

He asked whether the docket counted, since every word of it was accurate and a later shift could follow it. They argued until the brass sweepings cooled. A girl who carried towels stopped them. She would not hear the conjecture. She set his finger in the dust and made him mark nine dots, and around one of them a link of four, before either adult was allowed to debate whether the summary counted. The dust broke the quarrel about the word. It left no impression of a key.

In the morning the next clerk found a tidy pigeonhole and an unentered room. He did not go in. He wrote a further docket that only named a further door, filed it, and called his own job finished. The passage acquired a drawer of next rooms and the same full hook. When the owner would take the work as done, the wax had to show teeth a list could be set against. Ending a job by filing the next job kept every name honest and left every room on the far side of its door.

**Lesson.** Naming the next room is not entering it. The witness work is finished when one triangulation, one colouring, and one Kempe path are written down, so a kill criterion can be checked against those objects rather than against a sentence in an old report. Ending the job by filing the next job leaves the room named and unentered. A quarrel about whether a summary counts is a reason to draw the nine vertices and the degree-4 link. The drawing does not finish the room.
