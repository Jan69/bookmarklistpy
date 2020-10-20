#fancy stuff for using makefile's location, from https://timmurphy.org/2015/09/27/how-to-get-a-makefile-directory-path/

#default file
BASE="$(dir $(realpath $(firstword $(MAKEFILE_LIST))))/"
IN=$(BASE)links.txt
#OUT=$(BASE)/links.html

#with no arguments, just build
.PHONY: all
all:
	@python3 $(BASE)generate.py $(IN) $(OUT)
#placeholder so the *.txt rule doesn't skip "because not changed"
true:
	@true
#if given argument, run with it
IN="$@"
*.txt: true
	@python3 $(BASE)generate.py $(IN) $(OUT)
