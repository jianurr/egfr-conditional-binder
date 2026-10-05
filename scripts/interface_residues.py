"""List EGFR residues touching the binder and binder residues near EGFR Asp/Glu.
Usage: python interface_residues.py design_complex.pdb [../data/egfr_targets.fasta]
Assumes chain A = EGFR domain III (renumbered from 1 by BindCraft, mature = index + 309
unless the file keeps original numbering) and chain B = binder."""
import sys
from Bio.PDB import PDBParser, NeighborSearch

pdb = sys.argv[1]
fasta = sys.argv[2] if len(sys.argv) > 2 else "../data/egfr_targets.fasta"
seqs, k = {}, None
for l in open(fasta):
    l = l.strip()
    if l.startswith(">"): k = l[1:]; seqs[k] = ""
    elif k: seqs[k] += l
human = [v for n, v in seqs.items() if n.startswith("human_EGFR_domIII")][0]
mouse = [v for n, v in seqs.items() if n.startswith("mouse_EGFR_domIII")][0]

m = PDBParser(QUIET=True).get_structure("x", pdb)[0]
A = [r for r in m["A"] if r.id[0] == " "]
first = A[0].id[1]
print("target first residue number:", first, "length:", len(A))

print("\n== EGFR residues within 4.5 A of the binder ==")
nsB = NeighborSearch(list(m["B"].get_atoms()))
for r in A:
    if any(nsB.search(a.coord, 4.5) for a in r):
        mat = r.id[1] + 309 if first < 310 else r.id[1]
        i = mat - 310
        h, mo = human[i], mouse[i]
        print(f"mature {mat} {r.get_resname()}  human {h} mouse {mo} {'' if h == mo else 'DIFFERS'}")

print("\n== binder residues within 6 A of EGFR Asp/Glu ==")
nsA = NeighborSearch(list(m["A"].get_atoms()))
for r in m["B"]:
    near = {}
    for a in r:
        for t in nsA.search(a.coord, 6.0):
            tr = t.get_parent()
            if tr.get_resname() in ("ASP", "GLU"):
                key = f"{tr.get_resname()}{tr.id[1]}"
                near[key] = min(near.get(key, 99), round(float(a - t), 1))
    if near:
        print(f"binder {r.get_resname()}{r.id[1]} -> {near}")
