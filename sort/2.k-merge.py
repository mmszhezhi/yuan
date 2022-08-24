from queue import PriorityQueue
from typing import List


class ListNode:
    def __init__(self,value):
        self.val = value
        self.next = None
        self.prev = None



def mergeKLists(lists: List[ListNode]) -> ListNode:
    #小顶堆
    pq = PriorityQueue()
    #遍历所有链表第一个元素
    for i in range(len(lists)):
        #不为空则加入小顶堆
        if lists[i] != None:
            pq.put((lists[i].val, i))
            lists[i] = lists[i].next
    #加一个表头
    res = ListNode(-1)
    head = res
    #直到小顶堆为空
    while not pq.empty():
        #取出最小的元素
        val, idx = pq.get()
        #连接
        head.next = ListNode(val)
        head = head.next
        if lists[idx] != None:
            #每次取出链表的后一个元素加入小顶堆
            pq.put((lists[idx].val, idx))
            lists[idx] = lists[idx].next
    return res.next


lists = []
cur = None

x= [[3,2,1],[9,5]]
for xx in x:
    head = None
    cur = None
    prev = None
    for i in xx:
        if cur:
            prev = cur
        cur = ListNode(i)
        if prev:
            prev.next = cur
        if not head:
            head = cur
            lists.append(head)
result = mergeKLists(lists)
print(result)
while result:
    print(result.val)
    result = result.next