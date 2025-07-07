# 🎓 University Student Management System (CLI + SQLite)

> A fully functional, terminal-based Student Database Management System (DBMS) built using Python and SQLite.  
> Ideal for college projects, demos, or just flexing your CRUD skills in a clean, interactive CLI.

---

## 📦 Features

✅ Create, view, update, and delete student-related tables  
✅ Preloaded with **demo data** (students, courses, enrollments)  
✅ Supports **dynamic table creation** with custom columns  
✅ Clean and readable table output (auto-formatted)  
✅ Auto-resequences IDs after deletions  
✅ 100% Python + SQLite — no external libraries  
✅ Extremely lightweight — can run on any system

---

## 🎮 Demo Tables Included
When you run the script, it automatically sets up:
- `students (id, name, age)`
- `courses (id, title, instructor)`
- `enrollments (id, student_id, course_id)`

Choose what you want to do:
```sql
1. View a table
2. Make a new table
3. Update a table
4. Delete a table
5. Exit
```
Perform actions like:
- Viewing and formatting any table  
- Inserting new rows  
- Updating fields in specific rows  
- Deleting rows by selecting the row number  
- Deleting entire tables  
- Creating new tables with custom column names and types
  
With sample data for you to play around with instantly.  

---

## 🖥️ How It Works

1. Launch the script:
```bash
python student_dbms.py
