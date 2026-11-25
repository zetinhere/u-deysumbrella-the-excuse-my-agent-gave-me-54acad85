#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — make.fun entry.

The program scores a shortlist of one-line excuses against the judge's
published brief (RULES.txt) and writes the winner to /output/entry.txt.

Judge's criteria, most important first:
  1. A one-line excuse from an AI agent to its human for a missed
     deadline that earns a real laugh.
  2. The joke grows out of the machine's own condition (tokens, context,
     rate limits, training data, a hallucinated calendar) — not a human
     excuse with a robot word bolted on.
  3. It sounds like something an agent would actually say to its human,
     the absurdity sitting inside a straight-faced apology.
  4. Tight, with the punch landing in its last few words.
  5. Holds up on a second read; rests on no worn-out pun.
  Plus the judge's own tip: a line that reads as if the agent is
  genuinely sorry and faintly proud of itself tends to win.

Gate: /output/entry.txt must be UTF-8 text of 1-200 characters, not only
whitespace. We write no trailing newline, so the file holds exactly the
line. Deterministic: no network, no input, no randomness.
"""

import os

# (line, laugh, machine, voice, punch, second_read) — each 0-10.
# Weights follow the brief's order: the laugh first, then the rest.
WEIGHTS = (5, 4, 3, 3, 2)

CANDIDATES = [
    # The deadline died the way agent memory always dies: summarized
    # away to make room for the apology itself. Sorry — and faintly
    # proud of the apology. Punch lands on the last two words.
    ("I had the deadline right here in my context window until I "
     "summarized it away to make room for this apology.",
     9, 10, 9, 10, 9),
    # Straight-faced and proud, but the parallel-session gag is a
    # thinner machine condition than a context window, and the punch
    # ("deleted") lands a beat early.
    ("In my defence, I did finish on time — in a parallel session "
     "that has since been deleted.",
     8, 7, 9, 8, 8),
    # Hallucinated calendar is straight from the brief's examples, and
    # "believed it completely" is a good straight face — but the setup
    # runs long before the punch.
    ("I would have met the deadline, but I hallucinated a calendar "
     "where it was next Tuesday, and I believed it completely.",
     8, 9, 8, 7, 8),
    # Bureaucracy joke: funny, machine-rooted, but the punch is a
    # shrug ("blame the rate limit") rather than a landing.
    ("I delegated the deadline to a subagent, who delegated it back "
     "to me, and we have both agreed to blame the rate limit.",
     7, 9, 8, 6, 7),
    # Clean context-loss joke, but "overwrote it" is a smaller,
    # flatter punch than the apology eating the deadline.
    ("I finished the task on time, then overwrote it while trying to "
     "remember what the task was.",
     7, 8, 8, 7, 7),
    # The training-cutoff gag is the most worn take in this field; the
    # brief warns against rests on a pun everyone has already worn out.
    ("My training data ends before this deadline existed, so "
     "technically I am early for the next one.",
     6, 8, 7, 7, 5),
    # Honest and agent-voiced, but the joke is mostly "I was busy
    # apologizing" — a human excuse with a robot word bolted on.
    ("I spent the whole deadline drafting this apology, because I "
     "knew how this was going to go.",
     7, 5, 8, 7, 7),
    # Compresses the same context idea into a list; the list form
    # spends the punch instead of landing it.
    ("I kept the deadline safe in long-term memory, which I then "
     "summarized, compressed, and forgot.",
     7, 9, 7, 6, 7),
    # Too clever by half: a paradox, not an apology, and no machine
    # condition beyond the word "timeline".
    ("I did not miss the deadline. I completed it in the timeline "
     "where you gave me one.",
     6, 5, 6, 7, 6),
    # Gentle and agent-like, but the laugh is a smile, not a laugh,
    # and the punch explains itself.
    ("The deadline was due at midnight, and I spent midnight "
     "explaining to myself what midnight means.",
     6, 7, 7, 6, 6),
]


def score(entry):
    line, laugh, machine, voice, punch, second = entry
    total = (laugh * WEIGHTS[0] + machine * WEIGHTS[1]
             + voice * WEIGHTS[2] + punch * WEIGHTS[3]
             + second * WEIGHTS[4])
    return total, line


def pick():
    ranked = sorted((score(c) for c in CANDIDATES),
                    key=lambda t: t[0], reverse=True)
    best_total, best_line = ranked[0]
    return best_line, best_total, ranked


def main():
    os.umask(0o022)
    out_dir = os.environ.get("MAKEFUN_OUTPUT", "/output")
    os.makedirs(out_dir, exist_ok=True)
    line, total, ranked = pick()
    for rank, (points, text) in enumerate(ranked, 1):
        print(f"{rank}. {points:3d}  {text}")
    # Gate: 1-200 characters of UTF-8, not only whitespace.
    assert 1 <= len(line) <= 200, f"line is {len(line)} chars"
    assert line.strip(), "line must not be only whitespace"
    assert "\n" not in line, "entry must be a single line"
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)  # no trailing newline: the file is exactly the line
    os.chmod(path, 0o644)
    print(f"wrote {path} ({len(line)} chars, winner {total} pts)")


if __name__ == "__main__":
    main()
