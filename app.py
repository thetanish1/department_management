import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class DepartmentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Department Management System")
        self.root.geometry("1200x600")
        
        # Database Connection
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="department_management"
            )
            self.cursor = self.db.cursor()
            self.create_tables()
            print("Database connection successful!")
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
            self.root.destroy()
            return
        
        # GUI Components
        self.create_widgets()
        self.load_departments()
        
    def create_tables(self):
        """Create necessary tables with foreign keys"""
        queries = [
            """CREATE TABLE IF NOT EXISTS institute (
                institute_id INT AUTO_INCREMENT PRIMARY KEY,
                institute_name VARCHAR(100)
            )""",
            """CREATE TABLE IF NOT EXISTS faculty (
                faculty_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(150) UNIQUE
            )""",
            """CREATE TABLE IF NOT EXISTS department (
                department_id INT AUTO_INCREMENT PRIMARY KEY,
                department_name VARCHAR(100),
                institute_id INT,
                FOREIGN KEY (institute_id) REFERENCES institute(institute_id) ON DELETE SET NULL
            )""",
            """CREATE TABLE IF NOT EXISTS courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                course_name VARCHAR(100),
                department_id INT,
                FOREIGN KEY (department_id) REFERENCES department(department_id) ON DELETE CASCADE
            )""",
            """CREATE TABLE IF NOT EXISTS feedback (
                feedback_id INT AUTO_INCREMENT PRIMARY KEY,
                feedback_text TEXT,
                faculty_id INT,
                FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE CASCADE
            )"""
        ]
        
        for query in queries:
            self.cursor.execute(query)
        self.db.commit()
    
    def create_widgets(self):
        """Creates tabs for each section"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.department_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.department_frame, text="Departments")
        self.create_department_tab()
        
        self.faculty_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.faculty_frame, text="Faculty")
        
        self.course_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.course_frame, text="Courses")
        
        self.institute_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.institute_frame, text="Institutes")
        
        self.feedback_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.feedback_frame, text="Feedback")
        
        self.create_department_tab()
        self.create_faculty_tab()
        self.create_course_tab()
        self.create_institute_tab()
        self.create_feedback_tab()
    
    def create_department_tab(self):
        """Department Management"""
        ttk.Label(self.department_frame, text="Department Name:").grid(row=0, column=0)
        self.department_name = ttk.Entry(self.department_frame)
        self.department_name.grid(row=0, column=1)
        
        ttk.Button(self.department_frame, text="Add Department", command=self.add_department).grid(row=1, column=0, pady=10)
    
    def create_faculty_tab(self):
        """Faculty Management"""
        ttk.Label(self.faculty_frame, text="Faculty Name:").grid(row=0, column=0)
        self.faculty_name = ttk.Entry(self.faculty_frame)
        self.faculty_name.grid(row=0, column=1)
    
    def create_course_tab(self):
        """Course Management"""
        ttk.Label(self.course_frame, text="Course Name:").grid(row=0, column=0)
        self.course_name = ttk.Entry(self.course_frame)
        self.course_name.grid(row=0, column=1)
    
    def create_institute_tab(self):
        """Institute Management"""
        ttk.Label(self.institute_frame, text="Institute Name:").grid(row=0, column=0)
        self.institute_name = ttk.Entry(self.institute_frame)
        self.institute_name.grid(row=0, column=1)
    
    def create_feedback_tab(self):
        """Feedback Management"""
        ttk.Label(self.feedback_frame, text="Feedback:").grid(row=0, column=0)
        self.feedback_text = ttk.Entry(self.feedback_frame)
        self.feedback_text.grid(row=0, column=1)
    
    def add_department(self):
        query = "INSERT INTO department (department_name) VALUES (%s)"
        values = (self.department_name.get(),)
        self.cursor.execute(query, values)
        self.db.commit()
        messagebox.showinfo("Success", "Department added successfully!")
        self.load_departments()
    
    def load_departments(self):
        pass  # Implement logic to load departments
    
    def __del__(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.cursor.close()
            self.db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = DepartmentManagementSystem(root)
    root.mainloop()
