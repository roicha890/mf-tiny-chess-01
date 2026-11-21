# E2E verification

- Pack: pyminify --rename-globals --remove-literal-statements --no-hoist-literals, lzma preset 9|EXTREME pb=0, base85 loader. 4088 bytes <= 4096 cap.
- Run: python3 -P -s main.py with MAKEFUN_ENV_URL at a fresh kit env (program/env/server.mjs).
- Gauntlet: depth-2 W (checkmate), depth-3 W (checkmate), depth-4 L (checkmate), nodes-100k L (checkmate), nodes-250k W (checkmate), nodes-500k D (adjudicated). 3.5/6.
- 338/338 env calls HTTP 200; 0 tracebacks; 0 illegal moves; 0 abandoned games.
- Bugs fixed during E2E: S shadowing sunfish's S=10, double-append of our own move from the /move response, delta-replay placement inside the your_move loop, missing Stop fallback to the first legal move.
- Timing: about 5 s per move on the env's half-CPU, under the 10 s forfeit.
