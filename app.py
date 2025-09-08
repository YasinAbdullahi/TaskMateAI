import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# OpenAI API key will be loaded from environment variables

# Todo Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    due_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# AI Assistant for natural language processing
class AIAssistant:
    @staticmethod
    def process_natural_language(user_input, existing_todos):
        """
        Process natural language input using a rule-based approach
        This is more reliable than API calls and works offline
        """
        user_input = user_input.lower().strip()
        
        # Try rule-based processing first
        try:
            result = AIAssistant._rule_based_parser(user_input, existing_todos)
            if result:
                return result
        except Exception as e:
            print(f"Rule-based parsing error: {e}")
        
        # Fallback to Claude API if available and rule-based fails
        try:
            return AIAssistant._claude_fallback(user_input, existing_todos)
        except Exception as e:
            print(f"Claude API fallback error: {e}")
            return {
                "action": "response", 
                "message": f"I understood '{user_input}' but couldn't process it fully. Try phrases like:\n• 'add [task name]'\n• 'complete task [number]'\n• 'show tasks'\n• 'delete task [number]'\n• 'add [task] with high priority'"
            }
    
    @staticmethod
    def _rule_based_parser(user_input, existing_todos):
        """Enhanced rule-based natural language parser"""
        
        # CREATE todo patterns
        create_patterns = [
            'add ', 'create ', 'new ', 'make ', 'todo ', 'task ', 'remind me to ', 'i need to '
        ]
        
        # UPDATE/COMPLETE patterns
        complete_patterns = [
            'complete ', 'finish ', 'done ', 'mark ', 'check off ', 'finished '
        ]
        
        # DELETE patterns
        delete_patterns = [
            'delete ', 'remove ', 'cancel ', 'erase ', 'get rid of '
        ]
        
        # LIST/SHOW patterns
        list_patterns = [
            'show ', 'list ', 'display ', 'what ', 'see ', 'view ', 'get '
        ]
        
        # PRIORITY patterns
        priority_words = {
            'high': ['urgent', 'important', 'critical', 'asap', 'priority', 'high'],
            'medium': ['normal', 'medium', 'regular', 'standard'],
            'low': ['low', 'later', 'someday', 'eventually', 'when possible']
        }
        
        # Extract priority from input
        detected_priority = 'medium'  # default
        for priority, keywords in priority_words.items():
            if any(keyword in user_input for keyword in keywords):
                detected_priority = priority
                break
        
        # Check if this is a complete/update command first (higher priority)
        is_complete_command = any(pattern in user_input for pattern in complete_patterns)
        is_delete_command = any(pattern in user_input for pattern in delete_patterns)
        is_list_command = any(pattern in user_input for pattern in list_patterns)
        
        # CREATE TODO (only if not a complete/delete/list command)
        if not (is_complete_command or is_delete_command or is_list_command):
            for pattern in create_patterns:
                if pattern in user_input:
                    # Extract title after the pattern
                    title_start = user_input.find(pattern) + len(pattern)
                    title = user_input[title_start:].strip()
                    
                    # Clean up common words
                    title = title.replace(' to my list', '').replace(' to the list', '')
                    title = title.replace(' with high priority', '').replace(' with low priority', '')
                    title = title.replace(' with medium priority', '')
                    
                    if title:
                        return {
                            "action": "create",
                            "title": title.capitalize(),
                            "description": "",
                            "priority": detected_priority
                        }
        
        # COMPLETE/UPDATE TODO
        for pattern in complete_patterns:
            if pattern in user_input:
                # Look for task number or reference
                import re
                
                # Extract task ID (e.g., "task 1", "first task", "task number 2")
                task_match = re.search(r'task (\d+)', user_input)
                number_match = re.search(r'\b(\d+)\b', user_input)
                
                task_id = None
                
                # First try to match by ID/number
                if task_match:
                    task_id = int(task_match.group(1))
                elif number_match:
                    task_id = int(number_match.group(1))
                elif 'first' in user_input and existing_todos:
                    task_id = existing_todos[0]['id']
                elif 'last' in user_input and existing_todos:
                    task_id = existing_todos[-1]['id']
                
                # If no ID found, try to match by task title/name
                if not task_id and existing_todos:
                    # Remove the completion pattern from the input to get the task name
                    task_name_part = user_input.replace(pattern, '').strip()
                    
                    # Remove common words
                    task_name_part = task_name_part.replace('the ', '').replace('my ', '').replace('task ', '')
                    task_name_part = task_name_part.replace('called ', '').replace('named ', '').replace('about ', '')
                    
                    # Find matching task by title with improved matching logic
                    incomplete_todos = [todo for todo in existing_todos if not todo['completed']]
                    
                    # First pass: Look for exact match (case insensitive)
                    for todo in incomplete_todos:
                        todo_title = todo['title'].lower()
                        if task_name_part.lower() == todo_title:
                            task_id = todo['id']
                            break
                    
                    # Second pass: Look for exact substring match
                    if not task_id:
                        for todo in incomplete_todos:
                            todo_title = todo['title'].lower()
                            if task_name_part.lower() in todo_title:
                                task_id = todo['id']
                                break
                    
                    # Third pass: Look for word-by-word match (all words must be present)
                    if not task_id:
                        task_words = [word for word in task_name_part.lower().split() if len(word) > 2]
                        if task_words:
                            for todo in incomplete_todos:
                                todo_title = todo['title'].lower()
                                # Check if ALL significant words are present in the title
                                if all(word in todo_title for word in task_words):
                                    task_id = todo['id']
                                    break
                    
                    # Fourth pass: Fallback to partial word match (at least 2 words match)
                    if not task_id and len(task_words) >= 2:
                        for todo in incomplete_todos:
                            todo_title = todo['title'].lower()
                            matching_words = sum(1 for word in task_words if word in todo_title)
                            if matching_words >= min(2, len(task_words)):
                                task_id = todo['id']
                                break
                
                if task_id:
                    return {
                        "action": "update",
                        "id": task_id,
                        "completed": True
                    }
        
        # DELETE TODO
        for pattern in delete_patterns:
            if pattern in user_input:
                import re
                
                # Extract task ID
                task_match = re.search(r'task (\d+)', user_input)
                number_match = re.search(r'\b(\d+)\b', user_input)
                
                task_id = None
                
                # First try to match by ID/number
                if task_match:
                    task_id = int(task_match.group(1))
                elif number_match:
                    task_id = int(number_match.group(1))
                elif 'first' in user_input and existing_todos:
                    task_id = existing_todos[0]['id']
                elif 'last' in user_input and existing_todos:
                    task_id = existing_todos[-1]['id']
                
                # If no ID found, try to match by task title/name
                if not task_id and existing_todos:
                    # Remove the delete pattern from the input to get the task name
                    task_name_part = user_input.replace(pattern, '').strip()
                    
                    # Remove common words
                    task_name_part = task_name_part.replace('the ', '').replace('my ', '').replace('task ', '')
                    task_name_part = task_name_part.replace('called ', '').replace('named ', '').replace('about ', '')
                    
                    # Find matching task by title with improved matching logic
                    # First pass: Look for exact match (case insensitive)
                    for todo in existing_todos:
                        todo_title = todo['title'].lower()
                        if task_name_part.lower() == todo_title:
                            task_id = todo['id']
                            break
                    
                    # Second pass: Look for exact substring match
                    if not task_id:
                        for todo in existing_todos:
                            todo_title = todo['title'].lower()
                            if task_name_part.lower() in todo_title:
                                task_id = todo['id']
                                break
                    
                    # Third pass: Look for word-by-word match (all words must be present)
                    if not task_id:
                        task_words = [word for word in task_name_part.lower().split() if len(word) > 2]
                        if task_words:
                            for todo in existing_todos:
                                todo_title = todo['title'].lower()
                                # Check if ALL significant words are present in the title
                                if all(word in todo_title for word in task_words):
                                    task_id = todo['id']
                                    break
                    
                    # Fourth pass: Fallback to partial word match (at least 2 words match)
                    if not task_id and len(task_words) >= 2:
                        for todo in existing_todos:
                            todo_title = todo['title'].lower()
                            matching_words = sum(1 for word in task_words if word in todo_title)
                            if matching_words >= min(2, len(task_words)):
                                task_id = todo['id']
                                break
                
                if task_id:
                    return {
                        "action": "delete",
                        "id": task_id
                    }
        
        # LIST/SHOW TODO
        for pattern in list_patterns:
            if pattern in user_input:
                filter_type = "all"
                
                if any(word in user_input for word in ['pending', 'incomplete', 'unfinished', 'not done']):
                    filter_type = "pending"
                elif any(word in user_input for word in ['completed', 'finished', 'done']):
                    filter_type = "completed"
                elif any(word in user_input for word in ['high priority', 'urgent', 'important']):
                    filter_type = "all"
                
                return {
                    "action": "list",
                    "filter": filter_type
                }
        
        # GREETINGS AND HELP
        greetings = ['hello', 'hi', 'hey', 'help', 'what can you do']
        if any(greeting in user_input for greeting in greetings):
            return {
                "action": "response",
                "message": "Hello! I can help you manage your todos. Try saying:\n• 'Add buy groceries'\n• 'Complete task 1'\n• 'Show all tasks'\n• 'Delete task 2'\n• 'Add urgent meeting with high priority'"
            }
        
        # If no pattern matches, return None to try fallback
        return None
    
    @staticmethod
    def _claude_fallback(user_input, existing_todos):
        """Use Anthropic Claude API for natural language processing"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            
            # Create context about existing todos
            todos_context = "\n".join([
                f"- {todo['title']} (ID: {todo['id']}, Status: {'Completed' if todo['completed'] else 'Pending'}, Priority: {todo['priority']})"
                for todo in existing_todos[:5]  # Limit context to avoid token limits
            ])
            
            prompt = f"""You are a todo list assistant. Parse the user's request and respond with ONLY valid JSON.

Current todos:
{todos_context if todos_context else "No existing todos"}

For the user request: "{user_input}"

Return JSON in one of these formats:

1. CREATE todo:
{{"action": "create", "title": "task title", "description": "optional description", "priority": "low|medium|high"}}

2. UPDATE/COMPLETE todo:
{{"action": "update", "id": task_number, "completed": true}}

3. DELETE todo:
{{"action": "delete", "id": task_number}}

4. LIST todos:
{{"action": "list", "filter": "all|pending|completed"}}

5. GENERAL response:
{{"action": "response", "message": "helpful message"}}

Examples:
- "add buy milk" → {{"action": "create", "title": "Buy milk", "priority": "medium"}}
- "complete task 1" → {{"action": "update", "id": 1, "completed": true}}
- "delete first task" → {{"action": "delete", "id": {existing_todos[0]['id'] if existing_todos else 1}}}
- "show all tasks" → {{"action": "list", "filter": "all"}}

RESPOND WITH ONLY JSON - NO OTHER TEXT."""

            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.1,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text.strip()
            print(f"Claude response: {response_text}")  # Debug log
            
            # Parse JSON response
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as je:
                print(f"Claude JSON parse error: {je}")
                print(f"Raw Claude response: {response_text}")
                
                # Try to extract JSON from the response if it's wrapped in other text
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group())
                    except:
                        pass
                
                # Fallback response
                return {
                    "action": "response", 
                    "message": f"I understood '{user_input}' but had trouble processing it. Please try rephrasing your request."
                }
                
        except Exception as e:
            print(f"Claude API error: {e}")
            raise  # Re-raise to trigger graceful fallback
    

# API Routes

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    
    todo = Todo(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium'),
        due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
    )
    
    db.session.add(todo)
    db.session.commit()
    
    return jsonify(todo.to_dict()), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    
    if 'title' in data:
        todo.title = data['title']
    if 'description' in data:
        todo.description = data['description']
    if 'completed' in data:
        todo.completed = data['completed']
    if 'priority' in data:
        todo.priority = data['priority']
    if 'due_date' in data:
        todo.due_date = datetime.fromisoformat(data['due_date']) if data['due_date'] else None
    
    todo.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(todo.to_dict())

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    
    return '', 204

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    data = request.get_json()
    user_input = data.get('message', '')
    
    # Get current todos for context
    todos = Todo.query.all()
    todos_data = [todo.to_dict() for todo in todos]
    
    # Process with AI
    ai_response = AIAssistant.process_natural_language(user_input, todos_data)
    
    # Execute the action
    result = None
    if ai_response['action'] == 'create':
        todo = Todo(
            title=ai_response['title'],
            description=ai_response.get('description', ''),
            priority=ai_response.get('priority', 'medium'),
            due_date=datetime.fromisoformat(ai_response['due_date']) if ai_response.get('due_date') else None
        )
        db.session.add(todo)
        db.session.commit()
        result = todo.to_dict()
        
    elif ai_response['action'] == 'update':
        todo = Todo.query.get(ai_response['id'])
        if todo:
            if 'title' in ai_response:
                todo.title = ai_response['title']
            if 'description' in ai_response:
                todo.description = ai_response['description']
            if 'completed' in ai_response:
                todo.completed = ai_response['completed']
            if 'priority' in ai_response:
                todo.priority = ai_response['priority']
            if 'due_date' in ai_response:
                todo.due_date = datetime.fromisoformat(ai_response['due_date']) if ai_response['due_date'] else None
            
            todo.updated_at = datetime.utcnow()
            db.session.commit()
            result = todo.to_dict()
        
    elif ai_response['action'] == 'delete':
        todo = Todo.query.get(ai_response['id'])
        if todo:
            db.session.delete(todo)
            db.session.commit()
            result = {'deleted': True, 'id': ai_response['id']}
    
    elif ai_response['action'] == 'list':
        query = Todo.query
        if ai_response.get('filter') == 'completed':
            query = query.filter_by(completed=True)
        elif ai_response.get('filter') == 'pending':
            query = query.filter_by(completed=False)
        
        todos = query.all()
        result = [todo.to_dict() for todo in todos]
    
    return jsonify({
        'ai_response': ai_response,
        'result': result
    })

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
