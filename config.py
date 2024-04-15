from dataclasses import dataclass

@dataclass
class Config:
    tg_api: str
    db_url: str
    yandex_api_key: str
    yandex_cloud_catalog: str

config = Config(
    tg_api="6547749986:AAHL9BXMmOlSZ0aQtxFgqIqX0LR4DDTlJWU",
    db_url="postgresql+asyncpg://kandev:kandev@127.0.0.1:5432/kandev",
    yandex_api_key="AQVNyJRotHlHIhGec5YfWrslmo8tsbsc8eatOf_V",
    yandex_cloud_catalog="b1glihj9h7pkj7mnd6at")
