# %%

array1 = [33, 12, 45, 7, 88, 21, 56, 39, 10, 17, 92, 25, 68, 31, 84, 50, 3, 62, 95, 14]
array2 = [18, 75, 28, 9, 41, 64, 29, 53, 86, 37, 22, 59, 4, 67, 90, 13, 48, 81, 36, 5]
array3 = [72, 20, 43, 8, 55, 98, 15, 78, 32, 69, 91, 24, 57, 83, 46, 1, 74, 27, 60, 38]


# %%
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

sorted_array1_bubble = bubble_sort(array1)
sorted_array1_bubble



# %%
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

sorted_array2_insertion = insertion_sort(array2)
sorted_array2_insertion


# %%
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    linkerkant = [x for x in arr if x < pivot]
    middelkant = [x for x in arr if x == pivot]    
    rechterkant = [x for x in arr if x > pivot]

    return quicksort(linkerkant) + middelkant + quicksort(rechterkant)

sorted_array3_quicksort = quicksort(array3)
sorted_array3_quicksort



