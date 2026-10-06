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

  // 4. Interactive 3D Globe Portfolio
  // Projects are explored directly inside the 3D Real-Time Earth

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
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector(".form-btn");
      const originalHTML = btn.innerHTML;

      // Show loading state
      btn.innerHTML = `<span>Sending...</span> <i class="fa-solid fa-spinner fa-spin"></i>`;
      btn.disabled = true;
      btn.style.opacity = "0.7";

      // Collect form data
      const formData = {
        name: document.getElementById("name").value.trim(),
        email: document.getElementById("email").value.trim(),
        subject: document.getElementById("subject").value.trim(),
        message: document.getElementById("message").value.trim(),
      };

      try {
        const response = await fetch("/api/contact", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (response.ok && result.success) {
          // Success
          btn.innerHTML = `<span>Sent Successfully!</span> <i class="fa-solid fa-check"></i>`;
          btn.style.backgroundColor = "#10b981";
          btn.style.opacity = "1";
          form.reset();
        } else {
          // Server returned an error
          btn.innerHTML = `<span>${result.error || "Failed to send"}</span> <i class="fa-solid fa-xmark"></i>`;
          btn.style.backgroundColor = "#ef4444";
          btn.style.opacity = "1";
        }
      } catch (error) {
        // Network error
        btn.innerHTML = `<span>Network error. Try again.</span> <i class="fa-solid fa-xmark"></i>`;
        btn.style.backgroundColor = "#ef4444";
        btn.style.opacity = "1";
      }

      // Restore button after 3 seconds
      setTimeout(() => {
        btn.innerHTML = originalHTML;
        btn.style.backgroundColor = "";
        btn.style.opacity = "";
        btn.disabled = false;
      }, 3000);
    });
  }

  // 7. Status / Progress Modal Initializer
  initStatusModal();

  // 8. 3D Space Earth Globe with Fullscreen
  initEarthGlobe();
});

// ── Global Status / Progress Modal Functions ──
function openStatusModal(title, message, repoUrl, iconClass = "fa-solid fa-robot", badgeText = "In Active Development") {
  const modal = document.getElementById("statusModal");
  if (!modal) return;
  const titleEl = document.getElementById("modalTitle");
  const msgEl = document.getElementById("modalMessage");
  const linkEl = document.getElementById("modalActionLink");
  const iconEl = document.getElementById("modalIcon");
  const badgeEl = document.getElementById("modalBadge");

  if (titleEl) titleEl.textContent = title;
  if (msgEl) msgEl.textContent = message;
  if (linkEl) {
    if (repoUrl) {
      linkEl.href = repoUrl;
      linkEl.style.display = "inline-flex";
    } else {
      linkEl.style.display = "none";
    }
  }
  if (iconEl) iconEl.className = iconClass;
  if (badgeEl) badgeEl.innerHTML = `<i class="fa-solid fa-screwdriver-wrench"></i> ${badgeText}`;

  modal.classList.add("open");
  modal.setAttribute("aria-hidden", "false");
}

function closeStatusModal() {
  const modal = document.getElementById("statusModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

function initStatusModal() {
  const modal = document.getElementById("statusModal");
  const modalCloseBtn = document.getElementById("modalCloseBtn");
  const modalAckBtn = document.getElementById("modalAckBtn");

  if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeStatusModal);
  if (modalAckBtn) modalAckBtn.addEventListener("click", closeStatusModal);

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeStatusModal();
    });
  }

  // Hook all demo buttons in portfolio cards
  document.querySelectorAll(".project-demo-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const projectId = btn.getAttribute("data-project");
      if (projectId === "musa") {
        openStatusModal(
          "MUSA Assistant",
          "Musa Assistant is still in progress... Voice recognition, student portal integrations, and AI scheduling modules are actively being built. Live demo will be available soon!",
          "https://github.com/leroymatienga-jpg/MUSA",
          "fa-solid fa-robot",
          "In Active Development"
        );
      } else if (projectId === "inventory") {
        openStatusModal(
          "Inventory Management GUI",
          "Inventory Management GUI is a desktop Python/Tkinter application. The online interactive web sandbox is in progress. View the full source code on GitHub!",
          "https://github.com/leroymatienga-jpg",
          "fa-solid fa-boxes-stacked",
          "Desktop GUI"
        );
      } else if (projectId === "visualizer") {
        openStatusModal(
          "Dynamic Data Visualizer",
          "Dynamic Data Visualizer is currently receiving an algorithm performance optimization update. The live demo will be ready soon!",
          "https://github.com/leroymatienga-jpg",
          "fa-solid fa-chart-pie",
          "Under Maintenance"
        );
      }
    });
  });
}

function initEarthGlobe() {
  const container = document.getElementById("globe-container");
  const wrapper = document.getElementById("globeWrapper");
  const fullscreenBtn = document.getElementById("fullscreenBtn");
  const backBtn = document.getElementById("globeBackBtn");

  if (!container || typeof THREE === "undefined") return;

  // ── Project Data Registry ──
  const PROJECTS_DATA = {
    musa: {
      projectId: "musa",
      title: "MUSA Assistant",
      location: "Harare, Zimbabwe (Africa)",
      lat: -19.0154,
      lon: 29.1549,
      timezone: 2, // UTC+2
      img: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=600&q=80",
      desc: "Voice- and text-activated AI assistant integrated with student portal systems for academic queries, automated notifications, and AI scheduling management.",
      tags: ["Africa", "Python", "NLP", "AI Assistant", "REST API"],
      codeHref: "https://github.com/leroymatienga-jpg/MUSA",
      demoHref: "#",
      color: 0x3b82f6
    },
    inventory: {
      projectId: "inventory",
      title: "Inventory Management GUI",
      location: "New York, USA (North America)",
      lat: 40.7128,
      lon: -74.006,
      timezone: -4, // UTC-4 (EDT)
      img: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=600&q=80",
      desc: "Comprehensive desktop inventory control system built with Python OOP architecture, SQLite atomic transactions, report generators, and instant search caching.",
      tags: ["North America", "Python", "Tkinter", "SQLite", "OOP"],
      codeHref: "https://github.com/leroymatienga-jpg",
      demoHref: "#",
      color: 0x818cf8
    },
    visualizer: {
      projectId: "visualizer",
      title: "Dynamic Data Visualizer",
      location: "London, UK (Europe)",
      lat: 51.5074,
      lon: -0.1278,
      timezone: 1, // UTC+1 (BST)
      img: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=600&q=80",
      desc: "Interactive web analytics platform for real-time charting, high-throughput dataset parsing, algorithmic step visualizations, and CSV exports.",
      tags: ["Europe", "HTML5", "CSS3", "JavaScript", "Canvas API"],
      codeHref: "https://github.com/leroymatienga-jpg",
      demoHref: "#",
      color: 0x38bdf8
    }
  };

  // Helper: Calculate whether a location is currently experiencing day or night
  function getLocalDaylightStatus(timezoneOffset) {
    const now = new Date();
    const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60;
    let localHour = (utcHours + timezoneOffset) % 24;
    if (localHour < 0) localHour += 24;
    const isDay = localHour >= 6 && localHour < 18;
    const timeStr = `${String(Math.floor(localHour)).padStart(2, "0")}:${String(now.getUTCMinutes()).padStart(2, "0")}`;
    return {
      isDay,
      timeStr,
      label: isDay ? `☀️ Daylight (${timeStr} Local)` : `🌙 Night Lights Active (${timeStr} Local)`
    };
  }

  // Helper: Convert Geographic Lat/Lon to 3D Sphere Vector
  function latLongToVector3(lat, lon, radius) {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lon + 180) * (Math.PI / 180);
    return new THREE.Vector3(
      -(radius * Math.sin(phi) * Math.cos(theta)),
      radius * Math.cos(phi),
      radius * Math.sin(phi) * Math.sin(theta)
    );
  }

  // Spherical SLERP helper for orbital camera arcs
  function slerpVectors(v1, v2, t) {
    const dot = Math.min(Math.max(v1.dot(v2), -1), 1);
    const theta = Math.acos(dot);
    if (Math.abs(theta) < 0.001) return v1.clone().lerp(v2, t).normalize();
    const sinTheta = Math.sin(theta);
    const w1 = Math.sin((1 - t) * theta) / sinTheta;
    const w2 = Math.sin(t * theta) / sinTheta;
    return v1.clone().multiplyScalar(w1).add(v2.clone().multiplyScalar(w2)).normalize();
  }

  // ── Scene & Camera Setup ──
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
  controls.enableZoom = true;
  controls.minDistance = 7.5;
  controls.maxDistance = 45;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.65;

  // 1. Procedural 3D Deep Space Starfield
  const starCount = 2800;
  const starGeometry = new THREE.BufferGeometry();
  const starPositions = new Float32Array(starCount * 3);

  for (let i = 0; i < starCount * 3; i += 3) {
    starPositions[i] = (Math.random() - 0.5) * 850;
    starPositions[i + 1] = (Math.random() - 0.5) * 850;
    starPositions[i + 2] = (Math.random() - 0.5) * 850;
  }

  starGeometry.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
  const starMaterial = new THREE.PointsMaterial({
    color: 0xffffff,
    size: 0.85,
    transparent: true,
    opacity: 0.88
  });
  const stars = new THREE.Points(starGeometry, starMaterial);
  scene.add(stars);

  // 2. Real-Time Solar Calculation & Lighting
  function getRealTimeSubsolarCoords() {
    const now = new Date();
    const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60 + now.getUTCSeconds() / 3600;
    const startOfYear = new Date(Date.UTC(now.getUTCFullYear(), 0, 1));
    const dayOfYear = Math.floor((now - startOfYear) / 86400000);
    // Solar declination (-23.44° to +23.44°)
    const declination = -23.44 * Math.cos(((2 * Math.PI) / 365.25) * (dayOfYear + 10));
    // Subsolar longitude: 0° at 12:00 UTC
    const subsolarLon = -(utcHours - 12) * 15;
    return { lat: declination, lon: subsolarLon };
  }

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
  scene.add(ambientLight);

  const sunLight = new THREE.DirectionalLight(0xffffff, 1.6);
  scene.add(sunLight);

  // 3. Earth Globe with Real-Time Day / Night Shader
  const globeRadius = 6.8;
  const textureLoader = new THREE.TextureLoader();

  const earthDayTexture = textureLoader.load(
    "https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
  );
  const earthNightTexture = textureLoader.load(
    "https://unpkg.com/three-globe/example/img/earth-night.jpg"
  );
  earthDayTexture.minFilter = THREE.LinearFilter;
  earthNightTexture.minFilter = THREE.LinearFilter;

  // Real-Time Day/Night Custom Shader Material
  const earthShaderMaterial = new THREE.ShaderMaterial({
    uniforms: {
      uDayTexture: { value: earthDayTexture },
      uNightTexture: { value: earthNightTexture },
      uSunDirection: { value: new THREE.Vector3(1, 0, 0) },
    },
    vertexShader: `
      varying vec2 vUv;
      varying vec3 vNormal;
      varying vec3 vWorldNormal;

      void main() {
        vUv = uv;
        vNormal = normalize(normalMatrix * normal);
        vWorldNormal = normalize((modelMatrix * vec4(normal, 0.0)).xyz);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: `
      uniform sampler2D uDayTexture;
      uniform sampler2D uNightTexture;
      uniform vec3 uSunDirection;

      varying vec2 vUv;
      varying vec3 vNormal;
      varying vec3 vWorldNormal;

      void main() {
        vec3 dayColor = texture2D(uDayTexture, vUv).rgb;
        vec3 nightColor = texture2D(uNightTexture, vUv).rgb;

        // Cosine of angle between surface normal and sun direction
        float sunDot = dot(vWorldNormal, normalize(uSunDirection));

        // Smooth terminator transition across dawn/dusk (-0.12 to 0.15)
        float dayMix = smoothstep(-0.12, 0.15, sunDot);

        // Warm sunset/sunrise atmospheric amber glow along the twilight rim
        float twilight = (1.0 - smoothstep(0.0, 0.22, abs(sunDot))) * 0.55;
        vec3 sunsetGlow = vec3(1.0, 0.44, 0.16) * twilight;

        // Brilliant golden city lights on dark side
        vec3 nightLights = nightColor * 2.2;
        vec3 nightAmbient = dayColor * 0.04 + vec3(0.015, 0.02, 0.04);
        vec3 nightSide = nightLights + nightAmbient;

        // Daylight side with subtle diffuse shading
        vec3 daySide = dayColor * (0.85 + 0.35 * max(sunDot, 0.0));

        // Blend night and day + add sunset rim
        vec3 finalColor = mix(nightSide, daySide, dayMix) + sunsetGlow;

        // Atmospheric rim Fresnel glow
        float fresnel = pow(1.0 - max(dot(vNormal, vec3(0.0, 0.0, 1.0)), 0.0), 3.5);
        vec3 atmosphereGlow = vec3(0.2, 0.55, 1.0) * fresnel * 0.65 * max(sunDot + 0.2, 0.05);
        finalColor += atmosphereGlow;

        gl_FragColor = vec4(finalColor, 1.0);
      }
    `
  });

  const earthGeometry = new THREE.SphereGeometry(globeRadius, 64, 64);
  const earth = new THREE.Mesh(earthGeometry, earthShaderMaterial);
  scene.add(earth);

  // 4. Clouds Sphere Layer (Rotating Slowly)
  const cloudsTexture = textureLoader.load(
    "https://unpkg.com/three-globe/example/img/earth-clouds.png"
  );
  const cloudsGeo = new THREE.SphereGeometry(globeRadius + 0.07, 64, 64);
  const cloudsMat = new THREE.MeshStandardMaterial({
    map: cloudsTexture,
    transparent: true,
    opacity: 0.35,
    blending: THREE.AdditiveBlending
  });
  const clouds = new THREE.Mesh(cloudsGeo, cloudsMat);
  earth.add(clouds);

  // Function: Update Sun vector based on live real-time subsolar position
  function updateSunVector() {
    const subsolar = getRealTimeSubsolarCoords();
    const localSunVec = latLongToVector3(subsolar.lat, subsolar.lon, 1.0).normalize();
    const worldSunVec = localSunVec.clone().applyEuler(earth.rotation).normalize();

    earthShaderMaterial.uniforms.uSunDirection.value.copy(worldSunVec);
    sunLight.position.copy(worldSunVec.clone().multiplyScalar(40));
  }
  updateSunVector();

  // ── Project Poles & Clickable Beacons ──
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  const clickableMeshes = [];
  let isZoomedIn = false;
  let isAnimating = false;
  let activeProjectId = null;
  const savedCamera = { pos: new THREE.Vector3(), target: new THREE.Vector3() };

  function addProjectPole(project) {
    const poleHeight = 1.7;
    const basePos = latLongToVector3(project.lat, project.lon, globeRadius);
    const tipPos = latLongToVector3(project.lat, project.lon, globeRadius + poleHeight);

    // Pole stem
    const poleGeo = new THREE.CylinderGeometry(0.045, 0.045, poleHeight, 16);
    const poleMat = new THREE.MeshBasicMaterial({ color: project.color });
    const poleMesh = new THREE.Mesh(poleGeo, poleMat);

    poleMesh.position.copy(basePos).lerp(tipPos, 0.5);
    poleMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tipPos.clone().normalize());
    earth.add(poleMesh);

    // Glowing tip beacon (Clickable)
    const tipGeo = new THREE.SphereGeometry(0.36, 16, 16);
    const tipMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.95 });
    const tipMesh = new THREE.Mesh(tipGeo, tipMat);
    tipMesh.position.copy(tipPos);
    tipMesh.userData = project;
    earth.add(tipMesh);
    clickableMeshes.push(tipMesh);

    // Outer beacon pulse halo
    const haloGeo = new THREE.SphereGeometry(0.52, 16, 16);
    const haloMat = new THREE.MeshBasicMaterial({ color: project.color, transparent: true, opacity: 0.45 });
    const haloMesh = new THREE.Mesh(haloGeo, haloMat);
    haloMesh.position.copy(tipPos);
    earth.add(haloMesh);

    // Canvas billboard label
    const canvas = document.createElement("canvas");
    canvas.width = 340;
    canvas.height = 76;
    const ctx = canvas.getContext("2d");

    ctx.fillStyle = "rgba(10, 14, 26, 0.88)";
    ctx.strokeStyle = "#38bdf8";
    ctx.lineWidth = 4;
    ctx.roundRect(10, 10, 320, 56, 28);
    ctx.fill();
    ctx.stroke();

    ctx.font = "Bold 22px Poppins, sans-serif";
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.fillText(project.title, 170, 46);

    const textTexture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: textTexture, depthTest: false });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(3.5, 0.88, 1);
    sprite.position.copy(latLongToVector3(project.lat, project.lon, globeRadius + poleHeight + 0.65));
    earth.add(sprite);
  }

  // Create poles for all 3 projects
  Object.values(PROJECTS_DATA).forEach(addProjectPole);

  // ── Project Overlay Inside Globe ──
  let projectOverlay = null;

  function showProjectOverlay(projectId) {
    const data = PROJECTS_DATA[projectId];
    if (!data) return;

    if (projectOverlay) projectOverlay.remove();

    const sunStatus = getLocalDaylightStatus(data.timezone);

    projectOverlay = document.createElement("div");
    projectOverlay.className = "globe-project-overlay";
    projectOverlay.innerHTML = `
      <div class="gpo-card glass-card">
        <button class="gpo-close-btn" id="gpoCloseBtn" aria-label="Close Project View" title="Return to Orbit">
          <i class="fa-solid fa-xmark"></i>
        </button>
        <div class="gpo-img-wrap">
          <img src="${data.img}" alt="${data.title}" />
          <div class="gpo-img-shine"></div>
        </div>
        <div class="gpo-body">
          <div class="gpo-top-row">
            <div class="gpo-tags">
              <span><i class="fa-solid fa-location-dot"></i> ${data.tags[0]}</span>
              ${data.tags.slice(1, 4).map(t => `<span>${t}</span>`).join("")}
            </div>
            <span class="gpo-sun-status ${sunStatus.isDay ? 'sun-day' : 'sun-night'}">
              ${sunStatus.label}
            </span>
          </div>
          <h3 class="gpo-title">${data.title}</h3>
          <p class="gpo-desc">${data.desc}</p>
          <div class="gpo-links">
            <a href="${data.codeHref}" target="_blank" rel="noopener noreferrer" class="gpo-link-item">
              <i class="fa-brands fa-github"></i> Code
            </a>
            <button type="button" class="gpo-link-item" id="gpoDemoBtn" data-project="${projectId}">
              <i class="fa-solid fa-arrow-up-right-from-square"></i> Demo
            </button>
          </div>
        </div>
      </div>
    `;
    wrapper.appendChild(projectOverlay);

    // Close button
    const closeBtn = projectOverlay.querySelector("#gpoCloseBtn");
    if (closeBtn) closeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      zoomOut();
    });

    // Demo button handler
    const demoBtn = projectOverlay.querySelector("#gpoDemoBtn");
    if (demoBtn) {
      demoBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        if (projectId === "musa") {
          openStatusModal(
            "MUSA Assistant",
            "Musa Assistant is still in progress... Voice recognition, student portal integrations, and AI scheduling modules are actively being built. Live demo will be available soon!",
            "https://github.com/leroymatienga-jpg/MUSA",
            "fa-solid fa-robot",
            "In Active Development"
          );
        } else {
          openStatusModal(
            data.title,
            `${data.title} is currently in active development. Live demo preview will be available soon!`,
            data.codeHref,
            "fa-solid fa-laptop-code",
            "In Progress"
          );
        }
      });
    }

    // Click backdrop to zoom out
    projectOverlay.addEventListener("click", (e) => {
      if (e.target === projectOverlay) {
        zoomOut();
      }
    });

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (projectOverlay) projectOverlay.classList.add("visible");
      });
    });
  }

  function hideProjectOverlay() {
    if (!projectOverlay) return;
    projectOverlay.classList.remove("visible");
    setTimeout(() => {
      if (projectOverlay) { projectOverlay.remove(); projectOverlay = null; }
    }, 450);
  }

  // Update active pill in dock
  function updateDockActive(key) {
    document.querySelectorAll(".dock-pill").forEach((pill) => {
      if (pill.getAttribute("data-dock") === key) {
        pill.classList.add("active");
      } else {
        pill.classList.remove("active");
      }
    });
  }

  // ── Google Earth Hyper-Dive Flight Engine ──
  function flyToLocation(project, onComplete) {
    if (isAnimating) return;
    isAnimating = true;
    activeProjectId = project.projectId;

    // Temporarily pause controls during flight
    controls.autoRotate = false;
    controls.enabled = false;

    // Save orbit state if starting from space orbit
    if (!isZoomedIn) {
      savedCamera.pos.copy(camera.position);
      savedCamera.target.copy(controls.target);
    }

    // Calculate target ground position in current world space
    const localPos = latLongToVector3(project.lat, project.lon, globeRadius);
    const targetWorldPos = localPos.clone().applyEuler(earth.rotation);
    const normal = targetWorldPos.clone().normalize();

    // End camera parameters (Google Earth close aerial perspective)
    const finalAltitude = 1.35; // Close to surface (radius 6.8 + 1.35 = 8.15)
    const finalLookAt = targetWorldPos.clone();
    const finalCamPos = targetWorldPos.clone().add(normal.clone().multiplyScalar(finalAltitude));

    const startCamPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const startDir = startCamPos.clone().normalize();
    const endDir = finalCamPos.clone().normalize();
    const startDist = startCamPos.length();
    const endDist = finalCamPos.length();

    // Trigger flight HUD notification
    const flightHud = document.getElementById("globeFlightHud");
    const hudLocationText = document.getElementById("hudLocationText");
    if (flightHud && hudLocationText) {
      hudLocationText.textContent = `DIVING INTO ${project.title.toUpperCase()}`;
      flightHud.classList.add("active");
    }

    const duration = 2300; // 2.3 seconds Google Earth dive
    const startTime = performance.now();

    function stepFlight() {
      const elapsed = performance.now() - startTime;
      const p = Math.min(elapsed / duration, 1);

      // Smooth spherical interpolation over the planetary surface
      const easedP = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
      const currentDir = slerpVectors(startDir, endDir, easedP);

      // Multi-stage Google Earth altitude curve:
      // High orbital alignment (0 to 0.35) -> Atmospheric dive plunge (0.35 to 0.85) -> Touchdown flare (0.85 to 1.0)
      let altP;
      if (p < 0.35) {
        altP = (p / 0.35) * 0.12;
      } else if (p < 0.85) {
        const sub = (p - 0.35) / 0.50;
        const smooth = sub * sub * (3 - 2 * sub);
        altP = 0.12 + smooth * 0.80;
      } else {
        const sub = (p - 0.85) / 0.15;
        altP = 0.92 + Math.sin(sub * Math.PI * 0.5) * 0.08;
      }

      const currentDist = THREE.MathUtils.lerp(startDist, endDist, altP);
      camera.position.copy(currentDir.multiplyScalar(currentDist));

      // Dynamic FOV speed sensation (widens on plunge, tightens on arrival)
      camera.fov = 45 + Math.sin(p * Math.PI) * 8.0;
      camera.updateProjectionMatrix();

      controls.target.lerpVectors(startTarget, finalLookAt, easedP);
      controls.update();

      if (p < 1) {
        requestAnimationFrame(stepFlight);
      } else {
        camera.fov = 44;
        camera.updateProjectionMatrix();
        isAnimating = false;
        isZoomedIn = true;
        controls.enabled = true;

        if (flightHud) flightHud.classList.remove("active");
        if (backBtn) backBtn.classList.add("visible");

        updateDockActive(project.projectId);
        showProjectOverlay(project.projectId);

        if (onComplete) onComplete();
      }
    }

    requestAnimationFrame(stepFlight);
  }

  // ── Pull Back to Orbit View ──
  function zoomOut() {
    if (!isZoomedIn || isAnimating) return;
    isAnimating = true;
    controls.enabled = false;

    hideProjectOverlay();
    if (backBtn) backBtn.classList.remove("visible");

    const flightHud = document.getElementById("globeFlightHud");
    const hudLocationText = document.getElementById("hudLocationText");
    if (flightHud && hudLocationText) {
      hudLocationText.textContent = "PULLING OUT TO ORBIT...";
      flightHud.classList.add("active");
    }

    const startCamPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endCamPos = savedCamera.pos.length() > 0 ? savedCamera.pos : new THREE.Vector3(0, 4, 24);
    const endTarget = new THREE.Vector3(0, 0, 0);

    const startDir = startCamPos.clone().normalize();
    const endDir = endCamPos.clone().normalize();
    const startDist = startCamPos.length();
    const endDist = endCamPos.length();

    const duration = 1500;
    const startTime = performance.now();

    function stepPullOut() {
      const elapsed = performance.now() - startTime;
      const p = Math.min(elapsed / duration, 1);
      const easedP = p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;

      const currentDir = slerpVectors(startDir, endDir, easedP);
      const currentDist = THREE.MathUtils.lerp(startDist, endDist, easedP);
      camera.position.copy(currentDir.multiplyScalar(currentDist));

      controls.target.lerpVectors(startTarget, endTarget, easedP);
      controls.update();

      if (p < 1) {
        requestAnimationFrame(stepPullOut);
      } else {
        camera.fov = 45;
        camera.updateProjectionMatrix();
        isAnimating = false;
        isZoomedIn = false;
        controls.enabled = true;
        controls.autoRotate = true;

        if (flightHud) flightHud.classList.remove("active");
        updateDockActive("orbit");
      }
    }

    requestAnimationFrame(stepPullOut);
  }

  if (backBtn) {
    backBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      zoomOut();
    });
  }

  // ── Quick-Dive Dock Pill Buttons ──
  document.querySelectorAll(".dock-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      const dockKey = pill.getAttribute("data-dock");
      if (dockKey === "orbit") {
        zoomOut();
      } else if (PROJECTS_DATA[dockKey]) {
        flyToLocation(PROJECTS_DATA[dockKey]);
      }
    });
  });

  // ── Keyboard Escape to Zoom Out / Close Modal ──
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      const modal = document.getElementById("statusModal");
      if (modal && modal.classList.contains("open")) {
        closeStatusModal();
      } else if (isZoomedIn) {
        zoomOut();
      }
    }
  });

  // ── Raycasting: Click on 3D Poles on Globe ──
  let pointerDownPos = new THREE.Vector2();

  container.addEventListener("pointerdown", (e) => {
    pointerDownPos.set(e.clientX, e.clientY);
  });

  container.addEventListener("pointerup", (e) => {
    // Only trigger if it wasn't a drag to rotate
    const dx = e.clientX - pointerDownPos.x;
    const dy = e.clientY - pointerDownPos.y;
    if (Math.sqrt(dx * dx + dy * dy) > 6) return;

    const rect = container.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(clickableMeshes.map(m => {
      const worldMesh = m.clone();
      const worldPos = new THREE.Vector3();
      m.getWorldPosition(worldPos);
      worldMesh.position.copy(worldPos);
      worldMesh.updateMatrixWorld(true);
      return worldMesh;
    }));

    if (intersects.length > 0) {
      const hitWorldPos = intersects[0].object.position;
      let closest = null;
      let closestDist = Infinity;
      for (const tip of clickableMeshes) {
        const wp = new THREE.Vector3();
        tip.getWorldPosition(wp);
        const dist = wp.distanceTo(hitWorldPos);
        if (dist < closestDist) {
          closestDist = dist;
          closest = tip;
        }
      }
      if (closest && closest.userData) {
        flyToLocation(closest.userData);
      }
    }
  });

  container.addEventListener("pointermove", (e) => {
    const rect = container.getBoundingClientRect();
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(clickableMeshes.map(m => {
      const worldMesh = m.clone();
      const worldPos = new THREE.Vector3();
      m.getWorldPosition(worldPos);
      worldMesh.position.copy(worldPos);
      worldMesh.updateMatrixWorld(true);
      return worldMesh;
    }));

    container.style.cursor = intersects.length > 0 ? "pointer" : "grab";
  });

  // ── Fullscreen & Window Resize ──
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

  // ── Animation Loop ──
  function animate() {
    requestAnimationFrame(animate);

    // Subtle drift
    stars.rotation.y += 0.00015;
    clouds.rotation.y += 0.0003;

    // Update solar position relative to Earth
    updateSunVector();

    controls.update();
    renderer.render(scene, camera);
  }
  animate();
}