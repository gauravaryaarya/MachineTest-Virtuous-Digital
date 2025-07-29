import sqlite3

conn = sqlite3.connect('test3.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS STUDENTS(
    StudentName VARCHAR(30) NOT NULL,
    CollegeName VARCHAR(50) NOT NULL,
    Round1Marks FLOAT CHECK(Round1Marks BETWEEN 0 AND 10),
    Round2Marks FLOAT CHECK(Round2Marks BETWEEN 0 AND 10),
    Round3Marks FLOAT CHECK(Round3Marks BETWEEN 0 AND 10),
    TechnicalRoundMarks FLOAT CHECK(TechnicalRoundMarks BETWEEN 0 AND 20),
    TotalMarks FLOAT CHECK(TotalMarks BETWEEN 0 AND 50),
    Result VARCHAR(20),
    Rank INT 
);
''')
conn.commit()


def get_valid_float(prompt, minimum, maximum):
    while True:
        try:
            value = float(input(prompt))
            if value < minimum or value > maximum:
                print(f"Input must be between {minimum} and {maximum}. Please try again.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

while True:
    StudentName = input("Enter Student Name (max 30 chars): ").strip()[:30]
    CollegeName = input("Enter College Name (max 50 chars): ").strip()[:50]
    Round1Marks = get_valid_float("Enter Round 1 Marks (0-10): ", 0, 10)
    Round2Marks = get_valid_float("Enter Round 2 Marks (0-10): ", 0, 10)
    Round3Marks = get_valid_float("Enter Round 3 Marks (0-10): ", 0, 10)
    TechnicalRoundMarks = get_valid_float("Enter Technical Round Marks (0-20): ", 0, 20)

    TotalMarks = Round1Marks + Round2Marks + Round3Marks + TechnicalRoundMarks

    Result = "Selected" if TotalMarks >= 35 else "Rejected"

    cur.execute('''
        INSERT INTO STUDENTS (StudentName, CollegeName, Round1Marks, Round2Marks,
                              Round3Marks, TechnicalRoundMarks, TotalMarks, Result, Rank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks,
          TechnicalRoundMarks, TotalMarks, Result, 0))
    conn.commit()

    repeat = input("ADD NEXT STUDENT? (yes/no): ").strip().lower()
    if repeat == "no":
        break

cur.execute("SELECT ROWID, TotalMarks FROM STUDENTS ORDER BY TotalMarks DESC")
students = cur.fetchall()

rank = 0
prev_score = None
actual_rank = 0
for rowid, score in students:
    actual_rank += 1
    if score != prev_score:
        rank = actual_rank
    
    cur.execute("UPDATE STUDENTS SET Rank = ? WHERE ROWID = ?", (rank, rowid))
    prev_score = score

conn.commit()


print("\nCandidate List Sorted by Rank:\n")
cur.execute("SELECT StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result, Rank FROM STUDENTS ORDER BY Rank, StudentName")
rows = cur.fetchall()

print(f"{'Name':30} {'College':50} {'R1':>4} {'R2':>4} {'R3':>4} {'Tech':>5} {'Total':>6} {'Result':10} {'Rank':>4}")
print("-" * 120)
for r in rows:
    print(f"{r[0]:30} {r[1]:50} {r[2]:4.1f} {r[3]:4.1f} {r[4]:4.1f} {r[5]:5.1f} {r[6]:6.1f} {r[7]:10} {r[8]:4}")

conn.close()
