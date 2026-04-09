// Global data
let alertData = [];
let currentFilter = "All";

const container = document.getElementById("alertsContainer");


// LOAD ALERTS FROM BACKEND

async function loadAlerts() {
    try {
        container.innerHTML = "<p>Loading alerts...</p>";

        const response = await fetch("http://localhost:5000/alerts");

        if (!response.ok) {
            throw new Error("Failed to fetch alerts");
        }

        const data = await response.json();
        alertData = data;

        filterAlerts(currentFilter);

    } catch (error) {
        console.error(error);
        container.innerHTML = "<p>Failed to load alerts ❌</p>";
    }
}


// DISPLAY ALERTS

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

        let statusClass = alert.status.toLowerCase();

        card.innerHTML = `
            <img src="${alert.image}" alt="Garbage Image">
            <h3>${alert.location}</h3>
            <p class="status ${statusClass}">
                Status: ${alert.status}
            </p>

            <div class="buttons">
                <button class="yes-btn" onclick="giveFeedback(${alert.id}, 'Yes')">Yes</button>
                <button class="no-btn" onclick="giveFeedback(${alert.id}, 'No')">No</button>
            </div>
        `;

        container.appendChild(card);
    });
}


// FILTER ALERTS

function filterAlerts(filter) {
    currentFilter = filter;

    // Active button highlight
    document.querySelectorAll(".filters button").forEach(btn => {
        btn.classList.remove("active");
    });

    // Fix for event not defined issue
    if (window.event) {
        window.event.target.classList.add("active");
    }

    searchAlerts();
}


// SEARCH ALERTS

function searchAlerts() {
    const searchValue = document
        .getElementById("searchInput")
        .value.toLowerCase();

    let filtered = alertData;

    if (currentFilter !== "All") {
        filtered = filtered.filter(a => a.status === currentFilter);
    }

    filtered = filtered.filter(a =>
        a.location.toLowerCase().includes(searchValue)
    );

    displayAlerts(filtered);
}


// UPDATE STATS

function updateStats() {
    const total = alertData.length;
    const pending = alertData.filter(a => a.status === "Pending").length;
    const confirmed = alertData.filter(a => a.status === "Confirmed").length;
    const rejected = alertData.filter(a => a.status === "Rejected").length;

    document.getElementById("totalCount").innerText = total;
    document.getElementById("pendingCount").innerText = pending;
    document.getElementById("confirmedCount").innerText = confirmed;
    document.getElementById("rejectedCount").innerText = rejected;
}


// SEND FEEDBACK TO BACKEND

async function giveFeedback(id, response) {
    try {
        const status = response === "Yes" ? "Confirmed" : "Rejected";

        const res = await fetch(`http://localhost:5000/alerts/${id}`, {
            method: "PUT", // or PATCH (confirm with backend teammate)
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ status })
        });

        if (!res.ok) {
            throw new Error("Failed to update alert");
        }

        // Update locally for instant UI response
        const alert = alertData.find(a => a.id === id);
        if (alert) alert.status = status;

        filterAlerts(currentFilter);

    } catch (error) {
        console.error(error);
        alert("Failed to update status ❌");
    }
}


// INITIAL LOAD

loadAlerts();


// AUTO REFRESH

setInterval(() => {
    loadAlerts();
}, 5000);