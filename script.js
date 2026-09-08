function analyseSchedule() {

    const crop = document.getElementById("crop").value;
    const quantity = document.getElementById("quantity").value;
    const location = document.getElementById("location").value;

    if (crop === "" || quantity === "" || location === "") {
        alert("Please enter crop, quantity and location.");
        return;
    }

    const recommendation = document.getElementById("recommendation");

    // Demo centre data
    const centres = [
        {
            name: "Centre A",
            distance: "2.4 km",
            queue: "18 farmers",
            capacity: "High",
            arrival: "3:45 PM",
            service: "4:00 – 4:30 PM"
        },
        {
            name: "Centre B",
            distance: "4.1 km",
            queue: "32 farmers",
            capacity: "Medium",
            arrival: "4:15 PM",
            service: "4:30 – 5:15 PM"
        },
        {
            name: "Centre C",
            distance: "6.8 km",
            queue: "11 farmers",
            capacity: "Low",
            arrival: "3:30 PM",
            service: "3:45 – 4:15 PM"
        }
    ];

    // Best centre for demo
    const best = centres[0];

    // Update recommendation card
    recommendation.querySelector("h2").innerText = best.name;

    recommendation.querySelector(".distance").innerText =
        "📍 " + best.distance + " from your location";

    const items = recommendation.querySelectorAll(".recommendation-item");

    items[0].querySelector("strong").innerText = best.arrival;
    items[1].querySelector("strong").innerText = best.service;
    items[2].querySelector("strong").innerText = best.queue;
    items[3].querySelector("strong").innerText = best.capacity;

    recommendation.classList.remove("hidden");
    document.getElementById("centreComparison")
    .classList.remove("hidden");

    recommendation.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


function bookSlot() {

    const message = document.getElementById("bookingMessage");
    const queueSection = document.getElementById("queueSection");

    // Show booking confirmation
    message.innerText =
        "✓ Slot booked successfully! Your token is #48. Please arrive by 3:45 PM.";

    // Show live queue
    if (queueSection) {
        queueSection.classList.remove("hidden");

        queueSection.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
}

function viewQueue() {

    alert("Live Queue feature coming next!");
}
function processFarmer(button) {

    const row = button.closest(".queue-row");

    const status = row.querySelector(".status");

    status.innerText = "Processing";
    status.className = "status processing";

    button.innerText = "Processing...";
    button.disabled = true;
}


function completeFarmer(button) {

    const row = button.closest(".queue-row");

    const status = row.querySelector(".status");

    status.innerText = "Completed";
    status.className = "status completed";

    button.innerText = "✓ Completed";
    button.disabled = true;

    const completedCount =
        document.getElementById("completedCount");

    completedCount.innerText =
        parseInt(completedCount.innerText) + 1;
}


function verifyProduce() {

    const message = document.getElementById("procurementMessage");

    message.innerText =
        "✓ Produce verified successfully.";

    localStorage.setItem("farmerStatus", "Verified");
}


function weighProduce() {

    const message = document.getElementById("procurementMessage");

    message.innerText =
        "✓ Weighing completed. Final quantity recorded: 50 Quintals.";

    localStorage.setItem("farmerStatus", "Weighed");
}

function processPayment() {

    const status = document.getElementById("paymentStatus");

    status.innerText =
        "🔵 Payment Processing...";

    setTimeout(function () {

        status.innerText =
            "🟢 Payment Completed — ₹1,11,550";

    }, 1500);
}
function saveFamilyMember() {

    const name = document.getElementById("familyName").value.trim();
    const relation = document.getElementById("familyRelation").value;
    const mobile = document.getElementById("familyMobile").value.trim();

    if (name === "" || relation === "" || mobile === "") {
        alert("Please enter all family member details.");
        return;
    }

    localStorage.setItem("familyMemberName", name);
    localStorage.setItem("familyRelation", relation);
    localStorage.setItem("familyMemberMobile", mobile);

    document.getElementById("familySaveMessage").innerText =
        "✓ " + name + " has been added successfully.";
}
