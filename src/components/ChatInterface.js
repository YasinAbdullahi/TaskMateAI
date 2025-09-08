import React, { useState, useRef, useEffect } from 'react';
import { Form, Button, Alert, Badge, Card } from 'react-bootstrap';
import { sendChatMessage } from '../services/todoService';

const ChatInterface = ({ onAction }) => {
  const [messages, setMessages] = useState([
        {
          id: 1,
          type: 'ai',
          content: "Hi! I'm your AI assistant. I can help you manage your todos using natural language. You can now complete tasks by name! Try:\n\n• \"Add buy groceries to my list\"\n• \"Complete groceries\" (no need for task numbers!)\n• \"Finish workout routine\"\n• \"Delete meeting task\"\n• \"Show me all high priority tasks\"\n\nJust tell me what you want to do!",
          timestamp: new Date()
        }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);
    setError('');

    try {
      const response = await sendChatMessage(userMessage.content);
      
      // Create AI response message
      let aiMessageContent = '';
      let actionResult = null;

      if (response.ai_response) {
        switch (response.ai_response.action) {
          case 'create':
            if (response.result) {
              aiMessageContent = `✅ I've added "${response.result.title}" to your todo list with ${response.result.priority} priority.`;
              actionResult = { type: 'create', data: response.result };
            } else {
              aiMessageContent = "I understood you want to create a task, but there was an issue. Could you try rephrasing your request?";
            }
            break;
            
          case 'update':
            if (response.result) {
              aiMessageContent = `✅ I've updated "${response.result.title}". `;
              if (response.ai_response.completed !== undefined) {
                aiMessageContent += response.ai_response.completed ? 
                  "It's now marked as completed! 🎉" : 
                  "It's now marked as pending.";
              }
              actionResult = { type: 'update', data: response.result };
            } else {
              aiMessageContent = "I couldn't find that task to update. Could you be more specific?";
            }
            break;
            
          case 'delete':
            if (response.result?.deleted) {
              aiMessageContent = `🗑️ I've deleted the task for you.`;
              actionResult = { type: 'delete', data: response.result };
            } else {
              aiMessageContent = "I couldn't find that task to delete. Could you specify which task you'd like to remove?";
            }
            break;
            
          case 'list':
            if (response.result && response.result.length > 0) {
              const filter = response.ai_response.filter || 'all';
              aiMessageContent = `Here are your ${filter} tasks:\n\n`;
              response.result.forEach((todo, index) => {
                const status = todo.completed ? '✅' : '⏳';
                const priority = todo.priority === 'high' ? '🔴' : todo.priority === 'medium' ? '🟡' : '🟢';
                aiMessageContent += `${status} ${priority} ${todo.title}\n`;
              });
              actionResult = { type: 'list', data: response.result };
            } else {
              const filter = response.ai_response.filter || 'all';
              aiMessageContent = `You don't have any ${filter === 'all' ? '' : filter + ' '}tasks yet.`;
            }
            break;
            
          case 'response':
          default:
            aiMessageContent = response.ai_response.message || "I'm here to help you manage your todos! What would you like to do?";
            break;
        }
      } else {
        aiMessageContent = "I had trouble understanding that. Could you try rephrasing your request?";
      }

      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: aiMessageContent,
        timestamp: new Date(),
        actionResult
      };

      setMessages(prev => [...prev, aiMessage]);
      
      // Notify parent component about the action
      if (actionResult && onAction) {
        onAction(actionResult);
      }

    } catch (err) {
      console.error('Chat error:', err);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: "Sorry, I'm having trouble connecting right now. Please check that the backend server is running and try again.",
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
      setError('Failed to send message. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const clearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'ai',
        content: "Chat cleared! How can I help you with your todos?",
        timestamp: new Date()
      }
    ]);
  };

  return (
    <div className="h-100 d-flex flex-column">
      {/* Chat Header */}
      <div className="d-flex justify-content-between align-items-center p-3 pb-2">
        <div>
          <Badge bg="success" className="me-2">🤖 AI Assistant</Badge>
          <small className="text-muted">Online</small>
        </div>
        <Button variant="outline-secondary" size="sm" onClick={clearChat}>
          Clear Chat
        </Button>
      </div>

      {/* Unified Chat Container */}
      <div className="flex-grow-1 d-flex flex-column bg-white rounded" style={{ 
        border: '1px solid #e9ecef',
        height: '470px'
      }}>
        {/* Messages Area */}
        <div className="flex-grow-1 p-2 overflow-auto">
          {error && (
            <Alert variant="danger" dismissible onClose={() => setError('')} className="mb-3">
              {error}
            </Alert>
          )}

          {messages.map((message) => (
            <div key={message.id} className="mb-3">
              <div 
                className={`chat-message ${message.type} ${message.isError ? 'border border-danger' : ''}`}
              >
                <div style={{ whiteSpace: 'pre-line' }}>
                  {message.content}
                </div>
                <div className="mt-1">
                  <small className="opacity-75">
                    {formatTimestamp(message.timestamp)}
                  </small>
                </div>
              </div>
            </div>
          ))}
          
          {loading && (
            <div className="text-center mb-3">
              <div className="spinner-border spinner-border-sm text-primary" role="status">
                <span className="visually-hidden">AI is thinking...</span>
              </div>
              <small className="text-muted ms-2">AI is thinking...</small>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area - Integrated */}
        <div className="p-2 border-top">
          <Form onSubmit={handleSubmit}>
            <div className="input-group">
              <Form.Control
                type="text"
                placeholder="Type your message..."
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                disabled={loading}
                style={{ 
                  border: '1px solid #dee2e6',
                  fontSize: '0.95rem',
                  borderRadius: '20px 0 0 20px'
                }}
              />
              <Button
                type="submit"
                className="btn-gradient"
                disabled={loading || !inputMessage.trim()}
                style={{ 
                  border: 'none',
                  fontSize: '0.95rem',
                  fontWeight: '600',
                  borderRadius: '0 20px 20px 0'
                }}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                    ...
                  </>
                ) : (
                  <>
                    Send
                  </>
                )}
              </Button>
            </div>
          </Form>
        </div>
      </div>

      {/* Compact Tips Section */}
      <div className="mt-2">
        <div className="bg-light rounded px-3 py-1 border d-flex justify-content-center align-items-center" style={{ fontSize: '0.75rem', minHeight: '35px' }}>
          <span className="text-muted me-3">💡 <strong>Try:</strong></span>
          <span className="text-primary me-2">"Add groceries"</span>
          <span className="text-muted me-2">•</span>
          <span className="text-success">"Complete task"</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
