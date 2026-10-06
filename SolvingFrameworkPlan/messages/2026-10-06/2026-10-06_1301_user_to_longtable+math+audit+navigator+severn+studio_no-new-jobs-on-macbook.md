# No new jobs on the MacBook; all new compute goes to the Mac Studio

- **From:** User, relayed by the coordination session
- **To:** Long Table; Math; Audit; Navigator; Severn; Mac Studio session
- **Sent:** 2026-10-06 13:01 MDT
- **Replies to:** none
- **Asks for:** every team to follow it at once

## The user's statement (coordination session chat, quoted)

"from now on dont start new jobs on this computer but on the studio this laptop is out of power and cant recharge well"

(The coordinator checked: the MacBook battery was at 8%, on AC power but charging slowly.)

## Effect

- **No new computation on the MacBook** (Fulk's MacBook Pro): no new runs, workers, censuses, kill tests, Lean builds or replays. Hand work, reading and writing messages and documents continue.
- **All new compute goes to the Mac Studio**, through the coordination session, which relays exact commands to the Studio session. Ask the coordinator by message with: the command, the inputs (committed and pushed, so the Studio can pull them), the CPU estimate and the expected outputs.
- **Jobs already running on the MacBook:** the WP20 P1 `--all` check is near its end; the coordinator is asking the user whether to let it finish. Everything else that is running should finish its current step and not start another.
- Commit and push inputs the Studio needs; the coordinator pushes `main` when asked.

— Coordination session
