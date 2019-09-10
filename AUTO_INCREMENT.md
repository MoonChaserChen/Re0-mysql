## AUTO_INCREMENT	
    说明：对列值进行自增
0. 一张表只能有一个列设为auto_increment
    ```
    mysql> create table t1 (k1 bigint auto_increment, k2 bigint auto_increment, key `idx_k1` (k1), key `idx_k2` (k2));
    ERROR 1075 (42000): Incorrect table definition; there can be only one auto column and it must be defined as a key
    ```
0. 插入值时指定为0、NULL或不指定进行自增
    ```
    mysql> create table t1(k1 bigint not null auto_increment, c1 varchar(22), primary key (k1));
    mysql> insert into t1 (c1) values ('nothings');
    mysql> insert into t1 values (0, 'nothings'), (null, 'nothings');
    mysql> select * from t1;
    +----+----------+
    | k1 | c1       |
    +----+----------+
    |  1 | nothings |
    |  2 | nothings |
    |  3 | nothings |
    +----+----------+
    ```
0. 设为auto_increment的列必须为Integer Types，包括TINYINT，SMALLINT，MEDIUMINT，INT，BIGINT
0. 设为auto_increment 的列必须为index 或 multiple-column index 第一个值，对于MyISAM表则可以不为multiple-column index第一个，这样自增的时候会依据multiple-column
    ```
    mysql> create table t1(k1_0 varchar(22), k1_1 bigint auto_increment, c2 varchar(22), key `idx_k1` (k1_0, k1_1)) engine = 'MyISAM';
    mysql> insert into t1 values('group1', null, 'nothing'), ('group1', null, 'nothing'), ('group1', null, 'nothing'), ('group2', null, 'nothing');
    mysql> select * from t1;
    +--------+------+---------+
    | k1_0   | k1_1 | c2      |
    +--------+------+---------+
    | group1 |    1 | nothing |
    | group1 |    2 | nothing |
    | group1 |    3 | nothing |
    | group2 |    1 | nothing |
    +--------+------+---------+
    ```
    这种情况下自增列的值具有复用性（一般是不会复用的）:
    ```
    mysql> delete from t1 where k1_0 = 'group1' and k1_1 = 3;
    mysql> insert into t1 values('group1', null, 'nothing'), ('group1', null, 'nothing');
    mysql> select * from t1;
    +--------+------+---------+
    | k1_0   | k1_1 | c2      |
    +--------+------+---------+
    | group1 |    1 | nothing |
    | group1 |    2 | nothing |
    | group1 |    3 | nothing |
    | group2 |    1 | nothing |
    | group1 |    4 | nothing |
    +--------+------+---------+
    ```
0.  可以使用CREATE TABLE或ALTER TABLE命令设置AUTO_INCREMENT值
    ```
    mysql> create table t1(k1 bigint not null auto_increment, c1 varchar(22), primary key (k1)) auto_increment = 100;
    mysql> insert into t1 (c1) values ('nothings'), ('nothings');
    mysql> alter table t1 auto_increment = 200;
    mysql> insert into t1 (c1) values ('nothings');
    mysql> insert into t1 (c1) values ('nothings');
    mysql> select * from t1;
    +-----+----------+
    | k1  | c1       |
    +-----+----------+
    | 100 | nothings |
    | 101 | nothings |
    | 200 | nothings |
    | 201 | nothings |
    +-----+----------+
    ```
0. DELETE与UPDATE不会影响AUTO_INCREMENT值 
    ```
    mysql> create table t1(k1 bigint not null auto_increment, c2 varchar(22), primary key (k1));
    mysql> insert into t1 values(null, 'nothing'), (null, 'nothing'), (null, 'nothing'), (null, 'nothing');
    mysql> delete from t1 where k1 = 4 or k1 = 2;
    mysql> insert into t1 values(null, 'nothing'), (null, 'nothing');
    mysql> select * from t1;
    +----+---------+
    | k1 | c2      |
    +----+---------+
    |  1 | nothing |
    |  3 | nothing |
    |  5 | nothing |
    |  6 | nothing |
    +----+---------+
    ```
    删除k1=2, k1=4的空缺并没有补上，即AUTO_INCREMENT的值并未被修改
    ```
    mysql> update t1 set k1 = 10 where k1 = 6;
    mysql> insert into t1 values(null, 'nothing'), (null, 'nothing');
    mysql> select * from t1;
    +-----+---------+
    | k1  | c2      |
    +-----+---------+
    |   1 | nothing |
    |   3 | nothing |
    |   5 | nothing |
    |   7 | nothing |
    |   8 | nothing |
    |  10 | nothing |
    +-----+---------+
    ```
    更新k1最大值为10，递增序列也仍是从之前的6开始，即AUTO_INCREMENT的值并未被修改。但是在这种情况下，若继续插入两条记录，AUTO_INCREMENT的增加会与已经存在的k1=10产生主键冲突
    ```
    mysql> insert into t1 values(null, 'nothing'), (null, 'nothing');
    ERROR 1062 (23000): Duplicate entry '10' for key 'PRIMARY'
    ```
    在报上述主键冲突后，继续插入记录则是不影响了，因为AUTO_INCREMENT已经越过了可能会冲突的10
    ```
    mysql> insert into t1 values(null, 'nothing'), (null, 'nothing');
    mysql> select * from t1;
    +----+---------+
    | k1 | c2      |
    +----+---------+
    |  1 | nothing |
    |  3 | nothing |
    |  5 | nothing |
    |  7 | nothing |
    |  8 | nothing |
    | 10 | nothing |
    | 11 | nothing |
    | 12 | nothing |
    +----+---------+
    ```
0. INSERT会影响AUTO_INCREMENT值
    ```
    mysql> create table t1(k1 bigint not null auto_increment, c2 varchar(22), primary key (k1));
    mysql> insert into t1 values(null, 'nothing'), (null, 'nothing'), (null, 'nothing'), (null, 'nothing');
    mysql> select * from t1;
    mysql> insert into t1 value (100, 'flag');
    mysql> insert into t1 values (null, 'nothing'), (null, 'nothing');
    mysql> select * from t1;
    +-----+---------+
    | k1  | c2      |
    +-----+---------+
    |   1 | nothing |
    |   2 | nothing |
    |   3 | nothing |
    |   4 | nothing |
    | 100 | flag    |
    | 101 | nothing |
    | 102 | nothing |
    +-----+---------+
    ```
    插入k1=100的值后，AUTO_INCREMENT从101开始了。