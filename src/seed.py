from .redis_client import get_client

MUNICIPALITIES = [
    {
        "ibge": "3550308",
        "name": "São Paulo",
        "admissions": 1280,
        "deaths": 74,
        "risk_score": 91,
        "lat": -23.5505,
        "lon": -46.6333,
    },
    {
        "ibge": "3509502",
        "name": "Campinas",
        "admissions": 690,
        "deaths": 31,
        "risk_score": 72,
        "lat": -22.9056,
        "lon": -47.0608,
    },
    {
        "ibge": "3525904",
        "name": "Jundiaí",
        "admissions": 410,
        "deaths": 19,
        "risk_score": 64,
        "lat": -23.1857,
        "lon": -46.8845,
    },
    {
        "ibge": "3547809",
        "name": "Santo André",
        "admissions": 520,
        "deaths": 27,
        "risk_score": 68,
        "lat": -23.6639,
        "lon": -46.5383,
    },
]

DIAGNOSES = {"F00", "F01", "F02", "F03", "G30"}

EVENTS = [
    "Atualização da competência 2025-10",
    "Validação de município",
    "Atualização do ranking territorial",
    "Reprocessamento de indicadores",
]


def seed() -> None:
    r = get_client()
    r.ping()

    # String: status da camada Redis.
    r.set("mindlink:status", "online")

    # Hash: um pequeno objeto por município.
    for municipality in MUNICIPALITIES:
        key = f"mindlink:municipality:{municipality['ibge']}"
        r.hset(
            key,
            mapping={
                "name": municipality["name"],
                "admissions": municipality["admissions"],
                "deaths": municipality["deaths"],
                "risk_score": municipality["risk_score"],
            },
        )

    # List: eventos mais recentes.
    r.delete("mindlink:events:recent")
    r.rpush("mindlink:events:recent", *EVENTS)

    # Set: conjunto sem duplicidade.
    r.delete("mindlink:diagnoses")
    r.sadd("mindlink:diagnoses", *DIAGNOSES)

    # Sorted Set: ranking por score.
    r.delete("mindlink:ranking:risk")
    for municipality in MUNICIPALITIES:
        r.zadd(
            "mindlink:ranking:risk",
            {municipality["name"]: municipality["risk_score"]},
        )

    # GEO: localização dos municípios.
    r.delete("mindlink:geo:municipalities")
    for municipality in MUNICIPALITIES:
        r.geoadd(
            "mindlink:geo:municipalities",
            (municipality["lon"], municipality["lat"], municipality["name"]),
        )

    # Cache com expiração de 60 segundos.
    r.set("mindlink:cache:summary", "4 municípios | 2860 internações | risco agregado 73", ex=60)

    print("Redis populado com sucesso.")


if __name__ == "__main__":
    seed()
