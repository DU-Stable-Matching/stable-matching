import { RoundedBox } from '@react-three/drei';
import { Canvas, useFrame } from '@react-three/fiber'; // 👈 first!
import React, { useRef, useEffect, useState, useMemo } from 'react';
import * as THREE from 'three';
import { seededRandom } from 'three/src/math/MathUtils';

interface NodeConnectionProps {
  index: number;
  scroll: number;
  startY: number;
  endY: number;
}

const NodeConnection: React.FC<NodeConnectionProps> = ({ index, scroll, startY, endY }) => {
  const leftX = -7;
  const rightX = 7;
  const leftY = startY;
  const rightY = endY;

  const visibleThreshold = index * 100;
  const shouldAnimate = scroll > visibleThreshold;

  const wireRef = useRef<THREE.Mesh>(null);
  const [progress, setProgress] = useState(0);

  useFrame((_, delta) => {
    if (shouldAnimate && progress < 1) {
      setProgress((prev) => Math.min(prev + delta * 0.85, 1));
    }
  });

  if (!shouldAnimate && progress === 0) return null;

  // Straight line from left to right, relative to (0,0)
  const dx = rightX - leftX;
  const dy = rightY - leftY;

  const line = new THREE.LineCurve3(
    new THREE.Vector3(0, 0, 0),
    new THREE.Vector3(dx, dy, 0)
  );

  const geometry = new THREE.TubeGeometry(line, 1, 0.03, 6, false); 
  const circle = new THREE.CircleGeometry(0.325, 64);

  return (
    <>
      <mesh ref={wireRef} geometry={geometry} position={[leftX, leftY, 0]}  scale={[progress, 1, 1]}>
        <meshBasicMaterial color="black" transparent opacity={0.2} />
      </mesh>

      {/* Left Node */}
      <mesh position={[leftX, leftY, 0]} geometry={circle} scale={[progress, progress, progress]}>
        <meshBasicMaterial color="black" />
      </mesh>

      {/* Right Node */}
      <mesh position={[rightX, rightY, 0]} geometry={circle} scale={[progress, progress, progress]}>
        <meshBasicMaterial color="black" />
      </mesh>
    </>
  );
};


const yVals = [ // we can make these whatever we want
  2, 3, 4.2, -.5, -1.2
];

const BackgroundCanvas: React.FC = () => {
  const [scroll, setScroll] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScroll(window.scrollY);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const NUM_CONNECTIONS = 7;

  return (
    <Canvas
      camera={{ position: [0, 0, 10], fov: 50 }}
      style={{
      position: 'absolute',
      top: 0,
      left: 0,
      zIndex: 1,
      width: '100%',
      height: '100%',
      pointerEvents: 'none',
      }}
    >
      <ambientLight />
      {Array.from({ length: Math.floor(NUM_CONNECTIONS/2) }).map((_, i) => (
      <>
      <NodeConnection key={i} index={i} scroll={scroll} startY={yVals[i]} endY={yVals[(i+1)%NUM_CONNECTIONS]}/> 
      <NodeConnection key={i+1} index={i+1} scroll={scroll} endY={yVals[i]} startY={yVals[(i+2)%NUM_CONNECTIONS]}/>
      </>
      ))}
    </Canvas>
  );
};

export default BackgroundCanvas;
