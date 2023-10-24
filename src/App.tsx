import { useRef } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

function Polyhedron(props) {
  const ref = useRef();

  return (
    <mesh {...props} ref={ref}>
      <icosahedronGeometry args={[3, 1]} />{" "}
      <meshStandardMaterial color="green" />{" "}
    </mesh>
  );
}

export default function App() {
  return (
    <div style={{ height: "50vh", width: "100vw" }}>
      <Canvas>
        <gridHelper args={[10, 10]} />
        <directionalLight position={[0, 5, 5]} intensity={10} />{" "}
        <Polyhedron position={[0, 0, 0]} />
        <OrbitControls />
      </Canvas>
    </div>
  );
}
