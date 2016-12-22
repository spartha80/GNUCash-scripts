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
_accountName = 'NAssets:Savings:ICICIBank'
_accountType = 'TSavings'
_accountDesc = 'DICICI Bank Account'

_closingBalance = 'Closing Balance'
_statementDateString = 'Summary of Account information'
_stmtStartRowIdent = 'S No.'

_indexDate = 3
_indexDesc = 5
_indexWid = 6
_indexDep = 7
_indexStart = 1
_startTrans = False

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
                if _startTrans == False:
                    continue
                _writeTransactionPartToFile(ofile, _day + row[_indexDate])
                trans = ''
                if row[_indexWid] != '0':
                    trans = _withdrawl + row[_indexWid].replace(',','')
                else:
                    trans = _deposit + row[_indexDep].replace(',','')
                _writeTransactionPartToFile(ofile, trans)
                desc = _description + row[_indexDesc]
                _writeTransactionPartToFile(ofile, desc)
                _writeTransactionPartToFile(ofile, _endOfRecord)
            except ValueError:
                if row[_indexStart] == _stmtStartRowIdent:
                    _writeTransactionPartToFile(ofile,_type)
                    _startTrans = True
ofile.close()
