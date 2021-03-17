# AND两侧均有索引
根据[官方文档](https://dev.mysql.com/doc/refman/5.7/en/multiple-column-indexes.html)，当AND两侧均有索引时，
optimizer将会使用Index Merge optimization或者使用能排除更多行的索引。

## 测试
```
drop table if exists t1;
create table t1(k1 varchar(22), k2 varchar(22), index `idx_k1` (k1), index `idx_k2` (k2));
insert into t1 values
('Lettie', 'SpasianoK2'),
('Vivienne', 'LimogesK2'),
('Stella', 'CascoK2'),
('Ruthann', 'BusickK2'),
('Jay', 'WetzelK2'),
('Glendora', 'ShackeltonK2'),
('Hye', 'AffeltrangerK2'),
('Terrence', 'BihmK2'),
('Doretta', 'KleinhenzK2'),
('Dallas', 'CanoK2'),
('Tena', 'CayerK2'),
('Karlene', 'FeltusK2'),
('Jenifer', 'LevangieK2'),
('Michel', 'LottiK2'),
('Emelda', 'SlackmanK2'),
('Nereida', 'ManganoK2'),
('Cristobal', 'BeardedK2'),
('Barbar', 'TagK2'),
('Concepcion', 'MangK2'),
('Kimberely', 'SchaapK2'),
('Marlana', 'BitettoK2'),
('Coreen', 'CollumsK2'),
('Monnie', 'ThalK2'),
('Tammara', 'FinzelK2'),
('Dolly', 'SimleyK2'),
('Kimberely', 'KettlewellK2'),
('Cheree', 'McenroeK2'),
('Elbert', 'RemkusK2'),
('Nola', 'PeaceK2'),
('Joelle', 'KronK2'),
('Raymon', 'TorranceK2'),
('Alton', 'WarringK2'),
('Giovanna', 'BorshK2'),
('Kandace', 'GuerardK2'),
('Un', 'JacquezK2'),
('Noelle', 'MensahK2'),
('Brooks', 'HableK2'),
('Robert', 'DykasK2'),
('Adelaida', 'BoehnleinK2'),
('Mellisa', 'RolenK2'),
('Salvatore', 'MarcheskiK2'),
('Nisha', 'AumavaeK2'),
('Bennie', 'BennettsK2'),
('Carole', 'PatagueK2'),
('Anika', 'AshingK2'),
('Tesha', 'DevaultK2'),
('Rea', 'ZaisK2'),
('Victoria', 'BarberiK2'),
('Jerry', 'NantzK2'),
('Patsy', 'MirlesK2');
```

- 走k1索引：
```
mysql> explain select * from t1 where k1 = 'abc' and k2 = 'cde';
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key    | key_len | ref   | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------------+
|  1 | SIMPLE      | t1    | NULL       | ref  | idx_k1,idx_k2 | idx_k1 | 69      | const |    1 |     5.00 | Using where |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------------+
```
- 走k2索引
```
mysql> explain select * from t1 where k1 like 'A%' and k2 = 'cde';
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------------+
| id | select_type | table | partitions | type | possible_keys | key    | key_len | ref   | rows | filtered | Extra       |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------------+
|  1 | SIMPLE      | t1    | NULL       | ref  | idx_k1,idx_k2 | idx_k2 | 69      | const |    1 |     6.00 | Using where |
+----+-------------+-------+------------+------+---------------+--------+---------+-------+------+----------+-------------+
```
- Index Merge
```
mysql> explain select * from t1 where k1 like 'A%' and k2 like 'M%';
+----+-------------+-------+------------+-------+---------------+--------+---------+------+------+----------+------------------------------------+
| id | select_type | table | partitions | type  | possible_keys | key    | key_len | ref  | rows | filtered | Extra                              |
+----+-------------+-------+------------+-------+---------------+--------+---------+------+------+----------+------------------------------------+
|  1 | SIMPLE      | t1    | NULL       | range | idx_k1,idx_k2 | idx_k1 | 69      | NULL |    3 |    12.00 | Using index condition; Using where |
+----+-------------+-------+------------+-------+---------------+--------+---------+------+------+----------+------------------------------------+
```
这里的例子不对，`Index Merge` 时在Extra中会显示： `Using index` ；
但是这里显示： `Using index condition` 表示发生了 `Index Condition Pushdown`