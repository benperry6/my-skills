#!/usr/bin/env python3
"""Check that all required dependencies for pdf-stealth-edit are available."""
import shutil
import sys


def check():
    ok = True

    # qpdf CLI
    if shutil.which("qpdf"):
        print("[OK] qpdf found")
    else:
        print("[MISSING] qpdf — install with: brew install qpdf")
        ok = False

    # Python packages
    for pkg, import_name in [("pikepdf", "pikepdf"), ("pdfplumber", "pdfplumber"), ("pypdf", "pypdf")]:
        try:
            mod = __import__(import_name)
            version = getattr(mod, "__version__", "unknown")
            print(f"[OK] {pkg} {version}")
        except ImportError:
            print(f"[MISSING] {pkg} — install with: pip install {pkg}")
            ok = False

    if ok:
        print("\nAll dependencies satisfied.")
    else:
        print("\nSome dependencies are missing. Install them before proceeding.")
        sys.exit(1)


if __name__ == "__main__":
    check()
