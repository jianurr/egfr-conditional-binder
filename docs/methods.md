# Challenge 1 (conditional EGFR binder): methods and design summary

## Summary
Nine single-chain designs (76 aa each). Two passed BindCraft's filters; six are histidine variants of the best one; one is a lower-confidence BindCraft design. Nothing was tested experimentally. No pH selectivity or mouse cross-reactivity was predicted computationally.

## Target and epitope
- Target: human EGFR extracellular region, domain III (mature residues 310-480), PDB 6ARU chain A, trimmed to domain III.
- Numbering: mature numbering = position in the competition page sequence (UniProt number minus 24). In the 6ARU file the chain A residue numbers equal mature numbers.
- EGFR residues within 4 Å of the cetuximab Fab in 6ARU (domain III), compared with the mouse sequence (Q01279, competition page sequence):

| Mature | Human | Mouse | Same? |
|---|---|---|---|
| 408 | Q | Q | yes |
| 409 | H | H | yes |
| 411 | Q | Q | yes |
| 412 | F | F | yes |
| 417 | V | V | yes |
| 418 | S | G | no |
| 438 | I | I | yes |
| 440 | S | S | yes |
| 441 | G | G | yes |
| 443 | K | R | no |
| 465 | K | K | yes |
| 466 | I | I | yes |
| 467 | I | M | no |
| 468 | S | N | no |
| 469 | N | N | yes |
| 471 | G | A | no |
| 473 | N | K | no |

- Hotspots given to BindCraft: 408, 409, 412, 465, 469 (conserved, highest atom-contact counts). Residues 467 and 468 were avoided because they differ in mouse.
- No cetuximab, panitumumab or other known binder sequence was used as a starting point.

## Generation
- Tool: BindCraft (AlphaFold2 backpropagation, ProteinMPNN, PyRosetta), Google Colab notebook.
- Settings: chain A, binder length 60-80, default design/prediction/interface/template protocols, Relaxed filters, 2 final designs requested.
- Compatibility patches were needed for newer JAX versions (jax.lib.xla_bridge and jnp.clip keyword names); these do not change the method.

## Designs
| Name | Description | His | i_pTM (BindCraft) | i_pAE |
|---|---|---|---|---|
| egfr_c1_01 | mpnn3, accepted | 1 | 0.85 | 0.17 |
| egfr_c1_02 | mpnn3 R11H | 2 | not computed | - |
| egfr_c1_03 | mpnn3 R11H K40H | 3 | not computed | - |
| egfr_c1_04 | mpnn3 K40H | 2 | not computed | - |
| egfr_c1_05 | mpnn3 Y14H | 2 | not computed | - |
| egfr_c1_06 | mpnn3 S38H | 2 | not computed | - |
| egfr_c1_07 | mpnn3 R11H Y14H K40H | 4 | not computed | - |
| egfr_c1_08 | mpnn1, accepted | 1 | 0.84 | 0.17 |
| egfr_c1_09 | mpnn9, scored but not in accepted set | 3 | 0.59 | 0.35 |

mpnn3 and mpnn1 come from one trajectory and are 74% identical. mpnn9 is on a different backbone (about 16% identity to mpnn1). Sequences are in submission_upload.csv.

## pH-switch hypothesis (untested)
- In the mpnn3 complex, His7 is 2.1 Å from EGFR Asp14 (numbering from 1 in the BindCraft output file; I infer this corresponds to mature D323).
- Binder residues within 6 Å of an EGFR Asp/Glu: His7 (Asp14), Arg11 (Asp35, Asp14), Tyr14 (Asp46), Ser38 (Glu163), Lys40 (Glu163).
- Idea: a protonated histidine can pair with the carboxylate at pH 6.5 and lose that contact at pH 7.4. Arg11 and Lys40 are positive at both pH values, so replacing them with histidine could make their contact pH dependent. Variants 02-07 test this.

## Limitations
- AlphaFold2-based folding does not model pH, so no pH selectivity was predicted.
- The histidine variants were not refolded or scored.
- No mouse cross-reactivity prediction was done.
- The target residue numbering in the BindCraft output was inferred and not independently verified.
- A residue-distance cutoff does not show whether an EGFR carboxylate is partly buried, which a pKa shift needs.
- Binding of all designs is untested.
