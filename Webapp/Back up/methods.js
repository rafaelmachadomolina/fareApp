//Execute API function
async function executeAPI(raw) {
  // Create header
  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
  };

  //Call API
  var obj;

  const predicted_price_json = await fetch("https://6ckm3i3zb1.execute-api.eu-west-2.amazonaws.com/production", requestOptions);
  const response = await predicted_price_json.json()
  return response;

};

// define the callAPI function that takes a first name and last name as parameters
async function callAPI() {

    // Disable button
    document.getElementById("button_estimate").disabled = true;

    // Read features
    var bedrooms = document.getElementById("bedrooms").value;
    var bathroom_number = document.getElementById("bathroom_number").value;
    var postcode = document.getElementById("postcode").value;
    var total_amenities = document.getElementById("total_amenities").value;
    var accommodates = document.getElementById("accommodates").value;
    var min_nights = document.getElementById("min_nights").value;
    var customer_name = document.getElementById("customer_name").value;
    var ocupation_days = document.getElementById("ocupation_days").value;
    var seniority = document.getElementById("seniority").value;
    var host_total_listings = document.getElementById("host_total_listings").value;

    try {
      var room_type = document.querySelector('input[name="room_type"]:checked').value;
    }
    catch(err) {
      console.log("You must select room type");
      document.getElementById("button_estimate").disabled = false;
      alert("You must select room type");
      return "";

    }

    // Check if some feature is empty
    const list = [bedrooms, bathroom_number, room_type, postcode,
        total_amenities, accommodates, min_nights, customer_name,
        ocupation_days, seniority, host_total_listings];

    if(list.includes("") == true) {
      console.log("All values must be registered");
      document.getElementById("button_estimate").disabled = false;
      alert("All values must be registered");
      return "";
    }

    var raw = JSON.stringify({"bedrooms": bedrooms,
        "bathroom_number": bathroom_number,
        "postcode": postcode,
        "total_amenities": total_amenities,
        "accommodates": accommodates,
        "min_nights": min_nights,
        "customer_name": customer_name,
        "customer_name": customer_name,
        "ocupation_days": ocupation_days,
        "seniority": seniority,
        "host_total_listings": host_total_listings,
        "room_type": room_type});

    const predicted_fare_json = await executeAPI(raw);
    var predicted_fare_dict = JSON.parse(predicted_fare_json)

    if(predicted_fare_dict["statusCode"] == 200) {
      var predicted_fare = predicted_fare_dict["body"];
      var pound = "£";
      var predicted_fare_text = pound.concat(predicted_fare);
      console.log(predicted_fare_text);
      document.getElementById("fare_per_night").value = predicted_fare_text;
    }
    else {
      console.log("There was an error calling the API");
      alert("There was an error calling the API");
    };

}

//Reset variables in form
function resetValues() {

  document.getElementById("form_all_fields").reset();
  document.getElementById("form_result").reset();
  console.log("All values erased.");
  document.getElementById("button_estimate").disabled = false;

}
