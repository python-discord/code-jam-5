const inputName = document.getElementById('name');
const form = document.getElementById('search-form');
const map = document.getElementById('map');

const restrictions = {'country': ['us']};

/* eslint-disable no-undef */
autocomplete = new google.maps.places.Autocomplete(inputName);
autocomplete.setFields(['geometry']);
autocomplete.setComponentRestrictions(restrictions);

const acService = new google.maps.places.AutocompleteService();
const placesService = new google.maps.places.PlacesService(map);
const sessionToken = new google.maps.places.AutocompleteSessionToken();
/* eslint-enable no-undef */

/**
 * Plot the data for the indicator using Plotly.js
 *
 * @param   indicator   The indicator element for which to plot the data.
 */
function plot(indicator) {
    const graph = indicator.querySelector('.graph');
    if (!graph) {
        console.error(`Could not find a graph element for ${graph.id}`);
        return;
    }

    const trace = {
        x: JSON.parse(graph.dataset.x),
        y: JSON.parse(graph.dataset.y),
        mode: 'lines+markers',
        type: 'scatter'
    };

    const layout = {
        xaxis: {'title': 'year'},
        yaxis: {'title': graph.dataset.units}
    };

    Plotly.newPlot(graph, [trace], layout, {responsive: true}); // eslint-disable-line no-undef
}

/**
 * Update the DOM to show the indicator.
 *
 * @param   response    The response with the HTML for the indicator.
 */
function showIndicator(response) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(response, 'text/html');

    document.getElementById('sidebar').appendChild(doc.querySelector('.nav-item'));

    const indicator = document.getElementById('indicators').appendChild(
        doc.querySelector('.indicator')
    );

    plot(indicator);

    document.getElementById('loading-spinner').hidden = true;

    const results = document.getElementById('results');
    if (results.hidden) {
        results.hidden = false;

        /* eslint-disable no-undef */
        $('#sidebar li:first-child a').tab('show');
        $('[data-toggle="tooltip"]').tooltip();
        /* eslint-enable no-undef */
    }
}

/**
 * Return URL search parameters for the given location object.
 *
 * The latitude and longitude are truncated to 6 decimal places.
 *
 * @param   location            The location to convert.
 * @returns {URLSearchParams}   The search parameters for the location.
 */
function getURLParams(location) {
    location = location.toJSON();

    // Truncate to 6 decimal places
    for (const key in location) {
        location[key] = location[key].toFixed(6);
    }

    return new URLSearchParams(location);
}

/**
 * Update the URL in the browser with a new location and clear the search box input.
 *
 * @param   location    The new location to put in the URL.
 */
function setURL(location) {
    const params = getURLParams(location);
    history.pushState(null, null, `/?${params}`);

    // Clear search box
    inputName.value = '';
}

/**
 * Get the nearest supported city for the given coordinates.
 *
 * @param   location    The location for which to find the nearest city.
 */
function getCity(location) {
    const params = getURLParams(location);

    fetch(`/location?${params}`)
        .then(response => response.json())
        .then(getIndicators)
        .then(() => setURL(location))
        .catch(error => console.error(error));
}

/**
 * Get indicator data for a city.
 *
 * @param   city    The city for which to get indicators.
 */
function getIndicators(city) {
    document.getElementById('city-name').innerText = city.name;
    document.getElementById('city-admin').innerText = city.admin;

    const indicators = [
        'dry_spells',
        'extreme_cold_events',
        'extreme_heat_events',
        'extreme_precipitation_events',
        'heat_wave_incidents',
        'total_precipitation',
        'average_high_temperature',
        'average_low_temperature',
    ];

    for (let indicator of indicators) {
        fetch(`/search/${city.id}/${indicator}`)
            .then(response => response.text())
            .then(showIndicator)
            .catch(error => console.log(`Error getting ${indicator}: `, error));
    }
}

/**
 * Get the location for the top autocomplete prediction.
 *
 * @param   predictions     The predictions from Google Autocomplete.
 * @param   status          The status of the request for predictions.
 */
function getTopLocation(predictions, status) {
    // eslint-disable-next-line no-undef
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
        console.error('Could not get predictions: status is ' + status);
        return;
    }

    const request = {
        fields: ['geometry.location'],
        placeId: predictions[0].place_id,
        sessionToken: sessionToken
    };

    placesService.getDetails(request, (result, status) => {
        // eslint-disable-next-line no-undef
        if (status !== google.maps.places.PlacesServiceStatus.OK) {
            console.error('Could not get details: status is ' + status);
            return;
        }

        getCity(result.geometry.location);
    });
}

/**
 * Remove all children of an element.
 *
 * @param   id  The id of the element.
 */
function clear(id) {
    const element = document.getElementById(id);
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

/**
 * Clear the DOM of previous search results.
 */
function reset() {
    const results = document.getElementById('results');
    results.hidden = true;

    clear('indicators');
    clear('sidebar');

    document.getElementById('loading-spinner').hidden = false;
}

form.addEventListener('submit', e => {
    e.preventDefault();
    reset();

    const place = autocomplete.getPlace(); // eslint-disable-line no-undef

    if (place === undefined || place.geometry === undefined) {
        const request = {
            componentRestrictions: restrictions,
            input: inputName.value,
            sessionToken: sessionToken
        };

        acService.getPlacePredictions(request, getTopLocation);
    } else {
        getCity(place.geometry.location);
    }
});
