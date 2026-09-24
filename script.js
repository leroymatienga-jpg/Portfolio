document.addEventListener("DOMContentLoaded", () => {
  // 1. Sliding Magnetic Indicator Pill
  const navContainer = document.getElementById("navLinks");
  const indicator = document.getElementById("navIndicator");
  const navItems = document.querySelectorAll(".nav-links a");
  const sections = document.querySelectorAll("section");

  let isDragging = false;
  let activeItem = document.querySelector(".nav-links a.active") || navItems[0];

  function positionIndicator(target) {
    if (!target || !indicator) return;
    const targetRect = target.getBoundingClientRect();
    const containerRect = navContainer.getBoundingClientRect();

    indicator.style.width = `${targetRect.width}px`;
    indicator.style.transform = `translateX(${targetRect.left - containerRect.left}px)`;
  }

  positionIndicator(activeItem);
  window.addEventListener("resize", () => positionIndicator(activeItem));

  navItems.forEach((link) => {
    link.addEventListener("mouseenter", () => {
      positionIndicator(link);
    });

    link.addEventListener("mousedown", () => {
      isDragging = true;
    });

    link.addEventListener("click", () => {
      navItems.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
      activeItem = link;
      positionIndicator(activeItem);
    });
  });

  navContainer.addEventListener("mousemove", (e) => {
    if (isDragging) {
      const hoveredElement = document.elementFromPoint(e.clientX, e.clientY);
      if (hoveredElement && hoveredElement.classList.contains("nav-item")) {
        positionIndicator(hoveredElement);
      }
    }
  });

  window.addEventListener("mouseup", (e) => {
    if (isDragging) {
      isDragging = false;
      const releasedElement = document.elementFromPoint(e.clientX, e.clientY);
      if (releasedElement && releasedElement.classList.contains("nav-item")) {
        releasedElement.click();
      } else {
        positionIndicator(activeItem);
      }
    }
  });

  navContainer.addEventListener("mouseleave", () => {
    if (!isDragging) {
      positionIndicator(activeItem);
    }
  });

  // Dynamic Scroll Spy
  window.addEventListener("scroll", () => {
    if (isDragging) return;
    let currentSectionId = "";
    const scrollPosition = window.scrollY + 220;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        currentSectionId = section.getAttribute("id");
      }
    });

    if (currentSectionId) {
      navItems.forEach((link) => {
        if (link.getAttribute("href") === `#${currentSectionId}`) {
          navItems.forEach((i) => i.classList.remove("active"));
          link.classList.add("active");
          activeItem = link;
          positionIndicator(activeItem);
        }
      });
    }
  });

  // 2. Typewriter Effect
  const words = ["Software Developer!", "CS Student!", "Python Engineer!", "Tech Enthusiast!"];
  let wordIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  const typingElement = document.getElementById("typewriter");

  function typeEffect() {
    if (!typingElement) return;
    const currentWord = words[wordIndex];
    if (isDeleting) {
      typingElement.textContent = currentWord.substring(0, charIndex - 1);
      charIndex--;
    } else {
      typingElement.textContent = currentWord.substring(0, charIndex + 1);
      charIndex++;
    }

    let speed = isDeleting ? 50 : 100;
    if (!isDeleting && charIndex === currentWord.length) {
      speed = 1500;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      wordIndex = (wordIndex + 1) % words.length;
      speed = 400;
    }
    setTimeout(typeEffect, speed);
  }
  typeEffect();

  // 3. Mobile Navigation Toggle
  const toggleBtn = document.getElementById("menuToggle");
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      navContainer.classList.toggle("open");
      const icon = toggleBtn.querySelector("i");
      icon.classList.toggle("fa-bars");
      icon.classList.toggle("fa-xmark");
    });
  }

  // 4. Project Filtering
  const filterBtns = document.querySelectorAll(".filter-btn");
  const projectCards = document.querySelectorAll(".project-card");

  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const filter = btn.getAttribute("data-filter");
      projectCards.forEach((card) => {
        const category = card.getAttribute("data-category");
        if (filter === "all" || category === filter) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  // 5. Skill Bar Animations
  const progressBars = document.querySelectorAll(".progress-bar");
  const skillsObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animated");
        }
      });
    },
    { threshold: 0.3 }
  );
  progressBars.forEach((bar) => skillsObserver.observe(bar));

  // 6. Contact Form Submission
  const form = document.getElementById("contactForm");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const btn = form.querySelector(".form-btn");
      btn.innerHTML = `<span>Sent Successfully!</span> <i class="fa-solid fa-check"></i>`;
      btn.style.backgroundColor = "#10b981";
      form.reset();

      setTimeout(() => {
        btn.innerHTML = `<span>Send Message</span> <i class="fa-solid fa-paper-plane"></i>`;
        btn.style.backgroundColor = "";
      }, 3000);
    });
  }

  // 7. 3D Space Earth Globe with Fullscreen
  initEarthGlobe();
});

function initEarthGlobe() {
  const container = document.getElementById("globe-container");
  const wrapper = document.getElementById("globeWrapper");
  const fullscreenBtn = document.getElementById("fullscreenBtn");

  if (!container || typeof THREE === "undefined") return;

  // Scene & Camera Setup
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x020308); // Deep Space Black

  const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    2000
  );
  camera.position.set(0, 4, 24);

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // OrbitControls
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.enableZoom = true; // Allows zooming into space/earth
  controls.minDistance = 9;
  controls.maxDistance = 45;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.7;

  // 1. Procedural 3D Deep Space Starfield
  const starCount = 2500;
  const starGeometry = new THREE.BufferGeometry();
  const starPositions = new Float32Array(starCount * 3);

  for (let i = 0; i < starCount * 3; i += 3) {
    starPositions[i] = (Math.random() - 0.5) * 800;
    starPositions[i + 1] = (Math.random() - 0.5) * 800;
    starPositions[i + 2] = (Math.random() - 0.5) * 800;
  }

  starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
  const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.8,
    transparent: true,
    opacity: 0.85
  });
  const stars = new THREE.Points(starGeometry, starMaterial);
  scene.add(stars);

  // 2. Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 1.1);
  scene.add(ambientLight);

  const sunLight = new THREE.DirectionalLight(0x93c5fd, 1.8);
  sunLight.position.set(25, 15, 30);
  scene.add(sunLight);

  // 3. Earth Globe
  const globeRadius = 6.8;
  const textureLoader = new THREE.TextureLoader();
  const earthTexture = textureLoader.load(
    "https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
  );

  const earthGeometry = new THREE.SphereGeometry(globeRadius, 64, 64);
  const earthMaterial = new THREE.MeshStandardMaterial({
    map: earthTexture,
    roughness: 0.8,
    metalness: 0.1
  });
  const earth = new THREE.Mesh(earthGeometry, earthMaterial);
  scene.add(earth);

  // Atmosphere Outer Glow
  const atmosphereGeo = new THREE.SphereGeometry(globeRadius + 0.2, 64, 64);
  const atmosphereMat = new THREE.MeshBasicMaterial({
    color: 0x3b82f6,
    transparent: true,
    opacity: 0.18,
    side: THREE.BackSide
  });
  const atmosphere = new THREE.Mesh(atmosphereGeo, atmosphereMat);
  scene.add(atmosphere);

  // Lat/Long to 3D Coordinates
  function latLongToVector3(lat, lon, radius) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    return new THREE.Vector3(
      -(radius * Math.sin(phi) * Math.cos(theta)),
      radius * Math.cos(phi),
      radius * Math.sin(phi) * Math.sin(theta)
    );
  }

  // Create Project Pole & Hover Label
  function addProjectPole(lat, lon, title, poleColor = 0x60a5fa) {
    const poleHeight = 1.6;
    const basePos = latLongToVector3(lat, lon, globeRadius);
    const tipPos = latLongToVector3(lat, lon, globeRadius + poleHeight);

    // Pole stem
    const poleGeo = new THREE.CylinderGeometry(0.04, 0.04, poleHeight, 16);
    const poleMat = new THREE.MeshBasicMaterial({ color: poleColor });
    const poleMesh = new THREE.Mesh(poleGeo, poleMat);

    poleMesh.position.copy(basePos).lerp(tipPos, 0.5);
    poleMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tipPos.clone().normalize());
    earth.add(poleMesh);

    // Glowing tip
    const tipGeo = new THREE.SphereGeometry(0.18, 16, 16);
    const tipMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const tipMesh = new THREE.Mesh(tipGeo, tipMat);
    tipMesh.position.copy(tipPos);
    earth.add(tipMesh);

    // Canvas billboard label
    const canvas = document.createElement("canvas");
    canvas.width = 320;
    canvas.height = 70;
    const ctx = canvas.getContext("2d");

    ctx.fillStyle = "rgba(10, 14, 26, 0.85)";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 4;
    ctx.roundRect(10, 10, 300, 50, 25);
    ctx.fill();
    ctx.stroke();

    ctx.font = "Bold 24px Poppins, sans-serif";
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.fillText(title, 160, 43);

    const textTexture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: textTexture, depthTest: false });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(3.4, 0.85, 1);
    sprite.position.copy(latLongToVector3(lat, lon, globeRadius + poleHeight + 0.6));
    earth.add(sprite);
  }

  // Deployments:
  addProjectPole(-19.0154, 29.1549, "MUSA (Africa)", 0x2563eb);       // Zimbabwe
  addProjectPole(51.5074, -0.1278, "Visualizer (Europe)", 0x38bdf8);   // London
  addProjectPole(40.7128, -74.006, "Inventory (N. America)", 0x818cf8); // New York

  // Fullscreen Handlers
  function resizeRenderer() {
    setTimeout(() => {
      const newW = container.clientWidth;
      const newH = container.clientHeight;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    }, 100);
  }

  if (fullscreenBtn && wrapper) {
    fullscreenBtn.addEventListener("click", () => {
      if (!document.fullscreenElement) {
        wrapper.requestFullscreen().catch((err) => {
          console.error(`Error enabling fullscreen: ${err.message}`);
        });
      } else {
        document.exitFullscreen();
      }
    });

    document.addEventListener("fullscreenchange", () => {
      const icon = fullscreenBtn.querySelector("i");
      if (document.fullscreenElement) {
        icon.classList.remove("fa-expand");
        icon.classList.add("fa-compress");
      } else {
        icon.classList.remove("fa-compress");
        icon.classList.add("fa-expand");
      }
      resizeRenderer();
    });
  }

  window.addEventListener("resize", resizeRenderer);

  // Render & Slow Space Twinkle Animation
  function animate() {
    requestAnimationFrame(animate);
    stars.rotation.y += 0.0002;
    controls.update();
    renderer.render(scene, camera);
  }
  animate();
}