from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
#

import heapq
class Solution2:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        l = []
        size = len(lists)

        for index in range(size):
            # 针对一些特殊的测试用例，有的链表可能是空链表
            if lists[index]:
                heapq.heappush(l, (lists[index].val, index))

        dummy_node = ListNode(-1)
        cur = dummy_node

        while l:
            _, index = heapq.heappop(l)

            # 定位到此时应该出列的那个链表的头结点
            head = lists[index]
            # 开始“穿针引线”
            cur.next = head
            cur = cur.next
            # 同样不要忘记判断到链表末尾结点的时候
            if head.next:
                # 刚刚出列的那个链表的下一个结点成为新的链表头结点加入优先队列
                heapq.heappush(l, (head.next.val, index))
                # 切断刚刚出列的那个链表的头结点引用
                lists[index] = head.next
                head.next = None
        return dummy_node.next
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        # write code here
        if lists is None: return None
        result = []
        for pHead in lists:
            while pHead:
                result.append(pHead.val)
                pHead = pHead.next
        if len(result) == 0: return None
        result.sort()
        head1 = NewHead = ListNode(0)
        for data in result:
            NewHead.next = ListNode(0)
            NewHead = NewHead.next
            NewHead.val = data

        return head1.next


s = Solution2()

lists = []
cur = None

x= [[3,88,1],[900,5],[0]]
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
result = s.mergeKLists(lists)
print(result)

while result:
    print(result.val)
    result = result.next