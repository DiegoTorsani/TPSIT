(function () {
    var apiBase = '/gestionale_utenti/users/';
    var usersTableBody = document.getElementById('usersTableBody');
    var createForm = document.getElementById('createForm');
    var editForm = document.getElementById('editForm');
    var detailBox = document.getElementById('detailBox');
    var messageBox = document.getElementById('messageBox');
    var searchInput = document.getElementById('searchInput');
    var searchButton = document.getElementById('searchButton');
    var resetButton = document.getElementById('resetButton');

    function showMessage(text, isError) {
        messageBox.className = isError ? 'message-box error' : 'message-box success';
        messageBox.innerHTML = text;
    }

    function clearMessage() {
        messageBox.className = 'message-box';
        messageBox.innerHTML = '';
    }

    function validateText(value) {
        return /^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,40}$/.test(value);
    }

    function validateDate(value) {
        return /^\d{4}-\d{2}-\d{2}$/.test(value);
    }

    function readFormData(form) {
        return {
            nome: form.nome.value.replace(/^\s+|\s+$/g, ''),
            cognome: form.cognome.value.replace(/^\s+|\s+$/g, ''),
            data_nascita: form.data_nascita.value,
            mansione: form.mansione.value.replace(/^\s+|\s+$/g, '')
        };
    }

    function validatePayload(payload) {
        if (!validateText(payload.nome)) {
            return 'Nome non valido';
        }
        if (!validateText(payload.cognome)) {
            return 'Cognome non valido';
        }
        if (!validateText(payload.mansione)) {
            return 'Mansione non valida';
        }
        if (!validateDate(payload.data_nascita)) {
            return 'Data di nascita non valida';
        }
        return '';
    }

    function request(method, url, body, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) {
                return;
            }
            var response = null;
            try {
                response = xhr.responseText ? JSON.parse(xhr.responseText) : null;
            } catch (e) {
                response = null;
            }
            callback(xhr.status, response);
        };
        xhr.send(body ? JSON.stringify(body) : null);
    }

    function renderDetail(user) {
        if (!user) {
            detailBox.innerHTML = 'Seleziona un utente dalla lista.';
            return;
        }
        detailBox.innerHTML =
            '<p><strong>ID:</strong> ' + user.id + '</p>' +
            '<p><strong>Nome:</strong> ' + user.nome + '</p>' +
            '<p><strong>Cognome:</strong> ' + user.cognome + '</p>' +
            '<p><strong>Data di nascita:</strong> ' + user.data_nascita + '</p>' +
            '<p><strong>Mansione:</strong> ' + user.mansione + '</p>';
    }

    function fillEditForm(user) {
        editForm.id.value = user.id;
        editForm.nome.value = user.nome;
        editForm.cognome.value = user.cognome;
        editForm.data_nascita.value = user.data_nascita;
        editForm.mansione.value = user.mansione;
    }

    function loadUsers(query) {
        var url = apiBase;
        if (query) {
            url += '?q=' + encodeURIComponent(query);
        }
        request('GET', url, null, function (status, response) {
            if (status !== 200) {
                showMessage('Errore nel caricamento della lista utenti.', true);
                return;
            }
            renderTable(response.users || []);
        });
    }

    function renderTable(users) {
        var rows = [];
        var i;
        for (i = 0; i < users.length; i++) {
            rows.push(
                '<tr>' +
                '<td>' + users[i].id + '</td>' +
                '<td>' + users[i].nome + '</td>' +
                '<td>' + users[i].cognome + '</td>' +
                '<td>' + users[i].data_nascita + '</td>' +
                '<td>' + users[i].mansione + '</td>' +
                '<td>' +
                '<button type="button" data-action="detail" data-id="' + users[i].id + '">Dettaglio</button>' +
                '<button type="button" data-action="delete" data-id="' + users[i].id + '" class="danger">Elimina</button>' +
                '</td>' +
                '</tr>'
            );
        }
        usersTableBody.innerHTML = rows.join('');
        if (!users.length) {
            usersTableBody.innerHTML = '<tr><td colspan="6">Nessun utente presente.</td></tr>';
        }
    }

    usersTableBody.addEventListener('click', function (event) {
        var target = event.target;
        if (target.tagName !== 'BUTTON') {
            return;
        }
        var userId = target.getAttribute('data-id');
        var action = target.getAttribute('data-action');

        if (action === 'detail') {
            request('GET', apiBase + userId, null, function (status, response) {
                if (status === 200) {
                    renderDetail(response.user);
                    fillEditForm(response.user);
                    showMessage('Dettaglio utente caricato.', false);
                } else if (status === 404) {
                    showMessage('Utente non trovato.', true);
                } else {
                    showMessage('Errore nel caricamento del dettaglio.', true);
                }
            });
            return;
        }

        if (action === 'delete') {
            if (!window.confirm('Eliminare l\'utente selezionato?')) {
                return;
            }
            request('DELETE', apiBase + userId, null, function (status) {
                if (status === 200) {
                    showMessage('Utente eliminato con successo.', false);
                    renderDetail(null);
                    editForm.reset();
                    loadUsers(searchInput.value);
                } else if (status === 404) {
                    showMessage('Utente non trovato.', true);
                } else {
                    showMessage('Impossibile eliminare l\'utente.', true);
                }
            });
        }
    });

    createForm.addEventListener('submit', function (event) {
        event.preventDefault();
        clearMessage();
        var payload = readFormData(createForm);
        var validationError = validatePayload(payload);
        if (validationError) {
            showMessage(validationError, true);
            return;
        }

        request('POST', apiBase, payload, function (status, response) {
            if (status === 201) {
                showMessage('Utente creato con ID ' + response.user.id + '.', false);
                createForm.reset();
                loadUsers(searchInput.value);
            } else if (status === 400) {
                showMessage(response && response.error ? response.error : 'Richiesta errata.', true);
            } else {
                showMessage('Errore durante l\'inserimento.', true);
            }
        });
    });

    editForm.addEventListener('submit', function (event) {
        event.preventDefault();
        clearMessage();
        if (!editForm.id.value) {
            showMessage('Seleziona prima un utente dalla lista.', true);
            return;
        }

        var payload = readFormData(editForm);
        var validationError = validatePayload(payload);
        if (validationError) {
            showMessage(validationError, true);
            return;
        }

        request('PUT', apiBase + editForm.id.value, payload, function (status, response) {
            if (status === 200) {
                showMessage('Utente aggiornato con successo.', false);
                renderDetail(response.user);
                loadUsers(searchInput.value);
            } else if (status === 404) {
                showMessage('Utente non trovato.', true);
            } else {
                showMessage('Errore durante la modifica.', true);
            }
        });
    });

    searchButton.addEventListener('click', function () {
        loadUsers(searchInput.value);
    });

    resetButton.addEventListener('click', function () {
        searchInput.value = '';
        loadUsers('');
    });

    loadUsers('');
}());