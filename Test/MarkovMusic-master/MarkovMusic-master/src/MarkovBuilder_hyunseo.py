import random


class MarkovBuilder:
    def __init__(self, value_list):
        value_list.sort()
        self._value_lookup = {}
        self._reverse_value_lookup = value_list
        self._values_added = 0
        for i in range(0, len(value_list)):
            self._value_lookup[value_list[i]] = i
        self._matrix = [[0 for x in range(0, len(value_list))]
                        for i in range(0, len(value_list))]

    def add(self, from_value, to_value):
        value = self._value_lookup
        self._matrix[value[from_value]][value[to_value]] += 1
        self._values_added = self._values_added + 1

    def display(self):
        for i in range(0, len(self._matrix)):
            print(self._reverse_value_lookup[i], end=' ')
        print('\n')
        for i in range(0, len(self._matrix)):
            print(self._reverse_value_lookup[i], end=' ')
            for j in range(0, len(self._matrix[i])):
                print(self._matrix[i][j], end=' ')
            print("\n")

    # 2022-07-29
    def next_value(self, from_value):
        value = self._value_lookup[from_value]
        value_counts = self._matrix[value]
        value_index = self.randomly_choose(value_counts)
        if(value_index < 0):
            raise RuntimeError("Non-existent value selected.")
        else:
            # print("Value index: ", value_index)
            return self._reverse_value_lookup[value_index]

    def randomly_choose(self, choice_counts):
        counted_sum = 0
        count_sum = sum(choice_counts)
        # print(count_sum)

        if count_sum == 0:
            return random.randint(0, len(choice_counts)-1)
        else:
            selected_count = random.randrange(1, count_sum + 1)
            for index in range(0, len(choice_counts)):
                counted_sum += choice_counts[index]
                if(counted_sum >= selected_count):
                    return index
        raise RuntimeError("Impossible value selection made. BAD!")
