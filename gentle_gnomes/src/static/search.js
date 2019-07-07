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

function getURLParams(location) {
    location = location.toJSON();

    // Truncate to 6 decimal places
    for (const key in location) {
        location[key] = location[key].toFixed(6);
    }

    return new URLSearchParams(location);
}

function setURL(location) {
    const params = getURLParams(location);
    history.pushState(null, null, `/?${params}`);

    // Clear search box
    inputName.value = '';
}

function getCity(location) {
    const params = getURLParams(location);

    fetch(`/location?${params}`)
        .then(response => response.json())
        .then(getIndicators)
        .then(() => setURL(location))
        .catch(error => console.error(error));
}

function getIndicators(city) {
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

form.addEventListener('submit', e => {
    document.getElementById('loading-spinner').hidden = false;
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

    e.preventDefault();
});
