import sys

# pip install mysql-connector-python
import mysql.connector

def obtain_tables_info(db_host, db_port, db_user, db_password, db_database):
    conn = mysql.connector.connect(
        host = db_host,
        port = db_port,
        user = db_user,
        password = db_password,
        database = db_database
    )
    
    cursor = conn.cursor()
    
    # 获取所有表
    cursor.execute("show tables")
    
    results = cursor.fetchall()

    # 表名列表，按字母排序
    table_name_list = []
    table_fields_list = {}
    
    for row in results:
        table_name_list.append(row[0])
    
    for table_name in table_name_list:
        # 获取表结构
        cursor.execute(f"desc {table_name}")

        results = cursor.fetchall()

        field_list = []

        for field in results:
            field_list.append(field)
        
        table_fields_list[table_name] = field_list

    cursor.close()
    conn.close()

    return (table_name_list, table_fields_list, db_database)

def log(info):
    print(f"{info}\n")

def diff_tables(db1_tables, db2_tables):

    # 第一个数据库中的所有表
    db1_table_name_list = db1_tables[0]
    db1_table_fields_list = db1_tables[1]

    # 第一个数据库的名称
    db1_name = db1_tables[2]

    # 第二个数据库中的所有表
    db2_table_name_list = db2_tables[0]
    db2_table_fields_list = db2_tables[1]

    # 第二个数据库的名称
    db2_name = db2_tables[2]

    # 逐个表对比

    db1_table_index = 0
    db2_table_index = 0

    db1_tables_num = len(db1_table_name_list)
    db2_tables_num = len(db2_table_name_list)

    while True:

        if db1_table_index < db1_tables_num and db2_table_index < db2_tables_num:

            db1_table_name = db1_table_name_list[db1_table_index]
            db2_table_name = db2_table_name_list[db2_table_index]

            if db1_table_name == db2_table_name:

                # 表名称相同，比较各个字段

                db1_table_fields = db1_table_fields_list[db1_table_name]
                db2_table_fields = db2_table_fields_list[db2_table_name]

                db1_table_fields_len = len(db1_table_fields)
                db2_table_fields_len = len(db2_table_fields)

                if db1_table_fields_len == db2_table_fields_len:

                    # 逐个比较字段名称、字段类型等

                    field_index = 0

                    while field_index < db1_table_fields_len:
                        db1_table_field = db1_table_fields[field_index]
                        db2_table_field = db2_table_fields[field_index]

                        if db1_table_field[0] == db2_table_field[0] and db1_table_field[1] == db2_table_field[1]:
                            field_index = field_index + 1
                        else:
                            # 两张表有字段不同
                            log(f"{db1_table_name} 在两个数据库中有字段不同\n\t{db1_name} 中：{db1_table_field}\n\t{db2_name} 中：{db2_table_field}")
                            # 不用再比其他字段了
                            break;

                else:
                    # 字段数量都不一样，两张表肯定不同
                    log(f"{db1_table_name} 在两个数据库中字段数量不同\n\t{db1_name} 中：{db1_table_fields}\n\t{db2_name} 中：{db2_table_fields}")
                
                db1_table_index = db1_table_index + 1
                db2_table_index = db2_table_index + 1

            elif db1_table_name < db2_table_name:
                # 表名称是按字母排序的，如果 db1_table_name < db2_table_name，说明 db1_table_name 在 db2 中没有
                log(f"{db1_table_name} 在 {db1_name} 中存在、在 {db2_name} 中不存在")
                db1_table_index = db1_table_index + 1
            else:
                # 表名称是按字母排序的，如果 db1_table_name > db2_table_name，说明 db2_table_name 在 db1 中没有
                log(f"{db2_table_name} 在 {db1_name} 中不存在、在 {db2_name} 中存在")
                db2_table_index = db2_table_index + 1

        else:
            # 有一个 table list 已经遍历结束了，那么没结束的 list 中的 table 在另一个数据库中不存在
            break
    
    while db1_table_index < db1_tables_num:
        db1_table_name = db1_table_name_list[db1_table_index]
        log(f"{db1_table_name} 在数据库 {db2_name} 中不存在。")
    
    while db2_table_index < db2_tables_num:
        db2_table_name = db2_table_name_list[db2_table_index]
        log(f"{db2_table_name} 在数据库 {db1_name} 中不存在。")

def main():
    # 第一个数据库的连接信息
    db1_host = sys.argv[1]
    db1_port = sys.argv[2]
    db1_user = sys.argv[3]
    db1_password = sys.argv[4]
    db1_database = sys.argv[5]

    # 第二个数据库的连接信息
    db2_host = sys.argv[6]
    db2_port = sys.argv[7]
    db2_user = sys.argv[8]
    db2_password = sys.argv[9]
    db2_database = sys.argv[10]

    # 第一个数据库的表信息
    hive5_tables = obtain_tables_info(db1_host, db1_port, db1_user, db1_password, db1_database)

    # 第二个数据库的表信息
    hive7_tables = obtain_tables_info(db2_host, db2_port, db2_user, db2_password, db2_database)

    # 逐个表对比
    diff_tables(hive5_tables, hive7_tables)

if __name__=="__main__":
    main()