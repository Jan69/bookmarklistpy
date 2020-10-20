#with no arguments, just build
.PHONY: all
all:
	@python3 generate.py
#placeholder so the *.txt rule doesn't skip "because not changed"
true:
	true
#if given argument, run with it
*.txt: true
	@python3 generate.py $@
