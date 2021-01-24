// If a fetch error occurs, log it to the console and show it in the UI.
var handleFetchResult = function(result) {
  if (!result.ok) {
    return result.json().then(function(json) {
      if (json.error && json.error.message) {
        throw new Error(result.url + ' ' + result.status + ' ' + json.error.message);
      }
    }).catch(function(err) {
      showErrorMessage(err);
      throw err;
    });
  }
  return result.json();
};

// Create a Checkout Session with the selected plan ID
var createCheckoutSession = function(priceId) {
  return fetch("/create-checkout-session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      priceId: priceId
    })
  }).then(handleFetchResult);
};

// Handle any errors returned from Checkout
var handleResult = function(result) {
  if (result.error) {
    showErrorMessage(result.error.message);
  }
};

var showErrorMessage = function(message) {
  var errorEl = document.getElementById("error-message")
  errorEl.textContent = message;
  errorEl.style.display = "block";
};

/* Get your Stripe publishable key to initialize Stripe.js */
fetch("/setup")
  .then(handleFetchResult)
  .then(function(json) {
    var publishableKey = json.publishableKey;

    var jpyPriceId = json.jpyPriceId;
    var usdPriceId = json.usdPriceId;

    var stripe = Stripe(publishableKey);
    // // Setup event handler to create a Checkout Session when button is clicked
    // createCheckoutSession(basicPriceId).then(function (data) {
    //   // Call Stripe.js method to redirect to the new Checkout page
    //   stripe
    //     .redirectToCheckout({
    //       sessionId: data.sessionId
    //     })
    //     .then(handleResult);
    // });    
    
    
    document
      .getElementById("add_card_info")
      .addEventListener("click", function (evt) {
        let liveOutsideJapan = document.getElementById("live_outside_of_japan").checked
        if (liveOutsideJapan == true) {
          priceId = usdPriceId;
        }else{
          priceId = jpyPriceId;
        }
    
        createCheckoutSession(priceId).then(function (data) {
          // Call Stripe.js method to redirect to the new Checkout page
          stripe
            .redirectToCheckout({
              sessionId: data.sessionId
            })
            .then(handleResult);
        });
      });
      
    // document.addEventListener("DOMContentLoaded", function (evt) {
    //   createCheckoutSession(basicPriceId).then(function (data) {
    //     // Call Stripe.js method to redirect to the new Checkout page
    //     stripe
    //       .redirectToCheckout({
    //         sessionId: data.sessionId
    //       })
    //       .then(handleResult);
    //   });
    // });

  });
