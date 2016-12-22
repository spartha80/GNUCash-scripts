#!/usr/bin/python

import fileinput
import string
import csv
import sys
import time
from datetime import datetime

_type = '!Type:Bank'
_day = 'D'
_withdrawl = 'T-'
_deposit = 'T+'
_description = 'M'
_stmtDate = '/'
_balanceAmt = '$'
_endOfRecord = '^'
_account = '!Account'
_accountName = 'NAssets:Savings:Citibank'
_accountType = 'TSavings'
_accountDesc = 'DCitiBank Salary Account'

_closingBalance = 'Closing Balance'
_statementDateString = 'Summary of Account information'
_stmtStartRowIdent = 'Date'

_indexDate = 0
_indexDesc = 1
_indexWid = 2
_indexDep = 3

def _writeTransactionPartToFile(_file, _part):
    _file.write(_part+'\n')

ofile = open(sys.argv[2], 'w+')
_writeTransactionPartToFile(ofile, _account)
_writeTransactionPartToFile(ofile, _accountName)
_writeTransactionPartToFile(ofile, _accountType)
_writeTransactionPartToFile(ofile, _accountDesc)
with open(sys.argv[1]) as f:
    reader = csv.reader(f)
    for row in reader:
        if row[_indexDate] != '':
            try:
                transactionDate = datetime.strptime(row[_indexDate], "%d/%m/%Y")
                _writeTransactionPartToFile(ofile, _day + row[_indexDate])
                trans = ''
                if row[_indexWid] != '':
                    trans = _withdrawl + row[_indexWid].replace(',','')
                else:
                    trans = _deposit + row[_indexDep].replace(',','')
                _writeTransactionPartToFile(ofile, trans)
                desc = _description + row[_indexDesc]
                _writeTransactionPartToFile(ofile, desc)
                _writeTransactionPartToFile(ofile, _endOfRecord)
            except ValueError:
                if row[0] == _closingBalance:
                    cBalance = _balanceAmt+row[1].replace(',','')
                    _writeTransactionPartToFile(ofile, cBalance)
                    _writeTransactionPartToFile(ofile, _endOfRecord)
                elif row[0].startswith(_statementDateString):
                    stmtDate = _stmtDate + string.split(row[0],':')[1]
                    _writeTransactionPartToFile(ofile, stmtDate)
                elif row[0] == _stmtStartRowIdent:
                    _writeTransactionPartToFile(ofile,_type)
ofile.close()
