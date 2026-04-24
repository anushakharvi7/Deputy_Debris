let alertData = [];
let currentFilter = "All";

const container = document.getElementById("alertsContainer");

async function loadAlerts() {
    try {
        container.innerHTML = "<p>Loading alerts...</p>";

        const response = await fetch("http://127.0.0.1:5000/api/reports");

        const data = await response.json();

        // 🔴 FIX IMAGE URL
        alertData = data.map(item => ({
            id: item.id,
            location: item.location,
            status: item.status,
            timestamp: item.timestamp,
            image: "http://127.0.0.1:5000/" + item.image
        }));

        filterAlerts(currentFilter);

    } catch (error) {
        console.error(error);
        container.innerHTML = "<p>Failed to load alerts ❌</p>";
    }
}


function displayAlerts(alerts) {

    updateStats();

    if (alerts.length === 0) {
        container.innerHTML = "<p>No alerts available 🚫</p>";
        return;
    }

    container.innerHTML = "";

    alerts.forEach(alert => {
        const card = document.createElement("div");
        card.className = "alert-card";

        const statusClass = alert.status.toLowerCase();

        card.innerHTML = `
            <img src="${alert.image}" />
            <h3>${alert.location}</h3>
            <p>${alert.timestamp}</p>
            <p class="status ${statusClass}">
                Status: ${alert.status}
            </p>

            <div class="buttons">
                <button onclick="giveFeedback('${alert.id}', 'Confirmed')">Yes</button>
                <button onclick="giveFeedback('${alert.id}', 'Rejected')">No</button>
            </div>
        `;

        container.appendChild(card);
    });
}


function filterAlerts(filter) {
    currentFilter = filter;

    let filtered = alertData;

    if (filter !== "All") {
        filtered = filtered.filter(a => a.status === filter);
    }

    displayAlerts(filtered);
}


function updateStats() {
    document.getElementById("totalCount").innerText = alertData.length;
    document.getElementById("pendingCount").innerText =
        alertData.filter(a => a.status === "Pending").length;
    document.getElementById("confirmedCount").innerText =
        alertData.filter(a => a.status === "Confirmed").length;
    document.getElementById("rejectedCount").innerText =
        alertData.filter(a => a.status === "Rejected").length;
}


// 🔴 CONNECT TO BACKEND UPDATE API
async function giveFeedback(id, status) {
    try {
        await fetch(`http://127.0.0.1:5000/api/reports/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status })
        });

        loadAlerts();

    } catch (error) {
        console.error(error);
        alert("Error updating feedback");
    }
}


loadAlerts();

// 🔁 AUTO REFRESH
setInterval(loadAlerts, 5000);