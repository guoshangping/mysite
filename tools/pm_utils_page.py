#!/usr/bin/python
# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

import math

"""-----------------------------------分页方法---------------------------------------"""


class PagePaging(object):
    def __init__(self, totalmsg, napage):
        self.totalmsg = totalmsg  # 此次分页的信息的总的条数
        self.napage = napage  # 每页所含的信息条数
        self.data = {}

    def totalpage(self):
        # totalpage是总的页数
        if self.napage >= self.totalmsg:
            return 1
        return int(math.ceil(self.totalmsg / float(self.napage)))

    def judge(self):
        totalpage = self.totalpage()
        if totalpage == 1:
            self.data[1] = Page(1, start=0, end=self.totalmsg)
        else:
            for pg in range(totalpage):
                # if 判断 是因为第一页的start是0，其他页的start是上一页 第一页没有上一页
                if pg == 0:
                    self.data[pg + 1] = Page(pagenum=pg + 1, start=0, end=self.napage)  # napage=10时 代表第0到第9条，
                else:
                    self.data[pg + 1] = Page(pagenum=pg + 1, start=self.data[pg].end,
                                             end=self.data[pg].end + self.napage) # napage=10时，代表第10到19条的10条数据

            if self.totalmsg % self.napage != 0:
                # 上面的循环 已经循环了最后一页，这层if是用来重置最后一页的 如果最后一页的数据不够10 就走这个if
                self.data[totalpage] = Page(pagenum=totalpage, start=self.data[totalpage - 1].end, end=self.totalmsg)
        return totalpage

    def re_page(self, pagenum):
        pagenum = int(pagenum)
        if pagenum in self.data.keys():
            return self.data[pagenum]
        else:
            return self.data[1]


class Page(object):
    def __init__(self, pagenum, start, end):
        self._pagenum = pagenum
        self._start = start
        self._end = end

    @property
    def pagenum(self):
        return self._pagenum

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
