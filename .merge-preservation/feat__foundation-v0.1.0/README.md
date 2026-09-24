# The Mathematics of Myth

A formal-methods project for extracting, representing, and testing mathematical structure in mythic and prophetic texts without collapsing textual interpretation into claims about physical reality.

## Core rule

Every result is typed into one of three layers:

1. **TEXT** — what the source explicitly states.
2. **FORMALIZATION** — a mathematical representation or derivation from the stated structure.
3. **PHYSICAL_HYPOTHESIS** — an empirical claim about the world. This layer requires evidence independent of textual resemblance.

The repository is designed to keep those layers mechanically separable.

## Initial scope

The first implementation provides:

- a deterministic half-turn detector for paired cyclic sequences;
- a provenance-preserving data record for the solar portal sequence in *1 Enoch* 72;
- a worked complex-carrier derivation for that sequence;
- a taxonomy for temporal/prophetic interpretations that distinguishes ordinary forward causation, self-fulfilling effects, retrodiction, global-consistency models, and genuine retrocausal candidates;
- tests for the mathematical invariants used by the case study.

The project does **not** treat structural similarity as proof that an ancient author possessed modern mathematical notation, nor as proof of paranormal or retrocausal physics.

## Reproducible check

```text
python -m unittest discover -s tests -v
```

## Status

`v0.1-foundation` — research scaffold. No physical retrocausality claim is established by this repository.
