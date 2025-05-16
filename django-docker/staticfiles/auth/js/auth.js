

document.addEventListener('DOMContentLoaded', () => {
      (function () {
    const data = 'dfhgibugsdf';
    axios({
        method: 'POST',
        url: window.API_URLS.getToken,
        withCredentials: true,
        headers: {
            'Content-type': 'application/json'
        },
        data: {
            initData: window.INIT_DATA.initData
        }
    }).then(function (response) {
        console.log(response)
    }).catch(function (error) {
        if (error.response && error.response.status === 500) {
            window.location.replace(window.ERROR.error_authorization);
            alert('Требуется авторизация');
        } else {
            console.error('Ошибка:', error.message);
            if (error.response) {
                console.error('Данные ошибки:', error.response.data);
            }
        }
    });
})();
});


