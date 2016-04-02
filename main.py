import time
from django.utils.timezone import now
from helperfunctions import fileMethods

__author__ = 'aditya'
import os,sys,re,sqlparse
import helperfunctions

CURRENT_DATABASE='information_schema'
CONST_DB='DATABASES'
CONST_SCHEMA='SCHEMA'
CONST_CREATE='CREATE'
CONST_DROP='DROP'
CONST_DELETE='DELETE'
CONST_INSERT='INSERT'
CONST_USE='USE'
CONST_SELECT='SELECT'
TABLE_NAME='information_schema.tables.data'
TABLE_COLUMNS='information_schema.columns.data'
TABLE_SCHEMATA='information_schema.schemata.data'


BYTE=0
UNSIGNED_BYTE= 1
SHORT=2
UNSIGNED_SHORT=3
INT=4
UNSIGNED_INT=5
LONG=6
UNSIGNED_LONG=7
CHAR=8
VARCHAR=9
FLOAT=10
DOUBLE=11
DATETIME=12
DATE=13

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def createSchemaQueryHandler(q):
    schema=q.split(' ')[2]
    writeInformationSchemaSchemata(schema)


def createTableQueryHandler(q):
    tablename=getTableName(q)
    columnsData=getColumnsData(q)
    colnames,data_type,primarykey,notnullable=processeColumnsData(columnsData)
    tuple=[]
    tuple.append(CURRENT_DATABASE)
    tuple.append(tablename)
    tuple.append('SYSTEM VIEW')
    tuple.append(0)
    tuple.append(long(time.time()))
    tuple.append(long(time.time()))
    writeInformationSchemaTables(tuple)

    for name,type,key,isnull in zip(colnames,data_type,primarykey,notnullable):
        tuple=[]
        tuple.append(CURRENT_DATABASE)
        tuple.append(tablename)
        tuple.append('SYSTEM VIEW')
        tuple.append(0)
        tuple.append(isnull)
        tuple.append(type)
        tuple.append(name)
        tuple.append(key)
        writeInformationSchemaColumns(tuple)


#writing to the TABLES table of the information schema
#tuple is an array that stores the data
def writeInformationSchemaTables(tuple):

    f=fileMethods(os.path.join(__location__, TABLE_NAME))
    table_schema,table_name,table_type,table_rows,create_time,update_time=tuple

    #length of the tuple
    #varchar1+varchar2+varchar3+table_rows,create time,update time, 1 bit to indicate whether it has been deleted or not
    #and one more byte for it's length
    lenTuple=len(tuple[0])+len(tuple[1])+len(tuple[2])+8*3+1+1
    f.openFile()
    #writing the length of the tuple
    f.writeInt(lenTuple)
    #set the delete bit as 0
    f.writeByte(0)
    f.writeVarChar(table_schema,len(table_schema))
    f.writeVarChar(table_name,len(table_name))
    f.writeVarChar(table_type,len(table_type))
    f.writeUnLong(table_rows)
    f.writeDateTime(long(create_time))
    f.writeDateTime(long(update_time))
    f.close()


def writeInformationSchemaColumns(tuple):
    f=fileMethods(os.path.join(__location__, TABLE_COLUMNS))
    #length of the tuple
    lentuple=len(tuple[0])+len(tuple[1])+len(tuple[2])+4+len(tuple[4])+len(tuple[5])+len(tuple[6])+len(tuple[7])+1+1

    table_schema,table_name,table_type,ordinal_position,is_nullable,data_type,column_name,column_key=tuple

    f.openFile()
    #write the length of the tuple
    f.writeInt(int(lentuple))
    #delete byte is set to 0
    f.writeByte(0)
    f.writeVarChar(table_schema,len(table_schema))
    f.writeVarChar(table_name,len(table_name))
    f.writeVarChar(table_type,len(table_type))
    f.writeUnInt(ordinal_position)
    f.writeVarChar(is_nullable,len(is_nullable))
    f.writeVarChar(data_type,len(data_type))
    f.writeVarChar(column_name,len(column_name))
    f.writeVarChar(column_key,len(column_key))
    f.close()


def writeInformationSchemaSchemata(schema):
    f=fileMethods(os.path.join(__location__, TABLE_SCHEMATA))
    f.openFile()
    f.writeVarChar(schema,len(schema))
    f.close()


def detectDataType(s):
    if(s=='BYTE'):
        return BYTE
    if(s=='UNSIGNED BYTE'):
        return UNSIGNED_BYTE
    if(s=='SHORT'):
        return SHORT
    if(s=='UNSIGNED SHORT'):
        return UNSIGNED_SHORT
    if(s=='INT'):
        return INT
    if(s=='UNSIGNED INT'):
        return UNSIGNED_INT
    if(s=='LONG'):
        return LONG
    if(s=='UNSIGNED LONG'):
        return UNSIGNED_LONG
    if(s=='CHAR'):
        return  CHAR
    if(s=='VARCHAR'):
        return VARCHAR
    if(s=='FLOAT'):
        return FLOAT
    if(s=='DOUBLE'):
        return DOUBLE
    if(s=='DATETIME'):
        return DATETIME
    if(s=='DATE'):
        return DATE


def getDataTypeofColumn(dbname,tablename,columnname):
    f=fileMethods(os.path.join(__location__,TABLE_COLUMNS))
    f.openFile()
    while(f.reachedEOF()!=True):
        tuplelength= f.readInt(None)
        flag=f.readByte(None)
        table_schema=f.readVarChar(None)
        table_name=f.readVarChar(None)
        table_type=f.readVarChar(None)
        ordinal_position=f.readUnInt(None)
        is_nullable=f.readVarChar(None)
        data_type=f.readVarChar(None)
        column_name=f.readVarChar(None)
        column_key=f.readVarChar(None)
        if(table_schema.upper()==dbname.upper() and table_name.upper()==tablename.upper() and column_name.upper()==columnname.upper()):
            f.close()
            return data_type
    f.close()

def getColumnsOfTable(dbname,tablename):
    f=fileMethods(os.path.join(__location__,TABLE_COLUMNS))
    cols=[]
    f.openFile()
    while(f.reachedEOF()!=True):
        tuplelength= f.readInt(None)
        flag=f.readByte(None)
        table_schema=f.readVarChar(None)
        table_name=f.readVarChar(None)
        table_type=f.readVarChar(None)
        ordinal_position=f.readUnInt(None)
        is_nullable=f.readVarChar(None)
        data_type=f.readVarChar(None)
        column_name=f.readVarChar(None)
        column_key=f.readVarChar(None)
        if(table_schema.upper()==dbname.upper() and table_name.upper()==tablename.upper()):
            cols.append(column_name)
    f.close()
    return cols

def getQueryType(q):
    return q.split(' ')[0].upper()

def processQuery(q):
    type= getQueryType(q)
    if(type==CONST_SELECT):
        pass
    if(type==CONST_CREATE):
        if(q.split(' ')[1]=='SCHEMA'):
            createSchemaQueryHandler(q)
        else:
            createTableQueryHandler(q)
    if(type==CONST_DELETE):
        pass
    if(type==CONST_DROP):
        pass
    if(type==CONST_USE):
        pass


def useQueryHandler(q):
    CURRENT_DATABASE=q.split(' ')[1].lower()


def showQueryHandler(q):
    val=q.split(' ')[1]
    if(val.upper()==CONST_DB or val.upper()==CONST_SCHEMA):
        pass
    else:
        pass

def processeColumnsData(s):
    array=s.split(',')#split the string on commas
    colnames=[]
    primarykey=[]
    notnullable=[]
    data_type=[]
    for col in array:
        colnames.append(col.split(' ')[0])
        if('NOT NULL' in col):
            notnullable.append('YES')
        else:
            notnullable.append('NO')
        if('PRIMARY' in col):
            primarykey.append('YES')
        else:
            primarykey.append('NO')
        data_type.append(col.split(' ')[1])
    return colnames,data_type,primarykey,notnullable





def insertQueryHandler(q):
    table=getTableName(q)
    print 'insert'

def deleteQueryHandler(q):
    table=getTableName(q)
    print 'delete'

def dropQueryHandler(q):
    table=getTableName(q)

def selectQueryHandler(q):
    table=getTableName(q)

def getTableName(q):
    Q=q.upper()
    type=getQueryType(Q)
    val=Q.split(' ')
    if(type==CONST_CREATE):
        return val[val.index('TABLE')+1]
    elif(type==CONST_INSERT):
        return val[val.index('INTO')+1]
    elif(type==CONST_DELETE or type==CONST_SELECT):
        return val[val.index('FROM')+1]
    elif(type==CONST_DROP):
        return val[val.index(CONST_DROP)+1]
    else:
        return None


def getColumnsData(q):
    type=getQueryType(q)
    if(type==CONST_CREATE):
        re1='.*?'	# Non-greedy match on filler
        re2='(\\(.*\\))'	# Round Braces 1
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(q)
        if m:
            rbraces1=m.group(1)
            return  rbraces1[1:len(rbraces1)-1]   #comma separated columns and their description

    elif(type==CONST_INSERT):
        re1='.*?'	# Non-greedy match on filler
        re2='(\\(.*\\))'	# Round Braces 1
        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(q)
        if m:
            rbraces1=m.group(1)
            print rbraces1
            s=rbraces1.split('VALUES')
            #two list one with the label name and other with the value
            label=s[0][s[0].index('(')+1:s[0].index(')')]
            value=s[1][s[1].index('(')+1:s[1].index(')')]

    elif(type==CONST_DELETE):
        s=q[q.index('WHERE')+5:].split(',')
        label=[]
        value=[]
        for i in s:
            temp=i.split('=')
            #two list one with the label and the other with the value
            label.append(temp[0])
            value.append(temp[1])

    elif(type==CONST_SELECT):
        selectcols=q[q.index(CONST_SELECT)+6:q.index('FROM')]
        #columns to be selected
        selectcols.split(',')
        s=q[q.index('WHERE')+5:].split(',')
        label=[]
        value=[]
        for i in s:
            temp=i.split('=')
            #two list one with the label and the other with the value
            label.append(temp[0])
            value.append(temp[1])

    else:
        return None


# s=''
# while(s!='exit'):
#      sys.stdout.write('davisql>')
#      s=raw_input()
#      s=sqlparse.format(s, keyword_case='upper')
#      processQuery(s)

print getColumnsOfTable('information_schema','table_name')
