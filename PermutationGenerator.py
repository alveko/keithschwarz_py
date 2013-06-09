# File: PermutationGenerator.py
# Author: Keith Schwarz (htiek@cs.stanford.edu)
#
# An application of Python coroutines to the iterative generation of
# permutations.  This code exports the permutations() function, which, given a
# list of elements, iteratively produces all permutations of that list.  The
# goal is to be able to write code to this effect:
#
#   for p in permutations([1, 2, 3]):
#       print p
#
# In order to generate all permutations, this code uses the following recursive
# procedure for exhaustively generating permutations:
#
#   - There is only one permutation of the empty list, which is [].
#   - Given a nonempty list of elements, we can form all permutations of that
#     list by, for each element in the list, prepending that element to all
#     permutations of the remaining elements.
#
# This recursive procedure will list all permutations, which is great in many
# contexts.  However, if we want to be able to generate those permutations
# iteratively, stopping whenever we choose, then this approach is not tenable.
# Given n elements, there are n! different permutations of those elements, and
# it's extraordinarily wasteful to generate all n! permutations if we only need
# a small number of them, say, only O(n).
#
# This program defines a coroutine permutations() that uses Python's yield
# facility to generate permutations one at a time.  That way, we can use the
# recursive strategy to generate permutations, but only run the recursion as
# much as is needed.

# Function: permutations(elems)
# Usage: for p in permutations([1, 2, 3]): ...
# -----------------------------------------------------------------------------
# A generator function that generates all permutations of the input elements.
# If the input contains duplicates, then some permutations may be visited with
# multiplicity greater than one.
def permutations(elems):
    # Our recursive algorithm requires two pieces of information, the elements
    # that have not yet been permuted and the partial permutation built up so
    # far.  We thus phrase this function as a wrapper around a recursive
    # function with extra parameters.
    for perm in recPermutations(elems, []):
        yield perm

# A helper function to recursively generate permutations.  The function takes
# in two arguments, the elements to permute and the partial permutation created
# so far, and then produces all permutations that start with the given sequence
# and end with some permutations of the unpermuted elements.
def recPermutations(elems, soFar):
    # Base case: If there are no more elements to permute, then the answer will
    # be the permutation we have created so far.
    if len(elems) == 0:
        yield soFar

    # Otherwise, try extending the permutation we have so far by each of the
    # elements we have yet to permute.
    else:
        for i in range(0, len(elems)):
            # Extend the current permutation by the ith element, then remove
            # the ith element from the set of elements we have not yet
            # permuted.  We then iterate across all the permutations that have
            # been generated this way and hand each one back to the caller.
            for perm in recPermutations(elems[0:i] + elems[i+1:], 
                                        soFar + [elems[i]]):
                yield perm
