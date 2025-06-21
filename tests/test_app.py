from bs4 import BeautifulSoup

def test_main_redirect_to_home(client):
    """
    Test that the root URL '/' redirects to the '/home' route.
    """
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/home'

def test_home_get(client):
    """Test that the '/home' route loads successfully with GET request."""
    response = client.get('/home')
    assert response.status_code == 200
    assert b"Hello World!" in response.data
    # You might also check for other elements in your 'home.html'

def test_home_post_valid_prompt(client):
    """Test a valid POST request to /home, including CSRF token handling."""

    # --- STEP 1: Make a GET request to obtain the CSRF token and set the session ---
    get_response = client.get('/home')
    assert get_response.status_code == 200

    # --- STEP 2: Parse the HTML to extract the CSRF token ---
    soup = BeautifulSoup(get_response.data, 'html.parser')
    csrf_token_tag = soup.find('input', {'name': 'csrf_token'})

    # Assert that the CSRF token field was found in the HTML
    assert csrf_token_tag is not None, "CSRF token input field not found in the HTML."

    csrf_token = csrf_token_tag.get('value') #type: ignore
    assert csrf_token is not None, "CSRF token value not found."

    # --- STEP 3: Perform the POST request with the extracted CSRF token ---
    response = client.post(
        '/home',
        data={
            'csrf_token': csrf_token, # <--- THIS IS THE KEY ADDITION
            'prompt': 'Test prompt from Pytest',
            'submit_chatAI': 'chatAI'
        },
        follow_redirects=True # Follow redirects if your view redirects after POST
    )

    # --- STEP 4: Assertions ---
    assert response.status_code == 200

    # The expected success message (Flask flashes are HTML escaped by default) [&#34; means " symbol]
    assert b"Sent prompt: &#34;Test prompt from Pytest&#34; to the AI." in response.data

    # You might also want to assert that the chat_reply or prompt_list is updated.
    # For example:
    # assert b"No AI response yet. Type a prompt to get started!" not in response.data
    # assert b"This is a mocked AI response for Test prompt from Pytest" in response.data # If you were mocking main_func

def test_home_post_empty_prompt(client):
    """Test an empty POST request to /home (form validation)."""
    response = client.post(
        '/home',
        data={'prompt': '', 'submit_chatAI': 'chatAI'}
    )
    assert response.status_code == 200 # Still 200 because it re-renders the page
    assert b"Chat Prompt validation failed. Please enter something." in response.data
