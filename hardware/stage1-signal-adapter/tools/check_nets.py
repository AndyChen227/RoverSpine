#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare a KiCad netlist against an expected net map, as a string comparison.

Why this exists: ERC checks structure, not intent. It verifies that nothing
dangles and every power rail has a driver, and it stays silent if PWM1 and PWM2
are swapped onto each other's connector pins — two nets, two pins each, no
violation, reversed motors. See
docs/devlog/2026-09-12-revA-schematic-complete.md.

So the net membership is compared against a written-down map instead of being
read by eye. Usage:

    python check_nets.py ../kicad/RoverSpine_Signal_Adapter_RevA.net \
                         revA_expected_nets.json

Exit status is 0 when everything matches and 1 otherwise, so it can gate a
commit. Standard library only, no KiCad installation required.
"""

import json
import re
import sys


# --------------------------------------------------------------------------
# A minimal S-expression reader. The netlist format is regular enough that a
# regex would work; a real parser is used anyway because a wrong answer here
# looks exactly like a wiring error, which is the one thing this must not do.
# --------------------------------------------------------------------------

TOKEN = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+')


def parse_sexp(text):
    stack = [[]]
    for tok in TOKEN.findall(text):
        if tok == "(":
            stack.append([])
        elif tok == ")":
            done = stack.pop()
            stack[-1].append(done)
        elif tok.startswith('"'):
            stack[-1].append(tok[1:-1])
        else:
            stack[-1].append(tok)
    if len(stack) != 1:
        raise ValueError("unbalanced parentheses in netlist")
    return stack[0][0]


def find(node, key):
    """All direct children of `node` that are lists headed by `key`."""
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def value(node, key, default=None):
    hits = find(node, key)
    if not hits or len(hits[0]) < 2:
        return default
    return hits[0][1]


# --------------------------------------------------------------------------
# Reading the netlist into {net name: set of node labels}
# --------------------------------------------------------------------------

def node_label(ref, pin, pin_agnostic_prefixes):
    """How one connection is written for comparison.

    Connector pins are compared as REF-PIN, because which physical pin a signal
    lands on is the entire point of this board.

    Two-pin passives are compared as REF alone. A resistor is symmetric, so
    which of its pads is pin 1 depends on how the symbol happens to be rotated
    on the sheet. Demanding a particular pin number there would check the
    drawing's orientation rather than the circuit, and would fail a schematic
    that is electrically correct. Wiring a resistor between the wrong two nets
    is still caught: it goes missing from one net and appears in another.
    """
    for prefix in pin_agnostic_prefixes:
        if ref.startswith(prefix):
            return ref
    return "%s-%s" % (ref, pin)


def read_netlist(path, pin_agnostic_prefixes):
    with open(path, encoding="utf-8") as fh:
        root = parse_sexp(fh.read())

    nets_sections = find(root, "nets")
    if not nets_sections:
        raise SystemExit("no (nets ...) section in %s — is it a KiCad netlist?" % path)

    nets = {}
    for net in find(nets_sections[0], "net"):
        name = value(net, "name", "")
        # Local labels carry the sheet path ("/PWM1"); power symbols are global
        # and carry none ("GND"). Irrelevant on a single sheet, so normalise it
        # away — but it will matter as soon as there are hierarchical sheets.
        name = name.lstrip("/")
        members = set()
        for nd in find(net, "node"):
            members.add(node_label(value(nd, "ref", "?"),
                                   value(nd, "pin", "?"),
                                   pin_agnostic_prefixes))
        nets[name] = members
    return nets


# --------------------------------------------------------------------------
# The comparison
# --------------------------------------------------------------------------

def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2

    netlist_path, expected_path = argv[1], argv[2]

    with open(expected_path, encoding="utf-8") as fh:
        spec = json.load(fh)

    prefixes = tuple(spec.get("pin_agnostic_prefixes", ["R"]))
    expected = {k: set(v) for k, v in spec["nets"].items()}
    expected_unconnected = spec.get("expected_unconnected")

    actual = read_netlist(netlist_path, prefixes)

    print("board:    %s" % spec.get("board", "?"))
    print("source:   %s" % spec.get("source", "?"))
    print("netlist:  %s" % netlist_path)
    print("")

    failures = []
    width = max(len(n) for n in expected)

    for name in sorted(expected):
        want = expected[name]
        got = actual.get(name)
        if got is None:
            print("[MISSING] %-*s  net does not exist in the netlist" % (width, name))
            failures.append(name)
            continue
        if got == want:
            print("[PASS]    %-*s = %s" % (width, name, " ".join(sorted(want))))
            continue
        print("[FAIL]    %s" % name)
        print("            expected: %s" % " ".join(sorted(want)))
        print("            actual:   %s" % " ".join(sorted(got)))
        missing = want - got
        extra = got - want
        if missing:
            print("            missing:  %s" % " ".join(sorted(missing)))
        if extra:
            print("            extra:    %s" % " ".join(sorted(extra)))
        failures.append(name)

    # Single-pin nets are unconnected pins. On a connector that is expected
    # behaviour, not a defect, so the count is checked rather than the report
    # being cleaned up with no-connect flags.
    singles = [n for n, m in actual.items() if len(m) == 1 and n not in expected]

    # A net KiCad had to invent a name for is a net with no label on it.
    unnamed = [n for n in actual
               if n.startswith("Net-(") or n.startswith("unconnected-(")]
    unnamed = [n for n in unnamed if len(actual[n]) > 1]

    extras = [n for n in actual
              if n not in expected and len(actual[n]) > 1
              and n not in unnamed]

    print("")
    print("single-pin unconnected nets: %-4d (expected %s)"
          % (len(singles),
             "any" if expected_unconnected is None else expected_unconnected))
    print("unexpected extra nets:       %d" % len(extras))
    print("auto-named (unlabelled) nets: %d" % len(unnamed))

    if extras:
        print("")
        for n in sorted(extras):
            print("  [EXTRA]   %s = %s" % (n, " ".join(sorted(actual[n]))))
    if unnamed:
        print("")
        for n in sorted(unnamed):
            print("  [UNNAMED] %s = %s" % (n, " ".join(sorted(actual[n]))))
            print("            a net with more than one pin and no label on it")

    count_ok = (expected_unconnected is None
                or len(singles) == expected_unconnected)
    if not count_ok:
        print("")
        print("  unconnected-pin count does not match. Every violation on this")
        print("  board is supposed to reconcile exactly; an unexplained one is")
        print("  the thing to chase.")

    ok = not failures and not extras and not unnamed and count_ok
    print("")
    print("RESULT: %s" % ("ALL PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
