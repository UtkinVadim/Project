#!/usr/bin/python3

import pymysql.cursors
import argparse
import json
import requests

#Парсинг переданного аргумента
parser = argparse.ArgumentParser()
parser.add_argument('file', type=argparse.FileType('r'))
args = parser.parse_args()

with args.file as file:
    json_pars = args.file.read()
    json_file = json.loads(json_pars)
    json_tran_id = json_file["receiptData"]["TransactionID"]
    json_payload = json_file["receiptData"]["Payload"]


#Подключение к БД
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='qaz123',                             
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#Верификация receipt payload с помощью Apple REST API
url = 'https://buy.itunes.apple.com/verifyReceipt'
r = requests.post(url, json={'receipt-data': json_payload})

if '"status":0' in r.text:
    result = 1
else:
    result = 0



#Добавление данных в БД
def add_in_sql():
    with connection.cursor() as cursor:
        cursor.execute('SELECT transaction_id FROM test_table WHERE transaction_id = (%s)', json_tran_id)
        row = cursor.fetchall()
    
    if json_tran_id in str(row):
        print('This transaction already exists.')
        quit()
    else:
        if result == 1:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO test_table(is_valid, transaction_id) VALUES ('is_valid=1', %s)", json_tran_id)
                connection.commit()
                print("Transaction ID has been added in MySQL.")
                print('Receipt is valid')
        else:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO test_table(is_valid, transaction_id) VALUES ('is_valid=0', %s)", json_tran_id)
                connection.commit()
                print("Transaction ID has been added in MySQL.")
                print('Error: ' + r.text)