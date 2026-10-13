const clock = document.querySelector("#clock");
const date = document.querySelector("#date");
const time = document.querySelector("#time");
function tick() {
  const now = new Date();
  clock.textContent = now.toLocaleTimeString("pt-BR", {hour:"2-digit",minute:"2-digit",hour12:false});
  time.textContent = now.toLocaleTimeString("pt-BR", {hour:"2-digit",minute:"2-digit"}) + " · Wi-Fi ▰";
  date.textContent = now.toLocaleDateString("pt-BR", {weekday:"long",day:"numeric",month:"long"});
}
tick();
setInterval(tick, 30000);