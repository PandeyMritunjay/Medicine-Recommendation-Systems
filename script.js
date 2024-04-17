function getRecommendation() {
    const input = document.getElementById('userInput').value;
    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({input: input})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('results').innerHTML = data.recommendations.join('<br>');
    })
    .catch(error => console.error('Error:', error));
}
