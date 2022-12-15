import asyncio
from aiohttp import ClientSession
from aiohttp_proxy import ProxyConnector
from fake_useragent import FakeUserAgent
from loguru import logger
from sys import stderr
from itertools import cycle
from time import sleep
from typing import Union


URL: str = "https://api.sendinblue.com/v3/contacts"

COUNT_OF_PROCESSES: int = 10
TIME_DELTA: int = .5
EMAILS_FILE_NAME: str = "emails.txt"
PROXIES_FILE_NAME: str = "proxies.txt"
OUTPUT_FILE_NAME: str = "output.txt"

logger.remove()
logger.add(stderr,
           format="<white>{time:HH:mm:ss}</white> | "
                  "<level>[{level}]</level> | "
                  "<white>{message}</white>")

headers = {
    "User-Agent": FakeUserAgent().random,
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "api-key": "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",
    "Referer": "https://krowdz.io/",
    "Content-Type": "application/json",
    "Origin": "https://krowdz.io",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers"
}


def get_file_data(file_name: str) -> list[str]:
    """Gets data from the file"""
    with open(file_name, "r") as file:
        return [line.rstrip() for line in file]


def save_email(email: str) -> None:
    """Save email to the file"""
    with open("output.txt", "a") as f:
        f.write(f"{email}\n")


async def get_request(email: str, proxy: Union[str, None] = None) -> bool:
    """Makes request to Phantom API"""
    async with ClientSession(headers=headers, connector=ProxyConnector.from_url(proxy)) as session:
        json = {
            "email": email,
            "updateEnabled": False
        }
        async with session.post(URL, json=json) as response:
            if response.status == 200 or response.status == 201:
                logger.success(f"[{str(response.status)}] {email} was successfully registered!")
                return True
            else:
                logger.error(f"[{str(response.status)}] {await response.text()}")
                return False


if __name__ == "__main__":
    emails = get_file_data(EMAILS_FILE_NAME)
    proxies = get_file_data(PROXIES_FILE_NAME)

    for email, proxy in zip(emails, cycle(proxies)):
        if asyncio.run(get_request(email, proxy)):
            save_email(email)

        # counter += 1
        # if counter % len(proxies) == 0:
        #     sleep(TIME_DELTA)
        sleep(TIME_DELTA)
