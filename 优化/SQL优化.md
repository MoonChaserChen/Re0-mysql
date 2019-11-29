# SQL优化
## 减少参与JOIN的行数量
比如JOIN+分页，可以试着将分页放到JOIN前面。

## 尽量避免不等于
应尽量避免在 where 子句中使用 != 或 <> 操作符，否则引擎将可能放弃使用索引而进行全表扫描。

## 避免SQL函数导致不走索引
```
SELECT * FROM student WHERE FIND_IN_SET(SId,('1,2'));
```


