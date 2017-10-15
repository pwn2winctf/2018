all:
	@echo nothing yet

nizkctf/iso3166.py: nizkctf/gen_iso3166 settings.json
	PYTHONPATH="." $< >$@

../lambda.zip: FORCE
	rm -f "$@"
	zip -ry "$@" * .git*

FORCE:
