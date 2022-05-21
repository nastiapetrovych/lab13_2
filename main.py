"""
Implementation of the function
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log2
import sys
import random
import time

sys.setrecursionlimit(10000)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)
        self.current = None

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node is not None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            self.level = level
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lst = list()
        branches = LinkedStack()
        node = self._root
        while not branches.isEmpty() or node is not None:
            if node is not None:
                branches.push(node)
                node = node.left
            else:
                node = branches.pop()
                lst.append(node.data)
                node = node.right
        return lst

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        if self._root.data == item:
            return True
        element = self._root
        while self._root:
            if element.data > item:
                if element.left is None:
                    break
                element = self._root.left
            if element.data < item:
                if element.right is None:
                    break
                element = self._root.right
            if element.data == item:
                return True
            else:
                break
        return False

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
        element = self._root
        while self._root:
            if element.data > item:
                if element.left is None:
                    element.left = BSTNode(item)
                    break
                element = element.left
            elif element.data < item:
                if element.right is None:
                    element.right = BSTNode(item)
                    break
                element = element.right
            else:
                break
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        """
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while currentNode.right is not None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left
        if self.isEmpty():
            return None
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while currentNode is not None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right
        if itemRemoved is None:
            return None
        if currentNode.left is not None \
                and currentNode.right is not None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:
            # Case 2: The node has no left child
            if currentNode.left is None:
                newChild = currentNode.right
            else:
                newChild = currentNode.left
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top=None):
            """
            Helper function
            :param top:object
            :return:int
            """
            if top is not None:
                if top.left is None and top.right is None:
                    return 0
                elif top.left is not None and top.right is None:
                    return height1(top.left) + 1
                elif top.left is None and top.right is not None:
                    return height1(top.right) + 1
                else:
                    return max(height1(top.left), height1(top.right)) + 1

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:bool
        """
        return self.height() < 2 * log2(len(list(self.inorder())) + 1) - 1

    def range_find(self, low, high):
        """
        Returns a list of the items in the tree, where low <= item <= high."""
        lst = []
        for item in self.inorder():
            if low <= item <= high:
                lst.append(item)
        return lst

    def rebalance(self):
        """
        Rebalanced the tree.
        :return:None
        """
        branches = self.inorder()
        self.clear()

        def recursive(items, lst):
            """
            Helpful function
            """
            if len(lst) == 0:
                return
            length = len(lst)
            items.add(lst[length // 2])
            lst.pop(length // 2)
            recursive(items, lst[:length // 2])

        recursive(self, list(branches))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = []
        for value in self.inorder():
            if value > item:
                lst.append(value)
        return min(lst) if len(lst) != 0 else None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = []
        for value in self.inorder():
            if value < item:
                lst.append(value)
        return max(lst) if len(lst) != 0 else None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        ranged = 10000
        test1 = 'Result of search in a list'
        test2 = 'Result of search in a sorted binary tree'
        test3 = 'Result of search in an unordered binary tree'
        test4 = 'Result of search in a balanced binary tree '
        first_object = LinkedBST()
        second_object = LinkedBST()
        another_object = LinkedBST()
        lst = []
        lst2 = []
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                lst.append(line)
                first_object.add(line)
                second_object.add(line)
                lst2.append(line)
            random.shuffle(lst2)
            for item in lst2:
                another_object.add(item)
        """
        Searching in an ordered binary tree
        """
        beginning = time.time()
        for _ in range(ranged):
            word = random.choice(lst)
            first_object.find(word)
        end = time.time()
        result1 = round(end - beginning, 2)

        """
        Searching in list with help of list.index
        """
        beginning = time.time()
        for _ in range(ranged):
            word = random.choice(lst)
            lst.index(word)
        final = time.time()
        result2 = round(final - beginning, 2)

        """
        Finding in rebalanced list
        """
        second_object.rebalance()
        beginning = time.time()
        for _ in range(ranged):
            word = random.choice(lst)
            second_object.find(word)
        final = time.time()
        result3 = round(final - beginning, 2)

        """
        Searching in random binary tree
        """
        beginning = time.time()
        for _ in range(ranged):
            word = random.choice(lst)
            another_object.find(word)
        end = time.time()
        result4 = round(end - beginning, 2)

        return f'{test1} : {result2} \n{test2} : {result1} \n{test3} : {result4} \n{test4} : {result3}'


tree = LinkedBST()
print(tree.demo_bst('empty.txt'))
