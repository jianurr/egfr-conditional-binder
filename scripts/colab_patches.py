"""Compatibility patches needed to run the BindCraft Colab notebook with a newer JAX.
Run AFTER the notebook's Installation cell and BEFORE 'Run BindCraft!'.
Symptoms fixed:
  AttributeError: module 'jax.lib' has no attribute 'xla_bridge'
  TypeError: clip() got an unexpected keyword argument 'a_max'
Do not restart the Colab session afterwards (that clears the notebook variables)."""

# Patch 1: colabdesign calls a JAX function that newer versions removed
p = "/content/colabdesign/shared/utils.py"
s = open(p).read()
old = "  backend = jax.lib.xla_bridge.get_backend()"
new = """  try:
    from jax.extend import backend as _jb
    backend = _jb.get_backend()
  except Exception:
    return"""
if old in s:
    open(p, "w").write(s.replace(old, new)); print("utils patched OK")
else:
    print("utils: already patched or line not found")

# Patch 2: jnp.clip renamed a_min/a_max to min/max
import jax.numpy as jnp
if not getattr(jnp.clip, "_patched", False):
    _orig_clip = jnp.clip
    def _clip(a, *args, a_min=None, a_max=None, **kw):
        if a_min is not None: kw["min"] = a_min
        if a_max is not None: kw["max"] = a_max
        return _orig_clip(a, *args, **kw)
    _clip._patched = True
    jnp.clip = _clip
print("clip patched")
