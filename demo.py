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
