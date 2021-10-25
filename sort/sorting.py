import random

# rand_num = []
# for n in range(20):
#     rand_num.append(random.randrange(1, 100))
# print(rand_num)

class SortNum:
    def __init__(self) -> None:
        pass
        
    # 선택정렬 (오름차순)
    def selection_sort(self, rand_num):
        for i in range(len(rand_num) - 1):
            min_idx = i

            for j in range(i+1, len(rand_num)):
                if rand_num[j] < rand_num[min_idx]:
                    min_idx = j

            rand_num[i], rand_num[min_idx] = rand_num[min_idx], rand_num[i]
        
        return rand_num

    # 선택정렬 (내림차순)
    def selection_sort_rev(self, rand_num):
        for i in range(len(rand_num) - 1):
            max_idx = i

            for j in range(i+1, len(rand_num)):
                if rand_num[j] > rand_num[max_idx]:
                    max_idx = j
            
            rand_num[i], rand_num[max_idx] = rand_num[max_idx], rand_num[i]

        return rand_num

    # 퀵정렬 (오름차순)
    def quick_sort(self, rand_num):
        if len(rand_num) <= 1:
            return rand_num
        pivot = rand_num[len(rand_num) // 2]
        lesser_list, equal_list, greater_list = [], [], []
        for i in rand_num:
            if i < pivot:
                lesser_list.append(i)
            elif i > pivot:
                greater_list.append(i)
            else:
                equal_list.append(i)

        return self.quick_sort(lesser_list) + equal_list + self.quick_sort(greater_list)

    # 퀵정렬 (내림차순)
    def quick_sort_rev(self, rand_num):
        if len(rand_num) <= 1:
            return rand_num
        pivot = rand_num[len(rand_num) // 2]
        lesser_list, equal_list, greater_list = [], [], []
        for i in rand_num:
            if i < pivot:
                lesser_list.append(i)
            elif i > pivot:
                greater_list.append(i)
            else:
                equal_list.append(i)

        return self.quick_sort_rev(greater_list) + equal_list + self.quick_sort_rev(lesser_list)

    # 삽입정렬 (오름차순)
    def insertion_sort(self, rand_num):
        for i in range(1, len(rand_num)):
            for j in range(i, 0, -1):
                if rand_num[j-1] > rand_num[j]:
                    rand_num[j-1], rand_num[j] = rand_num[j], rand_num[j-1]

        return rand_num

    # 삽입정렬 (내림차순)
    def insertion_sort_rev(self, rand_num):
        for i in range(1, len(rand_num)):
            for j in range(i, 0, -1):
                if rand_num[j-1] < rand_num[j]:
                    rand_num[j-1], rand_num[j] = rand_num[j], rand_num[j-1]

        return rand_num

# sort = SortNum()
# print(sort.selection_sort(rand_num))
# print(sort.selection_sort_rev(rand_num))
# print(sort.quick_sort(rand_num))
# print(sort.quick_sort_rev(rand_num))
# print(sort.insertion_sort(rand_num))
# print(sort.insertion_sort_rev(rand_num))
