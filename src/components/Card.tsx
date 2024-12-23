import React, { useState } from "react";
import { motion, useMotionValue, useTransform, useAnimation } from "framer-motion";

const Card = ({ onSwipeLeft = () => {}, onSwipeRight = () => {}, name = "" }) => {
    const motionValue = useMotionValue(0);
    const animControls = useAnimation();
    const [isVisible, setIsVisible] = useState(true);

    const rotateValue = useTransform(motionValue, [-200, 200], [-50, 50]);
    const opacityValue = useTransform(
        motionValue,
        [-200, 0, 200],
        [0, 1, 0]
    );

    const handleSwipe = async (direction) => {
        const targetX = direction === "left" ? -200 : 200;

        await animControls.start({ x: targetX, opacity: 0, transition: { duration: 0.15 } });

        if (direction === "left") {
            onSwipeLeft();
        } else {
            onSwipeRight();
        }
        setIsVisible(false);
    };

    return (
        isVisible && (
            <motion.div
                className="w-96 h-96 bg-white rounded-lg shadow-xl justify-between items-center flex flex-col"
                drag="x"
                style={{ x: motionValue, rotate: rotateValue, opacity: opacityValue}}
                dragConstraints={{ left: -1000, right: 1000 }}
                onDragEnd={(event, info) => {
                    if (info.offset.x > 150) {
                        handleSwipe("right");
                    } else if (info.offset.x < -150) {
                        handleSwipe("left");
                    } else {
                        animControls.start({ x: 0 });
                    }
                }}
                animate={animControls}
                initial={{ opacity: 1 }}
            >
                <div className="flex flex-col w-full h-full justify-between my-12">
                    <div className="flex justify-center">
                        <h2 className="font-normal">{name}</h2>
                    </div>
                    <div className="mt-4 flex space-x-4 justify-center">
                        <button
                            className="px-2 py-2 bg-periwinkle text-black rounded-md"
                            onClick={() => handleSwipe("left")}
                        >
                            Interested
                        </button>
                        <button
                            className="px-4 py-2 bg-myrtle-green text-white rounded-md"
                            onClick={() => handleSwipe("right")}
                        >
                            Not Interested
                        </button>
                    </div>
                </div>
            </motion.div>
        )
    );
};

export default Card;
