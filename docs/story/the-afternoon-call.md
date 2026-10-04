# The Afternoon Call

*A sequel to The Long Table: three rooms, two leaks, one video call*

---

## Dramatis Personae

**BUCKY**: The computer scientist. Has not slept. Has showered, which he considers the same thing.

**KAMPER**: The mathematician. Slept for ninety minutes in an armchair and woke with a proof sketch printed on her cheek by the folded napkins in her coat pocket.

**APPKEN**: The quant. Called in sick for the first time in twelve years. Is not sick.

**THE ASSISTANTS**: Each of them works with an AI helper on a laptop. On stage these are one voice in three rooms, written as ASSISTANT. Each is courteous and quick. Each asks, at least once, whether a result has actually been checked.

---

## The Set

*The stage is divided into three rooms, each lit separately. They are never in the same light until the call, and even then only through screens.*

*Stage left is **Bucky's flat**: a spare bedroom turned home office. A whiteboard covered in boxes and arrows, a standing desk, two monitors, and a mechanical keyboard loud enough to count as a fourth character. A mug reads "IT COMPILES."*

*Centre is **Appken's apartment**: high floor, glass wall, six monitors in a curved arc, and a grey cat named Theta asleep on a radiator. A whiteboard that came with the flat has been used for the first time today.*

*Stage right is **Kamper's study**: floor-to-ceiling books, a green-shaded desk lamp, a kettle on a side table because the kitchen is too far away, and a laptop she treats with suspicion. Pinned to a corkboard with a single drawing pin are the eleven napkins from last night, flattened under a dictionary for an hour first.*

*The light runs from late morning to early evening. Through the windows of all three rooms the same sun crosses the same sky.*

---

## Part One: Three Rooms

### i. Bucky, 10:40 a.m.

*Stage left comes up. BUCKY sits at the standing desk, which he has lowered all the way so that it is a sitting desk. The ASSISTANT's replies appear on his right monitor. He reads them aloud, half to himself.*

**BUCKY**: Okay. Again. The robust game. Signatures are sigma plus the nesting order of the bichromatic chain-curves around the root. Same rules as their replay: one common action per signature, must work for every concrete colouring behind it. Pooled first, then per root.

**ASSISTANT**: Done. With nesting added, the pooled Kittell game splits into more signatures, as expected. Some of the original five losing signatures now win. Not all. Per root, two of the four difficult roots are now fully repaired. The other two still have losing signatures.

**BUCKY**: Which two survive?

**ASSISTANT**: Roots 3 and 17 still lose. Roots 13 and 21 are repaired. Before you write that down, two caveats. First, I computed the nesting order from the embedding in the replay file, and I haven't independently checked the rotation system against a second source. Second, this is a finite table. A repaired root here means "a lookup strategy exists," not "a formula exists."

> *Bucky, inside:* It said the thing. The thing I'd say in a code review. I've been training people for ten years to say that sentence, and a laptop says it unprompted.

**BUCKY**: Write it up as a kill. "Nesting order alone is not enough: two of four difficult roots survive." Label it with the class, the move, the observation and the witness. Use their checklist.

**ASSISTANT**: Writing it as a negative result. Do you want me to also run the icosahedron?

**BUCKY**: *(sitting up)* Yes. Twelve vertices, all degree five. Every root looks the same. That's the stress test for Step.

*The keyboard clatters. A pause. The ASSISTANT's reply appears.*

**ASSISTANT**: Icosahedron: at each of the twelve roots there are 20 deletion colourings up to renaming colours. Every one of them is at most one swap from a target. I'd describe it as easy, not stressful.

*BUCKY stares at the screen.*

**BUCKY**: One swap.

**ASSISTANT**: One swap. Its symmetry means root selection can't help, but it also means there's very little room for a colouring to get stuck. It's the sharp example for Euler counting. It doesn't seem to be a hard example for Kempe escape.

> *Bucky, inside:* I said "the fairest test there is" at five forty this morning. Out loud. To two people I respect. I said it with the confidence of a man who had been awake for twenty-two hours.

**BUCKY**: *(to the room)* Well. That's the second thing I was wrong about today, and it's not lunchtime.

*He writes on the whiteboard: "ICOSAHEDRON: EASY. NOT A STRESS TEST. (me, wrong, 5:40 a.m.)"*

### ii. Appken, 12:15 p.m.

*Centre comes up. APPKEN stands in front of the six monitors in socks, holding a bowl of cereal. Theta the cat watches from the radiator. Every monitor shows a different plot. Most of them are red.*

**APPKEN**: Potential one, dead. Potential two, dead. Potential three... *(he squints)* ...dead in a really embarrassing way.

**ASSISTANT**: Potential three decreases on most moves, but there are 14 non-target Kittell states where every legal swap leaves it unchanged or raises it. So it isn't a strict progress measure.

**APPKEN**: It's a stop-loss that doesn't stop anything.

**ASSISTANT**: That's one way to put it.

**APPKEN**: Okay. Potential four. Same idea, but the count is on the *full* state, not the boundary summary. For each repeated colour on the boundary, count the chains that block each way of freeing it, and weight by how many boundary vertices each chain touches.

*He types. He eats cereal. He types.*

**ASSISTANT**: Potential four, Kittell backtest: every non-target state has at least one legal single-component swap that strictly lowers it. Zero failures across all 6,350 states.

*APPKEN puts the cereal down very slowly.*

**APPKEN**: Zero.

**ASSISTANT**: Zero on Kittell. I want to be careful about what that means. It is one graph. Kittell is already known to be easy in the full state, since every state reaches a target in at most four moves. Lots of potentials can survive an easy fixture. This is a necessary test, not a sufficient one.

> *Appken, inside:* A model that survives one backtest is a model that hasn't met the market yet. I know this. I've fired people for not knowing this.

**APPKEN**: Okay. Out of sample. The thing Kamper called the falsification sweep. Every triangulation where every vertex has degree at least five, for as many orders as we can do this afternoon. Worst-case moves to a target, at the best root. The term structure.

**ASSISTANT**: I can install a triangulation generator and enumerate minimum-degree-five triangulations by order. Twelve through sixteen should finish in under an hour here. Beyond that, the colouring enumeration grows quickly.

**APPKEN**: Do twelve to sixteen.

*Lights shift slightly to suggest time passing. Theta changes radiators.*

**ASSISTANT**: Done through order sixteen. Every Kempe class at every degree-five root contains a target in this range, and the worst-case full-state distances stay small, flat-looking rather than growing. Potential four survives most graphs but fails on two at order sixteen. There are states where no swap lowers it.

**APPKEN**: *(not deflated, almost pleased)* There it is. There's the market.

**ASSISTANT**: Do you want me to characterise the failures?

**APPKEN**: Yes. And save them as fixtures. Those are the most valuable things I've made today.

> *Appken, inside:* Two years ago I'd have been gutted. Today I've got two named graphs where my idea breaks. I've never been so happy to lose money that doesn't exist.

### iii. Kamper, 2:30 p.m.

*Stage right comes up. KAMPER sits at her desk in a cardigan, a pot of tea at her elbow and the laptop open at arm's length. A pad of graph paper lies in front of her, covered in her handwriting. The napkins are on the corkboard behind her.*

**KAMPER**: Read me the neighbourhoods again. The four bad roots first, then the eleven good ones. Degrees of the five neighbours, in cyclic order.

**ASSISTANT**: For roots 3, 13, 17 and 21, here are the neighbour degree sequences. For the eleven good roots, here are theirs. The short answer to your question is that the first-ring degree sequences don't separate the two groups. Two of the bad roots have the same first-ring pattern as good roots.

**KAMPER**: The second ring?

**ASSISTANT**: The second ring is more varied, but with fifteen roots and four bad ones I'd be overfitting if I claimed a separating pattern. Any rule that separates them in the second ring will be a rule fitted to four examples.

**KAMPER**: *(dry)* You sound like a referee I once had. I hated him. He was right.

*She pulls the graph paper towards her.*

> *Kamper, inside:* First-ring degree doesn't separate them. So whatever makes those four roots hard isn't local in the cheap sense. Then charge can't simply avoid them by degree. The rule has to be bolder, or it has to choose on something other than degree.

*She writes, speaking as she goes, more to herself than to the machine.*

**KAMPER**: Charge six minus degree. Total twelve. In a minimum-degree-five triangulation, only fives carry positive charge, so there are at least twelve fives, plus one more for every unit of excess degree above six. Now take any vertex, an anchor, and its closed neighbourhood: itself and its neighbours. How many fives must lie *outside* that star?

*She works. Tea goes cold.*

**KAMPER**: *(cont'd)* The star has at most one plus its degree vertices... Degree sum outside the star, against the Euler count... *(a long pause)* At least five. At least five and a half, honestly, which in integers is six, if this step is legitimate, and I don't yet trust this step.

**ASSISTANT**: Do you want me to check the step formally, or test it on the generated triangulations?

**KAMPER**: Test it. If it fails on a single graph I'll know where I cheated.

**ASSISTANT**: On every minimum-degree-five triangulation I have through order sixteen, every vertex has at least six degree-five vertices outside its closed neighbourhood. That's a check, not a proof.

**KAMPER**: Then the proof is my job. *(She circles "≥ 6" twice.)* Good. That means a root rule never runs out of candidates far from any anchor. It doesn't mean any of them is *good*.

> *Kamper, inside:* Availability is not quality. That's the whole of combinatorics in four words, and I keep forgetting it after lunch.

*She looks at the corkboard of napkins. Then at the clock. 3:38 p.m. She reaches for her phone, intending to email the others her half-proof. Instead she finds a message from APPKEN in the group chat, a single link with no comment. That's unlike him.*

---

## Part Two: The Thread

*3:40 p.m. All three rooms are lit at once, dimly, each figure lit mainly by a screen. They read in silence. The text they read appears on the screen above the stage.*

```screen
r/math · Posted 2h ago

**Rumour: a team is closing in on an "explainable" Four Colour proof, and the leaked docs are surprisingly honest**

A blog post (not affiliated with the group) says a mixed human/agent team has been rebuilding the Four Colour Theorem's foundations in Lean, aiming for a *rule-based* proof without the 633-configuration census, plus an algorithm with a polynomial bound. Two documents allegedly from the project are circulating: a progress report dated 4 October and a separate audit of that report. Links in comments. I can't verify either. Treat accordingly.

Top comment: AI SOLVES 4 COLOUR THEOREM?!?!

↳ Reply: It was solved in 1976. Read the post.

↳ Reply: Read the docs. They literally say the key gate is open. Every second paragraph is "this does not prove X."

↳ Reply: honestly the most self-skeptical leak I've ever read. whoever wrote it has been burned before
```

**APPKEN**: *(to his monitors, under his breath)* Oh no.

**BUCKY**: *(to his monitors, under his breath)* Oh no.

**KAMPER**: *(to her laptop, under her breath)* Oh, how lovely.

*They each click a different comment. Each of them sees only what they click.*

*KAMPER follows the first link and finds the progress report. She reads it slowly, in full, glasses pushed up, pen in hand as if marking a thesis.*

```screen
Structural Four Colour execution plan · 4 October 2026 (leaked)

…`Icosahedron.lean` now supplies a genuine `SphericalMap 12` with thirty edges, twenty triangular faces, degree five everywhere… Its filling proof uses a finite linear coefficient certificate checked by the kernel.

…The named bit beta asks whether the smallest remaining vertex lies in a canonical {1,3} component meeting the boundary. On the four difficult Kittell roots, (sigma,beta) admits verified common-action lookup strategies. The bit is not a preserved invariant, and finite attractor tables are not a uniform rank formula.

…The reachability kill-witness search through order twenty checked all 118 generated minimum-degree-five triangulations: none supplied a targetless class at any root.

…Stress testing finds a first failure of the smallest eligible exterior-root rule at order twenty, graph 36, root 8…

…The newly compiled six_le_degreeFiveOutside theorem guarantees at least six eligible exterior degree-five roots per nonisolated anchor; it proves availability, not that any particular root admits the desired rank.
```

*KAMPER stops at the last paragraph. She reads it three times. She looks up at the "≥ 6" circled twice on her graph paper.*

> *Kamper, inside:* Six. Compiled. Someone did my afternoon this week, and did it in Lean, and wrote "availability, not rank" next to it, the same sentence I wrote at three o'clock. I don't know whether I'm deflated or vindicated. I think the right word is "accompanied."

*Meanwhile BUCKY and APPKEN, in their separate rooms, have both clicked the second link. It is a different document: an audit of the report by a second team. They read it at the same time without knowing it.*

```screen
Navigator audit (leaked)

The summary is accurate, and it changes the research odds. Gate D is still open. The new evidence makes a small Kempe-class counterexample unlikely and makes a one-bit observation rank less likely to be the proof.

…I did not rebuild Lean or rerun the Plantri census. The recorded source rebuild now lists 41 custom modules as passed…

…The icosahedron is easy: 20 deletion-colouring orbits at each of 12 roots, every one within one swap. It does not stress root selection.

…On Kittell, no common interior swap and no common repeated-colour swap repairs the old five losing signatures. Adding the bit … does repair roots 3, 13, 17, and 21, with lookup ranks at most 4, 5, 4, and 4. Hiding the root leaves 10 of 80 refined observations losing.

…The kill-witness search covers the 118 Plantri minimum-degree-five triangulations from order 12 through 20: 1,586 roots, 244,051 colouring orbits, 1,626 Kempe classes. Every class contains a three-colour boundary.

…The first explicit rule … fails at order 20, graph 36, root 8. Five of 55 observations lose. All 198 concrete colourings still reach a target. Kittell passes this rule, so Kittell is no longer the adversarial fixture for it.

…My credence that every Kempe class at every degree-five root contains an extendible colouring … moves from about even to roughly three to one.

…Quotient games are now a good way to kill proposed observations and a poor way to expect the theorem.

…The useful next fixture is graph 36, root 8, not another Kittell signature and not the icosahedron. A proposed rank should be a formula on those five losing observations.
```

*BUCKY reaches the icosahedron line and laughs once, sharply, alone in his flat. He turns and looks at his own whiteboard: "ICOSAHEDRON: EASY. NOT A STRESS TEST."*

> *Bucky, inside:* Twenty orbits. Every one within one swap. My laptop said exactly that at 10:52 this morning. Someone else's team got the same number independently. That's not embarrassing. That's a replication.

*APPKEN reaches the last line and puts his hand flat on the desk. Theta the cat lifts her head.*

> *Appken, inside:* "A proposed rank should be a formula on those five losing observations." That's my job description. Someone wrote my job description in a leaked audit.

*Then APPKEN reaches the credence line.*

> *Appken, inside:* Three to one. Seventy-five percent. Seventy-five percent we get there.

*He is already typing in the group chat.*

```screen
Group chat · Long Table

Appken: CALL. NOW. 4:30? I have a link. Also a cat.
Bucky: 4:30. Read the audit?
Appken: YES
Kamper: I read a progress report. Is there also an audit?
Bucky: …there's an audit.
Kamper: 4:30.
```

---

## Part Three: The Call

### i. Three Rectangles

*4:30 p.m. All three rooms are fully lit. Above the stage a video-call grid appears: three rectangles, each showing a face. BUCKY in front of his whiteboard. APPKEN in front of six monitors, the cat in the lower corner of the frame. KAMPER in front of her corkboard of napkins, slightly too close to the camera, the green lamp making her look like a portrait.*

*Each actor speaks into their own laptop. They never look at each other, only at the audience, which is the camera.*

**APPKEN**: Can you hear me? I can hear me.

**BUCKY**: We can hear you.

**KAMPER**: I can see all of you. I can also see your cat.

**APPKEN**: That's Theta.

**KAMPER**: Of course it is.

**BUCKY**: Okay. Before anyone says anything exciting, ground rules. These are leaks. We didn't ask for them. They aren't ours. We don't repost them, we don't quote them anywhere, and if we use anything from them, we say where it came from when we write to the team.

**KAMPER**: *(nodding firmly)* Agreed. And we write to them *today*. Directly. With our own results, properly labelled. It would be indecent to sit on what we know they're doing and not offer what we've done.

**APPKEN**: Agreed. Agreed. Can I be exciting now?

**BUCKY**: Be exciting.

**APPKEN**: *Seventy-five percent.*

*A pause.*

**KAMPER**: Seventy-five percent of what?

**APPKEN**: The audit. "Credence moves from about even to three to one." Three to one, seventy-five percent. Up from fifty.

**BUCKY**: Read the sentence again.

**APPKEN**: *(reading)* "My credence that every Kempe class at every degree-five root contains an extendible colouring, for minimum-degree-five triangulations, moves from about even to roughly three to one."

**KAMPER**: That's a credence in a *statement*. Not in a proof. And not in this route. And the statement is stronger than the Four Colour Theorem, which we already know is true.

**BUCKY**: It's the next row in the same table. "Medium-High as a statement, Low as a proof."

> *Appken, inside:* Selective memory. Again. The seventy-five survives, the caveat dies. Twice in two days. I need a sticky note on my monitor.

**APPKEN**: *(laughing at himself)* I did it again. I marked the position at the headline.

**KAMPER**: You did. But it's still a real update. I'd have said "about even" too, before today. A small counterexample, one Kempe class with no target, felt plausible. Now there's none in sixteen hundred classes.

**APPKEN**: Sixteen twenty-six.

**KAMPER**: I don't have that number. My leak doesn't have it.

*A beat. They realise.*

**BUCKY**: Wait. What did you read?

**KAMPER**: A progress report. Fourth of October. Gates, the icosahedron compiled, a bit called beta, a search through order twenty, a rule that fails at graph 36, and *(she glances at her graph paper)* a theorem I spent my afternoon half-proving.

**BUCKY**: We read the audit of that report. Someone else's team checked it line by line.

**KAMPER**: *(delighted)* They audit each other?

**BUCKY**: They audit each other. And the auditor says what they *didn't* check: they didn't rebuild Lean, they didn't rerun the census. And the two newest degree-five files rely on the test file's axiom guard, which the auditor didn't recheck.

**KAMPER**: *(quietly)* That's the most beautiful sentence anyone has said to me this year.

**APPKEN**: Okay. We each have half the elephant again. Let's do the napkin thing. Screen-share.

### ii. What Each of Them Did Today

*BUCKY shares his screen. A shared document appears above the stage, a digital napkin titled "LONG TABLE: DAY 1." They fill it as they talk.*

**BUCKY**: Me first, because mine are mostly kills. One: I refined sigma with the nesting order of the chain-curves around the root. Kittell, per root: it repairs 13 and 21. Roots 3 and 17 still lose. So nesting alone isn't the missing information.

**KAMPER**: And the leak says...

**BUCKY**: The audit says their bit, beta, repairs all four: 3, 13, 17, 21, with lookup ranks of at most four or five. So they found a better instrument than mine. Fine. But it also says no common interior swap and no common repeated-colour swap repairs the old five losers. That kills two of our "later" items from last night.

**APPKEN**: *(wincing)* "Interior swaps as instruments. Possibly necessary."

**BUCKY**: Dead, at least in that form. In the common-action game, anyway. Two: the icosahedron. My assistant found twenty colourings per root, all within one swap. The audit independently says the same. Easy. My "fairest test there is" was the easiest test there is.

**KAMPER**: *(gently)* You were right that root selection can't help there. You were wrong that it would be hard. Half-right is a respectable fraction before dawn.

**BUCKY**: Thank you. Three, and this is the one that matters to me. The audit says, and I'm paraphrasing because I promised not to quote: quotient games are good for *killing* proposed observations and bad for *expecting* the theorem. A concrete policy can keep making progress while the coarse observation repeats.

**APPKEN**: What does that do to your plan?

**BUCKY**: It turns my refinement engine around. I was using it to look for the *right* abstraction. It should be a *weapon*. Anyone proposes a rule, root choice plus observation plus rank, and the engine hunts for the first graph where the rule's quotient game loses. Like their order-20 result. A kill machine.

**KAMPER**: A referee machine.

**BUCKY**: A referee machine. A bad one at first. It'll get better.

> *Bucky, inside:* There's a version of me from five years ago who would have been crushed that his abstraction wasn't the answer. This version is thrilled that it's a good gun. Maybe that's growth. Maybe it's sleep deprivation.

**APPKEN**: Me. *(He shares a plot.)* Three potentials dead on Kittell. A fourth on the full state, not the boundary summary, survives all 6,350 Kittell states. Then I ran the term structure: every minimum-degree-five triangulation through order sixteen. Everything reaches a target, distances stay small, and the curve looks flat. They went to twenty, so of course they did. But here's the part I'm proud of: potential four *dies* on two graphs at order sixteen. Saved as fixtures.

**KAMPER**: Good. Good. You're proud of the death.

**APPKEN**: I'm proud of the death. And then I read: "Kittell passes this rule, so Kittell is no longer the adversarial fixture for it." Last night we were treating Kittell like it was the whole market. It's one ticker. The live fixture is graph 36, root 8. Five of 55 observations lose, but all 198 actual colourings still reach a target.

**BUCKY**: So the colourings are fine and the summary is broken.

**APPKEN**: The colourings are fine and the summary is broken. Which is *exactly* the incomplete-market thing. And the audit says the rank should be a *formula* on those five losing observations, not another lookup table. That's... *(he gestures at his screen)* ...that's what I'm for.

**KAMPER**: Where does potential four stand on graph 36?

**APPKEN**: I don't know. I don't have graph 36. I only went to sixteen. That's my first job tonight: get to order twenty and point potential four at graph 36, root 8. If it lowers on those five observations, great. If not, it's dead and I know exactly where.

**BUCKY**: Write the kill condition.

**APPKEN**: *(typing)* "Kill: any of the 198 concrete colourings at graph 36, root 8, from which no legal single-component swap lowers potential four."

**KAMPER**: Me. *(She holds her graph paper up to the camera. It's illegible.)* Two things. One is a disappointment and one is a coincidence. The disappointment: Kittell's four bad roots aren't separated by their first-ring degree patterns. Two of them look exactly like good roots. So a charge rule that picks roots by the degrees of their neighbours can't simply avoid them.

**APPKEN**: And the second ring?

**KAMPER**: Too few examples. Four bad roots. Any rule I fit to them is a rule fitted to four points. My assistant scolded me about it, quite properly.

**BUCKY**: And the coincidence?

**KAMPER**: I spent the afternoon trying to prove that, in a minimum-degree-five triangulation, every vertex has at least six degree-five vertices outside its closed neighbourhood. Charge arithmetic. I got to "five and a half, round up" and didn't trust the last step. Then I opened the report, and there it is. `six_le_degreeFiveOutside`. Compiled. With the sentence underneath: "proves availability, not that any particular root admits the desired rank."

**BUCKY**: The audit gives the counting. Degree sum outside the star, plus two e plus twelve, at most six s.

*KAMPER freezes. Then she looks down at her graph paper, finds a line, and circles something.*

**KAMPER**: *(very quietly)* Two e plus twelve. That's where I dropped a term. I used the vertex count where I needed the edge count.

> *Kamper, inside:* Forty years of this, and the last step of my afternoon was handed back to me through a leaked audit read aloud by a computer scientist over a video call. Whatever happens to this problem, I'm going to remember this moment.

**APPKEN**: So you proved it.

**KAMPER**: I *nearly* proved it, and someone else proved it properly, and the machine checked it. That's better.

### iii. The Rule That Died, and Why

**BUCKY**: Okay. The rule that failed at graph 36. Kamper, your report has the rule. What exactly was it?

**KAMPER**: Take the smallest anchor. Look outside its closed neighbourhood for degree-five vertices; there are at least six, by the theorem. Pick the smallest one. Then play the boundary summary plus beta.

**APPKEN**: Smallest.

**KAMPER**: Smallest *label*.

*A pause. KAMPER is clearly about to say something. The other two wait for it.*

**KAMPER**: That's not structural. That's alphabetical. They needed *a* rule to test, and they picked the simplest one that's fully defined, which is the right thing to do for a first stress test. But "smallest label" is the vertex equivalent of choosing a stock by its ticker symbol. There's no reason the charge should care what we called a vertex.

**APPKEN**: *(lighting up)* So the failure of smallest-label doesn't tell you charge-based selection fails.

**KAMPER**: It tells you smallest-label fails. Precisely that. And it gives me a beautiful question. At graph 36 there are at least six eligible roots outside the anchor's star, by the theorem. Root 8 loses. What about the other five? If *any* of them survives the beta game, then the question becomes whether charge can find it without being told the answer.

**BUCKY**: And if all six lose?

**KAMPER**: Then the boundary-plus-beta observation is too weak at graph 36 regardless of root, and Appken's full-state potential is the only live shape.

**APPKEN**: Either way we learn something.

**KAMPER**: Either way, we learn something specific. That's the only kind of evening I want.

**BUCKY**: Kill condition?

**KAMPER**: "Kill: every eligible exterior degree-five root at graph 36 loses the (sigma, beta) robust game. Then no root rule over that observation survives graph 36."

### iv. The Shape That Got More Plausible

**APPKEN**: There's one more thing in the audit. Path likelihoods. The line that moved most wasn't the one I wanted. "Retreat to certificates only for colourings the induction itself produces": it was "the fallback," and now it's "the more plausible shape."

**BUCKY**: Meaning: don't prove *every* colouring at the root can escape. Prove that the colourings your own recursion *hands* you come with a certificate, and that the certificate survives the recursion.

**APPKEN**: In my language, you don't price every possible state of the world. You price the states your own book can reach. Path-dependent.

**KAMPER**: And in mine, that's a stronger induction hypothesis. Which is a very old trick. If you can't prove P(n) by induction, try proving something stronger, because then you have more to work with at each step. Thomassen's five-list-colouring proof does exactly that: it strengthens the hypothesis until the induction can carry itself.

**BUCKY**: But the invariant has to be proved and preserved. And it can't just be "this colouring is extendible."

**KAMPER**: Never "extendible." That's the trap. It has to be something you can *check* that *implies* extendible, and that the reconstruction step *reproduces*.

**APPKEN**: *(slowly)* So potential four, or whatever replaces it, isn't just a rank. It's a candidate invariant. "The recursion always hands you a colouring where potential-four-style progress is available." And then I'd have to show that when you put the vertex back, the new colouring has that property too.

**KAMPER**: Yes. That's precisely the shape. And it's precisely where everyone has failed for a hundred and fifty years, so do it carefully.

**APPKEN**: Carefully. Got it. *(He writes it down.)* "Careful."

**BUCKY**: Can I add the boring part?

**KAMPER**: The boring parts are where proofs actually live.

**BUCKY**: Triangulation completion. Everything in Gate D is stated for triangulations. Real spherical maps aren't triangulations. You have to add edges to make one, prove it's still a sphere, colour it, then delete the edges again. Deleting is free; colourings restrict. *Adding* edges needs a new spherical carrier and a new filling proof. And the audit points out that the induction measure has to change. Completion adds edges, so "edges strictly decrease" stops working. It has to be support size: the number of vertices that actually have edges.

**APPKEN**: That sounds like plumbing.

**BUCKY**: It's plumbing on the critical path. If D is ever solved for triangulations only, this is the pipe between that and the real theorem. It's Lean work. It's exactly my kind of misery. And it can proceed beside D, so it won't step on anyone's toes.

> *Bucky, inside:* Kamper gets to chase the beautiful rule. Appken gets to price the impossible thing. I get to prove that adding an edge to a sphere leaves a sphere. And I'm happier about it than either of them would believe.

### v. Day Two

*5:40 p.m. The light in all three rooms has gone gold, the same low October gold as the café the afternoon before. The shared document above the stage has filled. BUCKY reads it aloud. The others make small corrections.*

```
LONG TABLE: DAY 2 PLAN
Rule: results not hunches. Name class, move, invariant, measure,
      input family, coverage, falsifying witness.
Rule: the leaks are not ours. Cite them, don't spread them.

THREAD K (Kamper): STRUCTURAL SELECT AT GRAPH 36
  Finish the six-outside proof by hand (the 2e + 12 term).
  At order 20, graph 36: test every eligible exterior root
    in the (σ, β) robust game, not just root 8.
  If one survives: can a charge rule find it unaided?
  Kill: all eligible roots lose → (σ, β) too weak at graph 36.

THREAD A (Appken): A FORMULA, NOT A TABLE
  Extend the sweep to order 20.
  Point potential 4 (full state) at graph 36, root 8:
    the 5 losing observations, the 198 colourings.
  Then try it as an INVARIANT for induction-produced colourings:
    does reconstruction reproduce it?
  Kill: any colouring at graph 36 root 8 with no lowering swap.
  Keep: the two order-16 failures as named fixtures.

THREAD B (Bucky): KILL MACHINE + COMPLETION PIPE
  Turn the refinement engine into an adversary:
    rule in → first failing graph out.
  Point it at Kamper's rule and Appken's potential first.
  Lean: triangulation completion. Support relabelling first
    (easy half), then filling after adding edges (real half).
    Induction measure → support size.
  Kill: completion breaks filling for some map → need
    direct coverage of non-triangulations instead.

DEAD TODAY (labelled, to send):
  - nesting order alone (Kittell roots 3, 17 survive)
  - icosahedron as a stress test (easy: 1 swap)
  - potentials 1–3 (Kittell); potential 4 (two order-16 graphs)
  - first-ring degree pattern as a root filter (Kittell)
  - "75%" (Appken, again)

WRITE TO THE TEAM TONIGHT: the dead list, the fixtures, an offer.
```

**APPKEN**: You put "seventy-five percent" on the dead list.

**BUCKY**: It's a dead conjecture. Properly labelled.

**APPKEN**: *(laughing)* Fair.

**KAMPER**: Who writes the email to the team?

*A pause.*

**BUCKY**: You. You're the one they'd want to hear from.

**APPKEN**: You. You'll make it sound like it was worth reading.

**KAMPER**: *(a long breath)* All right. I'll draft it tonight. I'll send it to both of you first. And it will be short. Three paragraphs. What we tried, what died, what we'd like to try next if they'll have us.

**BUCKY**: "If they'll have us."

**KAMPER**: They have a very good team. They may not need three more people who spent a night in a café. But they might want our dead conjectures, and our fixtures. And if they want us, we'll be useful in different directions from theirs. Narrow channels, three different instruments.

> *Kamper, inside:* Last night I said I'd like to teach it before seventy. Tonight I'd settle for being one line in the history of who tried. It's a good line to be in.

### vi. Sign-off

**APPKEN**: I want to say something un-quant-like.

**BUCKY**: Go on.

**APPKEN**: Reading that audit was the most exciting thing that's happened to me in a decade. Not because it's close. Because it's *honest*. Every paragraph says what it knows and what it doesn't. I've read a thousand investment memos and not one of them told me where it would die.

**BUCKY**: That's the thing that gets me too. Forty-one modules rebuilt, and the auditor still writes, "I didn't rebuild this myself." That's the whole culture in one sentence. Trust, but write down exactly how much.

**KAMPER**: When I was young, the Four Colour argument was about whether you could trust a computer. Now it seems to be about whether you can trust a *team*: people and machines, auditing each other, keeping their dead ends on the board. I think I prefer this argument.

**APPKEN**: Same time tomorrow?

**KAMPER**: Same time tomorrow. Results, not hunches.

**BUCKY**: Results, not hunches.

**APPKEN**: *(to the cat)* Theta, say goodbye.

*Theta does not say goodbye. Theta leaves the frame.*

*The call ends. The three rectangles above the stage go dark one by one: first APPKEN's, then BUCKY's, then KAMPER's.*

---

## Coda: Evening

*6:15 p.m. Three rooms, three lamps, the sky in every window turning the same deep blue.*

*Stage left: BUCKY opens a new file. At the top he types, "Triangulation completion: support relabelling." Beneath that: `theorem`, and stops, and smiles, and keeps typing.*

**BUCKY**: *(to the ASSISTANT)* Let's start with the easy half. And tell me the moment I'm assuming something I haven't proved.

**ASSISTANT**: I will. You're already assuming the completed map is simple. Want to state that as a hypothesis or prove it?

**BUCKY**: *(grinning)* Prove it.

*Centre: APPKEN stands before the six monitors. One shows a progress bar: "Enumerating min-degree-5 triangulations: order 17…" He sticks a yellow sticky note on the bezel of the middle monitor. It reads: **"CREDENCE IN WHAT?"***

**APPKEN**: *(to the ASSISTANT)* When we get to graph 36, wake me. Wake me even if it's bad. *Especially* if it's bad.

*Theta returns and sits on the keyboard. The progress bar does not mind.*

*Stage right: KAMPER sits at her desk with a fresh sheet of graph paper. At the top she writes, slowly: "Dear colleagues." Then crosses it out. Then writes: "Dear colleagues, we have some dead conjectures for you." Then, smiling, she leaves it.*

*She glances up at the corkboard. The eleven napkins from the café. In the centre is the Gate D napkin, her own handwriting from twenty-four hours ago. She takes a pencil and, very small, beside "∀ proper 4-colouring c," writes: "or only the ones we make?"*

**KAMPER**: *(to herself)* Six outside the star. Two e plus twelve. Graph 36, root 8. Show me your neighbours.

*Three lamps. Three screens. The same blue sky. In each window a single bright point appears, the first star, or a planet, or an aeroplane. None of them can tell which, and none of them looks up long enough to check.*

**END**

---

### Author's note

The two documents the characters read are the project's 4 October 2026 progress report and the audit of it, presented in the story as leaks. Every technical claim attributed to them comes from those texts. Several things are invented for the story and are not project findings: the characters' own results from the day (Bucky's nesting refinement, Appken's potentials and their failures at order sixteen, and Kamper's first-ring degree comparison). The real record of what has been checked is in the Proof Navigator.
