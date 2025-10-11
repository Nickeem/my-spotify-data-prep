import hvac

class VaultConfig:
    def __init__(self, vault_url, vault_token, verify_tls=True):
        self.VAULT_CLIENT = hvac.Client(
            url=vault_url,
            token=vault_token,
            verify=verify_tls,
        )

    def get_secret(self, path, key, mount_point):
        read_response = self.VAULT_CLIENT.secrets.kv.v2.read_secret_version(path=path, mount_point=mount_point)
        return read_response['data']['data'][key]
    
    def update_secret(self, path, key, value, mount_point):
        self.VAULT_CLIENT.secrets.kv.v2.patch(
            path=path,
            mount_point=mount_point,
            secret={key: value},
        )

