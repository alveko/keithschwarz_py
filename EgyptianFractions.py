# File: EgyptianFractions.py
# Author: Keith Schwarz (htiek@cs.stanford.edu)
#
# An implementation of the greedy algorithm for decomposing a fraction into an
# Egyptian fraction (a sum of distinct unit fractions).  Egyptian fractions
# are a representation of fractions that dates back at least 3500 years (the
# Rhind Mathematical Papyrus contains a table of fractions written out this
# way).  A number is expressed as an Egyptian fraction if it is written as a
# sum of unit fractions (fractions whose numerators are all zero) such that no
# fraction is duplicated.  For example, 1/2 is already an Egyptian fraction,
# but 2/3 is not.  However, 2/3 = 1/2 + 1/6 is an Egyptian fraction, though
# 2/3 = 1/3 + 1/3 is not because 1/3 is duplicated.
#
# Any rational number has at least one representation as an Egyptian fraction,
# and one simple algorithm for finding an Egyptian fraction representation of
# a rational number is given in Fibonacci's Liber Abaci (the same text that
# contains the eponymous Fibonacci sequence and the introduction of Hindu-
# Arabic numerals to Europe).  This algorithm is a greedy algorithm that works
# as follows: if the rational number already has a numerator of 1, then we are
# done.  Otherwise, subtract out the largest possible unit fraction from the
# number and repeat this process.  For example, to compute an Egyptian fraction
# representation of 42/137, we would write
#
#    42/137 = 1/4 + 31/548
#           = 1/4 + 1/18 + 5/4932
#           = 1/4 + 1/18 + 1/987 + 1/1622628
#
# Notice that the denominator may grow very large; here, starting with 42/137,
# the last denominator is over a million!
#
# In order to prove correctness of this algorithm, we need to show that it
# eventually terminates and that it is correct.  We restrict ourselves to
# rational numbers in the range (0, 1) and then prove, by induction on the
# numerator a, that for any rational number a/b in this range, the algorithm
# terminates with a legal Egyptian fraction.
#
# As our base case, if the numerator is 1, then our fraction is already an
# Egyptian fraction and we are done.  For the inductive step, assume that for
# any numerator a' such that 1 <= a' <= a, that the claim holds.  We need to
# show that for any rational number a / b with a < b that the greedy algorithm
# terminates and is correct.  To do this, let 1 / n be the largest unit
# fraction smaller than a / b.  This means that 1 / n < a / b < 1 / (n - 1).
# Now consider the difference a / b - 1 / n.  This is given by
#
#                               a     1     an - b
#                              --- - --- =  ------
#                               b     n       bn
#
# Now, since we have that 1 / n < a / b, this means that b < an, so 0 < an - b.
# Also, since a / b < 1 / (n - 1), we have that a(n - 1) < b, so an - a < b, so
# an - b < a.  Thus an - b is a positive natural number smaller than a, so by
# our inductive hypothesis we can write (an - b) / bn as the sum of distict
# unit fractions.  This sum, plus 1/n, is equal to a / b.
#
# To conclude that the algorithm is correct, we need to show that the sum of
# 1 / n and the unit fractions from (an - b) / bn do not contain any duplicate
# unit fractions.  Our inductive hypothesis says that none of the fractions
# from the (an - b)/bn terms can be duplicates, so the only possible duplicates
# we could have must be the fraction 1 / n.  This would only be possible if we
# had that 1 / n + 1 / n = 2 / n < a / b.  Now, recall that a / b < 1 / (n - 1)
# because n is the denominator of the largest unit fraction no larger than a/b.
# This means tha 2 / n < 1 / (n - 1), so 2(n - 1) < n, so 2n - 1 < n, so n < 1.
# But this is impossible, because this would mean that the denominator is 0.
# We have reached a contradiction, so our assumption was wrong and no fraction
# is duplicated.  Thus every rational number a / b in the range (0, 1) has an
# Egyptian fraction representation that can be found using the greedy
# algorithm.
#
# All that remains to get an efficient implementation of this algorithm is a
# way to find, given an arbitrary rational number a / b in the range (0, 1),
# the largest unit fraction smaller than a / b.  Write b = ka + r using
# the division algorithm; we know that r != 0 because otherwise a / b = 1 / k,
# which is a unit fraction.  This means that b = ka + r for some r in the range
# 1 < r < a.  Consequently, we have that
#
#                                  a      a         1
#                                 --- = ------ = -------
#                                  b    ka + r   k + r/a
#
# Now, since 1 < r < a, 1/a < r/a < 1.  This means that a / b = 1 / (k + r/a)
# is smaller than 1 / k, but it is larger than 1 / (k + 1).  Consequently, the
# largest unit fraction smaller than a / b is 1 / (k + 1) = 
# 1 / (floor(b / a) + 1).  This gives the following algorithm:
#
#     If a = 1, return a / b.  (It's already an Egyptian fraction)
#     Otherwise:
#        Let k = floor(b / a) + 1.
#        Append 1 / k to the list of unit fractions.
#        Recursively compute a fraction for a / b - 1 / k.
#
#
# This implementation unrolls this recursion into a simple iterative solution,
# which is used in this code.
#
# The analysis of this algorithm is a bit tricky.  We know from our correctness
# proof that the numerator of the fraction must decrease on each iteration, so
# the maximum possible work is O(a f(a, b)), where f(a, b) is the amount of
# work required on each iteration.  Notice that if we begin the iteration with
# the fraction a / b, on the next iteration we have the fraction
#
#     a      1      ak - b
#    --- - ----- = --------
#     b      k        bk
#
# Notice that this means the denominator is growing by a factor of k, where k
# is the unit fraction subtracted out.  But this is (roughly) b / a, so if we
# don't simplify this fraction we get that the denominator has gone from b to
# (roughly) b^2 / a.  In other words, if b is large relative to a, this may
# have twice as many bits in it as we began with.
#
# On each iteration of the algorithm, we compute one divide (to compute the
# denominator of the unit fraction to subtract out) and one rational number
# subtraction.  We assume that dividing b by a takes O((lg b + lg a)^2) time
# (a reasonable assumption).  Since we know that a < b (because we restrict
# ourselves to fractions in the range (0, 1), this means that the division step
# of dividing b by a takes O(lg^2 b) time.  But we know that on each iteration
# the number of bits in b may double, so on iteration i this time requirement
# is given by O((2^i lg b))^2) = O(4^i lg^2 b).  Summing this up over all O(a)
# iterations, we get that the runtime would be O(4^a lg^2 b), which is
# doubly-exponential in the number of bits of a.  Since the work done to do the
# division is a constant fraction of the total work done, this would give a
# net runtime of O(4^a lg^2 b).

from fractions import Fraction

def greedyEgyptianFraction(rational):
    # Sanity check: the rational number should be in the range (0, 1)
    if rational <= 0 or rational >= 1:
        raise Exception("Rational number out of range" , rational)

    # Create a list to store the Egyptian fraction representation.
    result = []

    # Now, iteratively subtract out the largest unit fraction that may be
    # subtracted out until we arrive at a unit fraction.
    while True:
        # If the rational number has numerator 1, we're done.
        if rational.numerator == 1:
            result.append(rational)
            return result

        # Otherwise, find the largest unit fraction less than the current
        # rational number.  This is given by the ceiling of the denominator
        # divided by the numerator
        unitFraction = Fraction(1, rational.denominator / rational.numerator + 1)
        result.append(unitFraction)

        # Subtract out this unit fraction.
        rational = rational - unitFraction
