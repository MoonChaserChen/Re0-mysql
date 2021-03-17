## BIT_COUNT

考虑对下面的数据进行分月计数：
```
mysql> CREATE TABLE t1 (year YEAR(4), month int, day int);
mysql> INSERT INTO t1 VALUES (2000,1,1),(2000,1,20),(2000,1,30),(2000,2,2),(2000,2,23),(2000,2,23);
mysql> select * from t1;
+------+-------+------+
| year | month | day  |
+------+-------+------+
| 2000 |     1 |    1 |
| 2000 |     1 |   20 |
| 2000 |     1 |   30 |
| 2000 |     2 |    2 |
| 2000 |     2 |   23 |
| 2000 |     2 |   23 |
+------+-------+------+
```

一般的做法是：
```
mysql> select year, month, count(distinct day) as days from t1 group by year, month;
+------+-------+------+
| year | month | days |
+------+-------+------+
| 2000 |     1 |    3 |
| 2000 |     2 |    2 |
+------+-------+------+
```

使用BIT_COUNT：
```
mysql> SELECT year,month,BIT_COUNT(BIT_OR(1<<day)) AS days FROM t1 GROUP BY year,month;
+------+-------+------+
| year | month | days |
+------+-------+------+
| 2000 |     1 |    3 |
| 2000 |     2 |    2 |
+------+-------+------+
```

参考：

`https://dev.mysql.com/doc/refman/5.7/en/calculating-days.html`

注意BIT_COUNT数值大小有限制：
```
mysql> select BIT_COUNT(3 << 30);
+--------------------+
| BIT_COUNT(3 << 30) |
+--------------------+
|                  2 |
+--------------------+

mysql> select BIT_COUNT(3 << 63);
+--------------------+
| BIT_COUNT(3 << 63) |
+--------------------+
|                  1 |
+--------------------+

mysql> select BIT_COUNT(3 << 100);
+---------------------+
| BIT_COUNT(3 << 100) |
+---------------------+
|                   0 |
+---------------------+
```

Mysql数据类型最多64位
