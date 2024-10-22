document.getElementById('login-form').onsubmit = async function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    if (data.success) {
        // ملء قائمة الصفحات
        const pages = data.pages; // افترض أن الرد يحتوي على الصفحات
        const dropdown = document.getElementById('page-dropdown');
        pages.forEach(page => {
            const option = document.createElement('option');
            option.value = page.id;
            option.textContent = page.name;
            dropdown.appendChild(option);
        });
        
        document.getElementById('page-selection').style.display = 'block';
    } else {
        alert('فشل تسجيل الدخول، تحقق من البيانات.');
    }
};

document.getElementById('start-bot').onclick = async function() {
    const selectedPage = document.getElementById('page-dropdown').value;

    const response = await fetch('/start-bot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ page: selectedPage })
    });

    const result = await response.json();
    if (result.success) {
        document.getElementById('output').innerHTML = "تم بدء البوت بنجاح.";
        document.getElementById('output').style.display = 'block';
    }
};
