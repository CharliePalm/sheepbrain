import React from 'react';
import './Card.scss';
import { Suit } from '../model';
import * as a from '../assets/images/facedown.png'
function Card(num: number, suit: Suit, isFaceUp: boolean) {
  const cardStr = cardMap.get(num);
  if (!cardStr) {return (<div>internal error</div>)}
  const cardBorderClass = 'border-2 rounded-sm bg-gray-200 h-16 w-10 text-black grid grid-cols-1';
  const suitColor = isRed(suit) ? ' text-red-500' : ''
  
  return isFaceUp ? (
    <div className={cardBorderClass + ' grid-rows-2'}>
      <div className="flex">
        <div className='m-auto'>
          {num}
        </div>
        <div className={"text-right m-auto " + suitColor}>
          {suit}
        </div>
      </div>
      <div className="flex">
        <div className={suitColor + ' m-auto'}>
          {suit}
        </div>
        <div className="text-right m-auto">
          {num}
        </div>
      </div>
    </div>
  ) : (
    <img src={a.default} alt='back of card' className='h-16 w-10 ml-auto mr-auto'></img>
  );
}

const cardMap = new Map<number, string>([
  [1, '1'],
  [2, '2'],
  [3, '3'],
  [4, '4'],
  [5, '5'],
  [6, '6'],
  [7, '7'],
  [8, '8'],
  [9, '9'],
  [10, '10'],
  [11, 'J'],
  [12, 'Q'],
  [12, 'K'],
  [13, 'A'],
]);
const isRed = (suit: Suit) => [Suit.diamonds, Suit.hearts].includes(suit);
export default Card;
