set -e
cd "$1/FlowState"
uv venv --python /opt/homebrew/bin/python3.14 .venv
. .venv/bin/activate
uv pip install maturin numpy polars==1.38.1 pandas==3.0.6 pyarrow==23.0.1
(cd flowstate-core && maturin develop --release)
uv pip install -e .
python -W ignore benchmarks/reproduce.py --pandas-scale --runs 10
