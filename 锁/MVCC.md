# MVCC
MySQL、ORACLE、PostgreSQL等成熟的数据库，出于性能考虑，都是使用了以乐观策略为理论基础的MVCC（Multi-Version Concurrency Control多版本并发控制），
读不加锁，读写不冲突。Mysql的InnoDB实现RR事务隔离级别采用的手段：
## 版本号的实现机制
MVCC的版本号可分为两类：
- 系统版本号

    一个递增的数字，每开始一个新的事务，系统版本号就会自动递增。
- 事务版本号

    事务开始时的系统版本号。
    
在MySQL中，会在表中每一条数据后面添加两个字段：
1. 创建版本号：创建一行数据时，将当前系统版本号作为创建版本号赋值
2. 删除版本号：删除一行数据时，将当前系统版本号作为删除版本号赋值

### SELECT
select时读取数据的规则为：创建版本号<=当前事务版本号，删除版本号为空或>当前事务版本号。
### INSERT
insert时将当前的系统版本号赋值给创建版本号字段。
### DELETE
将当前的系统版本号赋值给删除版本号字段，标识该行数据在那一个事务中会被删除，在commit时删除该数据。
### UPDATE
插入一条新纪录，保存当前事务版本号为行创建版本号，同时保存当前事务版本号到原来删除的行，实际上这里的更新是通过delete和insert实现的

## MVCC的读
在MVCC并发控制中，读操作可以分为两类：快照读与当前读。
- 快照读

    简单的select操作，读取的是记录中的可见版本（可能是历史版本），不用加锁。

- 当前读

    特殊的select操作、insert、delete和update，读取的是记录中最新版本，并且当前读返回的记录都会加上锁，这样保证了了其他事务不会再并发修改这条记录。
    > 特殊的select操作包括 select .. for update; select .. lock in share mode
    
### MVCC如何解决“不可重复读”
不可重复读是指：在事务执行过程中，当两个完全相同的查询语句执行得到不同的结果集。（源自维基百科）
> 有的将“查询语句”仅限于理解为SELECT，我这里理解为也包含UPDATE中的WHERE等

MVCC采用快照读来解决“不可重复读”： 在事务A的第一个select语句会生成快照，之后的select都会返回这个快照，保证了同一事务多次读结果的一致性。
    
### MVCC解决了幻读？
幻读是指：在一个事务内，两次读取到的数据量不一致

参看以下例子：
```
mysql> drop table if exists t1;
mysql> create table t1(id bigint, name varchar(22));
mysql> insert into t1 values (10, 'Lisa'), (20, 'Marry'), (30, 'Tom');
```
#### SELECT情况
| 事务1 | 事务2 |
| :---- | :---- |
| begin; | - |
| select * from t1 where id between 10 and 30; | begin; |
| - | insert into t1 value (25, 'Jack'); |
| - | commit; |
| select * from t1 where id between 10 and 30; | - |
| commit; | - |
这里两次结果是相同的，因此在这种情况下是解决了幻读的。

#### UPDATE情况
| 事务1 | 事务2 |
| :---- | :---- |
| begin | - |
| select * where id between 10 and 30; | begin; |
| - | insert into t1 value (25, 'Jack'); |
| - | commit; |
| update t1 set name = 'same' where id between 10 and 30; | - |
| commit; | - |
在执行完成后：
```
mysql> select * from t1;
+------+------+
| id   | name |
+------+------+
|   10 | same |
|   20 | same |
|   30 | same |
|   25 | same |
+------+------+
4 rows in set (0.00 sec)
```

事务1中两次均会去查找id在10与30之间的数据，**第一次SELECT只会查出3条，但是第二次UPDATE时却查出了4条**（由更新后的结果得知）。

#### 特殊SELECT情况
| 事务1 | 事务2 |
| :---- | :---- |
| begin; | - |
| select * from t1 where id between 10 and 30; | begin; |
| - | insert into t1 value (25, 'Jack'); |
| - | commit; |
| select * from t1 where id between 10 and 30 lock in share mode; | - |
| commit; | - |
事务1第一次采用普通读，第二次采用特殊读，同样两次也会得出不同结果

因此可以得知MVCC并未完全解决幻读问题。

#### 如何解决幻读
可重复读的隔离级别没有办法彻底的解决幻读的问题，如果我们的项目中需要解决幻读的话也有两个办法：
1. 使用串行化读的隔离级别
2. MVCC + next-key locks
 > next-key locks由record locks(索引加锁) 和 gap locks(间隙锁，每次锁住的不光是需要使用的数据，还会锁住这些数据附近的数据)

实际上很多的项目中是不会使用到上面的两种方法的，串行化读的性能太差，而且其实幻读很多时候是我们完全可以接受的。


