// Fetch and display driver standings
async function fetchDriverStandings() {
    try {
        // fetch both driver data and session data
        const driversResponse = await fetch('https://api.openf1.org/v1/drivers?session_key=latest');

        

        if (!driversResponse.ok) {
            throw new Error('Network response was not ok');
        }
        
        const driversData = await driversResponse.json();
  
        displayDriverStandings(driversData);
    } catch (error) {
        console.error('Error fetching driver standings:', error);
        document.querySelector('.column_left').innerHTML += '<p class="error">Failed to load driver standings</p>';
    }
}
function displayDriverStandings(drivers) {
    const container = document.querySelector('.column_left');
    
    

    
    // Create table
    const table = document.createElement('table');
    table.classList.add('standings-table');
    
    // Table header
    table.innerHTML = `
        <thead>
            <tr>
                <th>No.</th>
                <th>Driver</th>
                <th>Team</th>
            </tr>
        </thead>
        <tbody>
            ${drivers.map(driver => `
                <tr>
                    <td>${driver.driver_number || '-'}</td>
                    <td>${driver.full_name || 'Unknown'}</td>
                    <td>${driver.team_name || 'Unknown'}</td>
                </tr>
            `).join('')}
        </tbody>
    `;

    container.appendChild(table);
}

// Fetch and display race schedule
async function fetchRaceSchedule() {
    try {
        // Using the meetings endpoint instead of sessions
        const response = await fetch('https://api.openf1.org/v1/meetings?year=2025');
        if (!response.ok) {
            throw new Error(`Network response was not ok: ${response.status}`);
        }
        const data = await response.json();
        console.log("Meetings data:", data);
        displayRaceSchedule(data);
    } catch (error) {
        console.error('Error fetching race schedule:', error);
        document.querySelector('.column_right').innerHTML += '<p class="error">Failed to load race schedule</p>';
    }
}

function displayRaceSchedule(meetings) {
    const container = document.querySelector('.column_right');
    
    // Keep the heading
    const heading = container.querySelector('h2');
    container.innerHTML = '';
    container.appendChild(heading);
    
    // Check if we have meetings data
    if (!meetings || meetings.length === 0) {
        container.innerHTML += '<p class="error">No race schedule available</p>';
        return;
    }
    
    // Sort meetings by date (oldest to newest)
    const sortedMeetings = meetings.sort((a, b) => {
        return new Date(a.date_start) - new Date(b.date_start);
    });
    
    // Create list of races
    const list = document.createElement('ul');
    list.classList.add('race-list');
    
    sortedMeetings.forEach(meeting => {
        // Format start date
        const startDate = new Date(meeting.date_start);
        const formattedDate = startDate.toLocaleDateString('en-US', { 
            weekday: 'short',
            month: 'short', 
            day: 'numeric',
            year: 'numeric'
        });
        
        // Calculate end date if available
        let dateRange = formattedDate;
        if (meeting.date_end) {
            const endDate = new Date(meeting.date_end);
            const formattedEndDate = endDate.toLocaleDateString('en-US', {
                day: 'numeric',
                month: 'short'
            });
            dateRange = `${formattedDate} - ${formattedEndDate}`;
        }
        
        const item = document.createElement('li');
        item.classList.add('race-item');
        item.innerHTML = `
            <div class="race-card">
                <h3>${meeting.meeting_name || meeting.location || 'Unknown Grand Prix'}</h3>
                <p>${meeting.country_name || ''}</p>
                <p>Date: ${dateRange}</p>
                <p>Track: ${meeting.circuit_short_name || meeting.circuit_name || 'TBA'}</p>
                <p>Round: ${meeting.meeting_official_name || 'TBA'}</p>
            </div>
        `;
        list.appendChild(item);
    });
    
    container.appendChild(list);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchDriverStandings();
    fetchRaceSchedule();
});