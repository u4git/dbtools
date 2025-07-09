python diff_databases_tables.py rds4emr.c1cg6qcu65yc.rds.cn-northwest-1.amazonaws.com.cn 3306 admin 11111111 hive5 rds4emr.c1cg6qcu65yc.rds.cn-northwest-1.amazonaws.com.cn 3306 admin 11111111 hive7

# 工具 diff_databases_tables.py

## 用途

用来对比两个数据库中表的不同，包括，
- 表只在一个数据库中存在、在另一个数据库中不存在；
- 两个库中都有的表，
    - 字段数量不同，
    - 字段名称不同，
    - 字段类型不同。

目前只适用于 MySql 数据库。

## 用法

1. 安装 ***mysql-connector-python***，
   ```
   pip install mysql-connector-python
   ```
2. 运行工具，
   ```
   python diff_databases_tables.py <db1_host> <db1_port> <db1_user> <db1_password> <db1_database> <db2_host> <db2_port> <db2_user> <db2_password> <db2_database>
   ```
   上述参数缺一不可。其中，
   - db1_host，第一个数据库的 host 名称；
   - db1_port，第一个数据库的端口，
   - db1_user，第一个数据库的用户名，
   - db1_password，第一个数据库的密码，
   - db1_database，第一个数据库的名称，
   - db2_host，第二个数据库的 host 名称，
   - db2_port，第二个数据库的端口，
   - db2_user，第二个数据库的用户名，
   - db2_password，第二个数据库的密码，
   - db2_database，第二个数据库的名称
