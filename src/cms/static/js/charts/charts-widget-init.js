var ctx = document.getElementById("chart_element");

document.addEventListener("DOMContentLoaded", async function(event) {
    
const data = await fetch(ctx.getAttribute('data-statistics-url'), {
    method: 'GET',
}).then(function (response) {
    // HTTP status 201 Created means the chat message was sent successfully (status 200 OK could also mean CSRF error)
    if (response.status === 200) {
        // The response text contains the rendered message html
        return response.json();
    } else {
        // Throw error which will then be caught later
        throw new Error("Chat message could not be sent: HTTP status " + response.status + " " + response.statusText);
    }
}).catch(error => {
    console.log(error);
    if (error instanceof TypeError) {
        // Handle network error
        u('#chat-network-error').removeClass("hidden");
    } else {
        // Handle server error
        u('#chat-server-error').removeClass("hidden");
    }
}).finally(() => {
    // Hide loading icon
    u('#chat-loading').addClass("hidden");
    // Enable form submitting again
    u("#send-chat-message").first().disabled = false;
});


var graph = new Chart(chart_element, {
    "type": "bar",
    "data": {
        "labels": Object.keys(data),
        "datasets": [ 
            {
                "label": ctx.getAttribute('data-label-translation'),
                "lineTension": 0,
                "data": Object.values(data),
                "type": "line",
                "fill": false,
                "borderColor": "blue"
                },
        ]},
        "options": {
            "scales": {
            "yAxes": [{
                "ticks": {
                "beginAtZero": true
                }
            }]
            } 
        }
    });
}

)
