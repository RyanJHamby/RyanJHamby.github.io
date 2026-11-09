set shell := ["bash", "-c"]

# local dev server with live reload
serve:
	hugo server

# build the site into public/ (what CI runs)
build:
	hugo

# run the site tests
test:
	python3 -m pytest -q

# scaffold a draft post: just new-post my-slug note (type: benchmark, dead-end or note)
new-post slug type:
	python3 tools/new_post.py {{slug}} --type {{type}}
