##大小写敏感性：
0. 排序时：
    
    默认不区分大小写
    ```
    mysql> select * from user_book order by user_name;
    +----+------------+-----------+---------+
    | id | user_id    | user_name | book_id |
    +----+------------+-----------+---------+
    |  2 | 1143013022 | abira     |       1 |
    |  1 | 1143013021 | Akira     |       1 |
    |  4 | 1143013024 | akira     |    NULL |
    |  3 | 1143013023 | Billy     |       2 |
    +----+------------+-----------+---------+
    ```
    
    区分大小写排序：
    ```
    mysql> select * from user_book order by binary user_name;
    +----+------------+-----------+---------+
    | id | user_id    | user_name | book_id |
    +----+------------+-----------+---------+
    |  1 | 1143013021 | Akira     |       1 |
    |  3 | 1143013023 | Billy     |       2 |
    |  2 | 1143013022 | abira     |       1 |
    |  4 | 1143013024 | akira     |    NULL |
    +----+------------+-----------+---------+
    ```
    
0. 查询时：

    默认不区分大小写
    ```
    mysql> select * from user_book where user_name = 'akira';
    +------+------------+-----------+---------+
    | id   | user_id    | user_name | book_id |
    +------+------------+-----------+---------+
    |    1 | 1143013021 | Akira     |       1 |
    |    4 | 1143013024 | akira     |    NULL |
    +------+------------+-----------+---------+
    ```
		
    区分大小写查询：
    ```
    mysql> select * from user_book where binary user_name = 'akira';
    +------+------------+-----------+---------+
    | id   | user_id    | user_name | book_id |
    +------+------------+-----------+---------+
    |    4 | 1143013024 | akira     |    NULL |
    +------+------------+-----------+---------+
    ```
    
0. 库名/表名：
    
    mysql每一个database都与mysql的data目录下的一个文件夹对应，而table则与database对应文件夹下的文件对应，如：windows操作系统下的akira数据库下有三个表cx, rn, test_auto_incr
    ```
    mysql> use akira;
    Database changed
    mysql> show tables;
    +-----------------+
    | Tables_in_akira |
    +-----------------+
    | cx              |
    | rn              |
    | test_auto_incr  |
    +-----------------+
    ```
    在winodws下的目录为：
			
    因此**database, table名的大小写敏感性与操作系统有关：**
    ```
    mysql> select * from Akira.Test_auto_incr;
    +----+----------+
    | id | username |
    +----+----------+
    |  1 | allen    |
    |  2 | abc      |
    +----+----------+
    ```
    但是**如果设置参数：lower_case_table_names=1，这样创建database, table时会自动转为小写，并且在查询语句里的database, table名也会转成小写**，这样也就和不区分大小写效果类似了（因为全是小写）
    例如在windows操作系统下：
    ```
    mysql> show variables like 'lower_case_table_names';
    +------------------------+-------+
    | Variable_name          | Value |
    +------------------------+-------+
    | lower_case_table_names | 1     |
    +------------------------+-------+
    
    mysql> create table ABC(id int);
    mysql> show tables;
    +-----------------+
    | Tables_in_akira |
    +-----------------+
    | abc             |
    | cx              |
    | rn              |
    | test_auto_incr  |
    +-----------------+
    ```
    可以看到这里文件名也转成了小写。备注：不要在Windows或者macOS下将lower_case_table_name设置为0
