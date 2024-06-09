from requests.exceptions import ConnectionError
from custom import Custom
from flask import Flask, request
from flask_cors import CORS
import os

# ------------------ SETUP ------------------


app = Flask(__name__)

# this will need to be reconfigured before taking the app to production
cors = CORS(app)

# ------------------ EXCEPTION HANDLERS ------------------

# Sends response back to Deep Chat using the Response format:
# https://deepchat.dev/docs/connect/#Response
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return {"error": str(e)}, 500

@app.errorhandler(ConnectionError)
def handle_exception(e):
    print(e)
    return {"error": "Internal service error"}, 500

# ------------------ CUSTOM API ------------------

custom = Custom()

@app.route("/chat", methods=["POST"])
def chat():
    body = request.json
    print(body)
    if body['messages'][0]['text'] == 'table':
         return {'html': '<div><h2>Simple Table</h2><table border=1><thead><tr><th>ID</th><th>Name</th><th>Age</th><th>Email</th></tr></thead><tbody><tr><td>1</td><td>John Doe</td><td>30</td><td>john@example.com</td></tr><tr><td>2</td><td>Jane Smith</td><td>25</td><td>jane@example.com</td></tr><tr><td>3</td><td>Michael Johnson</td><td>35</td><td>michael@example.com</td></tr></tbody></table></div>' 
  }
    if body['messages'][0]['text'] == 'image':
        return {'html': '<img src="https://e0.pxfuel.com/wallpapers/989/573/desktop-wallpaper-printable-ben-10-pdf-for-kids-coloring-sheets-ben-10-ben-10-comics-old-cartoon-shows-ben-10-classic-thumbnail.jpg" width="200" height="200">'}

    if body['messages'][0]['text'] == 'fm':
        return {'html': '<audio controls><source src="https://stream-162.zeno.fm/r2gn1pgm4qruv?zs=pOc0_V1hTj22jcdjeHAG0w"></audio>'}
    
    if body['messages'][0]['text'] == 'video':
        return {'html': '<video width="220" height="240" controls><source src="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" type="video/mp4"></video>'}
    
    if body['messages'][0]['text'] == 'calendar':
        return {'html': '''
            <style>
    *,
    *:before,
    *:after {
        box-sizing: border-box;
    }
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 5px;
        background-color: #f2f2f2;
    }
    .month-calendar {
        width: 200px;
        height: 200px;
        border: 1px solid #ddd;
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 10px; /* Added margin to create space between calendar and buttons */
        position: relative; /* Added relative positioning */
    }
    .month-header {
        background-color: #333;
        color: #fff;
        text-align: center;
        padding: 5px;
        font-size: 12px;
        position: relative; /* Added relative positioning */
    }
    .month-header h3 {
        margin: 0;
        display: inline-block; /* Display inline to position arrow buttons next to it */
    }
    .month-controls {
        position: absolute; /* Added absolute positioning */
        top: 5px; /* Adjusted top position */
    }
    .month-controls button {
        padding: 5px 10px; /* Adjusted padding */
        font-size: 12px;
        cursor:pointer;
    }
    .year-display {
        text-align:center;
        margin-top: 5px;
        font-size: 12px;
        color: #666;
    }
</style>
</head>
<body>
<div id="calendar-container">
    <div class="month-calendar" id="current-month-calendar">
        <div class="month-header">
            <button id="prev-month">&larr;</button>
            <h3 id="month-name"></h3>
            <button id="next-month">&rarr;</button>
            <div class="year-display" id="year-display"></div>
        </div>
        <table class="month-table" id="month-table">
            <thead>
                <tr>
                    <th>Sun</th>
                    <th>Mon</th>
                    <th>Tue</th>
                    <th>Wed</th>
                    <th>Thu</th>
                    <th>Fri</th>
                    <th>Sat</th>
                </tr>
            </thead>
            <tbody id="month-body"></tbody>
        </table>
    </div>
</div>

<script>
    // Get elements
    const monthNameElement = document.getElementById('month-name');
    const monthBodyElement = document.getElementById('month-body');
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const yearDisplay = document.getElementById('year-display');

    // Initialize current date
    let currentDate = new Date();
    let currentYear = currentDate.getFullYear();
    let currentMonth = currentDate.getMonth();

    // Function to generate calendar HTML for a specific month
    function generateMonthCalendar(year, month) {
        // Get the number of days in the month
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        // Get the name of the month
        const monthName = new Date(year, month, 1).toLocaleDateString('en-US', { month: 'long' });
        // Initialize HTML string for the month's table
        let monthHTML = '';
        // Start building the table
        monthHTML += `<tr>`;
        for (let i = 1; i <= daysInMonth; i++) {
            // Add each day as a table cell
            monthHTML += `<td>${i}</td>`;
            // If it's Saturday, start a new row
            if (new Date(year, month, i).getDay() === 6 && i < daysInMonth) {
                monthHTML += `</tr><tr>`;
            }
        }
        monthHTML += `</tr>`;
        // Set the month name and the month table HTML
        monthNameElement.textContent = monthName;
        monthBodyElement.innerHTML = monthHTML;
        // Update year display
        yearDisplay.textContent = year;
    }

    // Function to update the displayed month
    function updateMonth() {
        generateMonthCalendar(currentYear, currentMonth);
    }

    // Event listener for previous month button
    prevMonthButton.addEventListener('click', () => {
        // Move to the previous month
        currentMonth--;
        // If we reach January of the previous year, go back to December of the previous year
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        // Update the displayed month
        updateMonth();
    });

    // Event listener for next month button
    nextMonthButton.addEventListener('click', () => {
        // Move to the next month
        currentMonth++;
        // If we reach December of the next year, go back to January of the next year
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        // Update the displayed month
        updateMonth();
    });

    // Initial update to display the current month
    updateMonth();
</script>
</body>
</html>
            '''}

    
    if body['messages'][0]['text'] == 'chart':
        return {
        'html': '''
        
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>

<canvas id="myChart" style="max-width:350px"></canvas>

<script>
const xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
const yValues = [55, 49, 44, 24, 15];
const barColors = [
  "#b91d47",
  "#00aba9",
  "#2b5797",
  "#e8c3b9",
  "#1e7145"
];

new Chart("myChart", {
  type: "pie",
  data: {
 datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  
});
</script>
        '''
    }

    

    return {"text": "Hello"}

@app.route("/chat-stream", methods=["POST"])
def chat_stream():
    body = request.json
    return custom.chat_stream(body)

@app.route("/files", methods=["POST"])
def files():
    return custom.files(request)
@app.route("/", methods=["POST"])
def default():
    print("Im working")

# ------------------ START SERVER ------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use the port provided by the environment, or default to 8080
    app.run(host="0.0.0.0", port=port)