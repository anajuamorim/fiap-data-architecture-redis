from .redis_client import get_client


def main() -> None:
    r = get_client()

    result = r.geosearch(
        "mindlink:geo:municipalities",
        member="São Paulo",
        radius=100,
        unit="km",
        withdist=True,
        sort="ASC",
    )

    print("Municípios em até 100 km de São Paulo:")
    for name, distance in result:
        print(f"- {name}: {distance} km")


if __name__ == "__main__":
    main()
