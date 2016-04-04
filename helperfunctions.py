import  struct,os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class fileMethods():

     def __init__(self,filePath):
          self.file=filePath
          self.tempfile=None
     #Byte

     #opens up a file
     def openFile(self):
          f=open(self.file,'ab+')
          self.tempfile=f
          return f

     #packs  the number to the byte
     def packByte(self,num):
          try:
               return struct.pack('>b',num)
          except:
               return None

     #writing byte to a file
     # at a given offset
     def writeByte(self,num):
          f=self.tempfile
          bytenum=self.packByte(num)
          if(bytenum !=None):
               f.write(bytenum)


     #reading byte from given offset
     def readByte(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          tmp=f.read(1)
          val= struct.unpack('>b',tmp)[0]
          return val

     #Unsigned Byte

     def  packUnByte(self,num):
          try:
               return struct.pack('>B',num)
          except:
               return None

     def writeUnByte(self,num):
          f=self.tempfile
          val=self.packUnByte(int(num))
          if(val!=None):
               f.write(val)

     def readUnByte(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)

          val=struct.unpack('>B',f.read(1))[0]
          return val


     # Short

     def packShort(self,num):
          try:
               return struct.pack('>h',num)
          except:
               return None

     def writeShort(self,num):
          value=self.packShort(int(num))
          f=self.tempfile
          if(value!=None):
               f.write(value)

     def readShort(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=struct.unpack('>h',f.read(2))[0]
          return val


     # UnsignedShort

     def packUnShort(self,num):
          try:
               return struct.pack('>H',num)
          except:
               return None

     def writeUnShort(self,num):
          value=self.packShort(int(num))
          f=self.tempfile
          if(value!=None):
               f.write(value)

     def readUnShort(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=struct.unpack('>H',f.read(2))[0]
          return val


     # Integer

     def packInt(self,num):
          try:
               return struct.pack('>i',num)
          except:
               return None

     def writeInt(self,num):
          value=self.packInt(int(num))
          f=self.tempfile
          if(value!=None):
               f.write(value)

     def readInt(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=struct.unpack('>i',f.read(4))[0]
          return val



     # Unsigned int
     def packUnInt(self,num):
          try:
               return struct.pack('>I',num)
          except:
               return None

     def writeUnInt(self,num):
          value=self.packUnInt(int(num))
          f=self.tempfile
          if(value!=None):
               f.write(value)

     def readUnInt(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=struct.unpack('>I',f.read(4))[0]
          return val


     # Long

     def packLong(self,num):
          try:
               return struct.pack('>l',num)
          except:
               return None

     def writeLong(self,num):
          value=self.packShort(long(num))
          f=self.tempfile
          if(value!=None):
               f.write(value)

     def readLong(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=struct.unpack('>l',f.read(8))[0]
          return val


     # Unsigned Long
     def packUnLong(self,num):
          try:
               return struct.pack('>L',num)
          except:
               return None

     def writeUnLong(self,num):
          value=self.packShort(long(num))
          f=self.tempfile
          if(value!=None):
               f.write(value)

     def readUnLong(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=struct.unpack('>L',f.read(8))[0]
          return val

     # Char
     def packChar(self,letter):
          try:
               return struct.pack('>c',letter)
          except:
               return None

     def writeChar(self,S,length):
          f=self.tempfile
          S=str(S)
          #appending line breaks for strings having less than n characters
          if(len(S)<length):
               for i in range(length-len(S)):
                    S+='\0'
          for i in S:
               value=self.packChar(i)
               if(value!=None):
                    f.write(value)

     def readChar(self,offset,length):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=''
          for i in range(length):
               val=val+struct.unpack('>c',f.read(1))[0]
          return val



     # VarChar
     def writeVarChar(self,S,maxlength):
          f=self.tempfile
          #writing the maxlength
          f.write(self.packUnByte(maxlength))
          for i in str(S):
               value=self.packChar(i)
               if(value!=None):
                    f.write(value)

     def readVarChar(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=''
          length=struct.unpack('>B',f.read(1))[0]
          for i in range(length):
               temp=struct.unpack('>c',f.read(1))[0]
               val=val+temp
          return val


     # Float
     def packFloat(self,num):
          try:
               return struct.pack('>f',num)
          except:
               return None

     def writeFloat(self,num):
          f=self.tempfile
          val=self.packFloat(float(num))
          if(val!=None):
               f.write(val)

     def readFloat(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=''
          val=struct.unpack('>f',f.read(4))[0]
          return val


     # Double
     def packDouble(self,num):
          try:
               return struct.pack('>d',num)
          except:
               return None

     def writeDouble(self,num):
          f=self.tempfile
          val=self.packFloat(num)
          if(val!=None):
               f.write(val)

     def readDouble(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=''
          val=struct.unpack('>d',f.read(8))[0]
          return val


     # Date Time
     def packDateTime(self,val):
          try:
               return struct.pack('>L',val)
          except:
               return None

     def writeDateTime(self,timestamp):
          f=self.tempfile
          val=self.packDateTime(timestamp)
          if(val!=None):
               f.write(val)

     def readDateTime(self,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          val=''
          val=struct.unpack('>L',f.read(8))[0]
          return val

     def close(self):
          self.tempfile.close()

     def reachedEOF(self):
          return self.tempfile.tell() == os.fstat(self.tempfile.fileno()).st_size


     def readDataType(self,type,offset):
          f=self.tempfile
          if(offset!=None):
               f.seek(offset)
          if('VARCHAR' in type.upper()):
               return self.readVarChar(None)
          elif('DATE' in type.upper()):
               return self.readDateTime(None)
          elif('UNSIGNED' in type.upper()):
               if('BYTE' in type.upper()):
                    return self.readUnByte(None)
               elif('SHORT' in type.upper()):
                    return self.readUnShort(None)
               elif('INT' in type.upper()):
                    return self.readUnInt(None)
               else:
                    return self.readUnLong(None)
          elif('BYTE' in type.upper()):
               return self.readByte(None)
          elif('SHORT' in type.upper()):
               return self.readShort(None)
          elif('INT' in type.upper()):
               return self.readInt(None)
          elif('LONG' in type.upper()):
               return self.readLong(None)
          elif('FLOAT' in type.upper()):
               return self.readFloat(None)
          elif('DOUBLE' in type.upper()):
               return self.readDouble(None)
          elif('DATE' in type.upper()):
               return self.readDateTime(None)
          else:
               return self.readChar(None,int(type[type.find("(")+1:type.find(")")]))


     def seek(self,offset):
          self.tempfile.seek(offset)
