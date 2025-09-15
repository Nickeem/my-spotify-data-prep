import hvac

class VaultConfig:
    def __init__(self, vault_url, vault_token):
        self.VAULT_CLIENT = hvac.Client(
            url=vault_url,
            token=vault_token,
        )

    def get_secret(self, path, key):
        read_response = self.VAULT_CLIENT.secrets.kv.v2.read_secret_version(path=path)
        return read_response['data']['data'][key]
    
    def update_secret(self, path, key, value):
        self.VAULT_CLIENT.secrets.kv.v2.patch(
            path=path,
            secret={key: value},
        )

