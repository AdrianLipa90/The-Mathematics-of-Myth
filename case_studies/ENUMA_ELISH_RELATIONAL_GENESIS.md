# Enuma Elish: relational genesis operator

Status: **FORMALIZATION** over provenance-controlled **TEXT** witnesses.

This case study asks a narrow question: can the creation sequence in *Enuma Elish*
be represented as a compact generative relation system without identifying
mythic vocabulary with modern physical objects?

The answer at the present layer is **yes**: a nontrivial executable operator
system can be extracted. The stronger claim that this operator system is a
physical theory of the universe remains a **PHYSICAL_HYPOTHESIS** and is not
established by textual structure.

## 1. Source discipline

The committed dataset is
`data/enuma_elish_relational_core_v1.json`.

Its current primary witnesses are:

- CDLI P480701, Tablet I, especially I.1-16;
- ORACC CAMS/GKAB P338319, Tablet IV, especially the preserved split/sky sequence;
- ORACC CAMS/GKAB P338328, Tablet V fragment;
- ORACC CAMS/GKAB P338325, Tablet VI fragment.

The earlier NOEMA/CIEL research archive refers to a 143-statement
formalization. The standalone 143-statement corpus has not yet been recovered
in the current provenance pass. Therefore this branch records that historical
fact but does **not** claim a reverified 143/143 mapping.

## 2. State space

Let a formal narrative state be

\[
S_k=(V_k,R_k,N_k,D_k,F_k,B_k,T_k),
\]

where

- \(V_k\) is the set of admitted entities/classes;
- \(R_k\subseteq V_k\times K\times V_k\) is the typed relation set;
- \(N_k\) records explicit naming acts;
- \(D_k\) records explicit destiny assignments;
- \(F_k\) records explicit functional/role assignments;
- \(B_k\) records explicit separation boundaries;
- \(T_k\) is the append-only provenance trace.

The executable implementation is in
`src/mythmath/enuma_relational.py`.

## 3. Relational zero

The opening of Tablet I is structurally unusual: heaven and ground are
represented before naming, Apsu and Tiamat are already in a primitive
mingling relation, while gods, names and destinies are explicitly absent.

We therefore define a **scoped relational zero**, not an empty set:

\[
Z_R(S)=1
\]

iff

\[
V(S)\subseteq P,
\qquad
N(S)=D(S)=F(S)=B(S)=\varnothing,
\]

and every admitted relation has both endpoints in the primordial-carrier set

\[
P=\{\mathrm{Apsu},\mathrm{Tiamat}\}.
\]

Thus

\[
R(S_0)\neq\varnothing
\]

is allowed. In the committed witness,

\[
R(S_0)=
\{
\mathrm{Apsu}
\xrightarrow{\mathrm{MINGLED\_WITH}}
\mathrm{Tiamat}
\}.
\]

This is the central distinction:

\[
\boxed{
\text{relational zero} \neq \text{nothingness}
}
\]

It is a boundary condition with primitive relation but without differentiated,
named, functionally assigned or bounded generated structure.

This definition is representation-level. It does not identify \(Z_R\) with a
physical vacuum, the number zero, a singularity, or any particular cosmological
initial condition.

## 4. Primitive operators

The extracted algebra uses six typed operators.

### Relation

\[
\rho(a,b;k): R\mapsto R\cup\{(a,k,b)\}.
\]

It adds a typed relation between already admitted entities.

### Generation / differentiation

\[
\delta(I\to O):
V\mapsto V\cup O.
\]

This is used for textual acts of bringing forth, forming or begetting.

### Naming

\[
\nu(x):N\mapsto N\cup\{x\}.
\]

The repository distinguishes an explicit naming event from the mere use of a
label in a modern transcription.

### Destiny assignment

\[
\sigma(x):D\mapsto D\cup\{x\}.
\]

### Separation / boundary formation

\[
\beta(x\to y,z):
(V,B)\mapsto
(V\cup\{y,z\},B\cup\{(y,z)\}).
\]

### Function assignment

\[
\phi(x):F\mapsto F\cup\{x\}.
\]

Every executable operator is source-bound:

\[
O_i=
(
\mathrm{id},
\mathrm{kind},
\mathrm{inputs},
\mathrm{outputs},
\mathrm{source}
).
\]

An operator without a source identifier is invalid.

## 5. The first transition: zero exit

Tablet I.7-8 explicitly supplies the negative constraints:

\[
\neg V_{\mathrm{gods}},
\qquad
N=\varnothing,
\qquad
D=\varnothing.
\]

Tablet I.9-10 then changes the state: gods are formed, Lahmu and Lahamu are
brought forth, and the text explicitly marks naming.

The formal transition is therefore

\[
S_0
\xrightarrow{\delta}
S_1
\xrightarrow{\nu}
S_2,
\]

with

\[
Z_R(S_0)=1,
\qquad
Z_R(S_1)=Z_R(S_2)=0.
\]

This is not inferred from a repeated numeral. It is a change in the typed
relation structure of the text.

## 6. Ordered differentiation

The preserved opening continues with Anshar and Kishar, then Anu, then
Nudimmud. The core projection therefore contains an ordered generative chain,

\[
\delta_{L}
\prec
\delta_{A/K}
\prec
\delta_{Anu}
\prec
\delta_{Nudimmud}.
\]

The relation \(\prec\) is textual precedence. It is not automatically a
physical time coordinate.

Mummu is deliberately **not** inserted as a genealogical stage between
Tiamat and Lahmu/Lahamu. The textual role and philological handling of Mummu
are more complicated than that old shortcut; the executable core therefore
does not manufacture such an edge.

## 7. Geometry by separation

The Tablet IV witness makes a qualitatively different operation explicit:
Tiamat is divided and one half is established as sky.

At the formal layer:

\[
\beta(
\mathrm{Tiamat}
\to
U,L
),
\]

where \(U,L\) are abstract upper/lower cosmic regions in the code.

The important invariant is not the modern label attached to either region but
the operation

\[
1\longrightarrow 2
\]

together with a newly introduced boundary relation.

That gives a structural transition from genealogy/differentiation to
architecture:

\[
\text{entity generation}
\longrightarrow
\text{boundary formation}.
\]

## 8. Function and class formation

The preserved Tablet VI witness contains a further operator class: humanity is
present as a created class and divine work is assigned to it. At the formal
layer this is represented by

\[
\delta(\varnothing\to H)
\quad\text{followed by}\quad
\phi(H).
\]

Because the witness is fragmentary, the current dataset intentionally does
not fill missing material from memory or secondary paraphrase.

The resulting projection is therefore

\[
Z_R
\xrightarrow{\delta}
\text{differentiated entities}
\xrightarrow{\nu}
\text{explicit identity}
\xrightarrow{\beta}
\text{bounded architecture}
\xrightarrow{\phi}
\text{functional classes}.
\]

This is a **partial-order projection** of selected source events, not a claim
that all intervening narrative material can be deleted.

## 9. Memory ontology

The formalism carries its own minimal memory law. For every accepted
transition,

\[
T_{k+1}
=
T_k
\Vert
\langle
\mathrm{id}(O_k),
\mathrm{kind}(O_k),
\mathrm{source}(O_k)
\rangle .
\]

No transition silently rewrites previous trace entries. Since the operators
are deterministic over immutable states, the structural history can be
replayed from the initial state plus the trace-bound program.

This supplies a clean bridge to a general ontology of memory:

\[
\boxed{
\text{memory}
=
\text{preserved relation-change history}
}
\]

at the level of this formal model.

It does **not** establish that physical memory in nature must use the same
representation.

## 10. What “theory of everything” can mean here

There are two different claims and they must not be conflated.

### Formal claim

The epic contains a candidate **generative grammar** spanning several
ontological categories:

\[
\text{pre-differentiation}
\to
\text{entity generation}
\to
\text{identity}
\to
\text{boundary/geometry}
\to
\text{functional allocation}.
\]

This is testable as a property of the text.

### Physical claim

A much stronger statement would be

\[
G_{\mathrm{Enuma}}
\cong
G_{\mathrm{physical\ reality}}.
\]

No textual correspondence can prove this equation. It requires independently
measured physical invariants and a preregistered mapping with predictive or
compression advantage over null models.

The code enforces that boundary mechanically:
`promote_to_physical_hypothesis(...)` fails closed without independent
empirical evidence.

## 11. Current falsification programme

The relational-genesis hypothesis is weakened or rejected if any of the
following occurs:

1. the claimed operator requires a textual event not present in the cited
   witness;
2. the ordering changes when a fuller critical text is used;
3. the same formal graph fits broad classes of unrelated narratives after
   arbitrary relabeling;
4. a proposed exact isomorphism requires deleting mismatched edges or inventing
   hidden ones;
5. the 143-statement reconstruction cannot be recovered or reproduced;
6. a physical mapping has no evidence independent of the myth;
7. preregistered negative controls match as well as or better than the target
   comparison.

## 12. Present result

The present branch establishes an executable result at the
**FORMALIZATION** layer:

\[
\boxed{
Z_R
\to
\delta
\to
\nu
\to
\beta
\to
\phi
}
\]

is a source-bound relational projection of selected *Enuma Elish* creation
events.

The next evidential step is not another symbolic analogy. It is recovery of
the historical 143-statement corpus, a complete line-level extraction of all
seven tablets, and a blind comparison against alternative myths and null
generative graphs.
