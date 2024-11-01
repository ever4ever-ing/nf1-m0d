// app.js
document.addEventListener('DOMContentLoaded', (event) => {

    // Validación del formulario
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => {
            const nombre = document.getElementById('nombre').value;
            const tipo = document.getElementById('tipo').value;
            const color = document.getElementById('color').value;

            if (!nombre || !tipo || !color) {
                e.preventDefault();
                alert('Por favor, rellena todos los campos');
            } else {
                alert('¡Mascota registrada con éxito!');
            }
        });
    }

    // Efecto hover en los botones de navegación
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('mouseover', () => {
            link.style.transform = 'scale(1.1)';
        });
        link.addEventListener('mouseout', () => {
            link.style.transform = 'scale(1)';
        });
    });
});