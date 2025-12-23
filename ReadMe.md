STEP 0 — Always activate the correct environment (important)

You already asked earlier to always activate the session — so we’ll follow that discipline.

Check which Python is running your script:
python --version
which python


STEP 1 — Create a virtual environment (recommended)

cd ~/Documents/workspace/quantum-class/quantum-portfolio
python3 -m venv .venv


STEP 2 — Activate the virtual environment

source .venv/bin/activate


STEP 3 — Install Cirq (correct package)
pip install --upgrade pip
pip install --upgrade pip

python -c "import cirq; print(cirq.__version__)"


STEP 4 — Run your Day 4 script
python *.py
