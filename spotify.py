import tekore as tk

client_id, client_secret, redirect_uri = tk.config_from_file(".env")

token = tk.request_client_token(client_id, client_secret) # // tk.prompt_for_user_token(client_id, client_secret, redirect_uri)

