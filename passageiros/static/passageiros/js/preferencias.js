// Salva as preferências de notificação neste dispositivo (localStorage).
document.querySelectorAll("[data-pref]").forEach(function (campo) {
  var chave = "gobus_" + campo.dataset.pref;
  var salvo = localStorage.getItem(chave);
  if (salvo !== null) campo.checked = salvo === "1";
  campo.addEventListener("change", function () {
    localStorage.setItem(chave, campo.checked ? "1" : "0");
  });
});
