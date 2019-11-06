## DATETIME与TIMESTAMP的比较
DATETIME与TIMESTAMP均是MYSQL中可以表示**日期+时间**的数据类型，他们之间的差异如下：
1. 范围

    | 类型 | 范围 |
    | ---- | ---- |
    | DATETIME | 1000-01-01 00:00:00.000000 到 9999-12-31 23:59:59.999999 |
    | TIMESTAMP | 1970-01-01 00:00:01.000000 到 2038-01-19 03:14:07.999999 |
    
2. 时区

    TIMESTAMP是以UTC时区存储的，而DATETIME则未带时区信息。因此修改MYSQL时区设置后不会影响DATETIME的值，但是会影响TIMESTAMP的值
    ```
    mysql> create table t1(c1 datetime, c2 timestamp);
    mysql> insert into t1 value(now(), now());
    mysql> select * from t1;
    +---------------------+---------------------+
    | c1                  | c2                  |
    +---------------------+---------------------+
    | 2019-10-02 11:46:06 | 2019-10-02 11:46:06 |
    +---------------------+---------------------+
    
    mysql> set time_zone = '+05:00';    
    mysql> select * from t1;
    +---------------------+---------------------+
    | c1                  | c2                  |
    +---------------------+---------------------+
    | 2019-10-02 11:46:06 | 2019-10-02 08:46:06 |
    +---------------------+---------------------+
    ```
    
    在设置时区以前默认是：中国时间，GMT+8，也就是'+08:00'，当修改为'+05:00'后DATETIME的值并未改变，但是TIMESTAMP减小了3个小时
    
3. 月日为零

    DATETIME支持月日为零，TIMESTAMP不支持（0000-00-00除外）。
    ```
    mysql> create table t1(c1 datetime, c2 timestamp);
    mysql> insert into t1 value('2019-09-00', '2019-10-00');
    ERROR 1292 (22007): Incorrect datetime value: '2019-10-00' for column 'c2' at row 1
    ```
    其相关设置参见[NO_ZERO_IN_DATE](/数据类型/时间类型/时间类型相关设置.md#NO_ZERO_IN_DATE)
    
4. NOT NULL/NULL 与 DEFAULT

    DATETIME默认NULL（允许NULL值），且其默认值为NULL。
    其结果为：
    ```
    mysql> create table t1(c1 datetime);
    mysql> show create table t1;
    CREATE TABLE `t1` (
       `c1` datetime DEFAULT NULL
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    ```
    默认情况下（explicit_defaults_for_timestamp=OFF），TIMESTAMP类型自带NOT NULL
    ```
    mysql> create table t1(c1 timestamp);
    mysql> show create table t1;
    CREATE TABLE `t1` (
       `c1` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
     ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    ```
    其相关设置参见[explicit_defaults_for_timestamp](/数据类型/时间类型/时间类型相关设置.md#explicit_defaults_for_timestamp)

5. 存储及空间占用

    TIMESTAMP使用4bytes来存储1970年以来的秒，外加0-3bytes来存储秒的精度。
    DATETIME使用5bytes来存储年月日时分秒，外加0-3bytes来存储秒的精度。
    详见[时间类型的底层存储](/数据类型/时间类型/时间类型的底层存储.md)
    
6. 自动初始化(auto-initialized)及自动更新(auto-update)

    自动初始化(auto-initialized)：在插入数据时没有指明字段值时，默认赋予值。
    自动更新(auto-update)：在没有明确修改字段值，但是却修改了其它列值关导致了值的改变时，默认赋予值。
    默认情况下（explicit_defaults_for_timestamp=OFF），TIMESTAMP类型自带DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP。
    ```
    mysql> create table t1(c1 varchar(22), c2 timestamp);
    mysql> insert into t1 (c1) value('abc');
    mysql> select * from t1;
    +------+---------------------+
    | c1   | c2                  |
    +------+---------------------+
    | abc  | 2019-10-03 11:13:30 |
    +------+---------------------+
    
    mysql> update t1 set c1 = 'def';
    mysql> select * from t1;
    +------+---------------------+
    | c1   | c2                  |
    +------+---------------------+
    | def  | 2019-10-03 11:15:05 |
    +------+---------------------+
    ```
    上面创建表时，TIMESTAMP类型的c2自带DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP（可通过show create table t1查看）。
    在插入数据时不指明c2的值，自动设置当前时间（DEFAULT CURRENT_TIMESTAMP）。在修改数据时，只修改c1的值，c2也自动更新为当前时间（ON UPDATE CURRENT_TIMESTAMP）