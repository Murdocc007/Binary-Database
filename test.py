__author__ = 'aditya'
import os,sys
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
from sqlparse.lexer import tokenize
from sqlparse.filters import compact
from sqlparse.functions import getcolumns, getlimit, IsType
from helperfunctions import fileMethods
# CURRENT_DATABASE=''
# CONST_DB='DATABASES'
# CONST_SCHEMA='SCHEMA'
# CONST_CREATE='CREATE'
# CONST_DROP='DROP'
# CONST_DELETE='DELETE'
# CONST_INSERT='INSERT'
# CONST_USE='USE'
# CONST_SELECT='SELECT'
# def getQueryType(q):
#     return q.split(' ')[0].upper()
#
#
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
# import struct
# def ha():
#     try:
#         return struct.pack('>b',-128)
#     except:
#         print 'ha'
#
#
f=fileMethods(os.path.join(__location__, 'test.data'))
# f.openFile()
f.openFile()
f.writeInt(8)
f.close()

f.openFile()
f.writeInt(6)
f.close()
# f.close()
# k=raw_input()
# f.openFile()
# f.writeVarChar('test',len('test'))
# f.close()
# f.openFile()
# f.writeByte(0)
# f.close()
f.openFile()
print f.readInt(None)
# print f.readByte(None)
print f.readInt(None)
# print f.readByte(None)
f.close()
#
# SQL='select col1,col2 from table'
#
# columns = getcolumns(tokenize(SQL))
# print columns
# # print struct.unpack('>B',f.read(1))
#
# f.close()

# sql2 = """SELECT col1,col2, col3 FROM abc"""
# sql="""delete from table_name where ha=1"""
# s=sqlparse.format(sql, keyword_case='upper')
# print sqlparse.parse(s)[0].get_type()
# columns = getcolumns(tokenize(sql))
#
# print columns


