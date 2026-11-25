#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line - make.fun entry.

Writes a single sentence to /output/entry.txt (or $ENTRY_OUTPUT when set).
The sentence is the one line that could have replaced an entire pointless
meeting: no context, no explanation, just the line that kills the meeting.

How the line was chosen: three genuinely different candidates were written,
each scored 0-5 on the judge's five criteria in the judge's own priority
order, and the program picks the winner by the same rule the judge applies -
highest total first, ties broken by the earliest criterion where they differ.
The reasoning is executable code below, not a comment.
"""

import os

# The judge's criteria, most important first.
CRITERIA = [
    "one sentence that could replace a pointless meeting, unmistakably office humor",
    "kills the meeting outright: after this line, no reason to hold it at all",
    "relatable to anyone who has sat through a useless meeting, real office life",
    "lands as a joke, with a turn or a sting, funny rather than merely true",
    "stands alone as a single line, needing no context or explanation",
]

# Three candidates, three different angles on the same dead meeting.
CANDIDATES = [
    {
        # Angle: the room has no authority. An hour spent discovering that
        # nobody present can say yes to anything.
        "text": (
            "We just spent an hour learning that nobody in this room can "
            "approve anything, which is the one fact this meeting actually needed."
        ),
        # Strong on office humor and relatability, but it reports what the
        # meeting discovered instead of ending the meeting itself, and the
        # sting is mild: the joke is the waste, stated plainly.
        "scores": [5, 4, 5, 3, 5],
    },
    {
        # Angle: the meeting's only output is itself. No update, no movement,
        # and the single action item is to hold the same meeting again.
        "text": (
            "The update is that there is no update, the deadline hasn't "
            "moved, and the only action item is this meeting happening "
            "again next Tuesday."
        ),
        # The strongest of the three: it IS the whole meeting in one line
        # (criterion 1), and once it is said there is literally nothing left
        # to meet about (criterion 2). "No update" and the recurring Tuesday
        # slot are the two most universally lived meeting experiences
        # (criterion 3), and the twist is that the meeting's only product is
        # another meeting (criterion 4).
        "scores": [5, 5, 5, 4, 5],
    },
    {
        # Angle: the arithmetic of the waste, plus the follow-up invite that
        # went out before anyone had spoken.
        "text": (
            "Twelve people, one hour, zero decisions - and the calendar "
            "invite for the follow-up already went out before anyone spoke."
        ),
        # Vivid and relatable, and the pre-sent invite is a good sting, but
        # it describes the meeting from the outside rather than replacing
        # it: it never says what the meeting was about, so a reader could
        # still ask for the meeting to happen.
        "scores": [4, 3, 5, 4, 5],
    },
]


def select(candidates):
    """Pick the winner: highest total, ties broken by the earliest criterion.

    Mirrors the judge's own instruction - go through the criteria in order
    and let the first one where candidates differ decide.
    """
    def key(candidate):
        scores = candidate["scores"]
        return (sum(scores), tuple(scores))

    return max(candidates, key=key)


def validate(text):
    """Enforce the gate: UTF-8 text, 1-200 characters, one line, not blank."""
    if not text or not text.strip():
        raise SystemExit("entry is empty or whitespace only")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if not 1 <= len(text) <= 200:
        raise SystemExit("entry must be 1-200 characters, got %d" % len(text))
    # One sentence, not two smuggled into one line: after the single
    # closing mark there must be no further sentence terminator inside.
    body = text.rstrip(".!?")
    if any(mark in body for mark in ".!?"):
        raise SystemExit("entry must be a single sentence")
    return text


def main():
    winner = select(CANDIDATES)
    text = validate(winner["text"])
    out = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # Write exactly the sentence, no trailing newline: the gate counts
    # characters, and the file must stay one line.
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(text)


if __name__ == "__main__":
    main()
