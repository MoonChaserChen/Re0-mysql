### BINARY 和 VARBINARY
> 可以理解为存储二进制字符的CHAR与VARCHAR

1. char(1)中的1表示1个字符（一个中文也可），但binary(1)中的1表示1byte
    ```
    mysql> create table t1(c1 binary(1));
    mysql> insert into t1 value('a');
    mysql> insert into t1 value('陈');
    ERROR 1406 (22001): Data too long for column 'c1' at row 1
    ```
2. BINARY与CHAR一样，最大指定长度为255（但这里单位为byte，参看第1条）
    ```
    mysql> create table t1(c1 binary(256));
    ERROR 1074 (42000): Column length too big for column 'c1' (max = 255); use BLOB or TEXT instead
    ```
3. binary的列若值长度不足，则会使用0x00填充（相对于char的空格），并且在检索时填充不会被去掉（char在检索时会被去掉）
    ```
    mysql> create table t1(c1 char(3), c2 binary(3));
    mysql> insert into t1 values('a1', 'a'), ('a2', 'a ');
    mysql> select * from t1 where c2 = 'a';
    Empty set (0.00 sec)
    mysql> select * from t1 where c2 = 'a ';
    Empty set (0.00 sec)
    mysql> select * from t1 where c2 = 'a\0\0';
    +------+------+
    | c1   | c2   |
    +------+------+
    | a1   | a    |
    +------+------+
    mysql> select * from t1 where c2 = 'a \0';
    +------+------+
    | c1   | c2   |
    +------+------+
    | a2   | a    |
    +------+------+
    ```
4. 同样对于BINARY类型列若加上唯一约束，则只有尾部\0不同的两个值也会产生冲突。对于VARBINARY类型列则不会产生冲突。
    ```
    mysql> create table t1 (c1 binary(3), unique key `uqe_c1` (c1));
    mysql> insert into t1 value('a');
    mysql> insert into t1 value('a ');
    mysql> insert into t1 value('a\0');
    ERROR 1062 (23000): Duplicate entry 'a' for key 'uqe_c1'
    ```