const PLANET_DISTANCE = {
  Mercury: 3,
  Venus: 2,
  Earth: 0.5,
  Mars: 4,
  Jupiter: 25,
  Saturn: 50,
  Neptune: 200,
};

const MODE_SPEED = {
  1: 10,   // NORMAL
  2: 25,   // TURBO
  3: 100,  // HYPERJUMP
};

// Populate planet dropdown
window.onload = () => {
  const select = document.getElementById("planet");
  Object.keys(PLANET_DISTANCE).forEach((planet) => {
    const option = document.createElement("option");
    option.value = planet;
    option.textContent = planet;
    select.appendChild(option);
  });
};

function estimateDeliveryTime(planet, mode, surgeLoad, weatherDelay) {
  if (!(planet in PLANET_DISTANCE)) {
    throw new Error("Unknown destination");
  }
  if (!(mode in MODE_SPEED)) {
    throw new Error("Invalid delivery mode");
  }
  if (surgeLoad < 1) {
    throw new Error("surgeLoad must be >= 1");
  }
  if (weatherDelay < 0) {
    throw new Error("weatherDelay must be >= 0");
  }

  const distance = PLANET_DISTANCE[planet];
  const speed = MODE_SPEED[mode];

  let travelTime = distance / speed;

  // Fatigue penalty for extreme distances
  if (distance > 100) {
    travelTime *= 1.2;
  }

  const total = travelTime * surgeLoad + weatherDelay;
  return Math.round(total * 100) / 100;
}

// Wire UI to estimator
document.getElementById("estimate").onclick = () => {
  const planet = document.getElementById("planet").value;
  const mode = Number(document.getElementById("mode").value);
  const surge = Number(document.getElementById("surge").value);
  const weather = Number(document.getElementById("weather").value);

  try {
    const time = estimateDeliveryTime(planet, mode, surge, weather);
    document.getElementById("result").textContent =
      `Estimated delivery time: ${time} hours`;
  } catch (err) {
    document.getElementById("result").textContent = "Error: " + err.message;
  }
};
