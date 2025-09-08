import React, { useState } from 'react';
import { Card, Badge, Form, Button, Row, Col } from 'react-bootstrap';

const TodoList = ({ todos, onUpdateTodo, onDeleteTodo }) => {
  const [showAll, setShowAll] = useState(false);
  const handleToggleComplete = (todo) => {
    onUpdateTodo(todo.id, { completed: !todo.completed });
  };


  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'danger';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'secondary';
    }
  };

  const sortedTodos = [...todos].sort((a, b) => {
    // Sort by completed status first (pending first), then by priority, then by created date
    if (a.completed !== b.completed) {
      return a.completed - b.completed;
    }
    
    const priorityOrder = { high: 3, medium: 2, low: 1 };
    if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    }
    
    return new Date(b.created_at) - new Date(a.created_at);
  });

  if (todos.length === 0) {
    return (
      <Card className="text-center p-4 mt-3">
        <Card.Body>
          <h5 className="text-muted">No tasks yet!</h5>
          <p className="text-muted">Use the AI chat to get started! Try saying:</p>
          <div className="text-start mt-3">
            <small className="text-muted">
              • "Add buy groceries"<br/>
              • "Create workout routine with high priority"<br/>
              • "Remind me to call mom tomorrow"
            </small>
          </div>
        </Card.Body>
      </Card>
    );
  }

  const INITIAL_DISPLAY_COUNT = 3;
  const displayedTodos = showAll ? sortedTodos : sortedTodos.slice(0, INITIAL_DISPLAY_COUNT);
  const hasMoreTodos = sortedTodos.length > INITIAL_DISPLAY_COUNT;

  return (
    <div className="h-100 d-flex flex-column">
      <div className="flex-grow-1 overflow-auto">
        {displayedTodos.map((todo) => (
          <Card 
            key={todo.id} 
            className={`todo-card ${todo.completed ? 'completed' : ''}`}
            style={{ marginBottom: '8px' }}
          >
            <Card.Body className="p-2">
              <Row className="align-items-start">
                <Col xs={1}>
                  <Form.Check
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => handleToggleComplete(todo)}
                    className="mt-1"
                    style={{ transform: 'scale(0.9)' }}
                  />
                </Col>
                
                <Col xs={11}>
                  <h6 
                    className={`mb-1 ${todo.completed ? 'text-decoration-line-through text-muted' : ''}`}
                    style={{ fontSize: '0.95rem' }}
                  >
                    {todo.title}
                  </h6>
                  {todo.description && (
                    <p 
                      className={`small mb-1 ${todo.completed ? 'text-muted' : 'text-secondary'}`}
                      style={{ fontSize: '0.8rem' }}
                    >
                      {todo.description}
                    </p>
                  )}
                  
                  <div className="d-flex gap-1 flex-wrap">
                    <Badge 
                      bg={getPriorityColor(todo.priority)} 
                      className="priority-badge"
                      style={{ fontSize: '0.65rem' }}
                    >
                      {todo.priority.toUpperCase()}
                    </Badge>
                    
                    {todo.due_date && (
                      <Badge bg="info" className="priority-badge" style={{ fontSize: '0.65rem' }}>
                        Due: {formatDate(todo.due_date)}
                      </Badge>
                    )}
                    
                    <Badge bg="light" text="dark" className="priority-badge" style={{ fontSize: '0.65rem' }}>
                      {formatDate(todo.created_at)}
                    </Badge>
                  </div>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        ))}
      </div>
      
      {hasMoreTodos && (
        <div className="text-center mt-2">
          <Button
            variant="outline-primary"
            size="sm"
            onClick={() => setShowAll(!showAll)}
            className="d-flex align-items-center justify-content-center mx-auto"
            style={{ fontSize: '0.8rem' }}
          >
            {showAll ? (
              <>
                <span className="me-1">⬆️</span> Show Less
              </>
            ) : (
              <>
                <span className="me-1">⬇️</span> Show {sortedTodos.length - INITIAL_DISPLAY_COUNT} More
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
};

export default TodoList;
