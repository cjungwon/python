import random

rand_num = []
for n in range(20):
    rand_num.append(random.randrange(1, 100))

print(rand_num)
    
def selection_sort(rand_num):
    for i in range(len(rand_num) - 1):
        min_idx = i

        for j in range(i+1, len(rand_num)):
            if rand_num[j] < rand_num[min_idx]:
                min_idx = j

        rand_num[i], rand_num[min_idx] = rand_num[min_idx], rand_num[i]
    
    return rand_num

def quick_sort(rand_num):
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

    return quick_sort(lesser_list) + equal_list + quick_sort(greater_list)

# print(selection_sort())
print(quick_sort(rand_num))