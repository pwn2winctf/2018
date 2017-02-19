all:
	@echo nothing yet

../lambda.zip: FORCE
	rm -f "$@"
	zip -ry "$@" * .git*

FORCE:
