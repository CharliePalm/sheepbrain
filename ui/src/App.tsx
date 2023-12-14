import React from 'react';
import logo from './logo.svg';
import './App.scss';
import Card from './card/Card'
import GameBoard from './game-board/GameBoard';
function App() {
  return (
    <div className="App">
      <div className="font-bold italic text-6xl text-center">
        Sheepshead
      </div>
      <div className="top">
        {GameBoard()}
      </div>
    </div>
  );
}

export default App;
