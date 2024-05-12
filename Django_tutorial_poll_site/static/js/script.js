document.addEventListener('DOMContentLoaded', () => {
    // console.log("hello");
    document.body.addEventListener('click', (event) => {
        if (event.target.tagName === 'A' && event.target.classList.contains('async-link')) {
            // console.log("success");
            event.preventDefault();
            const url = event.target.href;
            fetch(url)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error(`HTTP error: ${response.status}`);
                    }
                    return response.text()
                })
                .then((html) => {
                    // console.log(html);
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#content-placeholder');
                    const currentContent = document.querySelector('#content-placeholder');
                    if (newContent && currentContent) {
                        currentContent.innerHTML = newContent.innerHTML;
                        history.pushState({ path: url }, '', url); // URLを更新
                    }
                })
                .catch(error => console.error('Failed to fetch:', error));
        }
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     // リンクに対する非同期処理
//     document.body.addEventListener('click', function(event) {
//         if (event.target.tagName === 'A' && event.target.classList.contains('async-link')) {
//             event.preventDefault();
//             const url = event.target.href;
//             fetchContent(url);
//         }
//     });

//     // フォームに対する非同期処理
//     document.body.addEventListener('submit', function(event) {
//         if (event.target.tagName === 'FORM' && event.target.classList.contains('async-form')) {
//             event.preventDefault();
//             const url = event.target.action;
//             const method = event.target.method;
//             const formData = new FormData(event.target);
//             fetch(url, {
//                 method: method,
//                 body: formData,
//                 headers: {
//                     'X-CSRFToken': formData.get('csrfmiddlewaretoken')  // CSRFトークンを追加
//                 }
//             }).then(response => response.text())
//               .then(html => updateContent(html, url))
//               .catch(error => console.error('Failed to fetch:', error));
//         }
//     });
// });

// function fetchContent(url) {
//     fetch(url)
//         .then(response => response.text())
//         .then(html => updateContent(html, url))
//         .catch(error => console.error('Failed to fetch:', error));
// }

// function updateContent(html, url) {
//     const parser = new DOMParser();
//     const doc = parser.parseFromString(html, 'text/html');
//     const newContent = doc.querySelector('main');
//     const currentContent = document.getElementById('content-placeholder');
//     if (newContent && currentContent) {
//         currentContent.innerHTML = newContent.innerHTML;
//         history.pushState({ path: url }, '', url); // URLを更新
//     }
// }
