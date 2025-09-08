#!/usr/bin/env python3
"""
Demo setup script for AI-Powered Todo List
Creates sample todos for testing the application
"""

import sys
import os
from datetime import datetime, timedelta

# Add the current directory to the path so we can import our app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Todo

def create_sample_todos():
    """Create sample todos for demonstration"""
    
    sample_todos = [
        {
            'title': 'Buy groceries',
            'description': 'Get milk, eggs, bread, and fruits from the store',
            'priority': 'high',
            'due_date': datetime.now() + timedelta(days=1)
        },
        {
            'title': 'Finish project report',
            'description': 'Complete the quarterly analysis report for the team meeting',
            'priority': 'high',
            'due_date': datetime.now() + timedelta(days=3)
        },
        {
            'title': 'Call dentist',
            'description': 'Schedule annual dental checkup appointment',
            'priority': 'medium',
            'due_date': datetime.now() + timedelta(days=7)
        },
        {
            'title': 'Exercise',
            'description': '30 minutes of cardio workout',
            'priority': 'medium',
            'completed': False
        },
        {
            'title': 'Read book',
            'description': 'Continue reading "The Pragmatic Programmer"',
            'priority': 'low',
            'completed': False
        },
        {
            'title': 'Water plants',
            'description': 'Water all the indoor plants',
            'priority': 'low',
            'completed': True
        },
        {
            'title': 'Update resume',
            'description': 'Add recent project experience and skills',
            'priority': 'medium',
            'due_date': datetime.now() + timedelta(days=14)
        }
    ]
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if we already have todos
        existing_todos = Todo.query.count()
        if existing_todos > 0:
            print(f"Database already has {existing_todos} todos.")
            response = input("Do you want to add sample todos anyway? (y/N): ")
            if response.lower() != 'y':
                print("Demo setup cancelled.")
                return
        
        print("Creating sample todos...")
        
        for todo_data in sample_todos:
            todo = Todo(
                title=todo_data['title'],
                description=todo_data['description'],
                priority=todo_data['priority'],
                completed=todo_data.get('completed', False),
                due_date=todo_data.get('due_date')
            )
            db.session.add(todo)
        
        db.session.commit()
        print(f"✅ Created {len(sample_todos)} sample todos!")
        
        # Display the created todos
        print("\n📋 Sample todos created:")
        todos = Todo.query.all()
        for i, todo in enumerate(todos, 1):
            status = "✅" if todo.completed else "⏳"
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            print(f"{i}. {status} {priority_emoji[todo.priority]} {todo.title}")
        
        print(f"\n🎉 Demo setup complete! You now have {len(todos)} todos in your database.")
        print("🚀 Start the application with: python app.py")
        print("💬 Try these AI commands:")
        print("   - 'Show me all high priority tasks'")
        print("   - 'Mark the first task as completed'")
        print("   - 'Add walk the dog to my list'")
        print("   - 'What tasks are due this week?'")

if __name__ == '__main__':
    create_sample_todos()
