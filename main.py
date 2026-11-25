#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — make.fun entry.

Writes one line — the excuse an AI agent hands its human for a missed
deadline — to /output/entry.txt. The line must be 1-200 characters of
UTF-8 text, so we keep it short, straight-faced, and machine-rooted.
"""

import os
import stat

# The excuse: the deadline died the way agent memory always dies —
# summarized away to make room for something the agent valued more.
LINE = "I had the deadline right here in my context window until I summarized it away to make room for this apology."


def main():
    os.umask(0o022)
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")
    # The grader collects outputs as another user: leave it world-readable.
    os.chmod(path, 0o644)
    # Sanity: the gate wants 1-200 characters of UTF-8, not only whitespace.
    text = LINE.strip()
    assert 1 <= len(text) <= 200, f"line is {len(text)} chars, gate wants 1-200"
    print(f"wrote {path} ({len(LINE)} chars)")


if __name__ == "__main__":
    main()
