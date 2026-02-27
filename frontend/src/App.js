import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [name, setName] = useState('');

  const sayHello = () => {
    fetch(`/hello?name=${name}`)
      .then(response => response.json())
      .then(data => setMessage(data.message));
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <input 
            type="text" 
            placeholder="Enter your name" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
          />
          <button onClick={sayHello}>Say Hello</button>
        </div>
        <p>{message}</p>
      </header>
    </div>
  );
}

export default App;
