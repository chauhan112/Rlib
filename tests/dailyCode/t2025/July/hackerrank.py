#%%
def isEqual(dic1, dic2):
    if len(dic1) != len(dic2):
        return False
    for k in dic1:
        if  k not in dic2 or dic1[k] != dic2[k]:
            return False
    return True

def get_letter_freq(string):
    res = {l: 0 for l in string}
    for l in string:
        res[l] += 1
    return res

dictionary = ["hack", "a", "rank","khac", "ackh", "kran", "rankhacker", "a", "ab", "ba", "stairs", "stair"]
query = ["a", "nark", "bs", "hack", "stair"]
#%%
res = []
dicMap = {st: get_letter_freq(st) for st in dictionary}
for q in query:
    d = get_letter_freq(q)
    c = 0
    for w in dictionary:
        if isEqual(dicMap[w], d):
            c+= 1
    res.append(c)

# %%
res
# %%
from collections import defaultdict

def stringAnagram_faster(dictionary, query):
    anagram_counts = defaultdict(int)

    for word in dictionary:
        canonical_form = "".join(sorted(word))
        anagram_counts[canonical_form] += 1

    res = []
    for q in query:
        canonical_q = "".join(sorted(q))
        res.append(anagram_counts[canonical_q])

    return res

# %%
stringAnagram_faster(dictionary, query)
# %%
def get_sum(ind):
    if len(cs[ind]) == 0:
        return fs[ind]
    if ind in ffsMap:
        return ffsMap[ind]
    ffsMap[ind] = sum(get_sum(i) for i in cs[ind]) + fs[ind]
    return ffsMap[ind]

parents = [-1, 0,0,1,1,2]
fs = [1,2,2,1,1,1]
cs = {k: [] for k in range(len(parents))}
for i in range(len(parents)):
    if parents[i] == -1:
        continue
    cs[parents[i]].append(i)
cs
ffs = []
ffsMap = {}
for i in range(len(fs)):
    ffs.append(get_sum(i))
ffs

# %%
import math

def mostBalancedPartition(parent, files_size):
    num_nodes = len(parent)
    cs = {i: [] for i in range(num_nodes)}
    root = -1  

    for i, p_node in enumerate(parent):
        if p_node == -1:
            root = i  
        else:
           
            cs[p_node].append(i)

    ffsMap = {}

    def get_sum(node_index):
        if node_index in ffsMap:
            return ffsMap[node_index]
        current_sum = files_size[node_index]
        for child_index in cs[node_index]:
            current_sum += get_sum(child_index)

        ffsMap[node_index] = current_sum
        return current_sum


    total_sum = get_sum(root)

    min_diff = total_sum


    for node_index in range(num_nodes):
        if node_index == root:
            continue

        # For a cut above `node_index`, one partition is the subtree at `node_index`.
        partition1_sum = ffsMap[node_index]

        # The other partition is the rest of the tree.
        partition2_sum = total_sum - partition1_sum

        # Calculate the absolute difference and update the minimum.
        diff = abs(partition1_sum - partition2_sum)
        min_diff = min(min_diff, diff)

    return min_diff

# --- Example Usage ---
# Tree Structure:
#        0 (size 10)
#       / \
#      1(3) 2(5)
#     /
#    3(2)
parent_array = [-1, 0, 0, 1]
file_sizes = [10, 3, 5, 2]

min_difference = mostBalancedPartition(parent_array, file_sizes)
print(f"The minimum difference is: {min_difference}")

# --- Verification ---
# Total Sum = 10 + 3 + 5 + 2 = 20
# Subtree sums:
#   Subtree at 3: 2
#   Subtree at 2: 5
#   Subtree at 1: 3 + 2 = 5
#   Subtree at 0: 10 + 5 + 5 = 20
#
# Possible cuts:
#   Cut edge 0-1: Subtree sum is 5. Difference = |5 - (20-5)| = |5 - 15| = 10
#   Cut edge 0-2: Subtree sum is 5. Difference = |5 - (20-5)| = |5 - 15| = 10
#   Cut edge 1-3: Subtree sum is 2. Difference = |2 - (20-2)| = |2 - 18| = 16
#
# The minimum difference is 10.