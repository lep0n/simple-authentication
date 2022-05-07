document.addEventListener("DOMContentLoaded", function () {
    let button = document.querySelector('input[type=submit]');
    button.addEventListener('click', async function (event) {
        event.preventDefault();

        let username = document.querySelector('input[name=username]').value;
        let password = document.querySelector('input[name=password]').value;
        let confirm_password = document.querySelector('input[name=confirm_password]').value;

        if (username && password && confirm_password) {
            let response = await fetch('/register', {
                method: "POST",
                body: new FormData(document.querySelector('form')),
            });

            let response_json = await response.json();

            if (response_json.success) {
                let success = document.querySelector('.success-text');
                success.innerHTML = response_json.msg;
                setTimeout(() => { window.location.replace("/login") }, 2000);
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