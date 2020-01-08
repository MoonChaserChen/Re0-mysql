# 联合索引的leftmost
在很多地方的博客都能看到联合索引只有对leftmost的条件才会走索引，例如：key `idx_multi_key` (k1_p1, k1_p2, k1_p3)。只有查询条件均涉及以下情况的时候才会走索引：
1. k1_p1
2. k1_p1 && k1_p2
3. k1_p1 && k1_p2 && k1_p3

## 非leftmost也能走索引？
但实际上我遇到了不对索引的leftmost进行查询时也走了索引，记录如下：
```
drop table if exists t1;
create table t1(k1 varchar(22), k2_p1 varchar(22), k2_p2 varchar(22), primary key (k1), index `idx_k2` (k2_p1, k2_p2));

insert into t1 values
('defreeze', 'unscalloped', 'dishwiping'),
('embodier', 'cenospecific', 'retrojugular'),
('disenchantress', 'manticism', 'oligoclase'),
('phosphoprotein', 'microstylospore', 'naillike'),
('downcast', 'protuberance', 'tymbalon'),
('eliasite', 'gausterer', 'paidology'),
('philanthropian', 'Telotremata', 'nonulcerous'),
('Rumanian', 'salvably', 'overunionized'),
('mobocracy', 'ferroaluminum', 'countertree'),
('visor', 'Lo', 'unconvoluted'),
('wheedlingly', 'arthrostomy', 'sarcoplasma'),
('Liz', 'transmigrator', 'postcondylar'),
('virginality', 'overiodize', 'eelcake'),
('Caesarotomy', 'Aeolia', 'unmodifiedness'),
('beice', 'angustifolious', 'dismissal'),
('Diomedeidae', 'carnaged', 'uncommitted'),
('archigenesis', 'untreasured', 'silkgrower'),
('mezzograph', 'inscrutably', 'Turkomanic'),
('feminality', 'cirsectomy', 'osteopath'),
('semitertian', 'sportfulness', 'photoinhibition'),
('insensate', 'flammable', 'heatingly');

explain select * from t1 where  k2_p2 = 'heatingly';
```

其结果为：
```
mysql> explain select * from t1 where  k2_p2 = 'heatingly';
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+--------------------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra                    |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+--------------------------+
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_k2    | 138     | NULL |   21 |    10.00 | Using where; Using index |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+--------------------------+
```
可以看到这里虽然没有possible_keys，但是有key，也就是走了索引的。

同时根据[官方文档](https://dev.mysql.com/doc/refman/5.7/en/multiple-column-indexes.html) 对于下面的表来说：
```
DROP table if exists test;
CREATE TABLE test (
    id         INT NOT NULL,
    last_name  CHAR(30) NOT NULL,
    first_name CHAR(30) NOT NULL,
    PRIMARY KEY (id),
    INDEX name (last_name,first_name)
);
```
下面的语句是不会走索引的：
```
explain SELECT * FROM test WHERE first_name='John';
explain SELECT * FROM test WHERE last_name='Jones' OR first_name='John';
```
但结果却是：
```
mysql> explain SELECT * FROM test WHERE first_name='John';
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+--------------------------+
| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows | filtered | Extra                    |
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+--------------------------+
|  1 | SIMPLE      | test  | NULL       | index | NULL          | name | 180     | NULL |    1 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+--------------------------+

mysql> explain SELECT * FROM test WHERE last_name='Jones' OR first_name='John';
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+--------------------------+
| id | select_type | table | partitions | type  | possible_keys | key  | key_len | ref  | rows | filtered | Extra                    |
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+--------------------------+
|  1 | SIMPLE      | test  | NULL       | index | name          | name | 180     | NULL |    1 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+-------+---------------+------+---------+------+------+----------+--------------------------+
```
确实是走了索引的。