function searchUsers() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    
    searchTable('usersTable', filter);
}

function searchTable(tableId, filter) {
    const table = document.getElementById(tableId);
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const name = rows[i].getElementsByTagName('td')[0];
        const email = rows[i].getElementsByTagName('td')[1];
        if (name || email) {
            const nameText = name.textContent || name.innerText;
            const emailText = email.textContent || email.innerText;
            if (nameText.toLowerCase().indexOf(filter) > -1 || 
                emailText.toLowerCase().indexOf(filter) > -1) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
}