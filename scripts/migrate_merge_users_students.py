"""
Migration script to merge 'students' into 'users' table in MySQL database.
Ensures data preservation, foreign key integrity, and drops 'students' table cleanly.
"""

import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

def run_migration():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'abc123'),
        database=os.getenv('DB_NAME', 'career_recommendation_db'),
        port=int(os.getenv('DB_PORT', 3306)),
        autocommit=True
    )
    cur = conn.cursor()

    print("Step 1: Adding student columns to `users`...")
    cur.execute("DESCRIBE `users`")
    existing_cols = [r[0] for r in cur.fetchall()]

    new_cols = [
        ("student_code", "VARCHAR(50) NULL UNIQUE AFTER `role`"),
        ("first_name", "VARCHAR(100) NULL AFTER `student_code`"),
        ("last_name", "VARCHAR(100) NULL AFTER `first_name`"),
        ("age", "TINYINT UNSIGNED NULL AFTER `last_name`"),
        ("gender", "VARCHAR(30) NULL AFTER `age`"),
        ("class_level", "TINYINT UNSIGNED NULL AFTER `gender`"),
        ("board", "VARCHAR(100) NULL DEFAULT 'CBSE' AFTER `class_level`"),
        ("medium", "VARCHAR(50) NULL DEFAULT 'English' AFTER `board`"),
        ("stream", "VARCHAR(100) NULL DEFAULT 'General' AFTER `medium`"),
        ("academic_scores", "JSON NULL AFTER `stream`")
    ]

    for col_name, col_def in new_cols:
        if col_name not in existing_cols:
            print(f"  Adding column `{col_name}`...")
            cur.execute(f"ALTER TABLE `users` ADD COLUMN `{col_name}` {col_def};")

    # Add indexes if not present
    cur.execute("SHOW INDEX FROM `users`")
    indexes = [r[2] for r in cur.fetchall()]
    if "idx_users_class" not in indexes:
        cur.execute("ALTER TABLE `users` ADD INDEX `idx_users_class` (`class_level`);")
    if "idx_users_stream" not in indexes:
        cur.execute("ALTER TABLE `users` ADD INDEX `idx_users_stream` (`stream`);")
    if "idx_users_code" not in indexes:
        cur.execute("ALTER TABLE `users` ADD INDEX `idx_users_code` (`student_code`);")

    cur.execute("SET FOREIGN_KEY_CHECKS = 0;")

    print("Step 2: Checking if `students` table exists to migrate data...")
    cur.execute("SHOW TABLES LIKE 'students'")
    if cur.fetchone():
        print("  Migrating existing data from `students` into `users`...")
        cur.execute("""
            UPDATE `users` u
            INNER JOIN `students` s ON s.user_id = u.id
            SET
                u.student_code = s.student_code,
                u.first_name = s.first_name,
                u.last_name = s.last_name,
                u.age = s.age,
                u.gender = s.gender,
                u.class_level = s.class_level,
                u.board = s.board,
                u.medium = s.medium,
                u.stream = s.stream,
                u.academic_scores = s.academic_scores;
        """)
        print(f"  Updated rows in `users`: {cur.rowcount}")

        print("Step 3: Dropping old foreign key constraints on `assessment_sessions`...")
        cur.execute("""
            SELECT CONSTRAINT_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = 'career_recommendation_db'
              AND TABLE_NAME = 'assessment_sessions'
              AND REFERENCED_TABLE_NAME = 'students'
        """)
        fks = cur.fetchall()
        for (fk_name,) in fks:
            print(f"  Dropping foreign key `{fk_name}`...")
            cur.execute(f"ALTER TABLE `assessment_sessions` DROP FOREIGN KEY `{fk_name}`;")

        print("Step 4: Remapping `assessment_sessions.student_id` to `users.id`...")
        cur.execute("""
            UPDATE `assessment_sessions` a
            INNER JOIN `students` s ON a.student_id = s.id
            SET a.student_id = s.user_id;
        """)
        print(f"  Updated rows in `assessment_sessions`: {cur.rowcount}")

        # Check if fk_sessions_user already exists
        cur.execute("""
            SELECT CONSTRAINT_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = 'career_recommendation_db'
              AND TABLE_NAME = 'assessment_sessions'
              AND CONSTRAINT_NAME = 'fk_sessions_user'
        """)
        if not cur.fetchone():
            print("  Adding foreign key `fk_sessions_user` referencing `users.id`...")
            cur.execute("""
                ALTER TABLE `assessment_sessions`
                ADD CONSTRAINT `fk_sessions_user`
                FOREIGN KEY (`student_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
            """)

        print("Step 5: Dropping `students` table...")
        cur.execute("DROP TABLE IF EXISTS `students`;")
        print("  `students` table dropped successfully!")
    else:
        print("  `students` table already dropped.")

    cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

    print("\nVerification: Current tables in `career_recommendation_db`:")
    cur.execute("SHOW TABLES;")
    for (t,) in cur.fetchall():
        print(f"  - {t}")

    print("\nVerification: Columns in `users`:")
    cur.execute("DESCRIBE `users`;")
    for r in cur.fetchall():
        print(f"  {r[0]}: {r[1]}")

    cur.close()
    conn.close()
    print("\nMigration completed successfully!")

if __name__ == '__main__':
    run_migration()
