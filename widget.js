import * as THREE from "https://esm.sh/three";
import { OrbitControls } from "https://esm.sh/three/examples/jsm/controls/OrbitControls.js";

function render({ model, el }) {
  let container = document.createElement("div");
  container.style.height = "500px";
  container.style.width = "500px";
  el.appendChild(container);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
  );
  camera.position.z = 15;

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.screenSpacePanning = false;
  controls.minDistance = 5;
  controls.maxDistance = 50;

  function getColor(value) {
    const minColor = new THREE.Color("yellow");
    const maxColor = new THREE.Color("red"); 
    return minColor.lerp(maxColor, value / 255);
  }

  function drawVoxels(data) {
    const offsetX = data.length / 2;
    const offsetY = data[0].length / 2;
    const offsetZ = data[0][0].length / 2;
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

  function clearScene() {
    scene.children.forEach((child) => {
      if (child instanceof THREE.Mesh) {
        child.geometry.dispose();
        child.material.dispose();
        scene.remove(child);
      }
    });
  }

  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }

  // Initial draw
  setTimeout(() => {
    const data = model.get("voxel_data");
    drawVoxels(data);
  }, 1000); // Adjust the timeout duration as needed

  model.on("change:voxel_data", () => {
    clearScene();
    const newData = model.get("voxel_data");
    drawVoxels(newData)
  });

  animate();
}

export default { render };