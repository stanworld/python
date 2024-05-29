class Solution:
    def isPerfectSquare(self, num):
        l=1
        r=num
        while(l<=r):
            mid = l+int((r-l)/2)
            if(mid*mid==num):
                return True
            elif (mid*mid>num):
                r=mid-1
            else:
                l=mid+1
        
        return False
"""   
class Solution:
    def twoSum(self, nums, target):
        n = len(nums)
        for i in range(n-1):
            for j in range(i+1,n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        
        return []
"""
class Solution:
    def twoSum(self, nums, target):
        numMap={}
        n=len(nums)
        for i in range(n):
            compliment = target-nums[i]
            if(compliment in numMap):
                return [i, numMap[compliment]]
            numMap[nums[i]]=i
        return []
    def longestCommonPrefix(self, strs: list[str]) -> str:
        pref = strs[0]
        pref_len = len(pref)
        for s in strs[1:]:
            while pref != s[0:pref_len]:
                pref_len = pref_len-1
                if pref_len == 0:
                    return ""
                pref = pref[0:pref_len]
            
        return pref


for i in range(10):
    print(i)

from typing import List, Dict

students: List[Dict[str, int]] = [
    {"name": 2},
    {"name": 1}
]
print(students)


class Solution:
    def removeDuplicates(self, nums) -> int:
        i = 0 
        while i < len(nums) - 1:  
            if nums[i] == nums[i + 1]:
                print(nums[i + 1])  
                nums.pop(i + 1)  #remove an element from the list based on the index 
            else:
                i += 1  

        return len(nums)  
    
    def lengthOfLastWord(self, s: str) -> int:
        words = s.strip().split()
        
        if not words:
            return 0
        
        return len(words[-1])

from typing import Optional

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
    

if __name__ == "__main__":
    s= Solution()

import heapq

# Example list
numbers = [4, 2, 9, 1, 5, 6]

# Transform the list into a heap
heapq.heapify(numbers)

print(numbers)  # Output: [1, 2, 6, 4, 5, 9] (elements are reordered to satisfy heap property)

heapq.heappush(numbers, 3)

print(numbers)  # Output: [1, 2, 6, 4, 5, 9, 3]

smallest = heapq.heappop(numbers)

print(smallest)  # Output: 1
print(numbers)  # Output: [2, 3, 6, 4, 5, 9]

import heapq

class MaxHeap:
    def __init__(self):
        self._heap = []

    def push(self, value):
        # Negate the value to simulate max-heap behavior
        heapq.heappush(self._heap, -value)

    def pop(self):
        # Negate the value again to get the original value
        return -heapq.heappop(self._heap)

    def peek(self):
        # Return the negated value of the smallest element
        return -self._heap[0]

    def __len__(self):
        # Return the number of elements in the heap
        return len(self._heap)

# Example usage
max_heap = MaxHeap()
max_heap.push(4)
max_heap.push(2)
max_heap.push(9)
max_heap.push(1)

print(max_heap.pop())  # Output: 9
print(max_heap.pop())  # Output: 4
print(max_heap.pop())  # Output: 2
print(max_heap.pop())  # Output: 1




for i in range(1,10):
    print(i)