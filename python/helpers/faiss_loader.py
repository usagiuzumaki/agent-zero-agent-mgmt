"""
This module handles importing FAISS, applying a monkey patch for Python 3.12 on ARM if necessary.
See: https://github.com/facebookresearch/faiss/issues/3936
"""
import sys

try:
    import faiss
except ImportError as e:
    # Check for the specific issue related to numpy.distutils which affects some FAISS versions on Python 3.12
    if "numpy.distutils" in str(e):
        import types
        import numpy as np
        from types import SimpleNamespace

        # fake numpy.distutils and numpy.distutils.cpuinfo packages
        dist = types.ModuleType("numpy.distutils")
        cpuinfo = types.ModuleType("numpy.distutils.cpuinfo")

        # cpu attribute that looks like the real one
        cpuinfo.cpu = SimpleNamespace(
            # FAISS only does   .info[0].get('Features', '')
            info=[{}]
        )

        # register in sys.modules
        dist.cpuinfo = cpuinfo
        sys.modules["numpy.distutils"] = dist
        sys.modules["numpy.distutils.cpuinfo"] = cpuinfo

        # crucial: expose it as an *attribute* of the already-imported numpy package
        np.distutils = dist # type: ignore

        # Try importing faiss again
        import faiss
    else:
        # Re-raise the exception if it's not the specific issue we are patching
        raise

# Re-export faiss
# We don't need to do anything special here as 'import faiss' puts it in the local namespace
