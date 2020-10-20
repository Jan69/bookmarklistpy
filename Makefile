all:
	@python3 generate.py
.txt:
	@python3 generate.py $@
*.txt: .txt
.PHONY: all
