document.addEventListener('DOMContentLoaded', () => {
    let salesChartInstance;
    let productsChartInstance;
    let customersChartInstance;

    // Function to fetch and update Sales Trend chart
    window.updateSalesChart = function () {
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        fetch(`/api/sales_trend?start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('salesChart').getContext('2d');
                
                if (salesChartInstance) {
                    salesChartInstance.destroy();
                }

                salesChartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Total Sales ($)',
                            data: data.data,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            });
    };

    // Function to fetch and update Top Products chart
    window.updateProductsChart = function () {
        const category = document.getElementById('category').value;

        fetch(`/api/top_products?category=${category}`)
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('productsChart').getContext('2d');
                
                if (productsChartInstance) {
                    productsChartInstance.destroy();
                }

                productsChartInstance = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: 'Quantity Sold',
                            data: data.data,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: true }
                        }
                    }
                });
            });
    };

    // Function to fetch and update Customer Distribution chart
    window.updateCustomersChart = function () {
        const country = document.getElementById('country').value;

        fetch(`/api/customer_distribution?country=${country}`)
            .then(response => response.json())
            .then(data => {
                const chartContainer = document.getElementById('customersChartContainer');
                const statContainer = document.getElementById('customersStatContainer');
                const statElement = document.getElementById('customersStat');

                // Destroy previous chart instance if it exists
                if (customersChartInstance) {
                    customersChartInstance.destroy();
                }

                // If only one data point, show stat card
                if (data.labels.length === 1) {
                    chartContainer.style.display = 'none';
                    statContainer.style.display = 'block';
                    statElement.textContent = `${data.labels[0]}: ${data.data[0]} customer${data.data[0] > 1 ? 's' : ''}`;
                } else {
                    // Otherwise, show pie chart
                    chartContainer.style.display = 'block';
                    statContainer.style.display = 'none';

                    const ctx = document.getElementById('customersChart').getContext('2d');
                    customersChartInstance = new Chart(ctx, {
                        type: 'pie',
                        data: {
                            labels: data.labels,
                            datasets: [{
                                label: 'Customers',
                                data: data.data,
                                backgroundColor: [
                                    'rgba(255, 99, 132, 0.6)',
                                    'rgba(54, 162, 235, 0.6)',
                                    'rgba(255, 206, 86, 0.6)',
                                    'rgba(75, 192, 192, 0.6)'
                                ]
                            }]
                        },
                        options: {
                            responsive: true
                        }
                    });
                }
            });
    };

    // Initial load of all charts
    updateSalesChart();
    updateProductsChart();
    updateCustomersChart();

    // Fetch and display Average Order Value
    fetch('/api/average_order_value')
        .then(response => response.json())
        .then(data => {
            document.getElementById('aov').textContent = `$${data.aov}`;
        });
});