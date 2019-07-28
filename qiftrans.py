#!/usr/bin/python

import sys
import json

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

recordBank = False

nameDict = {
    'citi' : {
               'name' : 'NAssets:Savings:Citibank',
               'desc' : 'DCitiBank Salary Account',
               'type' : 'TSavings',
               'category' : '!Type:Bank'
     },
    'icici' : {
               'name' : 'NAssets:Savings:ICICI',
               'desc' : 'DICICI Savings Account',
               'type' : 'TSavings',
               'category' : '!Type:Bank'
     },
    'sbi' : {
               'name' : 'NAssets:Savings:SBI',
               'desc' : 'DSBI Savings Account',
               'type' : 'TSavings',
               'category' : '!Type:Bank'
     }
}

def _writeTransactionPartToFile(_file, _part):
    _file.write(_part+'\n')

ofile = open(sys.argv[2], 'w+')

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in lines:
        trans = json.loads(line)
        if recordBank == False:
            _writeTransactionPartToFile(ofile, _account)
            _writeTransactionPartToFile(ofile, nameDict[trans['bank']]['name'])
            _writeTransactionPartToFile(ofile, nameDict[trans['bank']]['type'])
            _writeTransactionPartToFile(ofile, nameDict[trans['bank']]['desc'])
            _writeTransactionPartToFile(ofile, nameDict[trans['bank']]['category'])
            recordBank = True
        _writeTransactionPartToFile(ofile, _day + trans['date'])
        mtrans = ''
        if 'withdrawl' in trans and trans['withdrawl'] > 0.0:
            mtrans = _withdrawl + str(trans['withdrawl'])
        elif 'deposit' in trans and trans['deposit']:
            mtrans = _deposit + str(trans['deposit'])
        _writeTransactionPartToFile(ofile, mtrans)
        desc = _description + trans['description']
        _writeTransactionPartToFile(ofile, desc)
        _writeTransactionPartToFile(ofile, _endOfRecord)
ofile.close()
f.close()
