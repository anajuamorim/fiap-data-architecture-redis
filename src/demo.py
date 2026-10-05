from .redis_client import get_client


def main() -> None:
    r = get_client()
    print("PING:", r.ping())

    print("\n1) STRING")
    print("status =", r.get("mindlink:status"))

    print("\n2) HASH")
    print("São Paulo =", r.hgetall("mindlink:municipality:3550308"))

    print("\n3) LIST")
    print("eventos =", r.lrange("mindlink:events:recent", 0, -1))

    print("\n4) SET")
    print("diagnósticos =", sorted(r.smembers("mindlink:diagnoses")))

    print("\n5) SORTED SET")
    ranking = r.zrevrange("mindlink:ranking:risk", 0, -1, withscores=True)
    print("ranking =", ranking)

    print("\n6) CACHE + TTL")
    print("cache =", r.get("mindlink:cache:summary"))
    print("ttl =", r.ttl("mindlink:cache:summary"), "segundos")

    print("\n7) CONTADOR ATÔMICO")
    r.set("mindlink:metrics:views", 0)
    print("view 1 =", r.incr("mindlink:metrics:views"))
    print("view 2 =", r.incr("mindlink:metrics:views"))

    print("\nDemonstração concluída.")


if __name__ == "__main__":
    main()
