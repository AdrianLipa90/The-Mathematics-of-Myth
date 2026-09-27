# Mayor Formalism v0.1

Status: **FORMALIZATION_CANDIDATE**

Purpose: formalize the cross-disciplinary method visible in Adrienne Mayor's
research without assuming that myth is literal history, without treating
similarity as identity, and without importing a physical theory into the
source material.

The current evidence registry is
`data/mayor_research_cases_v0_1.json`; the executable core is
`src/mythmath/mayor_transform.py`.

## 1. Research scope

The current formalization is built from Mayor's documented research programme:

- geomythology and natural knowledge in myth and oral tradition;
- *Mythopedia* and cultural memory of natural events;
- the Styx/Mavroneri geomyth tested against geology and toxicology;
- ancient artificial beings and technological imagination;
- Amazons/Scythia across literature, art and archaeology;
- representation of extraordinary bodies and mythic creatures;
- ancient observations of animal self-medication.

These are treated as separate case families sharing a common methodological
question: **which relations survive comparison between a cultural
representation and evidence obtained through an independent channel?**

## 2. Mayor Transform

Let (E) denote a source phenomenon, event, practice, organism or material
configuration. Let (C) denote cultural transmission conditions and let (M)
denote the surviving narrative or representation.

We write only the forward abstraction

[
M=mathcal{T}(E,C).
]

No assumption is made that (mathcal{T}) is invertible, information-destroying,
or entropy-producing. In particular, v0.1 does **not** assume a lossy channel.

The reconstruction problem uses an independently acquired evidence set (X):

[
(M,X)longrightarrow mathcal{H},
]

where (mathcal{H}={H_1,ldots,H_n}) is a set of competing hypotheses.

The formal target is therefore not

[
MRightarrow E,
]

but constraint comparison:

[
H_jmodels C_Mland C_X.
]

A hypothesis that satisfies all preregistered constraints is marked
`INDEPENDENTLY_CONSTRAINED`; this status does not mean "proved."

## 3. Evidence separation

Every evidence item is assigned a type and an independence flag.

The principal boundary is

[
D=D_{m narrative}oplus D_{m independent}.
]

For empirical reconstruction, a narrative datum cannot count as its own
independent confirmation.

The executable gate therefore requires at least one independent, non-textual
evidence item before a candidate can obtain the
`INDEPENDENTLY_CONSTRAINED` status.

## 4. Name-independent relation signatures

A narrative and an independent dataset are converted to relation signatures

[
r=(s,k,t,o),
]

where

- (s) is a normalized source role;
- (k) is the relation type;
- (t) is a normalized target role;
- (o) is optional sequence order.

For example,

[
(mathrm{WATER_SOURCE},
mathrm{CAUSES},
mathrm{TOXIC_EFFECT},
1)
]

can be compared across a textual graph and a toxicological/geological graph
without requiring identical proper nouns.

The v0.1 implementation performs **exact comparison after normalization**.
It does not silently rename nodes, delete inconvenient edges, or search for a
desired graph isomorphism.

## 5. Retained invariants

Given a narrative relation graph (G_M) and an independent relation graph
(G_X), define

[
I(M,X)=E(G_M)cap E(G_X).
]

These are the retained relation invariants recoverable in both channels.

For descriptive diagnostics v0.1 computes

[
P=rac{|I|}{|E(G_M)|},
qquad
R=rac{|I|}{|E(G_X)|},
]

and

[
J=
rac{|I|}
{|E(G_M)cup E(G_X)|}.
]

These are overlap measures, not probabilities that a myth is historically
true.

## 6. Negative controls and specificity

A structural match is weak if unrelated comparison narratives fit equally
well. Therefore each domain should include preregistered negative controls.

For target graph (G_T), independent graph (G_X), and controls
(G_{C_i}), define

[
oxed{
Delta_{m spec}
=
J(G_T,G_X)
-
max_i J(G_{C_i},G_X)
}.
]

A positive value means only that the target is more structurally specific than
the supplied controls. It does not establish causal transmission.

## 7. Domain A: geomythology and Mythopedia

A natural-event case can be represented by an event signature

[
mathcal{E}
=
(lambda,	au,p,m,d,r),
]

where

- (lambda): location;
- (	au): temporal constraints;
- (p): process class, e.g. eruption, tsunami, impact, toxic lake;
- (m): motion or transformation pattern;
- (d): observable damage/effects;
- (r): persistent material residue or environmental constraint.

The research question becomes:

[
I_{m geo}
=
I(G_{m narrative},G_{m geology}).
]

The strongest cases are those in which several ordered relations survive and
where the same matching procedure performs worse on negative controls.

## 8. Domain B: Styx/Mavroneri

Mayor's 2025 paper explicitly proposes three hypotheses while emphasizing that
proof remains elusive. The formalism therefore treats Styx as a
constraint-satisfaction problem, not as a solved identification.

Let

[
D_{m Styx}
=
D_Toplus D_Goplus D_{m tox}oplus D_H,
]

for textual, geological, toxicological and historical evidence.

Candidate hypotheses are evaluated independently against each block:

[
H_jmodels
C_Tland C_Gland C_{m tox}land C_H.
]

Failure of any preregistered necessary constraint lowers or rejects that
candidate rather than being repaired by narrative reinterpretation.

This case is the reference implementation for the evidence-independence gate.

## 9. Domain C: ancient artificial beings

Represent an artificial-being narrative as an agent architecture

[
mathcal{A}
=
(B,S,A,G,C,V),
]

where

- (B): constructed body/substrate;
- (S): sensing or information intake;
- (A): action/actuation;
- (G): assigned goal or policy;
- (C): creator/control relation;
- (V): vulnerability, termination or failure condition.

This avoids the binary and historically loaded question "is Talos AI?".
Instead the test asks which agent relations are actually present in the
source and which are absent.

Negative controls should include magical or heroic beings that exhibit power
but lack artificial-construction and control relations.

## 10. Domain D: Amazons and Scythia

This domain requires a multiplex spatiotemporal evidence graph

[
G_A=(V,E,lambda,	au,sigma),
]

where

- (lambda(v)) is location;
- (	au(v)) is date/range;
- (sigma(v)) is evidence channel.

Useful node classes include

[
V=
V_{m text}
cup
V_{m image}
cup
V_{m burial}
cup
V_{m weapon}
cup
V_{m osteology}.
]

The critical methodological guard is that archaeological classification is
not inferred from literary expectation and then reused as "independent"
confirmation.

## 11. Domain E: extraordinary bodies and monsters

Mayor's 2026 work on baby monsters and centaur families suggests a measurable
representation/reception problem.

Let the visual/social feature vector be

[
x=
(x_{m infant},
x_{m family},
x_{m nurturing},
x_{m humanlike},
x_{m threat},
ldots),
]

and the reception vector

[
y=
(y_{m fear},
y_{m disgust},
y_{m awe},
y_{m curiosity},
y_{m sympathy},
y_{m empathy}).
]

The research task is to estimate a mapping

[
f:xmapsto y
]

from coded artifacts and texts, while controlling for period, medium and
cultural context.

A useful negative control is a matched representation without infant,
family or nurturing cues.

## 12. Domain F: animal self-medication

Represent each behavioral report as

[
Z=
(mathrm{species},
mathrm{substance},
mathrm{behavior},
mathrm{context},
mathrm{outcome}).
]

Ancient textual reports and modern zoological observations can then be
compared at the relation-signature level.

The target is not to infer that an ancient author possessed modern
pharmacology. It is to test whether behaviorally specific observations are
preserved.

## 13. Shared mathematical core

Across the six case families the common pipeline is

[
oxed{
mathrm{source representation}
ightarrow
mathrm{typed relation graph}
ightarrow
mathrm{independent evidence graph}
ightarrow
mathrm{invariant extraction}
ightarrow
mathrm{negative controls}
ightarrow
mathrm{hypothesis constraints}.
}
]

This is the **Mayor Transform v0.1**.

The formalism is intentionally neutral about the ultimate mechanism of
cultural memory. No cosmological, quantum, IDT, TIR, or orbital-fractal
mechanism is assumed at this stage. Those models may only be compared later
against the extracted invariants.

## 14. Falsification rules

The formalization must be downgraded or rejected for a case if:

1. an asserted relation is absent from the cited source;
2. supposedly independent evidence was selected or classified from the target
   narrative itself;
3. the match requires post-hoc role relabeling not fixed before comparison;
4. sequence-sensitive relations only match after order information is removed;
5. preregistered negative controls match as well as or better than the target;
6. a required geological, archaeological, toxicological, zoological or
   historical constraint fails;
7. a structural overlap is promoted to historical identity or physical truth
   without a separate evidential bridge.

## 15. Current result

Version 0.1 establishes a reusable, executable comparison layer:

[
oxed{
(M,X)
mapsto
left(
I(M,X),
J(M,X),
Delta_{m spec},
mathrm{constraint status}
ight).
}
]

This turns Mayor's cross-disciplinary research style into a falsifiable
relation-graph programme while preserving the distinction between narrative
evidence, independent evidence, and interpretation.

The next empirical step is to encode one complete case at source level. Styx
is the strongest first target because the 2025 paper already states explicit
hypotheses, candidate mechanisms, limitations, and possible scientific tests.
