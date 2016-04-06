import time
from datetime import datetime
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
CONST_SHOW='SHOW'
CONST_DESCRIBE='DESC'
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
    schema=q.split()[2]
    writeInformationSchemaSchemata(schema)
    updateTableCount(CURRENT_DATABASE,'schemata')


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

    count=0
    for name,type,key,isnull in zip(colnames,data_type,primarykey,notnullable):
        tuple=[]
        count+=1
        tuple.append(CURRENT_DATABASE)
        tuple.append(tablename)
        tuple.append('SYSTEM VIEW')
        #increasing the ordinal count
        tuple.append(count)
        tuple.append(isnull)
        tuple.append(type)
        tuple.append(name)
        tuple.append(key)
        writeInformationSchemaColumns(tuple)
    updateTableCount(CURRENT_DATABASE,'columns')
    updateTableCount(CURRENT_DATABASE,'tables')


#writing to the TABLES table of the information schema
#tuple is an array that stores the data
def writeInformationSchemaTables(tuple):

    f=fileMethods(os.path.join(__location__, TABLE_NAME))
    table_schema,table_name,table_type,table_rows,create_time,update_time=tuple

    #length of the tuple
    #varchar1+varchar2+varchar3+table_rows,create time,update time, 1 bit to indicate whether it has been deleted or not
    #and one more byte for it's length
    # lenTuple=len(tuple[0])+len(tuple[1])+len(tuple[2])+8*3+1+1
    f.openFile()
    #writing the length of the tuple
    # f.writeInt(lenTuple)
    #set the delete bit as 0
    f.writeByte(0)
    f.writeVarChar(table_schema,len(table_schema))
    f.writeVarChar(table_name,len(table_name))
    f.writeVarChar(table_type,len(table_type))
    f.writeUnLong(table_rows)
    f.writeDateTime(long(create_time))
    f.writeDateTime(long(update_time))
    f.close()

#prints all the tables present in the schema
def getDatabaseTables(dbname):
    f=fileMethods(os.path.join(__location__, TABLE_NAME))
    f.openFile()
    f.seek(0)
    result=[[]]
    while(f.reachedEOF()!=True):
        temp=[]
        # length=f.readInt(None)
        delete=f.readByte(None)
        schema_name=f.readVarChar(None)
        table_name=f.readVarChar(None)
        table_type=f.readVarChar(None)
        table_rows=f.readUnLong(None)
        create_time=f.readDateTime(None)
        update_time=f.readDateTime(None)
        if(schema_name==dbname and delete==0):
            print schema_name +' '+table_name+' '+table_type+' '+str(table_rows)+' '\
                  +str(datetime.fromtimestamp(create_time))+' '+str(datetime.fromtimestamp(update_time))


def writeInformationSchemaColumns(tuple):
    f=fileMethods(os.path.join(__location__, TABLE_COLUMNS))
    #length of the tuple
    lentuple=len(tuple[0])+len(tuple[1])+len(tuple[2])+4+len(tuple[4])+len(tuple[5])+len(tuple[6])+len(tuple[7])+1+1

    table_schema,table_name,table_type,ordinal_position,is_nullable,data_type,column_name,column_key=tuple

    f.openFile()
    #write the length of the tuple
    # f.writeInt(int(lentuple))
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


def updateTableCount(dbname,table):
    f=fileMethods(os.path.join(__location__, dbname+'.'+table.lower()+'.data'))
    columns=getColumnsOfTable(dbname,table)
    f.openFile()
    count=0
    while(f.reachedEOF()!=True):
        f.readByte(None)
        count=count+1
        for col in columns:
            type=getDataTypeofColumn(dbname,table,col)
            f.readDataType(type,None)
    f.close()
    f=fileMethods(os.path.join(__location__,TABLE_NAME))
    columns=getColumnsOfTable(dbname,'tables')
    f.openFile()
    flag=0
    pos=0
    while(f.reachedEOF()!=True and flag==0):
        f.readByte(None)
        for col in columns:
            temp=f.tell()
            type=getDataTypeofColumn(dbname,'tables',col)
            val=f.readDataType(type,None)
            if(col.upper()=='TABLE_ROWS'):
                pos=temp
            if(col.upper()=='TABLE_NAME' and val.upper()==table.upper()):
                flag=1
    f.close()
    #opening the file in write mode
    f.openWriteMode()
    f.seek(pos)
    f.writeUnLong(int(count))
    f.close()

def updateAccessTime(dbname,table):
    f=fileMethods(os.path.join(__location__,TABLE_NAME))
    columns=getColumnsOfTable(dbname,'tables')
    f.openFile()
    flag=0
    pos=0
    while(f.reachedEOF()!=True and flag==0):
        f.readByte(None)
        for col in columns:
            temp=f.tell()
            type=getDataTypeofColumn(dbname,'tables',col)
            val=f.readDataType(type,None)
            if(col.upper()=='UPDATE_TIME'):
                pos=temp
            if(col.upper()=='TABLE_NAME' and val.upper()==table.upper()):
                flag=1
    f.close()
    #opening the file in write mode
    f.openWriteMode()
    f.seek(pos)
    f.writeUnLong(long(time.time()))
    f.close()




def writeInformationSchemaSchemata(schema):
    f=fileMethods(os.path.join(__location__, TABLE_SCHEMATA))
    f.openFile()
    f.writeByte(0)
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
    f.seek(0)
    while(f.reachedEOF()!=True):
        # tuplelength= f.readInt(None)
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
    f.seek(0)
    f.seek(0)
    while(f.reachedEOF()!=True):
        # tuplelength= f.readInt(None)
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
    return q.split()[0].upper()

def processQuery(q):
    type= getQueryType(q)
    if(type.upper()==CONST_SELECT):
        selectQueryHandler(q)
    elif(type.upper()==CONST_CREATE):
        if(q.split()[1]=='SCHEMA'):
            createSchemaQueryHandler(q)
        else:
            createTableQueryHandler(q)
    elif(type.upper()==CONST_DELETE):
        pass
    elif(type.upper()==CONST_DROP):
        dropQueryHandler(q)
    elif(type.upper()==CONST_USE):
        useQueryHandler(q)
    elif(type.upper()==CONST_SHOW):
        showQueryHandler(q)
    elif(type.upper()==CONST_INSERT):
        insertQueryHandler(q)
    elif(type.upper()==CONST_DESCRIBE):
        describeQueryHandler(q)

def getDatabases():
    f=fileMethods(os.path.join(__location__, TABLE_SCHEMATA))
    f.openFile()
    f.seek(0)
    while(f.reachedEOF()!=True):
        print f.readVarChar(None)
    f.close()

def useQueryHandler(q):
    global  CURRENT_DATABASE
    CURRENT_DATABASE=q.split()[1].lower()

def describeQueryHandler(q):
    table=getTableName(q)
    columns=getColumnsOfTable(CURRENT_DATABASE,table)
    for col in columns:
        print(col,)
        type=getDataTypeofColumn(CURRENT_DATABASE,table,col)
        print (type)



#prints all the schemas present
def showQueryHandler(q):
    val=q.split()[1]
    if(val.upper()==CONST_DB ):
        getDatabases()
    else:
        getDatabaseTables(CURRENT_DATABASE)





def processeColumnsData(s):
    array=s.split(',')#split the string on commas
    colnames=[]
    primarykey=[]
    nullable=[]
    data_type=[]
    for col in array:
        colnames.append(col.split()[0])
        if('NOT NULL' in col):
            nullable.append('NO')
        else:
            nullable.append('YES')
        if('PRIMARY' in col):
            primarykey.append('YES')
        else:
            primarykey.append('NO')
        if(col.split(' ')[1].upper()=='UNSIGNED'):
            type= col.split(' ')[1]+' '+col.split(' ')[2]
        else:
            type=col.split()[1]
        data_type.append(type)
    return colnames,data_type,primarykey,nullable





def insertQueryHandler(q):
    table=getTableName(q)
    f=fileMethods(os.path.join(__location__,CURRENT_DATABASE+'.'+table.lower()+'.data'))
    if(checkIfDeleted(CURRENT_DATABASE,table)==1):
        print 'TABLE HAS ALREADY BEEN DELETED'
        return
    columns=getColumnsOfTable(CURRENT_DATABASE,table)
    values=getColumnsData(q)
    f.openFile()
    ##setting the delete bit as 0
    f.writeByte(0)
    for val,col in zip(values,columns):
        type=getDataTypeofColumn(CURRENT_DATABASE,table,col)
        tempf=fileMethods(os.path.join(__location__,CURRENT_DATABASE+'.'+table.lower()+'.'+col.lower()+'.ndx'))
        tempf.openFile()
        tempf.writeDataType(val,type,None)
        tempf.writeUnLong(int(f.tell()))
        tempf.close()
        f.writeDataType(val,type,None)
    f.close()

    updateTableCount(CURRENT_DATABASE,table)
    updateAccessTime(CURRENT_DATABASE,table)
    # #update the count of the table
    # f=fileMethods(os.path.join(__location__,TABLE_NAME))
    # columns=getColumnsOfTable(CURRENT_DATABASE,'tables')
    # f.openFile()
    # flag=0
    # pos=0
    # count=0
    # while(f.reachedEOF()!=True and flag==0):
    #     f.readByte(None)
    #     for col in columns:
    #         temp=f.tell()
    #         type=getDataTypeofColumn(CURRENT_DATABASE,'tables',col)
    #         val=f.readDataType(type,None)
    #         if(col.upper()=='TABLE_ROWS'):
    #             count=val
    #             pos=temp
    #         if(col.upper()=='TABLE_NAME' and val.upper()==table.upper()):
    #             flag=1
    # f.close()
    #
    # #opening the file in write mode
    # f.openWriteMode()
    # f.seek(pos)
    # f.writeUnLong(int(count)+1)
    # f.close()




def checkIfDeleted(dbname,table):
    f=fileMethods(os.path.join(__location__,TABLE_NAME))
    columns=getColumnsOfTable(dbname,'tables')
    f.openFile()
    f.seek(0)
    flag=0
    while(f.reachedEOF()!=True and flag==0):
        deletebit=f.readByte(None)
        for col in columns:
            type=getDataTypeofColumn('information_schema','TABLES',col)
            val=f.readDataType(type,None)
            if(col=='TABLE_NAME' and val.upper()==table.upper()):
                f.close()
                return deletebit
    f.close()


def dropQueryHandler(q):
    table=getTableName(q)
    f=fileMethods(os.path.join(__location__,TABLE_NAME))
    columns=getColumnsOfTable(CURRENT_DATABASE,'TABLES')
    f.openFile()
    f.seek(0)
    flag=0
    pos=0
    while(f.reachedEOF()!=True and flag==0):
        pos=f.tell()
        deletebit=f.readByte(None)
        for col in columns:
            type=getDataTypeofColumn(CURRENT_DATABASE,'TABLES',col)
            val=f.readDataType(type,None)
            if(col=='TABLE_NAME' and val.upper()==table.upper()):
                flag=1

    f.close()
    #open the write mode and move the pointer to the delete bit
    f.openWriteMode()
    f.seek(pos)
    f.writeByte(1)
    f.close()

    f=fileMethods(os.path.join(__location__,TABLE_COLUMNS))
    columns=getColumnsOfTable(CURRENT_DATABASE,'columns')
    f.openFile()
    f.seek(0)
    flag=0
    pos=0
    tuple=[]
    while(f.reachedEOF()!=True ):
        pos=f.tell()
        deletebit=f.readByte(None)
        for col in columns:
            type=getDataTypeofColumn(CURRENT_DATABASE,'columns',col)
            val=f.readDataType(type,None)
            if(col=='TABLE_NAME' and val.upper()==table.upper()):
                tuple.append(pos)

    f.close()
    #open the write mode and move the pointer to the delete bit
    f.openWriteMode()
    for i in tuple:
        f.seek(i)
        f.writeByte(1)
    f.close()



def deleteQueryHandler(q):
    table=getTableName(q)

#handles the select query
def selectQueryHandler(q):
    table=getTableName(q)
    if(checkIfDeleted(CURRENT_DATABASE,table)==1):
        print 'TABLE ALREADY HAS BEEN DELETED'
        return
    columns_requested,wherecolumn,wherevalue=getColumnsData(q)
    wherevalue=[col.strip("'") for col in wherevalue]
    f=fileMethods(os.path.join(__location__,CURRENT_DATABASE+'.'+table.lower()+'.data'))
    columns=getColumnsOfTable(CURRENT_DATABASE,table.upper())
    f.openFile()
    f.seek(0)
    if(columns_requested[0]=="*"):
        while(f.reachedEOF()!=True):
            deletebit=f.readByte(None)
            tuple=[]
            flag=0
            for col in columns:
                type=getDataTypeofColumn(CURRENT_DATABASE,table,col)
                val=f.readDataType(type,None)
                tuple.append(val)
                if(len(wherecolumn)!=0):
                    if(col in wherecolumn and str(wherevalue[0]).upper()==str(val).upper()):
                        flag=1
                else:
                    flag=1

            if(deletebit==0 and flag==1):
                print tuple
    else:
        while(f.reachedEOF()!=True):
            deletebit=f.readByte(None)
            flag=0
            tuple=[]
            for col in columns:
                type=getDataTypeofColumn(CURRENT_DATABASE,table,col)
                val=f.readDataType(type,None)

                if(len(wherecolumn)!=0):
                    if(wherecolumn[0].upper()==col.upper() and str(wherevalue[0]).upper()==str(val).upper()):
                        flag=1
                else:
                    flag=1
                if(col in columns_requested):
                    tuple.append(val)
                    # print (val,)
            if(deletebit==0 and flag==1):
                print tuple
    f.close()
    updateAccessTime(CURRENT_DATABASE,table)

def getTableName(q):
    Q=q.upper()
    type=getQueryType(Q)
    val=Q.split()
    if(type==CONST_CREATE):
        return val[val.index('TABLE')+1]
    elif(type==CONST_INSERT):
        return val[val.index('INTO')+1]
    elif(type==CONST_DELETE or type==CONST_SELECT):
        return val[val.index('FROM')+1]
    elif(type==CONST_DROP):
        return val[val.index('TABLE')+1]
    elif(type==CONST_DESCRIBE):
        return val[val.index(CONST_DESCRIBE)+1]
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
            values=rbraces1[rbraces1.index('(')+1:rbraces1.index(')')]
            return values.split(',')

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
        selectcols=selectcols.strip(" ")
        if(',' in selectcols):
            selectcols=selectcols.split(',')
            selectcols=[ col.strip(' ') for col in selectcols]
        s=[]
        if('WHERE' in q):
            s=q[q.index('WHERE')+5:].split(',')
        label=[]
        value=[]
        for i in s:
            temp=i.split('=')
            #two list one with the label and the other with the value
            label.append(temp[0].strip(' '))
            value.append(temp[1].strip(' '))
        return selectcols,label,value

    else:
        return None


s=''
while(s!='exit'):
     sys.stdout.write('davisql>')
     s=raw_input()
     s=sqlparse.format(s, keyword_case='upper')
     processQuery(s)

# updateTableCount(CURRENT_DATABASE,'tables')
# updateTableCount(CURRENT_DATABASE,'columns')
# updateTableCount(CURRENT_DATABASE,'schemata')