
document.getElementById('searchForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const featuresParams = {
        track_album_release_date: null,
        playlist_genre: null,
        playlist_subgenre: null,
        track_popularity: null,
        duration_in_minutes: null,
        loudness: null,
        track_artist: null,
        track_album_name: null,
        track_name: null
    };

    if (document.getElementById('fromDate').value && document.getElementById('toDate').value) {
        featuresParams.track_album_release_date = [
            document.getElementById('fromDate').value,
            document.getElementById('toDate').value
        ];
    }

    const selectedGenres = Array.from(document.getElementById('playlistGenre').selectedOptions).map(option => option.value);
    if (selectedGenres.length > 0) {
        featuresParams.playlist_genre = selectedGenres;
    }

    const selectedSubGenres = Array.from(document.getElementById('playlistSubGenre').selectedOptions).map(option => option.value);
    if (selectedSubGenres.length > 0) {
        featuresParams.playlist_subgenre = selectedSubGenres;
    }

    const minPop = document.getElementById('trackPopularityMin').value;
    const maxPop = document.getElementById('trackPopularityMax').value;
    if (minPop && maxPop) {
        featuresParams.track_popularity = [parseInt(minPop), parseInt(maxPop)];
    }

    const minDur = document.getElementById('durationMin').value;
    const maxDur = document.getElementById('durationMax').value;
    if (minDur && maxDur) {
        featuresParams.duration_in_minutes = [parseFloat(minDur), parseFloat(maxDur)];
    }

    const loudness = document.getElementById('loudness').value;
    if (loudness) {
        featuresParams.loudness = loudness;
    }

    const trackArtist = document.getElementById('trackArtist').value;
    if (trackArtist) {
        featuresParams.track_artist = trackArtist;
    }

    const albumName = document.getElementById('trackAlbumName').value;
    if (albumName) {
        featuresParams.track_album_name = albumName;
    }

    const trackName = document.getElementById('trackName').value;
    if (trackName) {
        featuresParams.track_name = trackName;
    }

    // console.log(featuresParams); // Debugging line
    // Send all fields to server
    await fetch('/features_params', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(featuresParams)
    });


    // Get filtered data
    const response = await fetch('/filtered_data');
    const data = await response.json();
    // console.log(data); // Debugging line
    const countDiv = document.getElementById('resultsCount');
    countDiv.innerHTML = `<p>Found ${data.length} results</p>`;
    showResults(data);  // 🚀 Update the page with new results
});

function showResults(data) {
    const tableDiv = document.getElementById('resultsTable');
    tableDiv.innerHTML = ''; // Clear old results

    if (data.length === 0) {
        tableDiv.innerHTML = '<p>No results found.</p>';
        return;
    }

    // Create HTML table
    const table = document.createElement('table');
    table.border = "1";

    // Create header row
    const headerRow = table.insertRow();
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement('th');
        th.innerText = key;
        headerRow.appendChild(th);
    });

    // Create data rows
    data.forEach(item => {
        const row = table.insertRow();
        Object.values(item).forEach(value => {
            const cell = row.insertCell();
            cell.innerText = value;
        });
    });

    tableDiv.appendChild(table);
}
