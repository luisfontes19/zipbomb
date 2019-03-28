B <- 36

# Combined length of n filenames generated according to our 36-digit
# scheme: 0 1 ... Z 00 01 ... 0Z 10 11 ... 1Z ... ZZ 000. Look at it
# like this: if we have n filenames, then all n of them have at least 1
# digit; all but 10 have at least 2 digits; all but 110 have at least 3
# digits, all but 1110 have at least 4 digits; and so on. In general,
# the length of the longest filename increases by 1 at each index that
# is a repunit 11...1₃₆ = 1 + 36 + 36² + ... + 36^(d−1) = (36^d−1)/(36−1).
# Let d be the length of the longest repunit not greater than n. Then
# the combined length of filenames is
#   Sum(i) from 1 to d of: n − (36^i−1)/(36−1) + 1
#    = d×(n+1) - Sum(i) from 1 to d of: (36^i−1)/(36−1)
#    = d×(n+1) − ((36^d−1)×36/(36−1)² - d/(36−1))
# where the last equality comes from adapting a formula for the partial
# sums of base-10 repunits from https://oeis.org/A014824.
#
# In the case where the base is 2, this is the same as
# https://oeis.org/A061168.
sum_filename_lengths <- function(n) {
	d <- floor(log((n+1)/(B/(B-1)), B)) + 1
	d*(n+1) - ((B^d-1)/(B-1) * B/(B-1) - d/(B-1))
}

triangular_sum_filename_lengths <- Vectorize(function(n) {
	m <- 1
	r <- -1
	s <- 0
	while (B^m <= n) {
		s <- s + m * B^m * (B^m + 1) / 2 + m * r * B^m
		n <- n - B^m
		r <- r + B^m
		m <- m + 1
	}
	s <- s + m * n * (n + 1) / 2 + m * r * n
	s
})

zipped_size <- function(deflate_size, num_additional) {
	size <- 0
	size <- size + num_additional * 5 # 5 is DEFLATE quoting overhead
	size <- size + 16 + deflate_size # 16 is DEFLATE compression overhead
	size <- size + 30 * (1 + num_additional) # Local File Headers
	size <- size + 46 * (1 + num_additional) # Central Directory Headers
	size <- size + 2 * sum_filename_lengths(1 + num_additional) # Filenames in Local File Headers and Central Directory Headers
	size <- size + 22 # EOCD
	size
}

unzipped_size <- function(deflate_size, num_additional) {
	size <- 0
	size <- size + (1 + 1032 + deflate_size * 1032) * (1 + num_additional)
	size <- size + 30 * (num_additional * (num_additional + 1)) / 2
	size <- size + triangular_sum_filename_lengths(1 + num_additional)
	size
}

additional_size <- function(num_additional) {
	num_additional * (30 + 46 + 5) + 2 * sum_filename_lengths(1 + num_additional)
}

optimize <- function(total_size) {
	avail <- total_size - 30 - 46 - 22
	num_additional <- with(list(n=0:(avail/(30+5+46))), {
		plot(n, unzipped_size(avail - additional_size(n), n))
		which.max(unzipped_size(avail - additional_size(n), n))
	})
	compressed_size = avail - additional_size(num_additional)
	list(compressed_size=compressed_size, num_additional=num_additional)
}

params <- optimize(42374)
params
zipped_size(params$compressed_size, params$num_additional)
