function getRecommendation() {
    const input = document.getElementById('userInput').value;
    if (!input) {
        document.getElementById('results').innerHTML = '<h3>Please select a medicine.</h3>';
        return;
    }

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: input })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        if (data.recommendations && data.recommendations.length > 0) {
            const recommendationsList = data.recommendations.map((item, index) => `
                <li>
                    <img src="/static/images/medicine${(index % 3) + 1}.jpg" alt="Medicine Image">
                    ${item}
                </li>`).join('');
            resultsDiv.innerHTML = `<h3>Recommended Medicines:</h3><ul>${recommendationsList}</ul>`;
        } else {
            resultsDiv.innerHTML = '<h3>No recommendations found.</h3>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('results').innerHTML = '<h3>Error fetching recommendations.</h3>';
    });
}
