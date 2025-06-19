#!/usr/bin/env python3
"""
Errika - Beautiful Translucent Todo Widget
A modern, draggable, translucent todo application for Mac and Linux
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import sys

class TodoWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.todos = []
        self.load_todos()
        self.setup_ui()
        self.setup_drag()
        
    def setup_window(self):
        """Configure the main window with translucency and modern styling"""
        self.root.title("Errika - Todo Widget")
        self.root.geometry("350x500")
        self.root.configure(bg='#2c2c2c')
        
        # Make window translucent
        self.root.attributes('-alpha', 0.9)
        
        # Always on top but not stealing focus
        self.root.attributes('-topmost', True)
        
        # Remove window decorations for a cleaner look (optional)
        # Uncomment the next line if you want borderless window
        # self.root.overrideredirect(True)
        
        # Set minimum size
        self.root.minsize(300, 400)
        
        # Configure for different platforms
        if sys.platform == "darwin":  # macOS
            self.root.attributes('-transparent', True)
        
    def setup_drag(self):
        """Enable window dragging"""
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.drag_window)
        
    def start_drag(self, event):
        """Start dragging the window"""
        self.x = event.x
        self.y = event.y
        
    def drag_window(self, event):
        """Drag the window"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('Dark.TFrame', background='#2c2c2c')
        style.configure('Dark.TLabel', background='#2c2c2c', foreground='white')
        style.configure('Dark.TButton', background='#404040', foreground='white')
        style.map('Dark.TButton', 
                 background=[('active', '#505050')])
        
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.setup_header()
        
        # Todo input section
        self.setup_input_section()
        
        # Todo list section
        self.setup_todo_list()
        
        # Footer with stats
        self.setup_footer()
        
    def setup_header(self):
        """Setup the header with title and controls"""
        header_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="✨ Errika Todo", 
                              font=('SF Pro Display', 18, 'bold') if sys.platform == "darwin" else ('Arial', 16, 'bold'),
                              bg='#2c2c2c', 
                              fg='#64b5f6')
        title_label.pack(side=tk.LEFT)
        
        # Close button
        close_btn = tk.Button(header_frame,
                             text="✕",
                             font=('Arial', 12, 'bold'),
                             bg='#f44336',
                             fg='white',
                             bd=0,
                             padx=8,
                             pady=2,
                             command=self.close_app)
        close_btn.pack(side=tk.RIGHT)
        
        # Minimize button
        min_btn = tk.Button(header_frame,
                           text="−",
                           font=('Arial', 12, 'bold'),
                           bg='#ff9800',
                           fg='white',
                           bd=0,
                           padx=8,
                           pady=2,
                           command=self.minimize_app)
        min_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
    def setup_input_section(self):
        """Setup the todo input section"""
        input_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Todo entry
        self.todo_entry = tk.Entry(input_frame,
                                  font=('Arial', 11),
                                  bg='#404040',
                                  fg='white',
                                  insertbackground='white',
                                  bd=1,
                                  relief='solid')
        self.todo_entry.pack(fill=tk.X, pady=(0, 8))
        self.todo_entry.bind('<Return>', lambda e: self.add_todo())
        
        # Priority and Add button frame
        control_frame = ttk.Frame(input_frame, style='Dark.TFrame')
        control_frame.pack(fill=tk.X)
        
        # Priority selection
        tk.Label(control_frame, 
                text="Priority:", 
                bg='#2c2c2c', 
                fg='white',
                font=('Arial', 9)).pack(side=tk.LEFT)
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = ttk.OptionMenu(control_frame, 
                                      self.priority_var,
                                      "Medium",
                                      "Low", "Medium", "High", "Urgent")
        priority_menu.pack(side=tk.LEFT, padx=(5, 10))
        
        # Add button
        add_btn = tk.Button(control_frame,
                           text="+ Add Todo",
                           font=('Arial', 10, 'bold'),
                           bg='#4caf50',
                           fg='white',
                           bd=0,
                           padx=15,
                           pady=5,
                           command=self.add_todo)
        add_btn.pack(side=tk.RIGHT)
        
    def setup_todo_list(self):
        """Setup the scrollable todo list"""
        # Create frame for todo list with scrollbar
        list_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(list_frame, 
                               bg='#2c2c2c', 
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, 
                                 orient="vertical", 
                                 command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Dark.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
    def setup_footer(self):
        """Setup the footer with statistics"""
        self.footer_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.stats_label = tk.Label(self.footer_frame,
                                   text="",
                                   font=('Arial', 9),
                                   bg='#2c2c2c',
                                   fg='#888888')
        self.stats_label.pack()
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def get_priority_color(self, priority):
        """Get color based on priority"""
        colors = {
            'Low': '#81c784',
            'Medium': '#64b5f6', 
            'High': '#ffb74d',
            'Urgent': '#e57373'
        }
        return colors.get(priority, '#64b5f6')
        
    def add_todo(self):
        """Add a new todo item"""
        text = self.todo_entry.get().strip()
        if not text:
            return
            
        todo = {
            'id': len(self.todos),
            'text': text,
            'priority': self.priority_var.get(),
            'completed': False,
            'created': datetime.now().isoformat()
        }
        
        self.todos.append(todo)
        self.todo_entry.delete(0, tk.END)
        self.refresh_todo_list()
        self.save_todos()
        
    def create_todo_item(self, todo):
        """Create a visual todo item"""
        # Main container for todo item
        item_frame = tk.Frame(self.scrollable_frame,
                             bg='#383838',
                             relief='raised',
                             bd=1)
        item_frame.pack(fill=tk.X, pady=2, padx=5)
        
        # Priority indicator
        priority_color = self.get_priority_color(todo['priority'])
        priority_indicator = tk.Frame(item_frame, 
                                     bg=priority_color, 
                                     width=4)
        priority_indicator.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        
        # Content frame
        content_frame = tk.Frame(item_frame, bg='#383838')
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)
        
        # Checkbox and text
        check_frame = tk.Frame(content_frame, bg='#383838')
        check_frame.pack(fill=tk.X)
        
        # Checkbox
        var = tk.BooleanVar(value=todo['completed'])
        checkbox = tk.Checkbutton(check_frame,
                                 variable=var,
                                 bg='#383838',
                                 fg='white',
                                 selectcolor='#383838',
                                 activebackground='#383838',
                                 command=lambda: self.toggle_todo(todo['id'], var.get()))
        checkbox.pack(side=tk.LEFT)
        
        # Todo text
        text_style = {'font': ('Arial', 10)}
        if todo['completed']:
            text_style.update({'fg': '#888888', 'font': ('Arial', 10, 'overstrike')})
        else:
            text_style.update({'fg': 'white'})
            
        todo_label = tk.Label(check_frame,
                             text=todo['text'],
                             bg='#383838',
                             anchor='w',
                             **text_style)
        todo_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Priority and actions frame
        meta_frame = tk.Frame(content_frame, bg='#383838')
        meta_frame.pack(fill=tk.X, pady=(2, 0))
        
        # Priority label
        priority_label = tk.Label(meta_frame,
                                 text=f"📌 {todo['priority']}",
                                 font=('Arial', 8),
                                 bg='#383838',
                                 fg=priority_color)
        priority_label.pack(side=tk.LEFT)
        
        # Action buttons frame
        actions_frame = tk.Frame(item_frame, bg='#383838')
        actions_frame.pack(side=tk.RIGHT, padx=8, pady=8)
        
        # Edit button
        edit_btn = tk.Button(actions_frame,
                            text="✏️",
                            font=('Arial', 10),
                            bg='#2196f3',
                            fg='white',
                            bd=0,
                            padx=5,
                            pady=2,
                            command=lambda: self.edit_todo(todo['id']))
        edit_btn.pack(side=tk.TOP, pady=(0, 2))
        
        # Delete button
        delete_btn = tk.Button(actions_frame,
                              text="🗑️",
                              font=('Arial', 10),
                              bg='#f44336',
                              fg='white',
                              bd=0,
                              padx=5,
                              pady=2,
                              command=lambda: self.delete_todo(todo['id']))
        delete_btn.pack(side=tk.TOP)
        
    def refresh_todo_list(self):
        """Refresh the todo list display"""
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Sort todos: incomplete first, then by priority
        priority_order = {'Urgent': 4, 'High': 3, 'Medium': 2, 'Low': 1}
        sorted_todos = sorted(self.todos, 
                             key=lambda x: (x['completed'], -priority_order.get(x['priority'], 0)))
        
        # Create todo items
        for todo in sorted_todos:
            self.create_todo_item(todo)
            
        # Update stats
        self.update_stats()
        
    def toggle_todo(self, todo_id, completed):
        """Toggle todo completion status"""
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['completed'] = completed
                break
        self.refresh_todo_list()
        self.save_todos()
        
    def edit_todo(self, todo_id):
        """Edit a todo item"""
        todo = next((t for t in self.todos if t['id'] == todo_id), None)
        if not todo:
            return
            
        new_text = simpledialog.askstring("Edit Todo", 
                                         "Edit todo text:", 
                                         initialvalue=todo['text'])
        if new_text and new_text.strip():
            todo['text'] = new_text.strip()
            self.refresh_todo_list()
            self.save_todos()
            
    def delete_todo(self, todo_id):
        """Delete a todo item"""
        if messagebox.askyesno("Delete Todo", "Are you sure you want to delete this todo?"):
            self.todos = [t for t in self.todos if t['id'] != todo_id]
            self.refresh_todo_list()
            self.save_todos()
            
    def update_stats(self):
        """Update the statistics display"""
        total = len(self.todos)
        completed = sum(1 for t in self.todos if t['completed'])
        pending = total - completed
        
        self.stats_label.config(text=f"Total: {total} | Completed: {completed} | Pending: {pending}")
        
    def save_todos(self):
        """Save todos to file"""
        try:
            config_dir = os.path.expanduser("~/.config/errika")
            os.makedirs(config_dir, exist_ok=True)
            
            with open(os.path.join(config_dir, "todos.json"), 'w') as f:
                json.dump(self.todos, f, indent=2)
        except Exception as e:
            print(f"Error saving todos: {e}")
            
    def load_todos(self):
        """Load todos from file"""
        try:
            config_dir = os.path.expanduser("~/.config/errika")
            todo_file = os.path.join(config_dir, "todos.json")
            
            if os.path.exists(todo_file):
                with open(todo_file, 'r') as f:
                    self.todos = json.load(f)
        except Exception as e:
            print(f"Error loading todos: {e}")
            self.todos = []
            
    def minimize_app(self):
        """Minimize the application"""
        self.root.iconify()
        
    def close_app(self):
        """Close the application"""
        self.save_todos()
        self.root.quit()
        
    def run(self):
        """Run the application"""
        self.refresh_todo_list()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 4)
        self.root.geometry(f'+{x}+{y}')
        
        self.root.mainloop()

def main():
    """Main function"""
    print("🚀 Starting Errika Todo Widget...")
    
    try:
        app = TodoWidget()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Errika Todo Widget closed by user")
    except Exception as e:
        print(f"❌ Error running Errika: {e}")

if __name__ == "__main__":
    main()