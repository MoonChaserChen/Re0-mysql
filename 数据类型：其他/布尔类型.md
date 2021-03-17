## 布尔类型BOOL, BOOLEAN
布尔类型本质上是TINYINT(1)，但是在比较时有独特的地方。0被认为false，非0被认为true；但是true与false又仅仅是1和0的别名。
如下：
```
mysql> select if(1, 'yes', 'no') as c1, if(2, 'yes', 'no') as c2,if(-1, 'yes', 'no') as c3, if(0, 'yes', 'no') as c4;
+-----+-----+-----+----+
| c1  | c2  | c3  | c4 |
+-----+-----+-----+----+
| yes | yes | yes | no |
+-----+-----+-----+----+
```
在这种隐式比较的时候，0被认为false，而非0被认为true
```
mysql> select (1=true) as c1,(2=true) as c2,(-1=true) as c3,(0=true) as c4;
+----+----+----+----+
| c1 | c2 | c3 | c4 |
+----+----+----+----+
|  1 |  0 |  0 |  0 |
+----+----+----+----+

mysql> select (1=false) as c1,(2=false) as c2,(-1=false) as c3,(0=false) as c4;
+----+----+----+----+
| c1 | c2 | c3 | c4 |
+----+----+----+----+
|  0 |  0 |  0 |  1 |
+----+----+----+----+
```
在上面的显式比较时，又只会把true当作1，false当作0