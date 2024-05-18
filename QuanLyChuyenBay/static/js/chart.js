function drawFlightChart(labels, data){
     const ctx = document.getElementById('flightStats');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lượng',
        data: data,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function drawRevenueChart(labels, data, colors, borderCorlors){
     const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: colors,
        borderCorlors: borderCorlors
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}