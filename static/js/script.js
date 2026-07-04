function fillExample() {

    document.getElementById("temperature").value = 32;
    document.getElementById("rh").value = 38;
    document.getElementById("ws").value = 18;
    document.getElementById("rain").value = 0.3;
    document.getElementById("ffmc").value = 91.5;
    document.getElementById("dmc").value = 68.2;
    document.getElementById("isi").value = 12.1;
    document.getElementById("classes").value = 1;
    document.getElementById("region").value = 1;

}

const form = document.getElementById("prediction-form");

if (form) {

    form.addEventListener("submit", function () {

        const btn = document.getElementById("predict-btn");

        btn.innerHTML = "⏳ Predicting...";

        btn.disabled = true;

    });

}