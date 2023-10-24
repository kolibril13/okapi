

import { useRef, useState } from "react";
import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

function Polyhedron(props) {
  const ref = useRef();
  return (
    <mesh {...props} ref={ref}>
      <icosahedronGeometry args={[3, 1]} />
      <meshStandardMaterial color="green" />
    </mesh>
  );
}

function DirectionalLight() {
  const { camera } = useThree();
  const [lightPosition, setLightPosition] = useState([0,0,0]);

  useFrame(() => {
    // Update the light position to match the camera position
    setLightPosition([camera.position.x, camera.position.y, camera.position.z]);
  });

  return <directionalLight position={lightPosition} intensity={10} />;
}

export default function App() {
  return (
    <div style={{ height: "50vh", width: "100vw" }}>
      <Canvas>
        <DirectionalLight />
        <Polyhedron position={[0, 0, 0]} />
        <gridHelper args={[20, 20]} />
        <OrbitControls />
      </Canvas>
    </div>
  );
}
