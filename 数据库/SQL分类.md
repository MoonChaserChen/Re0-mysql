# SQL分类
1. DDL - Data Definition Language

    其主要命令有CREATE，ALTER，DROP等，下面用例子详解。该语言不需要commit，因此慎重。

2. DML - Data Manipulation Language

    其主要命令有INSERT,UPDATE,DELETE等，这些例子大家常用就不一一介绍了。该语言需要commit。

3. DCL - Data Control Language

    数据库控制语言：授权，角色控制等
    GRANT - 为用户赋予访问权限
    REVOKE - 撤回授权权限

4. TCL - Transaction Control Language

    COMMIT - 保存已完成的工作
    SAVEPOINT - 在事务中设置保存点，可以回滚到此处
    ROLLBACK - 回滚
    SET TRANSACTION - 改变事务选项
