# InnoDB中的死锁
## 死锁例子
### 准备
```
mysql> CREATE TABLE t (i INT) ENGINE = InnoDB;
Query OK, 0 rows affected (1.07 sec)

mysql> INSERT INTO t (i) VALUES(1);
Query OK, 1 row affected (0.09 sec)
```
### 死锁场景
```dot
digraph G {

  subgraph T0 {
    style=filled;
    color=lightgrey;
    node [style=filled,color=white];
    a0 -> a1 -> a2 -> a3 -> a4;
    label = "事务A";
  }

  subgraph T1 {
    node [style=filled];
    b0 -> b1 -> b2 -> b3 -> b4;
    label = "事务B";
    color=grey
  }

    a0[label = "START TRANSACTION;"]
    a1[label = "SELECT * FROM t WHERE i = 1 LOCK IN SHARE MODE;"]
    a2[label = ""]
    a3[label = ""]
    a4[label = "DELETE FROM t WHERE i = 1;"]
    
    b0[label = ""]
    b1[label = ""]
    b2[label = "START TRANSACTION;"]
    b3[label = "DELETE FROM t WHERE i = 1;"]
    b4[label = ""]
}
```
### 死锁之后
发生了死锁后，InnoDB会在其中一个事务中提示错误信息，并释放此事务持有的锁。这样另一个事务就得以顺利进行了。
```
ERROR 1213 (40001): Deadlock found when trying to get lock;
try restarting transaction
```