import pymysql

pymysql.version_info = (1, 4, 6, "final", 0)  # change mysqlclient version
pymysql.install_as_MySQLdb()
