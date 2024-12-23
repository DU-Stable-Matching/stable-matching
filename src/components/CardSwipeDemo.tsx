import React from 'react'
import Card from '../components/Card.tsx'
import {sampleCards} from '../assets/data/people_data.ts'

const CardSwipeDemo = () => {

    const [leftCount, setLeftCount] = React.useState(0);

    const incrementLeft = () => {
        setLeftCount(leftCount + 1);
        setCurrentCardIndex((prevIndex) => prevIndex + 1);
    }
    const [rightCount, setRightCount] = React.useState(0);

    const incrementRight = () => {
        setRightCount(rightCount + 1);
        setCurrentCardIndex((prevIndex) => prevIndex + 1);
    }
    const [currentCardIndex, setCurrentCardIndex] = React.useState(0);

    return (
        <div className='bg-cool-gray min-h-screen flex justify-center items-center'>
            <div className='flex flex-col space-y-12 justify-center items-center h-screen bg-cool-gray'>
                <div className='flex flex-row space-x-12 justify-center items-center'>
                    {sampleCards.map((card, index) => (
                        index === currentCardIndex ? (
                            <Card
                                key={card.id}
                                onSwipeLeft={() => {
                                    incrementLeft();
                                }}
                                onSwipeRight={() => {
                                    incrementRight();
                                }}
                                name={card.name}
                            />
                        ) : null
                    ))}
                    <h2 className='text-white'>Left swipes: {leftCount}</h2>
                    <h2 className='text-white'>Right swipes: {rightCount}</h2>
                </div>
            </div>
        </div>
    )
}

export default CardSwipeDemo