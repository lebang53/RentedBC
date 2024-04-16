// static/js/stats.js
document.addEventListener("DOMContentLoaded", function () {
    fetch("/house_stats/")
    .then(response => response.json())
    .then(data => {
        const labels = data.map(entry => entry.month);
        const counts = data.map(entry => entry.total);
        renderChart(labels, counts);
    });
});


function renderChart(labels, counts) {
    var ctx = document.getElementById('houseStatsChart').getContext('2d');
    var userStatsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'House Statistics',
                data: counts,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });

//    var userStatsChart = new Chart(ctx, {
//        type: 'line',
//        data: {
//            labels: labels,
//            datasets: [{
//                label: 'User Statistics',
//                data: counts,
//                backgroundColor: 'rgba(54, 162, 235, 0.2)',
//                borderColor: 'rgba(54, 162, 235, 1)',
//                borderWidth: 1
//            }]
//        },
//        options: {
//            scales: {
//                yAxes: [{
//                    ticks: {
//                        beginAtZero: true
//                    }
//                }]
//            }
//        }
//    });

//    var userStatsChart = new Chart(ctx, {
//        type: 'pie',
//        data: {
//            labels: labels,
//            datasets: [{
//                label: 'User Statistics',
//                data: counts,
//                backgroundColor: [
//                    'rgba(255, 99, 132, 0.2)',
//                    'rgba(54, 162, 235, 0.2)',
//                    'rgba(255, 206, 86, 0.2)',
//                    'rgba(75, 192, 192, 0.2)',
//                    'rgba(153, 102, 255, 0.2)',
//                    'rgba(255, 159, 64, 0.2)'
//                ],
//                borderColor: [
//                    'rgba(255, 99, 132, 1)',
//                    'rgba(54, 162, 235, 1)',
//                    'rgba(255, 206, 86, 1)',
//                    'rgba(75, 192, 192, 1)',
//                    'rgba(153, 102, 255, 1)',
//                    'rgba(255, 159, 64, 1)'
//                ],
//                borderWidth: 1
//            }]
//        },
//        options: {
//            scales: {
//                yAxes: [{
//                    ticks: {
//                        beginAtZero: true
//                    }
//                }]
//            }
//        }
//    });

//    var userStatsChart = new Chart(ctx, {
//        type: 'doughnut',
//        data: {
//            labels: labels,
//            datasets: [{
//                label: 'User Statistics',
//                data: counts,
//                backgroundColor: [
//                    'rgba(255, 99, 132, 0.2)',
//                    'rgba(54, 162, 235, 0.2)',
//                    'rgba(255, 206, 86, 0.2)',
//                    'rgba(75, 192, 192, 0.2)',
//                    'rgba(153, 102, 255, 0.2)',
//                    'rgba(255, 159, 64, 0.2)'
//                ],
//                borderColor: [
//                    'rgba(255, 99, 132, 1)',
//                    'rgba(54, 162, 235, 1)',
//                    'rgba(255, 206, 86, 1)',
//                    'rgba(75, 192, 192, 1)',
//                    'rgba(153, 102, 255, 1)',
//                    'rgba(255, 159, 64, 1)'
//                ],
//                borderWidth: 1
//            }]
//        },
//        options: {
//            responsive: true,
//            maintainAspectRatio: false,
//            aspectRatio: 1,
//            scales: {
//                yAxes: [{
//                    ticks: {
//                        beginAtZero: true
//                    }
//                }]
//            }
//        }
//    });

}
