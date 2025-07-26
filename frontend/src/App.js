import React, { useState, useEffect } from "react";
import image from './downloaded_image.jpg';
import description from './description.wav';
import io from 'socket.io-client';
import './App.css';

const socket = io('http://localhost:8000');

function App() {
  const [pictureStatus, setPictureStatus] = useState("");
  const [temperature, setTemperature] = useState("");
  const [humidity, setHumidity] = useState("");
  const [ultrasonic, setUltrasonic] = useState("");
  const [light, setLight] = useState("");
   const [message, setMessage] = useState('');

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

  useEffect(() => {
    socket.on('connect', () => console.log('Connected:', socket.id));
    socket.on('temp', data => {
      if (data !== null){
        setTemperature(data);
      }
    });
    socket.on('ultrasonic', data => {
      if (data !== null){
        setUltrasonic(data);
      }
    });

    socket.on('humidity', data => {
      if (data !== null){
        setHumidity(data);
      }
    });

    socket.on('light', data => {
      if (data !== null){
        setLight(data);
      }
    });

    return () => {
      socket.off('temp');
      socket.off('ultrasonic');
      socket.off('humidity');
      socket.off('light');
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
          <button onClick={()=>{socket.emit('take_picture', true)}}>Take Screenshot!</button>
          <p></p>
          <img src={image} className="snapshot"/>
          <p>Description: {pictureStatus}</p>
          <audio controls src={description}>
            Your browser does not support the
            <code>audio</code> element.
          </audio>
        </div>
        <div>
          <div className="item-box">
            <h1 className="title">Topics</h1>
            <h3>Temp: {temperature}</h3>
            <h3>Light: {light}</h3>
            <h3>Humidity: {humidity}</h3>
            <h3>Ultrasonic: {ultrasonic}</h3>
          </div>
          <div className="item-box">
            <h2 className="title">Message</h2>
            <input type="text" onChange={(e) => setMessage(e.target.value)}/>
            <button onClick={() => {
              socket.emit('display', message);
              setMessage('');
            }}> Send </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
