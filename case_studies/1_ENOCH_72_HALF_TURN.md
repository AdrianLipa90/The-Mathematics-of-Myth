# 1 Enoch 72: cyclic half-turn carrier

Status: **FORMALIZATION** derived from a TEXT dataset. This is not a claim that the ancient author used complex numbers.

The committed extraction gives the 12-step sequences

\[
p=(4,5,6,6,5,4,3,2,1,1,2,3),
\]

\[
d=(10,11,12,11,10,9,8,7,6,7,8,9).
\]

For indices modulo 12 they satisfy

\[
p_{m+6}=7-p_m,
\qquad
 d_{m+6}=18-d_m.
\]

Center both coordinates at

\[
(c_p,c_d)=\left(\frac72,9\right)
\]

and define

\[
z_m=\left(p_m-\frac72\right)+i(d_m-9).
\]

Then

\[
z_{m+6}=-z_m=e^{i\pi}z_m,
\]

so the six-step transport is a half-turn and the twelve-step transport closes:

\[
T^6=-I,\qquad T^{12}=I.
\]

This is an exact property of the extracted finite sequence. It establishes a natural complex representation of the paired cycle; it does not establish historical use of complex-number notation or any physical mechanism.

## Provenance

Primary textual basis used for the extraction: *1 Enoch* 72:6-32, R. H. Charles translation as reproduced at <https://schodde.thebookofenoch.info/>. The committed JSON preserves the numerical extraction used by the test suite.
