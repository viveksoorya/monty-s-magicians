// Variables to hold selected time slot and classrooms
let selectedTimeSlot = null;
let selectedClassrooms = [];  // Array to hold multiple selected classrooms

// Add event listeners for time slot selection
const timeSlotOptions = document.querySelectorAll("#time-slot-options a");
timeSlotOptions.forEach(option => {
    option.addEventListener("click", function(event) {
        event.preventDefault();
        selectedTimeSlot = event.target.innerText;
        document.getElementById('time-slot-btn').innerText = selectedTimeSlot; // Update the text shown on that dropdown button
    });
});

// Event listeners for selecting multiple classrooms
const classroomButtons = document.querySelectorAll("#classroom-buttons button");
classroomButtons.forEach(button => {
    button.addEventListener("click", function() {
        const classroom = button.innerText;
        const currentBgColor = window.getComputedStyle(button).backgroundColor;

        if (currentBgColor === "rgba(255, 255, 255, 0.2)") {
            button.style.backgroundColor = "rgba(255, 255, 255, 0.9)";
            if (!selectedClassrooms.includes(classroom)) {
                selectedClassrooms.push(classroom);  // Add classroom to the array
            }
        } else {
            button.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
            selectedClassrooms = selectedClassrooms.filter(c => c !== classroom);  // Remove classroom from the array
        }
    });
});

// Function that sends booking data to the API
function sendBookingData() {                                          
    const purpose = document.getElementById("purpose").value;
    
    // Create a data object to send to the API
    const bookingData = {
        time_slot: selectedTimeSlot,   // Time slot selected from the dropdown list
        classrooms: selectedClassrooms,  // Array of selected classrooms
        purpose: purpose    // Purpose for booking
    };

    // Send booking data to the Python API using Fetch
    fetch('http://127.0.0.1:8000/book', {   // API endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookingData)
    })
    .then(response => response.json())   // Handle JSON response
    .then(data => {
        console.log(data.message);  // Output message from Flask
    })                       
    .catch(error => {
        console.error('Error:', error);   // Handle any errors
    });
}

// Add event listener for the "Book" button
const bookButton = document.getElementById("book-btn");
bookButton.addEventListener("click", function() {
    const purpose = document.getElementById("purpose").value;

    console.log("Booking Details:");
    console.log("Time Slot:", selectedTimeSlot ? selectedTimeSlot : "No time slot selected");   
    console.log("Classrooms:", selectedClassrooms.length > 0 ? selectedClassrooms.join(', ') : "No classrooms selected");
    console.log("Purpose:", purpose ? purpose : "You have no purpose");               

    // Call the function to send data to the Python API
    sendBookingData();
});

 ///////////// UPDATE CLASSROOM BUTTONS BASED ON TIMESLOT SELECTED //////////////



//const timeSlotOptions = document.querySelectorAll("#time-slot-options a");
timeSlotOptions.forEach(option => {
    option.addEventListener("click", function(event) {
        event.preventDefault();
        selectedTimeSlot = event.target.innerText;
        document.getElementById('time-slot-btn').innerText = selectedTimeSlot;
        
        // Fetch available classrooms for the selected time slot
        fetchAvailableClassrooms(selectedTimeSlot);
    });
});

// Function to fetch available classrooms from the API
function fetchAvailableClassrooms(timeSlot) {
    fetch(`http://127.0.0.1:8000/available_classrooms/${timeSlot}`)
        console.log('fetchAvailableClassrooms fetched.')
        .then(response => response.json())
        .then(data => {
            const availableClassrooms = data.available_classrooms;
            updateClassroomButtons(availableClassrooms);  // Update the buttons
        })
        .catch(error => console.error('Error:', error));
}

// Function to update classroom buttons based on availability
function updateClassroomButtons(availableClassrooms) {
    const classroomButtons = document.querySelectorAll("#classroom-buttons button");
    console.log('updateClassroomButtons called.')
    classroomButtons.forEach(button => {
        const classroom = button.innerText;
        
        if (availableClassrooms.includes(classroom)) {
            button.style.display = "inline-block";  // Show available classrooms
        } else {
            button.style.display = "none";  // Hide unavailable classrooms
        }
    });
}

