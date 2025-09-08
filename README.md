# 🚀 TaskMateAI - Intelligent Task Companion

**TaskMateAI** is a modern, user-friendly to-do list application powered by AI that enables natural language interactions for seamless task management. Built with React.js, Python Flask, and Anthropic Claude API.

## ✨ Features

- 🤖 **AI-Powered Chat Interface** - Interact with your tasks using natural language
- 📝 **Smart Task Management** - Create, complete, and delete tasks by simply talking to the AI
- 🎯 **Intelligent Task Matching** - Advanced matching algorithm for precise task completion
- 📊 **Priority System** - Organize tasks with High, Medium, and Low priorities
- 🎨 **Modern UI Design** - Beautiful glassmorphism design with responsive layout
- 💬 **Real-time Responses** - Instant AI feedback and task updates
- 🔍 **Smart Task Search** - Find and manage tasks by name, not just ID numbers
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices

## 🗣️ Natural Language Examples

```
✨ Creating Tasks:
• "Add buy groceries to my list"
• "Create workout plan"
• "Remind me to call mom"
• "Add urgent meeting with high priority"

🔧 Managing Tasks:
• "Complete groceries" (matches by name!)
• "Finish workout routine"
• "Delete meeting task"
• "Show me all pending tasks"
```

## 🛠️ Tech Stack

**Frontend:**
- React.js 18
- Bootstrap 5
- Axios for API calls
- Modern CSS with glassmorphism effects

**Backend:**
- Python Flask
- SQLAlchemy (SQLite database)
- Anthropic Claude API for natural language processing
- Rule-based parsing with AI fallback

**Features:**
- CORS enabled for cross-origin requests
- Environment variable configuration
- Robust error handling
- RESTful API design

## 🚀 Quick Start

### Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- Anthropic API key (optional, works with rule-based parsing)

### Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd TorpedoPrj
```

2. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

3. **Install Node.js dependencies:**
```bash
npm install
```

4. **Set up environment variables:**
```bash
cp env.example .env
# Edit .env file and add your ANTHROPIC_API_KEY (optional)
```

5. **Initialize database with sample data (optional):**
```bash
python3 demo_setup.py
```

### 🎯 Running the Application

**Option 1: Use the convenient startup script**
```bash
chmod +x start.sh
./start.sh
```

**Option 2: Manual startup**

Terminal 1 (Backend):
```bash
python3 app.py
```

Terminal 2 (Frontend):
```bash
npm start
```

The application will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5001

## 📁 Project Structure

```
TorpedoPrj/
├── 📁 src/
│   ├── 📁 components/
│   │   ├── TodoList.js          # Task list with show more functionality
│   │   └── ChatInterface.js     # AI chat interface
│   ├── 📁 services/
│   │   └── todoService.js       # API communication
│   ├── App.js                   # Main React component
│   ├── index.js                 # React entry point
│   └── index.css               # Global styles with light green theme
├── 📁 public/
│   ├── index.html              # HTML template
│   └── manifest.json           # PWA manifest
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── package.json               # Node.js dependencies
├── demo_setup.py              # Database initialization script
├── start.sh                   # Convenient startup script
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🤖 AI Processing System

TaskMateAI uses a sophisticated **hybrid approach** for natural language processing:

### 1. Rule-Based Parser (Primary)
- Fast, reliable, and works offline
- Handles common task management patterns
- Smart task matching with 4-tier algorithm:
  1. **Exact Match** - Perfect title match
  2. **Substring Match** - Partial title matching
  3. **Word Match** - All significant words present
  4. **Fallback Match** - Minimum word threshold

### 2. Claude API Fallback (Optional)
- Advanced natural language understanding
- Handles complex or ambiguous requests
- JSON-structured responses for consistent parsing

## 📚 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/todos` | Get all tasks |
| `POST` | `/api/todos` | Create new task |
| `PUT` | `/api/todos/:id` | Update specific task |
| `DELETE` | `/api/todos/:id` | Delete specific task |
| `POST` | `/api/chat` | AI chat interaction |

## 🎨 UI Features

- **Glassmorphism Design** - Modern, translucent card effects
- **Light Green Theme** - Calming gradient background
- **Responsive Layout** - Equal-sized task and chat sections
- **Show More Functionality** - Expandable task list for better organization
- **Real-time Updates** - Instant UI updates after AI interactions
- **Compact Quick Commands** - Helpful command examples
- **Status Badges** - Visual priority and completion indicators

## 🛡️ Error Handling

- Graceful API fallbacks when services are unavailable
- User-friendly error messages
- Robust task matching to prevent incorrect operations
- Input validation and sanitization

## 🔧 Configuration

### Environment Variables

```bash
# .env file
ANTHROPIC_API_KEY=your_api_key_here  # Optional
SECRET_KEY=your_secret_key_here      # Optional (dev-secret-key used by default)
```

### Customization

- **Colors:** Modify `src/index.css` for theme changes
- **AI Responses:** Update `app.py` rule-based patterns
- **UI Layout:** Adjust `src/App.js` component structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic Claude** for advanced natural language processing
- **React.js** for the dynamic frontend framework
- **Flask** for the lightweight backend API
- **Bootstrap** for responsive UI components

---

**Built with ❤️ by Yasin

*Transforming task management through the power of AI and natural language interaction.*
