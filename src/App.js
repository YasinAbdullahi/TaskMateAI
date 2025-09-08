import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Badge } from 'react-bootstrap';
import TodoList from './components/TodoList';
import ChatInterface from './components/ChatInterface';
import * as todoService from './services/todoService';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      const data = await todoService.getTodos();
      setTodos(data);
    } catch (error) {
      console.error('Error loading todos:', error);
    } finally {
      setLoading(false);
    }
  };


  const handleUpdateTodo = async (id, updates) => {
    try {
      const updatedTodo = await todoService.updateTodo(id, updates);
      setTodos(todos.map(todo => todo.id === id ? updatedTodo : todo));
      return updatedTodo;
    } catch (error) {
      console.error('Error updating todo:', error);
      throw error;
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await todoService.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
      throw error;
    }
  };

  const handleChatAction = (result) => {
    // Refresh todos after chat actions
    loadTodos();
  };

  if (loading) {
    return (
      <Container className="app-container d-flex justify-content-center align-items-center">
        <div className="text-center text-white">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading your todos...</p>
        </div>
      </Container>
    );
  }

  return (
    <Container className="app-container">
      {/* Brand Header */}
      <Card className="main-header text-center py-3 px-4 mb-4">
        <div className="d-flex align-items-center justify-content-center gap-3">
          <div className="d-flex align-items-center gap-2">
            <div className="position-relative">
              <span style={{fontSize: '2rem'}}>🚀</span>
              <span 
                style={{
                  position: 'absolute',
                  top: '-5px',
                  right: '-5px',
                  fontSize: '0.8rem'
                }}
              >
                ✨
              </span>
            </div>
            <div className="text-start">
              <h2 className="mb-0 fw-bold" style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text'
              }}>
                TaskMateAI
              </h2>
              <small className="text-muted fw-medium">
                Your intelligent task companion
              </small>
            </div>
          </div>
        </div>
      </Card>

      <Row className="g-4">
        {/* Left Column - Todo List */}
        <Col lg={6} className="d-flex">
          <Card className="glass-card w-100 d-flex flex-column">
            <Card.Header className="bg-transparent border-0 text-center py-3">
              <div className="d-flex align-items-center justify-content-center gap-2 mb-2">
                <span style={{fontSize: '1.2rem'}}>📝</span>
                <h5 className="mb-0 fw-bold text-primary">Your Tasks</h5>
              </div>
              <div className="d-flex justify-content-center gap-3">
                <Badge bg="primary" className="px-2 py-1">
                  {todos.length} Total
                </Badge>
                <Badge bg="warning" className="px-2 py-1">
                  {todos.filter(t => !t.completed).length} Pending
                </Badge>
                <Badge bg="success" className="px-2 py-1">
                  {todos.filter(t => t.completed).length} Done
                </Badge>
              </div>
            </Card.Header>
            <Card.Body className="flex-grow-1 d-flex flex-column p-3">
              <div className="flex-grow-1" style={{ minHeight: '550px', maxHeight: '550px' }}>
                <TodoList
                  todos={todos}
                  onUpdateTodo={handleUpdateTodo}
                  onDeleteTodo={handleDeleteTodo}
                />
              </div>
            </Card.Body>
          </Card>
        </Col>

        {/* Right Column - AI Chat */}
        <Col lg={6} className="d-flex">
          <Card className="glass-card w-100 d-flex flex-column">
            <Card.Header className="bg-transparent border-0 text-center py-3">
              <div className="d-flex align-items-center justify-content-center gap-2 mb-2">
                <span style={{fontSize: '1.2rem'}}>🤖</span>
                <h5 className="mb-0 fw-bold text-primary">AI Assistant</h5>
              </div>
              <div className="d-flex justify-content-center gap-2">
                <Badge bg="success" className="px-2 py-1">
                  <span className="me-1">🟢</span>Online
                </Badge>
                <Badge bg="info" className="px-2 py-1">
                  <span className="me-1">⚡</span>Instant Response
                </Badge>
              </div>
            </Card.Header>
            <Card.Body className="flex-grow-1 d-flex flex-column p-3">
              <div className="flex-grow-1" style={{ minHeight: '550px', maxHeight: '550px' }}>
                <ChatInterface onAction={handleChatAction} />
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Stats Footer */}
      <Card className="glass-card mt-4">
        <Card.Body className="text-center">
          <Row>
            <Col md={4}>
              <h5 className="text-primary">{todos.length}</h5>
              <small className="text-muted">Total Tasks</small>
            </Col>
            <Col md={4}>
              <h5 className="text-success">{todos.filter(t => t.completed).length}</h5>
              <small className="text-muted">Completed</small>
            </Col>
            <Col md={4}>
              <h5 className="text-warning">{todos.filter(t => !t.completed).length}</h5>
              <small className="text-muted">Pending</small>
            </Col>
          </Row>
        </Card.Body>
      </Card>
    </Container>
  );
}

export default App;
