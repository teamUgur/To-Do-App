import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {

  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchItems();
  }, []);

  // Function to fetch all items from the backend
  const fetchItems = async () => {
    try {
      const response = await axios.get(`${API_BASE}/items/`);
      setItems(response.data);
    } catch (error) {
      console.error("Error fetching items:", error);
    }
  }

  const createItem = async () => {
    try {
      const response = await axios.post(`${API_BASE}/items/`, {
        name, 
        description
      });
      setItems([...items, response.data]);
      setName('');
      setDescription('');
    } catch (error) {
      console.error("Error posting items", error);
    }
  }

  const editItem = async () => {
    try {
      const response = await axios.put(`${API_BASE}/items/${editingId}`,
        name,
        description
      );
      setItems(items.map(item => item.id === editingId ? response.data : item));
      setEditingId(null);
      setName('');
      setDescription('');
    } catch (error) {
      console.error("Error editing items", error);
    }
  }

  const deleteItem = async (id) => {
    try {
      const response = await axios.delete(`${API_BASE}/items/${id}`);
      setItems(items.filter(item => item.id !== id));
    } catch (error) {
      console.error("Error deleting items", error);
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
