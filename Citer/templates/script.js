function startProcess() {
    const circle = document.getElementById('progress-circle');
    const text = document.getElementById('progress-text');

    // Start the process and update progress animation
    text.innerText = 'Processing...';
    circle.style.background = 'conic-gradient(#0078D4 0%, #4ba4f3 50%, #a2cfff 75%, #f0f8ff 0%)';

    fetch('/run_all', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            text.innerText = 'Completed!';
            circle.style.background = 'conic-gradient(#32a852 0%, #85e089 75%, #f0f8ff 0%)';
        } else {
            text.innerText = 'Failed!';
            circle.style.background = 'conic-gradient(#a83232 0%, #e08585 75%, #f0f8ff 0%)';
        }
    })
    .catch(error => {
        text.innerText = 'Error!';
        circle.style.background = 'conic-gradient(#a83232 0%, #e08585 75%, #f0f8ff 0%)';
    });
}