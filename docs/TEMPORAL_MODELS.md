# Temporal Models for Prophecy Claims

This document defines analysis classes. It does not assert that any class is physically realized.

Let \(E_0\) be an earlier encoding, \(A_1\) an agent's later exposure to that encoding, and \(F_2\) a still-later event.

## Forward-causal model

\[
E_0 \rightarrow A_1 \rightarrow F_2.
\]

The earlier text influences later behavior. No backwards-in-time information flow is required.

## Self-fulfilling model

A special forward-causal case in which knowledge of the prediction materially contributes to the predicted outcome.

## Retrodictive model

Later evidence is used to infer an earlier hidden state:

\[
F_2 \rightarrow \widehat{X_0}
\]

as an inference performed at the later time. This is not physical backwards causation.

## Global-consistency model

The history is represented by a joint constraint over events,

\[
P(E_0,F_2),
\]

without assuming a local signal from \(F_2\) to \(E_0\). A block-time or boundary-value interpretation can fall in this class.

## Retrocausal candidate

The strong claim is that information available only at the later boundary affects the earlier encoding:

\[
I(F_2) \rightarrow E_0.
\]

To classify an observation as evidence for this model, ordinary information leakage, later editing, selection effects, ambiguous matching, and self-fulfilling influence must first be excluded.

## Bootstrap loop

A closed informational loop can be written

\[
I_{future}\rightarrow I_{past}\rightarrow I_{future}.
\]

This representation exposes the familiar provenance question: where does the information originate? The equation is a model of the paradox, not evidence that such loops occur physically.
