### BLOB 和 TEXT
> 大容量的字符类型。BLOB可视为大容量的VARBINARY，TEXT可视为大容量的VARCHAR（不同之处参见下面第4，5点）

1. TEXT类型数据与BLOB类型数据均没有填充
2. TEXT类型数据会去掉超出限定长度的空格，同时产生警告信息。
3. TEXT类型列若加上唯一约束，则只有尾部空格不同的两个值也会产生冲突。BLOB类型则不会。
4. BLOB与TEXT类型数据若加上索引，则必须指定索引长度
5. BLOB与TEXT类型数据不能有默认值
6. 由于MEMORY存储引擎并不支持BLOB和TEXT类型，因此如果将查询的BLOB或TEXT结果放置于临时表中的时候，MYSQL会使用硬盘表而不是内存表，这将影响性能。
7. 由于BLOB和TEXT的内容一般都很大，因此在参与排序的时候要注意这个配置：max_sort_length，默认为1024 bytes。同时在插入时也需要注意这个配置：max_allowed_packet，默认为4MB
8. BLOB与TEXT采用一个单独的对象存储，而其它数据类型则是一个列分配一个对象