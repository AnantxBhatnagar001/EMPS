import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, timedelta
import re
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
import seaborn as sns
from collections import Counter
import random
import json

class ModernEmployeeManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI-Powered Employee Management System")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#f0f2f5")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2563eb',      # Blue
            'secondary': '#f59e0b',    # Amber
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Yellow
            'info': '#06b6d4',         # Cyan
            'light': '#f8fafc',        # Light gray
            'dark': '#1e293b',         # Dark gray
            'background': '#f0f2f5',   # Background
            'surface': '#ffffff',      # White
            'accent': '#8b5cf6'        # Purple
        }
        
        # Database connection
        self.connection = None
        self.cursor = None
        
        # Current view
        self.current_view = tk.StringVar(value="dashboard")
        
        # AI insights data
        self.ai_insights_cache = {}
        
        # Settings
        self.settings = {
            'theme': 'light',
            'auto_backup': True,
            'notification_sound': True,
            'show_tooltips': True,
            'data_retention_days': 365
        }
        
        # Setup database connection
        self.setup_database()
        
        # Setup modern GUI
        self.setup_modern_gui()
        
        # Load initial data
        self.refresh_employee_list()
        self.update_dashboard()
    
    def setup_database(self):
        """Setup SQLite database connection and create enhanced table"""
        try:
            db_path = "advanced_employee_management.db"
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()
            
            # Create enhanced table with additional fields
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS employees (
                emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                department TEXT NOT NULL,
                position TEXT NOT NULL,
                salary REAL NOT NULL,
                joining_date DATE NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                performance_rating REAL DEFAULT 0.0,
                skills TEXT,
                manager_id INTEGER,
                status TEXT DEFAULT 'Active',
                last_promotion DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            self.cursor.execute(create_table_query)
            
            # Create performance tracking table
            performance_table_query = '''
            CREATE TABLE IF NOT EXISTS performance_reviews (
                review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id INTEGER,
                review_date DATE NOT NULL,
                rating REAL NOT NULL,
                feedback TEXT,
                goals TEXT,
                reviewer TEXT,
                FOREIGN KEY (emp_id) REFERENCES employees (emp_id)
            )
            '''
            self.cursor.execute(performance_table_query)
            
            # Create AI insights table
            ai_insights_query = '''
            CREATE TABLE IF NOT EXISTS ai_insights (
                insight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT NOT NULL,
                insight_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            self.cursor.execute(ai_insights_query)
            
            self.connection.commit()
            print(f"Enhanced database created/connected successfully: {db_path}")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            self.connection = None
            self.cursor = None
    
    def setup_modern_gui(self):
        """Setup modern GUI with dashboard and navigation"""
        # Configure modern styles
        self.setup_modern_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill='both', expand=True)
        
        # Create sidebar navigation
        self.create_sidebar()
        
        # Create main content area
        self.main_content = ttk.Frame(self.main_container)
        self.main_content.pack(side='right', fill='both', expand=True, padx=20, pady=20)
        
        # Initialize views
        self.create_dashboard_view()
        self.create_employee_view()
        self.create_analytics_view()
        self.create_ai_insights_view()
        self.create_settings_view()
        
        # Show dashboard by default
        self.show_view("dashboard")
    
    def setup_modern_styles(self):
        """Configure modern TTK styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure modern button styles
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        
        style.map('Modern.TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', '#1d4ed8')])
        
        # Primary button style
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        # Success button style
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['success'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        # Danger button style
        style.configure('Danger.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['danger'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(15, 8))
        
        # Modern frame styles
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       relief='flat',
                       borderwidth=1)
        
        # Modern label styles
        style.configure('Title.TLabel',
                       font=('Segoe UI', 24, 'bold'),
                       background=self.colors['background'],
                       foreground=self.colors['dark'])
        
        style.configure('Heading.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       background=self.colors['surface'],
                       foreground=self.colors['dark'])
        
        style.configure('Subheading.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       background=self.colors['surface'],
                       foreground=self.colors['primary'])
        
        style.configure('Body.TLabel',
                       font=('Segoe UI', 10),
                       background=self.colors['surface'],
                       foreground='#64748b')
        
        # Modern entry styles
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 10),
                       borderwidth=1,
                       insertwidth=2,
                       padding=(10, 8))
        
        # Sidebar styles
        style.configure('Sidebar.TFrame',
                       background=self.colors['dark'])
        
        style.configure('SidebarButton.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       background=self.colors['dark'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 15),
                       anchor='w')
        
        style.map('SidebarButton.TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', '#1d4ed8')])
    
    def create_sidebar(self):
        """Create modern sidebar navigation"""
        sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Title area
        logo_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        logo_frame.pack(fill='x', pady=30, padx=20)
        
        title_label = ttk.Label(logo_frame, text="EMS Pro", 
                               font=('Segoe UI', 20, 'bold'),
                               background=self.colors['dark'],
                               foreground='white')
        title_label.pack()
        
        subtitle_label = ttk.Label(logo_frame, text="AI-Powered Management", 
                                  font=('Segoe UI', 9),
                                  background=self.colors['dark'],
                                  foreground='#94a3b8')
        subtitle_label.pack()
        
        # Navigation buttons
        nav_buttons = [
            ("🏠 Dashboard", "dashboard"),
            ("👥 Employees", "employees"),
            ("📊 Analytics", "analytics"),
            ("🤖 AI Insights", "ai_insights"),
            ("⚙️ Settings", "settings")
        ]
        
        for text, view in nav_buttons:
            btn = ttk.Button(sidebar, text=text, style='SidebarButton.TButton',
                           command=lambda v=view: self.show_view(v))
            btn.pack(fill='x', padx=10, pady=2)
        
        # Footer
        footer_frame = ttk.Frame(sidebar, style='Sidebar.TFrame')
        footer_frame.pack(side='bottom', fill='x', pady=20, padx=20)
        
        footer_label = ttk.Label(footer_frame, text="© 2025 EMS Pro", 
                                font=('Segoe UI', 8),
                                background=self.colors['dark'],
                                foreground='#64748b')
        footer_label.pack()
    
    def create_dashboard_view(self):
        """Create modern dashboard view"""
        self.dashboard_frame = ttk.Frame(self.main_content)
        
        # Welcome header
        header_frame = ttk.Frame(self.dashboard_frame, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        welcome_label = ttk.Label(header_frame, text="Welcome to EMS Pro", style='Title.TLabel')
        welcome_label.pack(pady=20)
        
        date_label = ttk.Label(header_frame, 
                              text=f"Today is {datetime.now().strftime('%A, %B %d, %Y')}", 
                              style='Body.TLabel')
        date_label.pack()
        
        # Stats cards container
        stats_container = ttk.Frame(self.dashboard_frame)
        stats_container.pack(fill='x', pady=(0, 20))
        
        # Create stats cards
        self.create_stats_cards(stats_container)
        
        # Charts container
        charts_container = ttk.Frame(self.dashboard_frame)
        charts_container.pack(fill='both', expand=True)
        
        # Create dashboard charts
        self.create_dashboard_charts(charts_container)
    
    def create_stats_cards(self, parent):
        """Create statistics cards for dashboard"""
        # Create card data
        self.stats_vars = {
            'total_employees': tk.StringVar(value="0"),
            'avg_salary': tk.StringVar(value="$0"),
            'top_department': tk.StringVar(value="N/A"),
            'new_hires': tk.StringVar(value="0")
        }
        
        cards = [
            ("Total Employees", self.stats_vars['total_employees'], self.colors['primary'], "👥"),
            ("Average Salary", self.stats_vars['avg_salary'], self.colors['success'], "💰"),
            ("Top Department", self.stats_vars['top_department'], self.colors['info'], "🏢"),
            ("New Hires (30d)", self.stats_vars['new_hires'], self.colors['warning'], "📈")
        ]
        
        for i, (title, var, color, icon) in enumerate(cards):
            card = ttk.Frame(parent, style='Card.TFrame')
            card.grid(row=0, column=i, padx=10, pady=10, sticky='ew')
            
            # Icon and title
            header_frame = ttk.Frame(card, style='Card.TFrame')
            header_frame.pack(fill='x', padx=20, pady=(20, 10))
            
            icon_label = ttk.Label(header_frame, text=icon, font=('Segoe UI', 20),
                                  background=self.colors['surface'])
            icon_label.pack(side='left')
            
            title_label = ttk.Label(header_frame, text=title, 
                                   font=('Segoe UI', 11, 'bold'),
                                   background=self.colors['surface'],
                                   foreground='#64748b')
            title_label.pack(side='right')
            
            # Value
            value_label = ttk.Label(card, textvariable=var,
                                   font=('Segoe UI', 18, 'bold'),
                                   background=self.colors['surface'],
                                   foreground=color)
            value_label.pack(padx=20, pady=(0, 20))
        
        # Configure grid weights
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
    
    def create_dashboard_charts(self, parent):
        """Create dashboard charts"""
        # Left panel for department chart
        left_panel = ttk.Frame(parent, style='Card.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(left_panel, text="Department Distribution", style='Heading.TLabel').pack(pady=20)
        
        # Create matplotlib figure for pie chart
        self.dept_fig, self.dept_ax = plt.subplots(figsize=(6, 4))
        self.dept_canvas = FigureCanvasTkAgg(self.dept_fig, left_panel)
        self.dept_canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Right panel for salary trends
        right_panel = ttk.Frame(parent, style='Card.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        ttk.Label(right_panel, text="Salary Analysis", style='Heading.TLabel').pack(pady=20)
        
        # Create matplotlib figure for bar chart
        self.salary_fig, self.salary_ax = plt.subplots(figsize=(6, 4))
        self.salary_canvas = FigureCanvasTkAgg(self.salary_fig, right_panel)
        self.salary_canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=(0, 20))
    
    def create_employee_view(self):
        """Create enhanced employee management view"""
        self.employee_frame = ttk.Frame(self.main_content)
        
        # Header
        header_frame = ttk.Frame(self.employee_frame, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Employee Management", style='Title.TLabel').pack(pady=20)
        
        # Main container
        main_container = ttk.Frame(self.employee_frame)
        main_container.pack(fill='both', expand=True)
        
        # Left panel for enhanced form
        left_panel = ttk.LabelFrame(main_container, text="Employee Information", padding=20)
        left_panel.pack(side='left', fill='y', padx=(0, 20), pady=10)
        
        # Right panel for list and advanced features
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.setup_enhanced_form_panel(left_panel)
        self.setup_enhanced_list_panel(right_panel)
    
    def setup_enhanced_form_panel(self, parent):
        """Setup enhanced form panel with additional fields"""
        # Create form variables
        self.form_vars = {
            'emp_id': tk.StringVar(),
            'name': tk.StringVar(),
            'age': tk.StringVar(),
            'department': tk.StringVar(),
            'position': tk.StringVar(),
            'salary': tk.StringVar(),
            'joining_date': tk.StringVar(),
            'email': tk.StringVar(),
            'phone': tk.StringVar(),
            'address': tk.StringVar(),
            'performance_rating': tk.StringVar(),
            'skills': tk.StringVar(),
            'status': tk.StringVar(value='Active')
        }
        
        # Set default date
        self.form_vars['joining_date'].set(datetime.now().strftime('%Y-%m-%d'))
        
        # Create form fields
        fields = [
            ("Employee ID:", 'emp_id', 'readonly'),
            ("Full Name:", 'name', 'normal'),
            ("Age:", 'age', 'normal'),
            ("Department:", 'department', 'combobox'),
            ("Position:", 'position', 'normal'),
            ("Email:", 'email', 'normal'),
            ("Phone:", 'phone', 'normal'),
            ("Salary ($):", 'salary', 'normal'),
            ("Joining Date:", 'joining_date', 'normal'),
            ("Performance Rating:", 'performance_rating', 'normal'),
            ("Skills:", 'skills', 'text'),
            ("Status:", 'status', 'combobox')
        ]
        
        self.form_widgets = {}
        
        for i, (label, var_name, widget_type) in enumerate(fields):
            ttk.Label(parent, text=label, style='Subheading.TLabel').grid(
                row=i, column=0, sticky='w', pady=5, padx=(0, 10))
            
            if widget_type == 'readonly':
                widget = ttk.Entry(parent, textvariable=self.form_vars[var_name], 
                                 state='readonly', width=35, style='Modern.TEntry')
            elif widget_type == 'combobox':
                widget = ttk.Combobox(parent, textvariable=self.form_vars[var_name], width=33)
                if var_name == 'department':
                    widget['values'] = ('HR', 'IT', 'Finance', 'Marketing', 'Operations', 'Sales', 'Engineering', 'Design')
                elif var_name == 'status':
                    widget['values'] = ('Active', 'Inactive', 'On Leave', 'Terminated')
            elif widget_type == 'text':
                widget = tk.Text(parent, width=35, height=3, font=('Segoe UI', 10))
            else:
                widget = ttk.Entry(parent, textvariable=self.form_vars[var_name], 
                                 width=35, style='Modern.TEntry')
            
            widget.grid(row=i, column=1, pady=5, sticky='ew')
            self.form_widgets[var_name] = widget
        
        # Address field (multiline)
        ttk.Label(parent, text="Address:", style='Subheading.TLabel').grid(
            row=len(fields), column=0, sticky='nw', pady=5, padx=(0, 10))
        self.address_text = tk.Text(parent, width=35, height=3, font=('Segoe UI', 10))
        self.address_text.grid(row=len(fields), column=1, pady=5, sticky='ew')
        
        # Button frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=20)
        
        # Enhanced buttons
        buttons = [
            ("Add Employee", self.add_employee, 'Success.TButton'),
            ("Update Employee", self.update_employee, 'Primary.TButton'),
            ("Clear Form", self.clear_enhanced_form, 'Modern.TButton'),
            ("AI Suggestions", self.get_ai_suggestions, 'Modern.TButton')
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, style=style)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
    
    def setup_enhanced_list_panel(self, parent):
        """Setup enhanced employee list panel"""
        # Advanced search frame
        search_frame = ttk.LabelFrame(parent, text="Advanced Search & Filters", padding=15)
        search_frame.pack(fill='x', pady=(0, 10))
        
        # Search row
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill='x', pady=(0, 10))
        
        ttk.Label(search_row, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, width=25, style='Modern.TEntry')
        search_entry.pack(side='left', padx=(5, 0))
        
        # Filter row
        filter_row = ttk.Frame(search_frame)
        filter_row.pack(fill='x')
        
        ttk.Label(filter_row, text="Department:").pack(side='left')
        self.dept_filter = ttk.Combobox(filter_row, width=15)
        self.dept_filter['values'] = ('All', 'HR', 'IT', 'Finance', 'Marketing', 'Operations', 'Sales', 'Engineering', 'Design')
        self.dept_filter.set('All')
        self.dept_filter.pack(side='left', padx=(5, 15))
        
        ttk.Label(filter_row, text="Status:").pack(side='left')
        self.status_filter = ttk.Combobox(filter_row, width=12)
        self.status_filter['values'] = ('All', 'Active', 'Inactive', 'On Leave', 'Terminated')
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=(5, 15))
        
        # Action buttons
        ttk.Button(filter_row, text="Search", command=self.advanced_search, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(filter_row, text="Reset", command=self.reset_filters, style='Modern.TButton').pack(side='left', padx=5)
        
        # Employee list frame
        list_frame = ttk.LabelFrame(parent, text="Employee Directory", padding=15)
        list_frame.pack(fill='both', expand=True)
        
        # Enhanced Treeview
        columns = ('ID', 'Name', 'Age', 'Department', 'Position', 'Salary', 'Status', 'Performance', 'Joining Date')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Configure columns
        column_widths = {'ID': 50, 'Name': 150, 'Age': 50, 'Department': 100, 'Position': 120, 
                        'Salary': 100, 'Status': 80, 'Performance': 90, 'Joining Date': 100}
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c, False))
            self.tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_employee_select)
        self.tree.bind('<Double-1>', self.on_employee_double_click)
        
        # Enhanced action buttons
        action_frame = ttk.Frame(parent)
        action_frame.pack(fill='x', pady=15)
        
        action_buttons = [
            ("Delete Selected", self.delete_employee, 'Danger.TButton'),
            ("Export CSV", self.export_to_csv, 'Modern.TButton'),
            ("Import CSV", self.import_from_csv, 'Modern.TButton'),
            ("Generate Report", self.generate_report, 'Primary.TButton'),
            ("Sample Data", self.add_enhanced_sample_data, 'Success.TButton')
        ]
        
        for text, command, style in action_buttons:
            ttk.Button(action_frame, text=text, command=command, style=style).pack(side='left', padx=5)
    
    def create_analytics_view(self):
        """Create analytics dashboard view"""
        self.analytics_frame = ttk.Frame(self.main_content)
        
        # Header
        header_frame = ttk.Frame(self.analytics_frame, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Analytics Dashboard", style='Title.TLabel').pack(pady=20)
        
        # Analytics content
        content_frame = ttk.Frame(self.analytics_frame)
        content_frame.pack(fill='both', expand=True)
        
        # Top row - Key metrics
        metrics_frame = ttk.Frame(content_frame, style='Card.TFrame')
        metrics_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(metrics_frame, text="Key Performance Indicators", style='Heading.TLabel').pack(pady=15)
        
        # Bottom area - Charts
        charts_frame = ttk.Frame(content_frame)
        charts_frame.pack(fill='both', expand=True)
        
        # Left chart
        left_chart = ttk.Frame(charts_frame, style='Card.TFrame')
        left_chart.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        ttk.Label(left_chart, text="Salary Distribution", style='Heading.TLabel').pack(pady=15)
        
        # Right chart
        right_chart = ttk.Frame(charts_frame, style='Card.TFrame')
        right_chart.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        ttk.Label(right_chart, text="Performance Trends", style='Heading.TLabel').pack(pady=15)
        
        # Create analytics charts
        self.setup_analytics_charts(left_chart, right_chart)
    

    def setup_analytics_charts(self, left_parent, right_parent):
        """Setup analytics charts for salary distribution and performance trends"""
        # --- Salary Distribution Chart ---
        self.salary_dist_fig, self.salary_dist_ax = plt.subplots(figsize=(5, 3))
        self.salary_dist_canvas = FigureCanvasTkAgg(self.salary_dist_fig, left_parent)
        self.salary_dist_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        self.cursor.execute("SELECT salary FROM employees")
        salaries = [row[0] for row in self.cursor.fetchall()]
        self.salary_dist_ax.clear()
        if salaries:
            sns.histplot(salaries, bins=10, kde=True, ax=self.salary_dist_ax, color="#2563eb")
            self.salary_dist_ax.set_title("Salary Distribution")
            self.salary_dist_ax.set_xlabel("Salary")
            self.salary_dist_ax.set_ylabel("Count")
        else:
            self.salary_dist_ax.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.salary_dist_fig.tight_layout()
        self.salary_dist_canvas.draw()

        # --- Performance Trends Chart ---
        self.performance_fig, self.performance_ax = plt.subplots(figsize=(5, 3))
        self.performance_canvas = FigureCanvasTkAgg(self.performance_fig, right_parent)
        self.performance_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

        self.cursor.execute("""
            SELECT strftime('%Y-%m', joining_date) as month, AVG(performance_rating)
            FROM employees
            GROUP BY month
            ORDER BY month
        """)
        data = self.cursor.fetchall()
        months = [row[0] for row in data]
        ratings = [row[1] for row in data]
        self.performance_ax.clear()
        if months and ratings:
            self.performance_ax.plot(months, ratings, marker='o', color="#10b981")
            self.performance_ax.set_title("Performance Trends")
            self.performance_ax.set_xlabel("Month")
            self.performance_ax.set_ylabel("Avg. Performance Rating")
            self.performance_ax.tick_params(axis='x', rotation=45)
        else:
            self.performance_ax.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.performance_fig.tight_layout()
        self.performance_canvas.draw()
    
    def create_ai_insights_view(self):
        """Create AI insights view"""
        self.ai_insights_frame = ttk.Frame(self.main_content)
        
        # Header
        header_frame = ttk.Frame(self.ai_insights_frame, style='Card.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="🤖 AI-Powered Insights", style='Title.TLabel').pack(pady=20)
        
        # AI content area
        content_frame = ttk.Frame(self.ai_insights_frame)
        content_frame.pack(fill='both', expand=True)
        
        # Left panel - AI recommendations
        left_panel = ttk.LabelFrame(content_frame, text="Smart Recommendations", padding=20)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.ai_recommendations = tk.Text(left_panel, wrap='word', font=('Segoe UI', 10),
                                         height=20, width=50)
        self.ai_recommendations.pack(fill='both', expand=True)
        
        # Right panel - Predictive analytics
        right_panel = ttk.LabelFrame(content_frame, text="Predictive Analytics", padding=20)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.predictive_analytics = tk.Text(right_panel, wrap='word', font=('Segoe UI', 10),
                                           height=20, width=50)
        self.predictive_analytics.pack(fill='both', expand=True)
        
        # AI action buttons
        ai_button_frame = ttk.Frame(self.ai_insights_frame)
        ai_button_frame.pack(fill='x', pady=20)

        ai_buttons = [
            ("Generate Insights", self.generate_ai_insights, 'Primary.TButton'),
            ("Predict Turnover", self.predict_turnover, 'Modern.TButton'),
            ("Salary Analysis", self.ai_salary_analysis, 'Modern.TButton'),
            ("Performance Forecast", self.performance_forecast, 'Modern.TButton')
        ]

        for text, command, style in ai_buttons:
            ttk.Button(ai_button_frame, text=text, command=command, style=style).pack(side='left', padx=10)

    # --- AI Features Implementation ---

    def generate_ai_insights(self):
        """Generate real AI-powered insights based on employee data"""
        self.ai_recommendations.delete('1.0', tk.END)
        self.predictive_analytics.delete('1.0', tk.END)

        # Gather data
        self.cursor.execute("SELECT department, AVG(performance_rating), COUNT(*) FROM employees GROUP BY department")
        dept_perf = self.cursor.fetchall()
        self.cursor.execute("SELECT AVG(salary) FROM employees")
        avg_salary = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
        dept_salary = self.cursor.fetchall()
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE status='On Leave'")
        on_leave = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE status='Active'")
        active = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE status='Terminated'")
        terminated = self.cursor.fetchone()[0]

        # AI Recommendations
        self.ai_recommendations.insert(tk.END, "🔍 **AI Insights & Recommendations**\n\n")
        if dept_perf:
            best_dept = max(dept_perf, key=lambda x: x[1])
            self.ai_recommendations.insert(tk.END, f"• Highest average performance: {best_dept[0]} ({best_dept[1]:.2f})\n")
        if dept_salary:
            high_salary_dept = max(dept_salary, key=lambda x: x[1])
            low_salary_dept = min(dept_salary, key=lambda x: x[1])
            self.ai_recommendations.insert(tk.END, f"• Highest avg salary: {high_salary_dept[0]} (${high_salary_dept[1]:,.2f})\n")
            self.ai_recommendations.insert(tk.END, f"• Lowest avg salary: {low_salary_dept[0]} (${low_salary_dept[1]:,.2f})\n")
        self.ai_recommendations.insert(tk.END, f"• Employees on leave: {on_leave}\n")
        self.ai_recommendations.insert(tk.END, f"• Active employees: {active}\n")
        self.ai_recommendations.insert(tk.END, f"• Terminated employees: {terminated}\n")
        if avg_salary:
            self.ai_recommendations.insert(tk.END, f"• Company-wide average salary: ${avg_salary:,.2f}\n")
        self.ai_recommendations.insert(tk.END, "\n• Suggestion: Consider upskilling programs for departments with low performance.\n")
        self.ai_recommendations.insert(tk.END, "• Suggestion: Review compensation in departments with below-average salaries.\n")

    def predict_turnover(self):
        """Predict employee turnover using simple AI logic"""
        self.predictive_analytics.delete('1.0', tk.END)
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        total = self.cursor.fetchone()[0] or 1
        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE status='Terminated'")
        terminated = self.cursor.fetchone()[0]
        turnover_rate = (terminated / total) * 100
        self.predictive_analytics.insert(tk.END, "🔮 **Turnover Prediction**\n\n")
        self.predictive_analytics.insert(tk.END, f"• Estimated turnover rate: {turnover_rate:.2f}%\n")
        if turnover_rate > 10:
            self.predictive_analytics.insert(tk.END, "• High turnover detected! Consider employee engagement programs.\n")
        else:
            self.predictive_analytics.insert(tk.END, "• Turnover is within a healthy range.\n")

    def ai_salary_analysis(self):
        """AI-powered salary analysis"""
        self.predictive_analytics.delete('1.0', tk.END)
        self.cursor.execute("SELECT AVG(salary) FROM employees")
        avg_salary = self.cursor.fetchone()[0] or 0
        self.cursor.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
        dept_salary = self.cursor.fetchall()
        self.predictive_analytics.insert(tk.END, "💰 **Salary Analysis**\n\n")
        self.predictive_analytics.insert(tk.END, f"• Company-wide average salary: ${avg_salary:,.2f}\n")
        for dept, avg in dept_salary:
            self.predictive_analytics.insert(tk.END, f"• {dept}: ${avg:,.2f}\n")
        self.predictive_analytics.insert(tk.END, "\n• Suggestion: Review salary structure for equity across departments.\n")

    def performance_forecast(self):
        """AI-powered performance forecast"""
        self.predictive_analytics.delete('1.0', tk.END)
        self.cursor.execute("SELECT AVG(performance_rating) FROM employees")
        avg_perf = self.cursor.fetchone()[0] or 0
        self.predictive_analytics.insert(tk.END, "📈 **Performance Forecast**\n\n")
        self.predictive_analytics.insert(tk.END, f"• Current average performance rating: {avg_perf:.2f}\n")
        if avg_perf < 3:
            self.predictive_analytics.insert(tk.END, "• Forecast: Performance may decline. Recommend training and motivation.\n")
        else:
            self.predictive_analytics.insert(tk.END, "• Forecast: Performance is stable or improving.\n")

    def get_ai_suggestions(self):
        """Enable AI suggestions for the employee form"""
        name = self.form_vars['name'].get()
        dept = self.form_vars['department'].get()
        perf = self.form_vars['performance_rating'].get()
        salary = self.form_vars['salary'].get()
        suggestions = []
        if not name:
            suggestions.append("Enter the employee's full name.")
        if dept == "":
            suggestions.append("Select a department for the employee.")
        if perf and float(perf) < 3:
            suggestions.append("Performance is below average. Recommend training.")
        if salary and float(salary) < 30000:
            suggestions.append("Salary is below market average. Consider review.")
        if not suggestions:
            suggestions.append("All fields look good! Ready to add/update employee.")
        messagebox.showinfo("AI Suggestions", "\n".join(suggestions))

    def add_enhanced_sample_data(self):
        """Add realistic sample data to the database"""
        sample_employees = [
            ("Alice Johnson", 29, "IT", "Software Engineer", 85000, "2023-01-15", "alice.j@ems.com", "9876543210", "123 Main St", 4.5, "Python,SQL", "Active"),
            ("Bob Smith", 35, "Finance", "Accountant", 65000, "2022-03-10", "bob.s@ems.com", "8765432109", "456 Oak Ave", 3.8, "Excel,Finance", "Active"),
            ("Carol Lee", 41, "HR", "HR Manager", 72000, "2021-07-22", "carol.l@ems.com", "7654321098", "789 Pine Rd", 4.2, "Recruitment,Training", "On Leave"),
            ("David Kim", 27, "Engineering", "DevOps Engineer", 90000, "2023-06-01", "david.k@ems.com", "6543210987", "321 Cedar Blvd", 4.7, "AWS,Docker", "Active"),
            ("Eva Brown", 31, "Marketing", "Marketing Lead", 78000, "2022-11-18", "eva.b@ems.com", "5432109876", "654 Spruce Ln", 4.0, "SEO,Content", "Active"),
        ]
        for emp in sample_employees:
            self.cursor.execute('''
                INSERT INTO employees (name, age, department, position, salary, joining_date, email, phone, address, performance_rating, skills, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        self.connection.commit()
        self.refresh_employee_list()
        messagebox.showinfo("Sample Data", "Sample employee data added successfully!")

    def refresh_employee_list(self):
        """Refresh the employee list in the UI"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT emp_id, name, age, department, position, salary, status, performance_rating, joining_date FROM employees")
        for row in self.cursor.fetchall():
            self.tree.insert('', 'end', values=row)


    def update_dashboard(self):
        """Update dashboard stats and charts with latest data"""
        # Update stats cards
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        total_employees = self.cursor.fetchone()[0] or 0
        self.stats_vars['total_employees'].set(str(total_employees))

        self.cursor.execute("SELECT AVG(salary) FROM employees")
        avg_salary = self.cursor.fetchone()[0] or 0
        self.stats_vars['avg_salary'].set(f"${avg_salary:,.2f}")

        self.cursor.execute("SELECT department, COUNT(*) as cnt FROM employees GROUP BY department ORDER BY cnt DESC LIMIT 1")
        row = self.cursor.fetchone()
        self.stats_vars['top_department'].set(row[0] if row else "N/A")

        self.cursor.execute("SELECT COUNT(*) FROM employees WHERE joining_date >= ?", 
                            ((datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),))
        new_hires = self.cursor.fetchone()[0] or 0
        self.stats_vars['new_hires'].set(str(new_hires))

        # Update department pie chart
        self.cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
        dept_data = self.cursor.fetchall()
        self.dept_ax.clear()
        if dept_data:
            labels, sizes = zip(*dept_data)
            self.dept_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
            self.dept_ax.set_title("Department Distribution", fontsize=14, fontweight='bold')
        else:
            self.dept_ax.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.dept_fig.tight_layout()
        self.dept_canvas.draw()

        # Update salary bar chart
        self.cursor.execute("SELECT department, AVG(salary) FROM employees GROUP BY department")
        salary_data = self.cursor.fetchall()
        self.salary_ax.clear()
        if salary_data:
            depts, avgs = zip(*salary_data)
            sns.barplot(x=list(depts), y=list(avgs), ax=self.salary_ax, palette="Blues_d")
            self.salary_ax.set_title("Average Salary by Department", fontsize=14, fontweight='bold')
            self.salary_ax.set_ylabel("Average Salary ($)")
            self.salary_ax.set_xlabel("Department")
        else:
            self.salary_ax.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.salary_fig.tight_layout()
        self.salary_canvas.draw()

    def on_employee_select(self, event):
        """Populate form with selected employee data"""
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], 'values')
        keys = ['emp_id', 'name', 'age', 'department', 'position', 'salary', 'status', 'performance_rating', 'joining_date']
        for i, key in enumerate(keys):
            if key in self.form_vars:
                self.form_vars[key].set(values[i])
        # Load address and other fields
        emp_id = values[0]
        self.cursor.execute("SELECT address, email, phone, skills FROM employees WHERE emp_id=?", (emp_id,))
        row = self.cursor.fetchone()
        if row:
            self.address_text.delete('1.0', tk.END)
            self.address_text.insert(tk.END, row[0] or "")
            self.form_vars['email'].set(row[1] or "")
            self.form_vars['phone'].set(row[2] or "")
            self.form_vars['skills'].set(row[3] or "")

    def on_employee_double_click(self, event):
        """Show detailed employee info on double-click"""
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], 'values')
        emp_id = values[0]
        self.cursor.execute("SELECT * FROM employees WHERE emp_id=?", (emp_id,))
        emp = self.cursor.fetchone()
        if emp:
            info = f"ID: {emp[0]}\nName: {emp[1]}\nAge: {emp[2]}\nDepartment: {emp[3]}\nPosition: {emp[4]}\nSalary: ${emp[5]:,.2f}\nJoining Date: {emp[6]}\nEmail: {emp[7]}\nPhone: {emp[8]}\nAddress: {emp[9]}\nPerformance: {emp[10]}\nSkills: {emp[11]}\nStatus: {emp[13]}"
            messagebox.showinfo("Employee Details", info)

    def add_employee(self):
        """Add a new employee to the database"""
        try:
            data = {k: v.get() for k, v in self.form_vars.items()}
            address = self.address_text.get('1.0', tk.END).strip()
            self.cursor.execute('''
                INSERT INTO employees (name, age, department, position, salary, joining_date, email, phone, address, performance_rating, skills, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['name'], int(data['age']), data['department'], data['position'], float(data['salary']),
                data['joining_date'], data['email'], data['phone'], address, float(data['performance_rating'] or 0), data['skills'], data['status']
            ))
            self.connection.commit()
            self.refresh_employee_list()
            messagebox.showinfo("Success", "Employee added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {e}")

    def update_employee(self):
        """Update selected employee in the database"""
        try:
            data = {k: v.get() for k, v in self.form_vars.items()}
            address = self.address_text.get('1.0', tk.END).strip()
            emp_id = data['emp_id']
            if not emp_id:
                messagebox.showwarning("Update", "Select an employee to update.")
                return
            self.cursor.execute('''
                UPDATE employees SET name=?, age=?, department=?, position=?, salary=?, joining_date=?, email=?, phone=?, address=?, performance_rating=?, skills=?, status=?, updated_at=CURRENT_TIMESTAMP
                WHERE emp_id=?
            ''', (
                data['name'], int(data['age']), data['department'], data['position'], float(data['salary']),
                data['joining_date'], data['email'], data['phone'], address, float(data['performance_rating'] or 0), data['skills'], data['status'], emp_id
            ))
            self.connection.commit()
            self.refresh_employee_list()
            messagebox.showinfo("Success", "Employee updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {e}")

    def clear_enhanced_form(self):
        """Clear the employee form"""
        for var in self.form_vars.values():
            var.set("")
        self.address_text.delete('1.0', tk.END)

    def delete_employee(self):
        """Delete selected employee"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Select an employee to delete.")
            return
        emp_id = self.tree.item(selected[0], 'values')[0]
        if messagebox.askyesno("Delete", "Are you sure you want to delete this employee?"):
            self.cursor.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))
            self.connection.commit()
            self.refresh_employee_list()
            messagebox.showinfo("Deleted", "Employee deleted successfully.")

    def export_to_csv(self):
        """Export employee data to CSV"""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        self.cursor.execute("SELECT * FROM employees")
        rows = self.cursor.fetchall()
        headers = [description[0] for description in self.cursor.description]
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        messagebox.showinfo("Export", "Employee data exported to CSV successfully.")

    def import_from_csv(self):
        """Import employee data from CSV"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.cursor.execute('''
                        INSERT INTO employees (name, age, department, position, salary, joining_date, email, phone, address, performance_rating, skills, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['name'], int(row['age']), row['department'], row['position'], float(row['salary']),
                        row['joining_date'], row['email'], row['phone'], row['address'], float(row['performance_rating'] or 0), row['skills'], row['status']
                    ))
                except Exception:
                    continue
            self.connection.commit()
        self.refresh_employee_list()
        messagebox.showinfo("Import", "Employee data imported from CSV successfully.")

    def generate_report(self):
        """Generate a simple employee report"""
        self.cursor.execute("SELECT department, COUNT(*) FROM employees GROUP BY department")
        dept_counts = self.cursor.fetchall()
        report = "Employee Report\n\nDepartment-wise Count:\n"
        for dept, count in dept_counts:
            report += f"{dept}: {count}\n"
        messagebox.showinfo("Report", report)

    def advanced_search(self):
        """Advanced search/filter employees"""
        query = "SELECT emp_id, name, age, department, position, salary, status, performance_rating, joining_date FROM employees WHERE 1=1"
        params = []
        if self.search_var.get():
            query += " AND (name LIKE ? OR department LIKE ? OR position LIKE ?)"
            val = f"%{self.search_var.get()}%"
            params.extend([val, val, val])
        if self.dept_filter.get() and self.dept_filter.get() != "All":
            query += " AND department=?"
            params.append(self.dept_filter.get())
        if self.status_filter.get() and self.status_filter.get() != "All":
            query += " AND status=?"
            params.append(self.status_filter.get())
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', 'end', values=row)

    def reset_filters(self):
        """Reset all search filters"""
        self.search_var.set("")
        self.dept_filter.set("All")
        self.status_filter.set("All")
        self.refresh_employee_list()

    # --- Settings View with More Features ---
    def create_settings_view(self):
        """Create settings view with more features"""
        self.settings_frame = ttk.Frame(self.main_content)
        header = ttk.Label(self.settings_frame, text="⚙️ Settings", style='Title.TLabel')
        header.pack(pady=20)
        content = ttk.Frame(self.settings_frame, style='Card.TFrame')
        content.pack(fill='both', expand=True, padx=40, pady=40)

        # Theme option
        ttk.Label(content, text="Theme:", style='Subheading.TLabel').grid(row=0, column=0, sticky='w', pady=10)
        theme_combo = ttk.Combobox(content, values=['light', 'dark'], width=15)
        theme_combo.set(self.settings['theme'])
        theme_combo.grid(row=0, column=1, sticky='w', padx=10)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.change_theme(theme_combo.get()))

        # Auto backup
        auto_backup_var = tk.BooleanVar(value=self.settings['auto_backup'])
        ttk.Checkbutton(content, text="Enable Auto Backup", variable=auto_backup_var).grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

        # Notification sound
        notif_var = tk.BooleanVar(value=self.settings['notification_sound'])
        ttk.Checkbutton(content, text="Notification Sound", variable=notif_var).grid(row=2, column=0, columnspan=2, sticky='w', pady=10)

        # Tooltips
        tooltip_var = tk.BooleanVar(value=self.settings['show_tooltips'])
        ttk.Checkbutton(content, text="Show Tooltips", variable=tooltip_var).grid(row=3, column=0, columnspan=2, sticky='w', pady=10)

        # Data retention
        ttk.Label(content, text="Data Retention (days):", style='Subheading.TLabel').grid(row=4, column=0, sticky='w', pady=10)
        retention_spin = ttk.Spinbox(content, from_=30, to=3650, width=10)
        retention_spin.set(self.settings['data_retention_days'])
        retention_spin.grid(row=4, column=1, sticky='w', padx=10)

        # Save button
        def save_settings():
            self.settings['theme'] = theme_combo.get()
            self.settings['auto_backup'] = auto_backup_var.get()
            self.settings['notification_sound'] = notif_var.get()
            self.settings['show_tooltips'] = tooltip_var.get()
            self.settings['data_retention_days'] = int(retention_spin.get())
            messagebox.showinfo("Settings", "Settings saved successfully!")
            self.change_theme(self.settings['theme'])

        ttk.Button(content, text="Save Settings", command=save_settings, style='Success.TButton').grid(row=5, column=0, columnspan=2, pady=20)

        # Add more settings features as needed

    def change_theme(self, theme):
        """Change application theme (light/dark)"""
        if theme == 'dark':
            self.root.configure(bg="#1e293b")
        else:
            self.root.configure(bg="#f0f2f5")
        # You can expand this to change more widget colors

    # --- Navigation ---
    def show_view(self, view_name):
        """Show the selected view in the main content area"""
        for frame in [getattr(self, f"{v}_frame", None) for v in ["dashboard", "employee", "analytics", "ai_insights", "settings"]]:
            if frame:
                frame.pack_forget()
        if view_name == "dashboard":
            self.dashboard_frame.pack(fill='both', expand=True)
        elif view_name == "employees":
            self.employee_frame.pack(fill='both', expand=True)
        elif view_name == "analytics":
            self.analytics_frame.pack(fill='both', expand=True)
        elif view_name == "ai_insights":
            self.ai_insights_frame.pack(fill='both', expand=True)
        elif view_name == "settings":
            self.settings_frame.pack(fill='both', expand=True)

    # --- Main loop ---
    def run(self):
        self.root.mainloop()

# Entry point
if __name__ == "__main__":
    app = ModernEmployeeManagementSystem()
    app.run()