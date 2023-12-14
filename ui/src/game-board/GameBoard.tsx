import React from 'react';
import './GameBoard.scss';
import Card from '../card/Card'
import { Suit } from '../model';
import Bot from '../bot/Bot';
import { API } from '../assets/api/api';
const api = new API();


const botNames = [
  'Aria', 'Elias', 'Nora', 'Finn', 'Isabella', 'Mateo', 'Luna', 'Gabriel', 
  'Avery', 'Leo', 'Sofia', 'Ezra', 'Aurora', 'Asher', 'Mila', 'Sebastian',
  'Olivia', 'Liam', 'Amelia', 'Noah', 'Charlotte', 'Elijah', 'Harper', 'William',
  'Evelyn', 'James', 'Ava', 'Carter', 'Abigail', 'Logan', 'Emily', 'Henry',
  'Grace', 'Alexander', 'Chloe', 'Daniel', 'Scarlett', 'Michael', 'Zoe', 'Jackson',
  'Avery', 'Penelope', 'Owen', 'Victoria', 'Lucas', 'Madison', 'Wyatt', 'Eleanor',
];

const generateBotNames = (): string[] => {
  const shuffledNames = botNames.slice().sort(() => Math.random() - 0.5); // Shuffle the names
  return shuffledNames.slice(0, 4); // Select the first 4 shuffled names
}

function GameBoard() {
  const gridColClass = 'mr-auto ml-auto';
  const names = generateBotNames();
  const upsideDownCard = Card(7, Suit.clubs, false)

  return (
    <div className="grid grid-rows-3 grid-cols-3 mr-auto ml-auto w-full text-center p-5 h-screen">
      <div className={gridColClass}>
        {Bot(names[0])}
        {upsideDownCard}
      </div>
      <div className="">
      </div>
      <div className={gridColClass}>
        {Bot(names[1])}
        {upsideDownCard}
      </div>
      <div className={gridColClass}>
        {Bot(names[2])}
        {upsideDownCard}
      </div>
      <div>
        This is the middle
      </div>
      <div className={gridColClass}>
        {Bot(names[3])}
        {upsideDownCard}
      </div>
      <div className={gridColClass + " col-span-3 human"}>
        {upsideDownCard}
      </div>
    </div>
  );
}

export default GameBoard;
