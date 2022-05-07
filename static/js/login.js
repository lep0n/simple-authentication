document.addEventListener("DOMContentLoaded", function () {
    let button = document.querySelector('input[type=submit]');
    button.addEventListener('click', async function (event) {
        event.preventDefault();

        let username = document.querySelector('input[name=username]').value;
        let password = document.querySelector('input[name=password]').value;

        if (username && password) {

            let response = await fetch('/account', {
                method: "POST",
                body: new FormData(document.querySelector('form')),
            });

            let response_json = await response.json();

            if (response_json.success) {
                window.location.reload();
            }
            else {
                let error = document.querySelector('.error-text');
                error.innerHTML = response_json.msg;
            }
        }
        else {
            let error = document.querySelector('.error-text');
            error.innerHTML = "Username or password is empty";
        }
    });
});
