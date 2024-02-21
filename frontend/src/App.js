import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';

function App() {
  const mountRef = useRef(null);
  // Initialize the state for the word fetched from the backend
  const [word, setWord] = useState('');

  useEffect(() => {
    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    mountRef.current.appendChild(renderer.domElement);

    // Add a cube
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 5;

    // Animation loop
    const animate = function () {
      requestAnimationFrame(animate);

      cube.rotation.x += 0.01;
      cube.rotation.y += 0.01;

      renderer.render(scene, camera);
    };

    animate();

    // Fetch the word from the backend
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/giveup/521`)
      .then(response => response.json())
      .then(data => {
        // Assume the data object has a 'word' property
        setWord(data.word);
      })
      .catch(error => console.error('Error fetching word:', error));

    // Clean up
    return () => mountRef.current.removeChild(renderer.domElement);
  }, []); // Dependency array is empty, so this effect runs once on mount

  return (
    <div>
      <div ref={mountRef}></div>
      {/* Display the word fetched from the backend */}
      <div>
        <p>Word from backend: {word}</p>
      </div>
    </div>
  );
}

export default App;
