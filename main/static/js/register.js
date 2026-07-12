document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("profile_picture");
    const preview = document.getElementById("preview-image");
    const fileName = document.getElementById("file-name");

    input.addEventListener("change", function () {

        if (this.files && this.files[0]) {

            const file = this.files[0];

            fileName.textContent = file.name;

            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
            };

            reader.readAsDataURL(file);

        } else {

            preview.src = "/static/images/default-profile.png";
            fileName.textContent = "No file selected";

        }

    });

});