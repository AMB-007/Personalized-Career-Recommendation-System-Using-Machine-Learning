import os
import mysql.connector
import pandas as pd

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abc123",  # Replace with your MySQL password if different
    database="career_system_db"
)
cursor = conn.cursor()

dataset_path = os.path.join(os.path.dirname(__file__), 'models', 'Datasets', 'Career_Training_Dataset_v2.csv')
print("Importing Career Training Dataset...")
df = pd.read_csv(dataset_path)

# Insert rows into student_profiles table
for _, row in df.iterrows():
    sql = """
        INSERT INTO student_profiles (
            Student_ID, Age, Gender, Location_Type, Education_Level, 
            Current_Class_Or_Year, Board, Stream, Specialization, Specialization_Group, 
            Math_Score, Science_Score, Social_Science_Score, English_Score, 
            Overall_Academic_Percentage, Attendance_Percentage, General_Aptitude_Score, 
            Coding_Score, Verbal_Ability_Score, Domain_Knowledge_Score, Realistic_Score, 
            Investigative_Score, Artistic_Score, Social_Score, Enterprising_Score, 
            Conventional_Score, Communication_Skill_Score, Leadership_Score, Creativity_Score, 
            Teamwork_Score, Problem_Solving_Score, Extracurricular_Involvement_Score, 
            Preferred_Work_Environment, Risk_Tolerance, Career_Readiness_Score, 
            Skill_Interest_Alignment_Score, Recommended_Career, Career_Cluster
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    # Convert row to tuple and handle NaN values
    val = tuple(None if pd.isna(x) else x for x in row)
    cursor.execute(sql, val)

conn.commit()
print(f"Successfully imported {len(df)} rows into student_profiles!")

cursor.close()
conn.close()