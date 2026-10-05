"""Generate histidine variants of a parent design.
Edit PARENT and VARIANTS, then run:  python make_his_variants.py"""
PARENT = "MSPAPTHEEMRDVYFVAEFVKQVKEQKEYWKETGKEPSEKEKKDVEWMEEFVKKEMEKMKKKNPILVEMVKELVEK"  # mpnn3
VARIANTS = {  # name: [(position 1-based, expected parent residue, new residue)]
    "R11H": [(11, "R", "H")],
    "Y14H": [(14, "Y", "H")],
    "K40H": [(40, "K", "H")],
    "S38H": [(38, "S", "H")],
    "R11H_K40H": [(11, "R", "H"), (40, "K", "H")],
    "R11H_Y14H_K40H": [(11, "R", "H"), (14, "Y", "H"), (40, "K", "H")],
}
for name, muts in VARIANTS.items():
    s = list(PARENT)
    for pos, old, new in muts:
        assert s[pos - 1] == old, f"{name}: position {pos} is {s[pos-1]}, expected {old}"
        s[pos - 1] = new
    seq = "".join(s)
    print(f"{name}\tHis={seq.count('H')}\t{seq}")
