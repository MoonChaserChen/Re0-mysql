# 联合索引的leftmost
在很多地方的博客都能看到联合索引只有对leftmost的条件才会走索引，例如：key `idx_multi_key` (k1_p1, k1_p2, k1_p3)。只有查询条件均涉及以下情况的时候才会走索引：
1. k1_p1
2. k1_p1 && k1_p2
3. k1_p1 && k1_p2 && k1_p3

## 非leftmost也能走索引？
但实际上我遇到了不对索引的leftmost进行查询时也走了索引，记录如下：
```
create table t1(k1 varchar(22), k2_p1 varchar(22), k2_p2 varchar(22), primary key (k1), index `idx_k2_k3` (k2_p1, k2_p2));

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
|  1 | SIMPLE      | t1    | NULL       | index | NULL          | idx_k2_k3 | 138     | NULL |   21 |    10.00 | Using where; Using index |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+--------------------------+
```
可以看到这里虽然没有possible_keys，但是有key，也就是走了索引的。