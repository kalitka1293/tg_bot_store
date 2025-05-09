

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
    })
})();
});

