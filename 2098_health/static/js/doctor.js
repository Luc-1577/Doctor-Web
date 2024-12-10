// Alterna a exibição da barra lateral
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}

// Troca o conteúdo exibido na área principal
function showContent(sectionId) {
    const contents = document.querySelectorAll('.content');
    contents.forEach(content => content.classList.remove('active'));

    const section = document.getElementById(sectionId);
    section.classList.add('active');

    setTimeout(() => {
        toggleSidebar();
    }, 500);
}




document.addEventListener('DOMContentLoaded', () => {
    const completedAppointments = JSON.parse(localStorage.getItem('completedAppointments')) || [];

    // Ocultar linhas marcadas como concluídas
    completedAppointments.forEach(id => {
        const row = document.querySelector(`tr[data-id='${id}']`);
        if (row) row.style.display = 'none';
    });
});

function markAsDone(id) {
    const row = document.querySelector(`tr[data-id='${id}']`);
    if (row) {
        // Ocultar a linha
        row.style.display = 'none';
    }
} 