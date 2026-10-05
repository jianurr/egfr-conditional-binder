"""Step 1: find EGFR domain III residues in contact with the cetuximab Fab in PDB 6ARU,
map them to mature numbering, flag human/mouse conservation, write trimmed domain III PDB.
Run in Colab:  !pip install biopython   then   !python step1_contacts.py
Needs egfr_targets.fasta in the same folder. Needs internet (rcsb.org)."""
import urllib.request, os
from Bio.PDB import PDBParser, MMCIFParser, NeighborSearch, PDBIO, Select
from Bio.Data.IUPACData import protein_letters_3to1 as T
from Bio import Align
from Bio.Align import substitution_matrices

def read_fasta(p):
    d, k = {}, None
    for l in open(p):
        l = l.strip()
        if l.startswith(">"): k = l[1:]; d[k] = ""
        elif k: d[k] += l
    return d
fa = read_fasta("egfr_targets.fasta")
human = [v for k, v in fa.items() if k.startswith("human_EGFR_ECD")][0]
mouse = [v for k, v in fa.items() if k.startswith("mouse_EGFR_ECD")][0]

# get structure
if not os.path.exists("6ARU.pdb"):
    try: urllib.request.urlretrieve("https://files.rcsb.org/download/6ARU.pdb", "6ARU.pdb")
    except Exception: urllib.request.urlretrieve("https://files.rcsb.org/download/6ARU.cif", "6ARU.cif")
if os.path.exists("6ARU.pdb"): s = PDBParser(QUIET=True).get_structure("x", "6ARU.pdb")
else: s = MMCIFParser(QUIET=True).get_structure("x", "6ARU.cif")
model = s[0]
print("Chains:", [c.id for c in model])
A = model["A"]
res = [r for r in A if r.id[0] == " " and r.get_resname().capitalize() in T]
seqA = "".join(T[r.get_resname().capitalize()] for r in res)

# map chain A residues -> human mature numbering by local alignment
al = Align.PairwiseAligner(); al.mode = "local"
al.substitution_matrix = substitution_matrices.load("BLOSUM62")
al.open_gap_score, al.extend_gap_score = -11, -1
aln = al.align(human, seqA)[0]
mp = {}   # chain residue index -> mature position (1-based)
for (h0, h1), (a0, a1) in zip(*aln.aligned):
    for i in range(h1 - h0): mp[a0 + i] = h0 + i + 1
print("Aligned %d of %d chain-A residues to human ECD" % (len(mp), len(res)))

# contacts within 4 A of any other chain
others = [a for c in model if c.id != "A" for a in c.get_atoms() if a.element != "H" and a.get_parent().id[0] == " "]
ns = NeighborSearch(others)
rows = []
for i, r in enumerate(res):
    if i not in mp: continue
    n = sum(len(ns.search(a.coord, 4.0)) > 0 for a in r)
    if n:
        p = mp[i]; hu = human[p-1]; mo = mouse[p-1] if p-1 < len(mouse) else "?"
        rows.append((p, r.id[1], hu, mo, hu == mo, n))
print("\nmature  pdb_resnum  human  mouse  conserved  n_atoms_in_contact")
for p, pr, hu, mo, c, n in rows: print(f"{p:6d}  {pr:10d}  {hu:5s}  {mo:5s}  {'yes' if c else 'NO':9s}  {n}")
cons = [p for p, pr, hu, mo, c, n in rows if c and 310 <= p <= 480]
print("\nConserved contact residues in domain III (mature numbering):", cons)
print("Use these as BindCraft hotspots (convert to PDB resnums if they differ):",
      [pr for p, pr, hu, mo, c, n in rows if c and 310 <= p <= 480])

# write trimmed domain III, chain A only
keep = {r.id for i, r in enumerate(res) if i in mp and 310 <= mp[i] <= 480}
class Sel(Select):
    def accept_chain(self, c): return c.id == "A"
    def accept_residue(self, r): return r.id in keep
io = PDBIO(); io.set_structure(s); io.save("6ARU_domIII_chainA.pdb", Sel())
print("Wrote 6ARU_domIII_chainA.pdb (original PDB residue numbering kept)")
