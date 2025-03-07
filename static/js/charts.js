// Initialize charts if they exist on the page
document.addEventListener('DOMContentLoaded', () => {
    // Attack Distribution Chart
    const attackCtx = document.getElementById('attackChart')?.getContext('2d');
    if(attackCtx) {
        new Chart(attackCtx, {
            type: 'doughnut',
            data: {
                labels: ['Normal', 'DDoS', 'Probe', 'R2L', 'U2R'],
                datasets: [{
                    data: [65, 20, 10, 3, 2],
                    backgroundColor: [
                        '#28a745',
                        '#dc3545',
                        '#ffc107',
                        '#17a2b8',
                        '#6c757d'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    }
    
    // Traffic Analysis Chart
    const trafficCtx = document.getElementById('trafficChart')?.getContext('2d');
    if(trafficCtx) {
        new Chart(trafficCtx, {
            type: 'line',
            data: {
                labels: ['1h', '2h', '3h', '4h', '5h', '6h'],
                datasets: [{
                    label: 'Traffic Volume',
                    data: [65, 59, 80, 81, 56, 55],
                    fill: false,
                    borderColor: '#007bff',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
});
