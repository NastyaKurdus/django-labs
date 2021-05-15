(() => {
    const fetchJson = async (url, options) => {
        try {
            return await fetchWithError(url,
                {
                    ...options,
                    headers: {
                        ...options.headers,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(options.body)
                })
        } catch (e) {
            console.log('Error has been occurred in ' + url + " Return 'null' response by default.")
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
                method: 'POST',
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
                method: 'POST',
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
                console.log(`[${username}.message]: ${event.data}.`);
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

    const printOnlineUsers = async (token) => {
        const onlineUsers = await fetchWithError('online-users/',
            {
                headers:
                    {
                        'Authorization': 'Token ' + token
                    }
            })
        console.log('online', await onlineUsers.json())
    }

    const getTokens = async (usernames) => {
        return await Promise.all(usernames.map(loginUser))
    }

    const testWebsockets = async (...usernames) => {
        await Promise.all((await getTokens(usernames)).map(removeUser))
        await Promise.all(usernames.map(registerUser))
        const tokens = await getTokens(usernames)
        await createSocket(usernames[0], tokens[0], 'calculator/room1/')
        await printOnlineUsers(tokens[0])
        const socket2 = await createSocket(usernames[0], tokens[0], 'calculator/room1/')
        await printOnlineUsers(tokens[1])
        const socket3 = await createSocket(usernames[1], tokens[1], 'calculator/room1/')
        await createSocket(usernames[2], tokens[2], 'calculator/room1/')
        const wrongSocket = await createSocket('wrongUser', 'wrongToken', 'calculator/room1/')
        await printOnlineUsers(tokens[1])
        const testData = JSON.stringify({
            'type': 'data',
            'variables': {'a': 1}
        })
        socket3.send(testData)
        wrongSocket.send(testData)
        socket3.close()
        await printOnlineUsers(tokens[1])
        socket2.close()
        await printOnlineUsers(tokens[1])
    }

    testWebsockets('user1', 'user2', 'user3')

})();

