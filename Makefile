ZIPBOMB = python3 zipbomb

.PHONY: all
all: overlap.zip zbsm.zip zblg.zip zbxl.zip

overlap.zip:
	$(ZIPBOMB) --mode=full_overlap --alphabet ABCDEFGHIJKLMNOPQRSTUVWXYZ --numfiles=26 --compressed-size=10000 > "$@"

zbsm.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=250 --compressed-size=21179 > "$@"

zblg.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=65535 --max-uncompressed-size=4292788491 > "$@"

zbxl.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=190023 --compressed-size=22982788 --zip64 > "$@"

.DELETE_ON_ERROR:
