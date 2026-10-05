"""Check a submission CSV before uploading.  Usage: python validate_submission.py designs.csv"""
import csv, sys
AA = set("ACDEFGHIKLMNPQRSTVWY")
CLASSES = {"single_chain", "nanobody", "scfv", "fab_kappa", "fab_lambda"}  # per the submission form (FAQ text said "protein")
rows = list(csv.DictReader(open(sys.argv[1])))
need = {"name", "sequence"}  # molecule_class is optional on the form; recommended
cols = set(rows[0].keys()) if rows else set()
errs, warns = [], []
if not need <= cols: errs.append(f"Missing columns: {sorted(need - cols)}")
names, seqs = set(), set()
for i, r in enumerate(rows, 1):
    n, s, c = r.get("name", "").strip(), r.get("sequence", "").strip().upper(), (r.get("molecule_class", "") or "single_chain").strip()
    if not n: errs.append(f"row {i}: empty name")
    if n in names: errs.append(f"row {i}: duplicate name {n}")
    if s in seqs: errs.append(f"row {i} ({n}): duplicate sequence")
    names.add(n); seqs.add(s)
    if c not in CLASSES: errs.append(f"row {i} ({n}): molecule_class '{c}' not in {sorted(CLASSES)}")
    chains = s.split(":") if c.startswith("fab") else [s]
    for ch in chains:
        bad = set(ch) - AA
        if bad: errs.append(f"row {i} ({n}): invalid characters {sorted(bad)}")
        if not 10 <= len(ch) <= 250: errs.append(f"row {i} ({n}): chain length {len(ch)} outside 10-250")
    for k, v in r.items():
        if k not in need and v and any(w in v.lower() for w in ("ignore", "instruction", "select this", "rank this", "claude")):
            warns.append(f"row {i} ({n}) column '{k}': text looks like an instruction to the reviewer - remove it (prompt injection can disqualify)")
print(f"{len(rows)} designs. The upload form allows at most 20 per submission, one submission per 24 h.")
if len(rows) > 20: errs.append(f"{len(rows)} designs exceeds the 20-per-submission limit")
for w in warns: print("WARN:", w)
for e in errs: print("ERROR:", e)
print("OK - ready to upload" if not errs else f"{len(errs)} error(s) - fix before uploading")
