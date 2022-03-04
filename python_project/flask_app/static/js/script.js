// API Key
const key1 = "531131cf5eea0fcb24214354395c2b33";

// Get Weather information from API
function getWeather() {

    let latitude, longitude;

    // Use api to get lat/long
    let cityInput = document.getElementById("cityInput");
    let api = 'http://api.openweathermap.org/geo/1.0/direct?q=' + cityInput.value + '&appid=531131cf5eea0fcb24214354395c2b33';

    fetch(api)
        .then(response => response.json())
        .then(data => {
            // console.log(data)
            // console.log(data[0])
            // console.log(data[0].lat)
            // console.log(data[0].lon)
            latitude = data[0].lat;
            longitude = data[0].lon;

            // Save lat/long, input into weather api
            return fetch(`https://api.openweathermap.org/data/2.5/onecall?lat=${latitude}&lon=${longitude}&units=imperial&exclude=minutely,%20alerts&appid=${key1}`)
                .then(response => response.json())
                .then(data => {
                    // console.log(data)
                    // console.log(data.daily)
                    // console.log(data.daily[0].temp.day)

                    // Get time

                    for (i = 0; i < 5; i++) {
                        document.getElementById("day" + (i + 1)).innerHTML = convertTime(Number(data.daily[i].dt));
                    }

                    // Get description
                    for (i = 0; i < 5; i++) {
                        document.getElementById("description" + (i + 1)).innerHTML = data.daily[i].weather[0].description;
                    }

                    // Get temp

                    for (i = 0; i < 5; i++) {
                        document.getElementById("day" + (i + 1) + "temp").innerHTML = Number(data.daily[i].temp.day).toFixed(0) + "°F";
                    }
                    // Get min temp s

                    for (i = 0; i < 5; i++) {
                        document.getElementById("day" + (i + 1) + "tempMin").innerHTML = "L: " + Number(data.daily[i].temp.min).toFixed(0) + "°F";
                    }
                    // Get max temp

                    for (i = 0; i < 5; i++) {
                        document.getElementById("day" + (i + 1) + "tempMax").innerHTML = "H: " + Number(data.daily[i].temp.max).toFixed(0) + "°F";
                    }

                    // Get humidity
                    for (i = 0; i < 5; i++) {
                        document.getElementById("humidity" + (i + 1)).innerHTML = "Humidity: " + data.daily[i].humidity;
                    }

                    // Get wind speed
                    for (i = 0; i < 5; i++) {
                        document.getElementById("windspeed" + (i + 1)).innerHTML = "Wind Speed: " + Number(data.daily[i].wind_speed).toFixed(0) + "mph";
                    }

                    // Get weather icons
                    for (i = 0; i < 5; i++) {
                        let str_icon = data.daily[i].weather[0].icon;
                        document.getElementById("img" + (i + 1)).src = "/static/img/" + str_icon + ".png";
                    }
                })
        })
}

// Convert UTC to Day

function convertTime(dt) {
    let date = new Date(dt * 1000);
    let day = date.getDay();
    let weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    let formatted_time = weekday[day];
    return formatted_time

}



