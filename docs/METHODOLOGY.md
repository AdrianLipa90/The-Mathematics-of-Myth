# Methodology

## 1. Extraction before interpretation

For each passage, record the source location and extract only explicit entities, actions, orderings, counts, cycles, gates, transformations, records, or constraints. Do not begin by mapping the text onto a preferred modern theory.

A minimal operator record is:

\[
O=(\text{id},\text{domain},\text{inputs},\text{action},\text{outputs},\text{constraints},\text{source}).
\]

## 2. Three-layer epistemic typing

### TEXT
A statement or datum explicitly present in the source.

### FORMALIZATION
A representation derived from TEXT. Examples include graphs, permutations, involutions, cyclic groups, complex embeddings, or information-flow diagrams.

### PHYSICAL_HYPOTHESIS
A statement asserting that the formalization describes real physical dynamics. Such a claim is not promoted from FORMALIZATION without independent evidence.

## 3. Candidate isomorphisms

A structural match must be scored on relations rather than vocabulary. At minimum compare:

- node roles;
- directed edge types;
- operation order;
- multiplicities;
- invariants;
- forbidden or missing relations.

Shared nouns alone do not establish isomorphism.

## 4. Negative controls

Whenever a candidate structure is identified, compare it with at least one alternative representation that could plausibly fit the same text. Prefer predeclared scoring rules and preserve failures.

## 5. Temporal claims

A text that precedes a later event does not by itself demonstrate retrocausality. The project keeps distinct:

\[
\text{prediction},\quad
\text{self-fulfilling influence},\quad
\text{retrodiction},\quad
\text{global consistency},\quad
\text{retrocausal information transfer}.
\]

Only the final class requires evidence that cannot be explained by ordinary forward causal access, selection, or post-hoc fitting.

## 6. Provenance

Every numerical dataset must identify the passage or edition from which it was extracted. Derived values should be reproducible from committed data and code.
