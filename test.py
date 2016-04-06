__author__ = 'aditya'
import os
from helperfunctions import fileMethods

#
#
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

f=fileMethods(os.path.join(__location__, 'test.data'))
# # f.openFile()
# f.openFile()
# f.writeVarChar('a',len('a'))
# # f.writeVarChar('data_type',len('data_type'))
# f.close()
#
# f.openFile()
# # f.readVarChar(None)
# f.writeVarChar('e',len('e'))
# f.close()
#
# f.openWriteMode()
# f.writeVarChar('b',len('b'))
# f.close()

f.openFile()
f.writeByte(int('1'))
f.close()

# f.close()
# k=raw_input()
# f.openFile()
# f.writeVarChar('test',len('test'))
# f.close()
# f.openFile()
# f.writeByte(0)
# f.close()
# f.openFile()
# print f.readInt(None)
# # print f.readByte(None)
# print f.readInt(None)
# # print f.readByte(None)
# f.close()
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




