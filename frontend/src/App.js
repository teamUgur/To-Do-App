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
      const response = await axios.put(`${API_BASE}/items/${editingId}`, {
        name,
        description
      });
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
      await axios.delete(`${API_BASE}/items/${id}`);
      setItems(items.filter(item => item.id !== id));
    } catch (error) {
      console.error("Error deleting items", error);
    }
  }

  const startEdit = (item) => {
    setEditingId(item.id);
    setName(item.name);
    setDescription(item.description);
  }

  const cancelEdit = () => {
    setEditingId(null);
    setName('');
    setDescription('');
  }

  return (
    <div className="App">
      <h1>CRUD APP with FastAPI and React</h1>
      <div className="item-form">
        <h2>{editingId ? 'Edit Item' : 'Create new Item'}</h2>
        <input
          type="text"
          placeholder="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        {editingId ? (
          <>
            <button onClick={editItem}>Edit Item</button>
            <button onClick={cancelEdit}>Cancel</button>
          </>
        ) : (
          <button onClick={createItem}>Create Item</button>
        )}
      </div>

      <div className="items-list">
        <h2>Items</h2>
        {
          items.length === 0 ? (
            <p>No item yet</p>
          ) : (
            <ul>
              {items.map(item => (
                <li key={item.id}>
                  <h3>{item.name}</h3>
                  <p>{item.description}</p>
                  <button onClick={() => startEdit(item)}>Edit</button>
                  <button onClick={() => deleteItem(item.id)}>Delete</button>
                </li>
              ))}
            </ul>
          )}
      </div>
    </div>
  );
}

export default App;
