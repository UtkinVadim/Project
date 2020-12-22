#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pymysql

#Подключение к базе данных
con = pymysql.connect('localhost', 'root', 
    'qaz123', 'test')

#Получение версии PyMySQL
#try:
    #with con.cursor() as cur:
        #cur.execute('SELECT VERSION()')
        #version = cur.fetchone()
        #print(f'Database version: {version[0]}')
#finally:
    #con.close()

#Метод fetchAll (возвращает все отсавшиеся строки)
#try:
#    with con.cursor() as cur:
#        cur.execute('SELECT * FROM test_table')
#        rows = cur.fetchall()
#        for row in rows:
#            print(f'{row[0]} {row[1]} {row[2]}')
#finally:
#    con.close()

value = 1234
try:
    with con.cursor() as cur:
        cur.execute('SELECT transaction_id FROM test_table WHERE transaction_id = %s', value)
        rows = cur.fetchall()
        print(rows)
finally:
    con.close()

#    cursor = connection.cursor()
#    query = """ SELECT transaction_id FROM test_table WHERE transaction_id = inputvalve """
#
#    cursor.execute(query)
#    result = cursor.fetchall()
#    inputvalve = input("Input= ")
#
#    temp = False
#
#    for x in result:
#        if inputvalve in x:
#            temp = True
#    if temp:
#        print(inputvalve)
#    else:
#        print("Data Does Not Exist")


    #if True:
    #    print('This transaction already exists')
    #    quit()
    #else:
    #    add(json_file["receiptData"]["TransactionID"])