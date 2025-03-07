document.addEventListener('DOMContentLoaded', function() {
    // Get base path for the current environment
    const getBasePath = () => {
        const isDevServer = window.location.pathname.startsWith('/project/sandbox/user-workspace');
        return isDevServer ? '/project/sandbox/user-workspace' : '';
    };

    // Load components
    document.querySelectorAll('[data-include]').forEach(element => {
        const file = element.getAttribute('data-include');
        const basePath = getBasePath();
        
        fetch(`${basePath}/components/${file}.html`)
            .then(response => response.text())
            .then(html => {
                // Replace absolute paths with the correct base path
                const updatedHtml = html.replace(/href="\/([^"]*)"/g, (match, path) => {
                    return `href="${basePath}/${path}"`;
                });
                
                element.innerHTML = updatedHtml;
                
                // Execute any scripts in the component
                element.querySelectorAll('script').forEach(script => {
                    const newScript = document.createElement('script');
                    Array.from(script.attributes).forEach(attr => {
                        newScript.setAttribute(attr.name, attr.value);
                    });
                    newScript.textContent = script.textContent;
                    script.parentNode.replaceChild(newScript, script);
                });
            })
            .catch(error => console.error('Error loading component:', error));
    });
});
