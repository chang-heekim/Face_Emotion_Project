const cameraBtnEl = document.querySelector('body > div > button');
const camera = document.querySelector('body > div > .camera_comp .camera');
const recomendBtnEl = document.querySelector('body > div:nth-child(2) > a:nth-child(3)');

let isHide = true
cameraBtnEl.addEventListener('click', function() {
    isHide = !isHide
    if (isHide) {
        camera.classList.add('hide')
        cameraBtnEl.innerText = 'Turn On Camera'
        camera.setAttribute('src', 'http://127.0.0.1:8000/emotion_detector/off')
        recomendBtnEl.setAttribute('href', 'http://127.0.0.1:8000/emotion_detector/off/recomendation')
    } else {
        camera.classList.remove('hide')
        cameraBtnEl.innerText = 'Turn Off Camera'
        camera.setAttribute('src', 'http://127.0.0.1:8000/emotion_detector/on')
        recomendBtnEl.setAttribute('href', 'http://127.0.0.1:8000/emotion_detector/on/recomendation')
    }
});

// recomendBtnEl.addEventListener('click', function() {
//     if (isHide) {
//         recomendBtnEl.setAttribute('src', 'http://127.0.0.1:8000/emotion_detector/off/recomendation')
//     } else {
//         recomendBtnEl.setAttribute('src', 'http://127.0.0.1:8000/emotion_detector/on/recomendation')
//     }

// });