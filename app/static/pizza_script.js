const data = JSON.parse(document.getElementById('json-data').textContent);

const backgroundColors = {
    'POSITIVO': '#4CAF50',  // Verde
    'NEGATIVO': '#F44336',  // Vermelho
    'INCONCLUSIVO': '#FFC107'  // Amarelo
};

const ctx = document.getElementById('myPieChart').getContext('2d');
const myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: Object.keys(data),
        datasets: [{
            data: Object.values(data),
            backgroundColor: Object.keys(data).map(key => backgroundColors[key])
        }]
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        let total = tooltipItem.dataset.data.reduce((a, b) => a + b, 0);
                        let value = tooltipItem.raw;
                        let percentage = ((value / total) * 100).toFixed(2);
                        return `${tooltipItem.label}: ${value} (${percentage}%)`;
                    }
                }
            }
        }
    }
});
