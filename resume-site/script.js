fetch('https://u2l5m8yrz4.execute-api.us-east-1.amazonaws.com/Prod/put')
    .then(() => fetch('https://u2l5m8yrz4.execute-api.us-east-1.amazonaws.com/Prod/get'))
    .then(response => response.json())
    .then(data => {
        document.getElementById('visitorCount').innerText = data['counter']
    })