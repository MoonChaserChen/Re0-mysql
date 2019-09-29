## 关于VARCHAR(M)占用空间大小的猜想及疑惑
由于VARCHAR是可变长的，并不会有填充内容，在底层存储时并不知道该分配多大的内存。因此在存储时会包含原始数据的bytes大小信息。
1byte最大表示的数为255，因此如果原始数据大小不超过255bytes的时候，可以用额外的1byte来表示原始数据大小。同样，2bytes最大表示的数
为65535，如果原始数据大小不超过65535 bytes时，可以用额外的2byte来表示原始数据大小。那么问题来了，由于VARCHAR(M)中的M表示字符个数，
一个字符则是可能占用多个字节的，最终原始数据大小是可能超过65535 bytes的。如果VARCHAR(M)内存储的原始数据
大小超过了65535 bytes，会不会用额外的3 bytes或者更多的bytes来表示原始数据大小呢？
这点在Mysql的[说明文档](/https://dev.mysql.com/doc/refman/5.7/en/storage-requirements.html#data-types-storage-reqs-strings)
中并未有明确的说明。

另一个问题：
如果数据库是以指针的方式指向该VARCHAR数据存储头的位置，又是如何找到后面整个数据块呢？即如何判断出后面整个数据块的结束部分呢？
