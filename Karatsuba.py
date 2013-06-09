# File: Karatsuba.py
# Author: Keith Schwarz (htiek@cs.stanford.edu)
#
# An implementation of Karatsuba's algorithm for fast multiplication of
# arbitrary-precision integers.  Given two n-bit integers, Karatsuba's method
# can compute their product in O(n^(log_3 2)) time by using a clever recurrence
# relation.  Although there exist algorithms that are asymptotically faster
# than Karatsuba's method, Karatsuba's algorithm is easier to intuit and in
# many ways clearer.
#
# The idea behind Karatsuba's algorithm is as follows.  Suppose that we are
# given two numbers x and y that we wish to multiply, and that they are written
# out as strings in some base b.  Let's suppose that the two numbers have the
# same length (we'll pad the shorter of the two to the appropriate length if
# necessary), which we'll call m.  We can then split x and y each into two
# pieces of length m/2.  For example, if we wanted to multiply 1337 and 1000,
# we would split these numbers into 13, 37, 10, 10.  For simplicity, we'll call
# these values x0, x1, y0, and y1.  Now, our goal is to compute the product
#
#     xy = (x0 b^(m/2) + x1)(y0 b^(m/2) + y1)
#        = x0 y0 b^m + (x0 y1 + x1 y0) b^(m/2) + x1 y1
#
# To be more technically accurate, if m is odd, we'll split the number into two
# pieces of size m0 = ceil(m / 2) and m1 = floor(m / 2).  x0 and y0 will be of
# length m0, and x1 and y1 will be of length m1, so the above multiplication
# is actually given by
#
#     xy = (x0 b^m1 + x1)(y0 b^m1 + y1)
#        = x0 y0 b^(2 m1) + (x0 y1 + x1 y0) b^m1 + x1 y1
#
# There are two key tricks in this algorithm.  To see them, let's rewrite the
# above using the following notation.  Define
#
#    z0 = x0 y0
#    z1 = x0 y1 + x1 y0
#    z2 = x1 y1
#
# Now, the above product is given by
#
#     xy = z0 b^(2 m1) + z1 b^m1 + z2
#
# The first observation is that if we have values for z0, z1, and z2, we can
# compute the above value with no multiplications at all.  Because we're
# assuming the values are written out as strings of digits in some base, we
# can represent multiplication by powers of b by simply appending zeros to the
# value in question.  This means that given z0, z1, and z2, we can in O(n) time
# compute the above expression.
#
# The second observation, which is more clever, is that we can compute the
# values z0, z1, and z2 efficiently.  If we just write out
#
#    z0 = x0 y0
#    z1 = x0 y1 + x1 y0
#    z2 = x1 y1
#
# It looks like we need to do four multiplications (each of which would be a
# recursive call) - x0 y0, x0 y1, x1 y0, and x1 y1.  Karatsuba's main insight
# was that we don't actually need four multiplications to do this, and can
# instead just do this with three.  In particular, suppose that we compute
# these three products:
#
#    p0 = x0 y0
#    p1 = (x0 + x1)(y0 + y1)
#    p2 = x1 y1
#
# Now, we have that
#
#    z0 = x0 y0
#       = p0
#    z1 = x0 y1 + x1 y0
#       = x0 y1 + x1 y0 + (x0 y0 - x0 y0) + (x1 y1 - x1 y1)
#       = x0 y0 + x0 y1 + x1 y0 + x1 y1 - x0 y0 - x1 y1
#       = (x0 + x1)(y0 + y1) - x0 y0 - x1 y1
#       = p1 - p0 - p2
#    z2 = x1 y1
#        = p0
#
# In other words, if we're willing to do some extra additions and subtractions,
# we can compute these three products each using three recursive multiplies and
# a constant number of linear additions.
#
# If we work out the recurrence relation for the runtime of this function when
# computing the product, we get the following:
#
#   T(n) = 3T(n / 2) + O(n)
#
# The T(n / 2) term exists because each recursive multiply works with numbers
# that are half as large as the input numbers (though the ceiling does make the
# math a bit trickier).  Using the Master Theorem, this expands out to an
# overall runtime of O(n^(log_3 2)), which is about O(n^1.58).  Note that the
# naive algorithm that is traditionally used by hand runs in O(n^2) time, so
# this is indeed an asymptotic improvement.
#
# The implementation of Karatsuba multiplication included in this file contains
# a function that performs Karatsuba multiplication assuming that the input
# numbers are represented as arrays of integers corresponding to the digits of
# the numbers.  I have also included here an implementation of addition and
# subtraction for arbitrary-precision integers encoded in this format.

def add(lhs, rhs, base):
    """Adds two arbitrary-precision values in some base together.
    
    Given two arrays lhs and rhs of digits in some base 'base,' returns an
    array of the number lhs + rhs encoded in base 'base.'"""

    # Pad the two inputs to be the same length.
    length = max(len(lhs), len(rhs))
    lhs = [0 for i in range(len(lhs), length)] + lhs;
    rhs = [0 for i in range(len(rhs), length)] + rhs;

    # Track the carry from the previous column; initially this is zero.
    carry = 0

    # Track the result.  We'll build the array up in reverse to avoid costly
    # prepend operations that aren't relevant.
    result = [];

    # Iterate across the digits in reverse, computing the sum.
    for i in range(1, len(lhs) + 1):
        # Sum the carry and the two values in this column
        column = lhs[-i] + rhs[-i] + carry;

        # Output the column value (after modding by the base)
        result.append(column % base);

        # Update the carry
        carry = column / base;

    # Prepend the carry to the result if it's nonzero.
    if carry != 0: result.append(carry)

    # Reverse the order of the resulting digits; that's the more proper way
    # to hand them back.
    result.reverse();

    return result;

def subtract(lhs, rhs, base):
    """Subtracts two arbitrary-precision values in some base.
    
    Given two arrays lhs and rhs of digits in some base 'base,' returns an
    array of the number lhs - rhs encoded in base 'base.'  It is assumed that
    lhs >= rhs; an error occurs if this is not the case."""

    # Pad the two inputs to be the same length.
    length = max(len(lhs), len(rhs))
    lhs = [0 for i in range(len(lhs), length)] + lhs;
    rhs = [0 for i in range(len(rhs), length)] + rhs;

    # Track the result.  We'll build the array up in reverse to avoid costly
    # prepend operations that aren't relevant.
    result = [];

    # Iterate across the digits in reverse, subtracting the values.
    for i in range(1, len(lhs) + 1):
        # Compute the difference in this column.
        difference = lhs[-i] - rhs[-i]

        # If we can subtract without borrowing, do so.
        if difference >= 0:
            result.append(difference)
        # Otherwise, we have to borrow from previous columns.
        else:
            j = i + 1
            while j <= length:
                # Drop the value of this digit by one.  We do this by adding
                # base - 1 and then modding by base, which is equivalent to
                # subtracting one modulo base.
                lhs[-j] = (lhs[-j] + (base - 1)) % base
                
                # If this value didn't wrap around (i.e. its value is not
                # base - 1), then we're done.  Otherwise, we have to go to the
                # previous digit.
                if lhs[-j] != base - 1:
                    break
                else:
                    j = j + 1
            
            # Finally, update the result by appending the correct value.
            # Since we just computed lhs - rhs, we actually want to compute
            # (base + lhs) - rhs.
            result.append(difference + base)

    # Reverse the order of the resulting digits; that's the more proper way
    # to hand them back.
    result.reverse();

    return result;

def multiply(lhs, rhs, base):
    """Multiplies two arbitrary-precision values in some base.

    Given two arrays of lhs and rhs of digits in some base 'base,' returns
    an array of digits corresponding to their product using the Karatsuba
    algorithm."""

    assert len(lhs) > 0 and len(rhs) > 0

    # Pad the two inputs to be the same length.
    length = max(len(lhs), len(rhs))
    lhs = [0 for i in range(len(lhs), length)] + lhs;
    rhs = [0 for i in range(len(rhs), length)] + rhs;

    # If the numbers are one digit each, just multiply them and convert the
    # answer back to an (up to) two digit number.
    if length == 1:
        # Compute the true answer.
        result = lhs[0] * rhs[0]

        # Convert it back to an array.
        return [result] if result < base else [result / base, result % base]
    
    # Otherwise, we need to use Karatsuba's recursive algorithm to compute the
    # values.  To do this, we'll first compute how many digits we'll put into
    # each of the smaller numbers.  This is given by ceil(length / 2), which
    # can be represented beautifully by computing (length + 1) / 2.  This
    # works because if length is even (length + 1) / 2 = (2n + 1) / 2 = n
    # when using integer division, and if length is odd (length + 1) / 2 =
    # (2n + 1 + 1) / 2 = (2n + 2) / 2 = n + 1.
    m0 = (length + 1) / 2
    m1 = length / 2

    # Split the inputs in half.
    x0 = lhs[  : m0]
    x1 = lhs[m0 :  ]
    y0 = rhs[  : m0]
    y1 = rhs[m0 :  ]

    # Compute p0, p1, and p2.
    p0 = multiply(x0, y0, base)
    p1 = multiply(add(x0, x1, base), add(y0, y1, base), base)
    p2 = multiply(x1, y1, base)

    # Since z0 = p0 and z2 = p2, we don't need to compute them.  However, we
    # do need to compute z1 = p1 - p0 - p2.
    z0 = p0
    z1 = subtract(p1, add(p0, p2, base), base)
    z2 = p2

    # From these results, compute z0 b^(2m) + z1 b^m + z2.  We separate out
    # each of these operations.
    z0prod = z0 + [0 for i in range(0, 2 * m1)]
    z1prod = z1 + [0 for i in range(0, m1)]
    z2prod = z2

    return add(add(z0prod, z1prod, base), z2prod, base)
