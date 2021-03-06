// Get Stripe publishable key
fetch("/memberships/config/")
.then((result) => {
    return result.json();
})
.then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler
    let submitBtn = document.querySelector("#submitBtnGold");
    if (submitBtn !== null) {
        submitBtn.addEventListener("click", () => {
            // Get Checkout Session ID
            fetch("/memberships/create-checkout-session/")
            .then((result) => { return result.json(); })
            .then((data) => {
                console.log(data);
                // Redirect to Stripe Checkout
                return stripe.redirectToCheckout({sessionId: data.sessionId})
            })
            .then((res) => {
                console.log(res);
            });
        });
    }
});
// fetch("/memberships/create-checkout-session/")

// Handle any errors returned from Checkout
// let handleResult = function (result) {
//     if (result.error) {
//         let displayError = document.getElementById("error-message");
//         displayError.textContent = result.error.message;
//     }
// };


