B <- 36

# Combined length of n filenames generated according to our 36-digit
# scheme: 0 1 ... Z 00 01 ... 0Z 10 11 ... 1Z ... ZZ 000. Look at it
# like this: if we have n filenames, then all n of them have at least 1
# digit; all but 10 have at least 2 digits; all but 100 have at least 3
# digits, all but 1000 have at least 4 digits; and so on. In general,
# the length of the longest filename increases by 1 at each index that
# is a repunit 11...1₃₆ = 1 + 36 + 36² + ... + 36^(d−1) = (36^d−1)/(36−1).
# Let d be the length of the longest repunit not greater than n. Then
# the combined length of filenames is
#   Sum from 1 to d of: n+1 − (36^d−1)/(36−1)
#    = d×(n+1) - Sum from 1 to d of: (36^d−1)/(36−1)
#    = d×(n+1) − (36^d−1)×36/(36−1)² - d/(36−1)
# where the last equality comes from adapting a formula for the partial
# sums of base-10 repunits from https://oeis.org/A014824.
#
# In the case where the base is 2, this is the same as
# https://oeis.org/A061168.
sum_filename_lengths <- function(n) {
	d <- floor(log((n+1)/(B/(B-1)), B)) + 1
	d*(n+1) - ((B^d-1)/(B-1) * B/(B-1) - d/(B-1))
}

compressed_size <- function(deflate_size, num_aliases) {
	size <- 0
	size <- size + num_aliases * 5 # 5 is DEFLATE quoting overhead
	size <- size + 16 + deflate_size # 16 is DEFLATE compression overhead
	size <- size + 30 * (1 + num_aliases) # Local File Headers
	size <- size + 46 * (1 + num_aliases) # Central Directory Headers
	size <- size + 2 * sum_filename_lengths(1 + num_aliases) # Filenames in Local File Headers and Central Directory Headers
	size <- size + 22 # EOCD
	size
}

uncompressed_size <- Vectorize(function(deflate_size, num_aliases) {
	size <- 0
	size <- size + (1 + 1032 + deflate_size * 1032) * (1 + num_aliases)
	size <- size + 30 * (num_aliases * (num_aliases + 1)) / 2
	size <- size + sum(sum_filename_lengths(1+num_aliases) - sum_filename_lengths(1:num_aliases))
	size
})

# compressed_size(21094-16, 250)
# uncompressed_size(21094-16, 250)

# compressed_size(500000-16, 1297)
# uncompressed_size(500000-16, 1297)

aliases_size <- function(num_aliases) {
	num_aliases * (30 + 46 + 5) + 2 * sum_filename_lengths(1+num_aliases)
}

optimize <- function(total_size) {
	avail <- total_size - 30 - 46 - 16 - 22
	num_aliases <- with(list(n=0:(avail/(30+5+46))), {
		plot(n, uncompressed_size(avail - aliases_size(n), n))
		which.max(uncompressed_size(avail - aliases_size(n), n))
	})
	deflate_size = avail - aliases_size(num_aliases)
	list(deflate_size=deflate_size, num_aliases=num_aliases)
}

optimize(42374)
