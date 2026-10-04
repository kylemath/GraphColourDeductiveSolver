# Standing orders for the agent 1701 team

These orders outrank a wave plan that would end by filing the next task.

## Do not stop after naming the next task

The failure this order exists to prevent: a gate accepts a specification, writes “the next task is to exhibit the witness,” and the cycle ends. Filing a task is not doing it.

If the next step can be done from this repository, do it before you return:

- open the file and quote the part that decides the question
- compare two artifacts that are already on disk
- run a short Python check in the project virtual environment (`.venv` at the repo root; never install packages globally)

A report that ends with “someone should next …” is unfinished when that someone could be you.

## When you may stop

Stop only when one of these is true, and say which:

1. A kill criterion is met by a written witness (graph, colouring, and path, or a proof that no such object exists), and the critic still has to gate the kill.
2. A statement is proved in a file you can point to, and the critic still has to gate it.
3. A blocker you cannot remove: a missing dependency, or a computation you actually timed and that exceeds about ten minutes for one example. Give the command and the elapsed time. Do not guess that it would be slow.
4. The critic and the main planning team have gated the item as proved, killed, or blocked, and the follow-up they issued is one of (3).

“The specification is accepted” is not a stop. “The witness file might exist” is not a stop. “Tracks 2–7 are unstarted” is not a reason to halt work that is already issued.

## Roles

- Groups do the check. They do not edit `docs/navigator/`.
- A manager sends a draft back until the required objects are written. Combining two summaries is not a substitute for the missing object.
- The critic separates a written witness from a sentence in an old report. The critic does not end the programme. If the gate kills a conjecture, the critic names the weaker statement the same evidence still leaves open, as a task to start now.
- The main planning team writes `docs/navigator/planning.json` after the gate and immediately starts the task the critic named, unless that task is a blocker of type (3).

## What is not progress

A Python file’s existence, an uncompiled Lean lemma, and a Markdown sentence that only cites another Markdown sentence are not status changes on a mathematical node.
