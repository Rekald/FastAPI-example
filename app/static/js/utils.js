function download_file(url, file_name)
{
    fetch(url).then(resp => resp.blob()).then(blob => {
            if(!blob.size)
            {
                alert("Download failed");
                return;
            }
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = file_name;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
}

function get_json_ajax(method, url)
{
    let xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader("Content-Type", 'application/json');
    xhr.withCredentials = true;
    return xhr;
}
