# File: RandomBag.py
# Author: Keith Schwarz (htiek@cs.stanford.edu)
#
# A data structure representing a random bag of elements.  The random bag
# supports two operations: insert, which adds a new element to the random bag,
# and remove-random, which removes and returns a random element of the bag.
#
# Internally, the structure works by maintaining a list of the elements in the
# bag.  Whenever a new element is inserted, it is appended to the list.
# Whenever an element is to be removed, a random element is swapped to the last
# position of the list, then it is removed.  This gives O(1) insertion and
# removal of elements from the list, since removing from the end of a list runs
# in constant time.  If the element that's removed is picked uniformly at
# random, the removed element will be chosen uniformly at random from the list.
from random import randint

class RandomBag:
    _elems = []

    def insert(self, value):
        """Inserts a new value into the random bag."""
        self._elems.append(value)

    def __len__(self):
        """Returns the number of elements in the random bag."""
        return len(self._elems)

    def __iter__(self):
        """Returns an iterator over the elements in the random bag."""
        return iter(self._elems)

    def removeRandom(self):
        """Removes a random element from the bag, handing back its value.
        
        If the random bag is empty, an assertion error is raised."""

        # Confirm that the bag isn't empty.
        assert len(self) != 0

        # Pick a random index to swap to the end.
        i = randint(0, len(self) - 1)

        # Exchange this and the final element.
        self._elems[-1], self._elems[i] = self._elems[i], self._elems[-1]

        # Return and remove the last element
        return self._elems.pop();
