import sys
import time

from .redis_client import get_client

CHANNEL = "mindlink:events"


def publish() -> None:
    r = get_client()
    message = "Indicadores atualizados"
    subscribers = r.publish(CHANNEL, message)
    print(f"Mensagem publicada em '{CHANNEL}'. Assinantes alcançados: {subscribers}")


def subscribe() -> None:
    r = get_client()
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL)
    print(f"Aguardando mensagens em '{CHANNEL}'...")

    deadline = time.time() + 30
    while time.time() < deadline:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            print("Mensagem recebida:", message["data"])
            return

    print("Nenhuma mensagem recebida nos últimos 30 segundos.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in {"publish", "subscribe"}:
        raise SystemExit("Use: python -m src.pubsub_demo publish|subscribe")

    if sys.argv[1] == "publish":
        publish()
    else:
        subscribe()
