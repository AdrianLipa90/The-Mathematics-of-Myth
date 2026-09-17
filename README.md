# The Mathematics of Myth

A falsifiable comparative programme for extracting mathematical structure from mythic narratives without treating numerical resemblance as evidence by itself.

## Current research object

The first formal candidate is the ordered creation/closure pattern

\[
123\mid45\mid6\rightarrow7
\]

with active block lengths

\[
3\mid2\mid1\rightarrow0.
\]

The working interpretation is deliberately weak:

- `3` — candidate local transition threshold;
- `6` — candidate global closure/horizon;
- `7` — post-closure / cessation state;
- celestial "day" — candidate cycle-completion operator, not assumed to be 24 h.

These are hypotheses to test, not conclusions.

Current stress-test status: no full cross-cultural `3|2|1->0` isomorphism has been verified. Stronger projected relations have emerged for (i) a three-interval liminal threshold, and (ii) a six-to-seven active/cessation boundary. `data/relations.json` records the scope and downgrade conditions for each comparison.


## Method

Each comparison is processed in this order:

1. **Primary evidence** — establish what the source actually says.
2. **Provenance tier** — canonical/primary, ancient exegesis, later ritual tradition, or modern comparison.
3. **Event graph** — convert the narrative to ordered states and typed transitions.
4. **Relation class** — exact isomorphism, order-homomorphism, analogy, or unsupported number-match.
5. **Falsification** — actively search for mismatches and chronology problems.

This order follows the current GREMLIN candidate routing: `OWL` (primary-evidence methodology) before `SPIDER` (structural relation/dependency). GREMLIN outputs are candidate-only and never override source evidence.

## Repository layout

- `paper/main.tex` — buildable LaTeX note.
- `paper/sections/formal_transition_operator.tex` — formal core.
- `src/mythmath/transition.py` — executable definitions.
- `tests/test_transition.py` — falsification-oriented unit tests.
- `data/evidence.json` — provenance-controlled evidence registry.

## Epistemic rule

A repeated number is not an isomorphism.

\[
\text{number match} \not\Rightarrow \text{structural equivalence}.
\]

Amaterasu is an explicit guard case: the cave/emergence motif is old, but the specific "three days and three nights" duration used here is attested in a later blind-biwa ritual tradition, not in the oldest *Kojiki* account. The tests prevent that later datum from being silently promoted to canonical evidence.
