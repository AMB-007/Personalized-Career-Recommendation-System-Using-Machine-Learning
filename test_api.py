import requests

url = "http://127.0.0.1:5000/api/predict/career"

payload = {
    "Age": 17,
    "Gender": "Female",
    "Location_Type": "Urban",
    "Education_Level": "Class 11-12",
    "Current_Class_Or_Year": "Class 12",
    "Board": "CBSE",
    "Stream": "Science - PCM",
    "Specialization": "Not Applicable",
    "Specialization_Group": "STEM",
    "Math_Score": 85.5,
    "Science_Score": 88.0,
    "Social_Science_Score": 75.0,
    "English_Score": 82.0,
    "Overall_Academic_Percentage": 84.5,
    "Attendance_Percentage": 92.0,
    "General_Aptitude_Score": 78.5,
    "Coding_Score": 88.0,
    "Verbal_Ability_Score": 76.0,
    "Domain_Knowledge_Score": 81.0,
    "Realistic_Score": 45.0,
    "Investigative_Score": 85.0,
    "Artistic_Score": 30.0,
    "Social_Score": 40.0,
    "Enterprising_Score": 60.0,
    "Conventional_Score": 70.0,
    "Communication_Skill_Score": 75.0,
    "Leadership_Score": 65.0,
    "Creativity_Score": 55.0,
    "Teamwork_Score": 80.0,
    "Problem_Solving_Score": 89.0,
    "Extracurricular_Involvement_Score": 60.0,
    "Preferred_Work_Environment": "Mixed",
    "Risk_Tolerance": "Medium",
    "Career_Readiness_Score": 78.0,
    "Skill_Interest_Alignment_Score": 82.0,
    "Total_Skill_Score": 82.5,
    "Total_RIASEC_Score": 330.0
}

response = requests.post(url, json=payload)
print(response.json())