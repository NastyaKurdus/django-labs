(async () => {

    const table = document.createElement('table')
    const thead = document.createElement('thead')
    const tbody = document.createElement('tbody')

    const addRow = (values, parElem) => {
        const trElem = document.createElement('tr')
        values.forEach((value) => {
            const tdElem = document.createElement('td')
            const preElem = document.createElement('pre')
            tdElem.appendChild(preElem)
            preElem.appendChild(document.createTextNode(value))
            trElem.appendChild(tdElem)
        })
        parElem.appendChild(trElem)
    }
    const fetchJson = async (url, options) => {
        try {
            return await fetchWithError(url,
                {
                    method: 'POST',
                    ...options,
                    headers: {
                        ...options.headers,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(options.body)
                })
        } catch (e) {
            console.log('Error: ' + e + ' has been occured in ' + url + " Return 'null' response by default.")
            return null
        }
    }

    const fetchWithError = async (url, options) => {
        url = 'http://127.0.0.1:8000/api/' + url
        const response = await fetch(url, options)
        if (response && !response.ok) {
            console.log('Error has been occurred in ' + url + ' . Status: ' + response.status)
        }
        return response
    }

    const registerUser = async (username) => {
        return await fetchJson('auth/users/',
            {
                body: {
                    email: username + '@test.com',
                    password: '1234',
                    username: username,
                    sex: 'M'
                }
            })
    }

    const loginUser = async (username) => {
        const response = await fetchJson('auth/token/login/',
            {
                body: {
                    'email': username + "@test.com",
                    'password': '1234'
                }
            })
        return response && (await response.json())['auth_token']
    }

    const removeUser = async (token) => {
        if (token) {
            return await fetchJson('auth/users/me/',
                {
                    method: 'DELETE',
                    headers: {
                        'Authorization': 'Token ' + token
                    },
                    body: {
                        'current_password': '1234'
                    }
                })
        }
    }
    const createSocket = async (username, token, url) => {
        return new Promise((resolve, reject) => {
            const socket = new WebSocket('ws://127.0.0.1:8000/ws/' + url)
            socket.onopen = () => {
                console.log(`[${username}.open]: Connection established`);
                socket.send(JSON.stringify({'type': 'auth', 'token': token}))
                resolve(socket)
            }
            socket.onmessage = (event) => {
                const data = JSON.parse(event.data)
                console.log(`[${username}.message]: ${event.data}.`);
                if (data.type === 'success' || data.type === 'error') {
                    addRow(
                        [data.taskId, data.taskName, data.taskArgs, JSON.stringify(data.text || data.result, null, 2), data.finishTime],
                        tbody)
                }
            }
            socket.onclose = (event) => {
                if (event.wasClean) {
                    console.log(`[${username}.close] Clean close.`);
                } else {
                    console.log(`[${username}.close] Connection interrupted.`);
                }
            }
            socket.onerror = (error) => {
                console.log(`[${username}.error]: ${error.message}.`);
            }
            socket.onerror = error => reject(error);
        })
    }

    document.body.appendChild(table)
    table.append(thead, tbody)
    addRow(['Task id', 'Task name', 'Args', 'Result', 'Finish time'], thead)
    const testUser = 'user'
    await removeUser(await loginUser(testUser))
    await registerUser(testUser)
    const token = await loginUser(testUser)
    await createSocket(testUser, token, 'tasks/')
    const response1 = await fetchJson('emails/', {
        headers: {
            'Authorization': 'Token ' + token
        },
        body: ['nkurdus33@gmail.com']
    })
    console.log('[Response]:', response1 && (await response1.text()))
    const response2 = await fetchWithError('info/',
        {
            headers: {
                'Authorization': 'Token ' + token
            }
        })
    console.log('[Response]:', response2 && (await response2.text()))
})();

