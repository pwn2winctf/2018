all:
	python -m SimpleHTTPServer 8080

../lambda.zip: FORCE
	rm -f "$@"
	zip -ry "$@" * .git*

FORCE:
