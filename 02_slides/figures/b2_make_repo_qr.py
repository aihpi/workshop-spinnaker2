"""QR code for slide 2.1: the workshop repository on GitHub.
Run: uv run --with "qrcode[pil]" python b2_make_repo_qr.py
"""
from pathlib import Path

import qrcode

URL = "https://github.com/aihpi/workshop-spinnaker2"
img = qrcode.make(URL, box_size=20, border=2)
out = Path(__file__).with_name("b2_repo_qr.png")
img.save(out)
print("saved", out, "->", URL)
