// scripts.js - Xử lý hiệu ứng và logic tương tác

document.addEventListener("DOMContentLoaded", function () {
    // Hiệu ứng chuyển trang khi bấm nút
    document.querySelectorAll("button").forEach((button) => {
        button.addEventListener("click", function () {
            let targetPage = this.getAttribute("data-target");
            if (targetPage) {
                window.location.href = targetPage;
            }
        });
    });

    // Kiểm tra mật khẩu đăng ký (chỉ nhận 6 số)
    let signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            let password = document.getElementById("password").value;
            let phone = document.getElementById("phone").value;
            if (!/^[0-9]{6}$/.test(password)) {
                alert("Mật khẩu phải có đúng 6 chữ số!");
                event.preventDefault();
            }
            if (!/^[0-9]+$/.test(phone)) {
                alert("Số điện thoại chỉ được chứa số!");
                event.preventDefault();
            }
        });
    }
});
