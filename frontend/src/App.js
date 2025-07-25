import React, { useState, useEffect } from "react";
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");

  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('picture_taken', data => {
      setPictureStatus(data.message);
      setTimeout(() => setPictureStatus(""), 3000); // Clear status after 3 seconds
    });
    return () => {
      socket.off('picture_taken');
    };
  }, []);


  return (
    <div className="app">
      <header className="app-header">
        <h1 className="title">Sweetie Spies Control Panel</h1>
      </header>
      <div className="grid2">
        <div className="item-box">
          <h1 className="title">Camera</h1>
          <img src="http://10.17.241.102:81/stream"/>
        </div>
        <div className="item-box">
          <p>Hello!</p>
        </div>
      </div>
    </div>
  );
}

export default App;
