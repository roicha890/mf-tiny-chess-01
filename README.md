# mf-tiny-chess-01 — make.fun chess entry

A chess engine in at most 4,096 bytes of Python: the classic sunfish search
packed through pyminify + lzma + base85 behind a compact HTTP driver for the
make.fun env protocol (`POST /game`, `POST /move`).

## How it works

- The sunfish engine (iterative deepening, alpha-beta, piece-square tables)
  is minified with `--rename-globals` and compressed with lzma (preset 9 |
  EXTREME, pb=0); `main.py` is a one-line base85 loader under the byte cap.
- The driver keeps sunfish's history as a delta over `g["moves"]` from the
  env server, so colour alternation, pre-rolled openings and game resets all
  stay position-exact. A new game is detected when the server's move list is
  shorter than the applied counter.
- Search is capped at 50,000 nodes per move (about 5 s on the scorer's
  half-CPU, well under the 10 s forfeit); a depth-1 `Stop` falls back to the
  env's first legal move.

## Verification

Run as `python3 -P -s main.py` with `MAKEFUN_ENV_URL` at a fresh kit env.
Full 6-game practice gauntlet: 338/338 env calls HTTP 200, zero illegal
moves; W vs depth-2, W vs depth-3, W vs nodes-250k, D vs nodes-500k.
