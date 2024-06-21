import * as THREE from "https://esm.sh/three";
import { OrbitControls } from "https://esm.sh/three/examples/jsm/controls/OrbitControls.js";

function render({ model, el }) {
  let container = document.createElement("div");
  container.style.height = "500px";
  container.style.width = "500px";

  el.appendChild(container);
  let data = model.get("voxel_data");
  console.log(data);

  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(
    75,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 15;

  // Create the renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  // Initialize OrbitControls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; // Enable damping (inertia)
  controls.dampingFactor = 0.05;
  controls.screenSpacePanning = false; // Prevent camera from panning vertically
  controls.minDistance = 5; // Set minimum zoom distance
  controls.maxDistance = 50; // Set maximum zoom distance

  // Function to interpolate color based on value
  function getColor(value) {
    const minColor = new THREE.Color("yellow");
    const maxColor = new THREE.Color("red"); 
    return minColor.lerp(maxColor, value / 255);
  }

  // Function to draw voxels
  function drawVoxels(data) {
    // Calculate center offset
    const offsetX = data.length / 2;
    const offsetY = data[0].length / 2;
    const offsetZ = data[0][0].length / 2;

    // Iterate over the voxel data and create cubes
    const geometry = new THREE.BoxGeometry();

    for (let x = 0; x < data.length; x++) {
      for (let y = 0; y < data[x].length; y++) {
        for (let z = 0; z < data[x][y].length; z++) {
          if (data[x][y][z] > 0) {
            const color = getColor(data[x][y][z]);
            const material = new THREE.MeshBasicMaterial({ color });
            const cube = new THREE.Mesh(geometry, material);
            cube.position.set(x - offsetX, y - offsetY, z - offsetZ);
            scene.add(cube);
          }
        }
      }
    }
  }

  // Function to clear the scene and dispose of geometries and materials
  function clearScene() {
    scene.children.forEach((child) => {
      if (child instanceof THREE.Mesh) {
        child.geometry.dispose();
        child.material.dispose();
        scene.remove(child);
      }
    });
  }

  // Initial draw
  drawVoxels(data);

  // Listen for changes in the voxel data
  model.on("change:voxel_data", () => {
    // Clear the scene
    clearScene();

    // Get the new voxel data
    const newData = model.get("voxel_data");

    // Draw the new voxels
    drawVoxels(newData);
  });

  // Render the scene
  function animate() {
    requestAnimationFrame(animate);

    // Update controls
    controls.update();

    // Render the scene
    renderer.render(scene, camera);
  }

  animate();
}

export default { render };