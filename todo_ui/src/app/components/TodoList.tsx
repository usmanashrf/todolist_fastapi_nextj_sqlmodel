'use client';
import { useState, useEffect } from 'react';

function TodoList() {
  const [todos, setTodos] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newTask, setNewTask] = useState('');
  const [isTaskDone, setIsTaskDone] = useState(false);

  useEffect(() => {
    fetchTodos();
  }, []);

  async function fetchTodos() {
    const response = await fetch('http://127.0.0.1:8000/todos/');
    const data = await response.json();
    setTodos(data);
  }

  async function createTodo() {
    const newTodo = { task: newTask, is_done: isTaskDone };
    const response = await fetch('http://127.0.0.1:8000/todos/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTodo),
    });
    fetchTodos();
    setShowForm(false);
  }

  async function completeTodo(todoId:any) {
    const response = await fetch(`http://127.0.0.1:8000/todos/${todoId}/complete`, {
      method: 'PUT',
    });
    fetchTodos();
  }

  async function deleteTodo(todoId:any) {
    const response = await fetch(`http://127.0.0.1:8000/todos/${todoId}`, {
      method: 'DELETE',
    });
    fetchTodos();
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-md rounded-lg">
      <h1 className="text-2xl font-semibold mb-4">Todo List</h1>
      <button
        className="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        onClick={() => setShowForm(!showForm)}
      >
        Add New Task
      </button>
      {showForm && (
        <div className="mb-4">
          <input
            className="px-4 py-2 border rounded w-full"
            type="text"
            placeholder="Task name"
            value={newTask}
            onChange={(e) => setNewTask(e.target.value)}
          />
          <div className="flex items-center my-2">
            <input
              type="radio"
              id="isDone"
              name="isDone"
              checked={isTaskDone}
              onChange={() => setIsTaskDone(!isTaskDone)}
            />
            <label htmlFor="isDone" className="ml-2">
              Is Done
            </label>
          </div>
          <button
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
            onClick={createTodo}
          >
            Submit
          </button>
        </div>
      )}
      <ul>
        {todos.map((todo:any ) => (
          <li key={todo.id} className="border-b px-4 py-2">
            {todo.task} - {todo.is_done ? 'Completed' : 'Incomplete'}
            <button
              className="ml-2 px-2 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition"
              onClick={() => completeTodo(todo.id)}
            >
              Complete
            </button>
            <button
              className="ml-2 px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition"
              onClick={() => deleteTodo(todo.id)}
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoList;
