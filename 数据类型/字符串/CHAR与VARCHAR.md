### CHAR 和 VARCHAR
> 二者均是声明字符个数的字符数据类型，但在存储与检索的时候略有区别

1. CHAR的长度最大的255（不指定时默认为1），而VARCHAR的最大长度为65535个字符（但需要注意row的最大大小为: 65535bytes）。
2. 若未达到CHAR限定的长度，CHAR类型数据在存储时会在右侧用空格填充，因此CHAR占用的存储空间由定义决定。而VARCHAR类型数据未达到限定
长度时，则不会有任何填充。但是VARCHAR类型数据会额外使用1byte-2byte来说明实际长度（限定长度大于255时使用2byte）。
3. 在插入右侧带空格的数据时，若列为CHAR类型，则会自动去掉空格。若列为VARCHAR类型，则会去掉超出限定长度的空格，并产生警告信息。
4. 在检索CHAR类型数据时默认则会去掉填充的空格，VARCHAR类型数据则不会。
5. CHAR与VARCHAR类型的数据在非LIKE比较时都会忽略尾部空格。参照[这里](/比较/比较.md)
6. 对于VARCHAR类型列若加上唯一约束，则只有尾部空格不同的两个值也会产生冲突。（CHAR更是如此）
    ```
    mysql> drop table t1;
    mysql> create table t1(c1 varchar(22), unique key `uqe_c1` (c1));
    mysql> insert into t1 value('abc');
    mysql> insert into t1 value('abc ');
    ERROR 1062 (23000): Duplicate entry 'abc ' for key 'uqe_c1'
    ```