new Chart(document.getElementById("feelingChart"), {
    type: 'doughnut',
    data: {
      labels: ["Fear",
          "Anger",
          "Joy",
          "Sadness",
          "Disgust"],

      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: [20,10,60,5,5]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: "I'm excited to visit Paris next month."
      }
    }
});
