import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Todo CRUD operations
export const getTodos = async () => {
  try {
    const response = await api.get('/todos');
    return response.data;
  } catch (error) {
    console.error('Error fetching todos:', error);
    throw error;
  }
};

export const createTodo = async (todoData) => {
  try {
    const response = await api.post('/todos', todoData);
    return response.data;
  } catch (error) {
    console.error('Error creating todo:', error);
    throw error;
  }
};

export const updateTodo = async (id, updates) => {
  try {
    const response = await api.put(`/todos/${id}`, updates);
    return response.data;
  } catch (error) {
    console.error('Error updating todo:', error);
    throw error;
  }
};

export const deleteTodo = async (id) => {
  try {
    await api.delete(`/todos/${id}`);
  } catch (error) {
    console.error('Error deleting todo:', error);
    throw error;
  }
};

// AI Chat
export const sendChatMessage = async (message) => {
  try {
    const response = await api.post('/chat', { message });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

const todoService = {
  getTodos,
  createTodo,
  updateTodo,
  deleteTodo,
  sendChatMessage,
};

export default todoService;
