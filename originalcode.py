import sqlite3

conn = sqlite3.connect('test2.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS STUDENTS(
        StudentName VARCHAR(30) NOT NULL,
        CollegeName VARCHAR(50) NOT NULL,
        Round1Marks FLOAT CHECK(Round1Marks BETWEEN 0 AND 10),
        Round2Marks FLOAT CHECK(Round2Marks BETWEEN 0 AND 10),
        Round3Marks FLOAT CHECK(Round3Marks BETWEEN 0 AND 10),
        TechnicalRoundMarks FLOAT CHECK(TechnicalRoundMarks BETWEEN 0 AND 20),
        TotalMarks FLOAT CHECK(TotalMarks BETWEEN 0 AND 50),
        Result VARCHAR(20) ,
        Rank INT 
    );
''')

conn.commit()


while True:
    StudentName = input("Enter Student Name : ")
    CollegeName = input("Enter College Name : ")
    Round1Marks = float(input("Enter Round 1 Marks : "))
    Round2Marks = float(input("Enter Round 2 Marks : "))
    Round3Marks = float(input("Enter Round 3 Marks : "))
    TechnicalRoundMarks = float(input("Enter Technical Round Marks : "))
    TotalMarks = Round1Marks + Round2Marks + Round3Marks + TechnicalRoundMarks

    if(TotalMarks>=35):
        Result = "Selected"
    else:
        Result = "Rejected"
    
    if(TotalMarks>=40):
        Rank = 1
    elif(TotalMarks>=30):
        Rank = 2
    elif TotalMarks>=2:
        Rank = 3
    else :
        Rank = 4
        
    cur.execute('INSERT INTO STUDENTS VALUES (?,?,?,?,?,?,?,?,?)',(StudentName,CollegeName,Round1Marks,Round2Marks,Round3Marks,TechnicalRoundMarks,TotalMarks,Result,Rank))
    conn.commit()
     
    repeat = input("ADD NEXT STUDENT? (yes/no)")
    if repeat.lower()=="no":
        break
    
      
get_data = cur.execute('SELECT * FROM STUDENTS ORDER BY Rank')
for i in get_data:
    print(i)        