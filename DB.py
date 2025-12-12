import sqlite3
import pandas as pd
from shutil import copyfile
import math

copyfile("Oscars.db","Bd.db")

conn = sqlite3.connect("Bd.db")

cur = conn.cursor()
cur.row_factory = sqlite3.Row

df = pd.read_excel("oscars.xlsx")

#print(df.head())

"""
Ceremony
Year
Class
CanonicalCategory
Category
NomId
Film
FilmId
Name
Nominees
NomineeIds
Winner
Detail
Note
Citation
MultifilmNomination
"""

print("Start")
cache = {"CEREMONY":set(),"CLASS":set(),"FILM":{("NULL","NULL")},"CATEGORY":set(),"NOMINATION":set(),"NOMINEE":set(),"NOMINATION_NOMINEE":set(),"NOMINATION_FILM":set()}
def check(entity,*atributes):
    global cache
    if atributes in cache[entity]: return False
    cache[entity].add(atributes)
    return True


def san(string):
    if isinstance(string,str): return string.replace("'","''")
    return string
def Nan(nan):
    if isinstance(nan,float) and math.isnan(nan): return 'NULL'
    return f"'{nan}'"



c = 0
NomIds = 0


for index,row in df.iterrows():
    #print(index)
    try:
        if check("CEREMONY",row["Ceremony"]):
            cur.execute(f'''insert into CEREMONY(CeremonyNumber,Year) values({row["Ceremony"]},'{row["Year"]}')''')
        if check("CLASS",row["Class"]):
            cur.execute(f'''insert into CLASS(ClassName) values('{row["Class"]}')''')
        if check("CATEGORY",row["Category"]):
            cur.execute(f'''insert into CATEGORY(ClassName,CanonicalCategory,CategoryName) values('{row["Class"]}','{row["CanonicalCategory"]}','{row["Category"]}')''')
        if check("FILM",Nan(row["FilmId"]),Nan(row["Film"])):
            cur.execute(f'''insert into FILM(FilmId,FilmName) values('{row["FilmId"]}','{san(row["Film"])}')''')
        if Nan(row["NomineeIds"]) == "NULL":
            NomIds+=1
            name = (san(row["Film"])if isinstance(t:=san(row["Name"]),float) else t) if isinstance(t:=san(row["Nominees"]),float) else t
            cur.execute(f'''insert into NOMINATION(ClassName,NomId,CeremonyNumber,CategoryName,NominationName,Winner,Detail,Note,Citation) values('{row["Class"]}',{NomIds},{row["Ceremony"]},'{row["Category"]}','{name}','{"FALSE" if math.isnan(t:=row["Winner"]) else "TRUE"}',{Nan(san(row["Detail"]))},{Nan(san(row["Note"]))},{Nan(san(row["Citation"]))})''')        
        else:
            if check("NOMINATION",row["Class"],row["Ceremony"],row["Category"],row["Nominees"]):
                NomIds+=1
                cur.execute(f'''insert into NOMINATION(ClassName,NomId,CeremonyNumber,CategoryName,NominationName,Winner,Detail,Note,Citation) values('{row["Class"]}',{NomIds},{row["Ceremony"]},'{row["Category"]}','{san(row["Nominees"]) if isinstance(t:=san(row["Name"]),float) else t}','{"FALSE" if math.isnan(t:=row["Winner"]) else "TRUE"}',{Nan(san(row["Detail"]))},{Nan(san(row["Note"]))},{Nan(san(row["Citation"]))})''')        
            else:           #append detail
                if Nan(row["Detail"]) != 'NULL':
                    cur.execute(f'''update NOMINATION set Detail = Detail || ', {san(row["Detail"])}' WHERE NomId = {NomIds}''')

            for nid,name in zip(t:=row["NomineeIds"].split(","),row["Nominees"].split(", ")):
                if name == "Australian News": name = "Australian News & Information Bureau"
                if nid != '?':
                    if check("NOMINEE",nid):
                        cur.execute(f'''insert into NOMINEE(NomineeId,Name) values('{nid}','{san(name)}') ''')
                    if check("NOMINATION_NOMINEE",NomIds,nid):
                        cur.execute(f'''insert into NOMINATION_NOMINEE(NomId,NomineeId) values({NomIds},'{nid}')''')
        if Nan(row["FilmId"]) != 'NULL':
            if check("NOMINATION_FILM",NomIds,row["FilmId"],row["Film"]):
                cur.execute(f'''insert into NOMINATION_FILM(NomId,FilmId,FilmName) values({NomIds},'{san(row["FilmId"])}','{san(row["Film"])}')''')
            else:
                if not math.isnan(row["Winner"]):
                    cur.execute(f'''update NOMINATION set Winner = 'TRUE' WHERE NomId = {NomIds}''')
    except Exception as e:
        c+=1
        raise e
print(c)
conn.commit()
