ZIPBOMB = python3 zipbomb

.PHONY: all
all: overlap.zip zbsm.zip zblg.zip

overlap.zip:
	$(ZIPBOMB) --mode=full_overlap --numfiles=442 --compressed-size=21141 > "$@"

zbsm.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=251 --compressed-size=21094 > "$@"

zblg.zip:
	$(ZIPBOMB) --mode=quoted_overlap --numfiles=65535 --uncompressed-size=4292788492 > "$@"
	# better
	# $(ZIPBOMB) --mode=quoted_overlap --numfiles=65535 --compressed-size=4159693 > "$@"
