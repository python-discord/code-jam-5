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

function setLocation(location) {
    const formData = new FormData(form);
    formData.set('location', JSON.stringify(location));

    fetch(form.getAttribute('action'), {
        method: 'POST',
        body: formData
    })
        .then(response => response.text())
        .then(response => {
            document.getElementById('results').innerHTML = response;
        })
        .catch(error => console.log('Error submitting form: ', error));
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

        setLocation(result.geometry.location);
    });
}

form.addEventListener('submit', e => {
    const place = autocomplete.getPlace(); // eslint-disable-line no-undef

    if (place === undefined) {
        const request = {
            componentRestrictions: restrictions,
            input: inputName.value,
            sessionToken: sessionToken
        };

        acService.getPlacePredictions(request, getTopLocation);
    } else {
        setLocation(place.geometry.location);
    }

    e.preventDefault();
});
