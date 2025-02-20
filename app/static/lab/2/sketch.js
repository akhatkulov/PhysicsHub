// Переменные для симуляции
let mass = 100; // Масса тела (кг)
let force = 10; // Приложенная сила (Н)
let friction = 2; // Сила трения (Н)
let acceleration = 0; // Линейное ускорение (м/с²)
let velocity = 0; // Линейная скорость (м/с)
let position = 50; // Положение тела
let distanceTraveled = 0; // Пройденное расстояние
let timeStep = 0.1; // Шаг времени (с)

let positionCircleX = 0;
let positionCircleY = 0;


// Переменные для вращения
let angularVelocity = 0; // Угловая скорость (рад/с)
let angle = 0; // Текущий угол вращения (рад)
let radius = 50; // Радиус мяча (размер объекта)
let prevRadius = radius;

// Настройка холста
function setup() {
  createCanvas(1900, 942);
  calculateAcceleration(); // Calculate initial acceleration

  // Attach event listeners for buttons and input fields
  document.getElementById('applyButton').addEventListener('click', applyParameters);
  document.getElementById('restartButton').addEventListener('click', resetSimulation);

  // Attach event listener to ball size input (range slider)
  document.getElementById('ballSizeInput').addEventListener('change', updateBallSize);
}

// Основной цикл отрисовки
function draw() {
  background(240);
  drawGround(); // Отрисовка земли
  drawObject(); // Отрисовка вращающегося объекта

  // Обновляем физику, если объект не достиг края
  if (position < width - 50) {
    updatePhysics();
    updateRotation();
  }

  // Отображение параметров симуляции
  displayInfo();
}

// Рисуем вращающийся объект
function drawObject() {
  fill(100, 150, 255);
  stroke(0);
  strokeWeight(2);

  // Move coordinate system to the object's position
  push();
  translate(position, height / 2);
  rotate(angle); // Rotate object based on the angle

  // Draw the ball with the current radius
  ellipse(positionCircleX, positionCircleY, radius * 2);

  // Add a line to show the angle of rotation
  fill(0);
  line(0, 0, radius, 0);
  pop();
}
function updateBallSize() {
  prevRadius = radius;
  radius = parseFloat(document.getElementById('ballSizeInput').value);
  // let farq = radius - prevRadius;

  // console.log(prevRadius, radius);
  // log

  // if (farq < prevRadius) {
  //   positionCircleY = positionCircleY + farq;
  // } else {
  //   positionCircleY = positionCircleY - Math.abs(farq);
  // }
  document.getElementById('ballSizeValue').textContent = radius; // Update displayed value
}

// Рисуем землю
function drawGround() {
  fill(100);
  rect(0, height / 2 + 25, width, height / 2);
}

// Рассчитываем линейное ускорение
function calculateAcceleration() {
  let netForce = force - friction; // Результирующая сила
  acceleration = netForce / mass; // Второй закон Ньютона
}

// Обновляем физику
function updatePhysics() {
  velocity += acceleration * timeStep; // Увеличение линейной скорости
  position += velocity * timeStep * 100; // Перемещение объекта
  distanceTraveled += velocity * timeStep; // Обновляем пройденное расстояние
}

// Обновляем вращение
function updateRotation() {
  // Рассчитываем угол, который должен быть пройден с учетом пройденного расстояния
  angle = distanceTraveled; // Угол вращения пропорционален пройденному пути
}

// // Отображение параметров
// function displayInfo() {
//   fill(0);
//   textSize(16);
//   text(`Og'irligi: ${mass} kg`, 10, 60);
//   text(`Kuchi: ${force} Н`, 10, 80);
//   text(`Ishqalanish: ${friction} Н`, 10, 100);
//   text(`Tezlanish chizig'i: ${acceleration.toFixed(2)} m/s²`, 10, 120);
//   text(`Tezlik: ${velocity.toFixed(2)} m/s`, 10, 140);
//   text(`Bosib o'tilgan masofa: ${distanceTraveled.toFixed(2)} m`, 10, 160);
//   text(`Aylanish burchagi: ${angle.toFixed(2)} rad`, 10, 180);
// }
function displayInfo() {
  // Set a background color for the info box
  fill(255, 255, 255, 200);  // Semi-transparent white background
  stroke(0);
  strokeWeight(1);
  rect(10, 70, 350, 220, 10);  // Draw a rounded rectangle behind the text

  // Set text properties
  fill(0);  // Black color for the text
  textSize(16);
  textAlign(LEFT, TOP); // Align the text to the left and top

  // Display each parameter with a bit of spacing
  text(`Og'irlik: ${mass} kg`, 20, 80);
  text(`Kuchi: ${force} Н`, 20, 105);
  text(`Ishqalanish: ${friction} Н`, 20, 130);
  text(`Tezlanish: ${acceleration.toFixed(2)} m/s²`, 20, 155);
  text(`Tezlik: ${velocity.toFixed(2)} m/s`, 20, 180);
  text(`Bosib o'tilgan masofa: ${distanceTraveled.toFixed(2)} m`, 20, 205);
  text(`Aylanish burchagi: ${angle.toFixed(2)} rad`, 20, 230);

  // Optional: Add a title or header to the info box
  textSize(18);
  textAlign(CENTER, TOP);
  fill(50, 50, 255);  // Blue color for the title

  text("Simulyatsiya Ma'lumotlari", 235, 20);
}

// Применение новых параметров
function applyParameters() {
  // Получаем значения из текстовых полей
  mass = parseFloat(document.getElementById('massInput').value);
  force = parseFloat(document.getElementById('forceInput').value);
  friction = parseFloat(document.getElementById('frictionInput').value);
  // radius = parseFloat(document.getElementById("ballSizeInput").value);

  // Перерасчет линейного ускорения
  calculateAcceleration();
}

// Сброс симуляции
function resetSimulation() {
  position = 50; // Reset position
  velocity = 0; // Reset velocity
  distanceTraveled = 0; // Reset distance traveled
  angle = 0; // Reset rotation angle
  // radius = 25; // Reset radius to default size
  calculateAcceleration(); // Recalculate acceleration
}
