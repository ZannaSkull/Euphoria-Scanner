import socket
import socks
import asyncio
import time
import ctypes
import os

RED = "\033[91m"
PURPLE = "\033[95m"
RESET = "\033[0m"

ctypes.windll.kernel32.SetConsoleTitleA("Euphoria")

ascii_text = r""" {purple}
  ______            _                _       
 |  ____|          | |              (_)      
 | |__  _   _ _ __ | |__   ___  _ __ _  __ _ 
 |  __|| | | | '_ \| '_ \ / _ \| '__| |/ _` |
 | |___| |_| | |_) | | | | (_) | |  | | (_| |
 |______\__,_| .__/|_| |_|\___/|_|  |_|\__,_|
             | |      Hisako On Top                       
             |_|                             
{reset} """.format(purple=PURPLE, reset=RESET)


async def scan_port(target, port, proxy, results, timeout, server_name):
    sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.set_proxy(socks.SOCKS5, proxy[0], proxy[1])

    try:
        await asyncio.wait_for(sock.connect((target, port)), timeout=timeout)
        results[port] = True
        save_to_file(server_name, port)
    except (socket.timeout, asyncio.TimeoutError):
        results[port] = False
    except Exception as e:
        results[port] = False
        print(f"An error occurred while scanning port {port}: {str(e)}")
    finally:
        sock.close()

def save_to_file(server_name, port):
    filename = f"{server_name}.txt"
    with open(filename, "a") as file:
        file.write(f"Port {port} is open\n")

async def scan_ports(target, ports, proxies, max_workers, timeout):
    total_ports = len(ports)
    scanned_ports = 0
    results = {}

    print(f"Euphoria Scanner | Made By Hisako")
    print("-" * 40)

    tasks = []
    for port in ports:
        scanned_ports += 1
        print(f"\rEuphoria Says : Scanned Ports {scanned_ports}", end="")

        for proxy in proxies:
            task = asyncio.ensure_future(scan_port(target, port, proxy, results, timeout, target))
            tasks.append(task)

    await asyncio.gather(*tasks)

    for port, open_status in results.items():
        if open_status:
            print(f"\n{PURPLE}Port {port} is open{RESET}")
            break
    else:
        print(f"\n{RED}All ports are closed{RESET}")

def main():
    print(ascii_text)
    print("Euphoria Scanner. Very Euphoric Scanner")
    print("-" * 40)

    try:
        target = input("Enter the target IP address or hostname: ")
        port_range = input("Enter the range of ports to scan (1-65535): ")
        proxy_file = input("Enter the filename containing proxies: ")
        max_workers = int(input("Enter the maximum number of workers (1-2000): "))
        timeout = float(input("Enter the connection timeout in seconds (0.5-1.0): "))

        start_port, end_port = map(int, port_range.split("-"))
        ports = range(start_port, end_port + 1)

        with open(proxy_file, "r") as file:
            proxies = [line.strip().split(":") for line in file]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(scan_ports(target, ports, proxies, max_workers, timeout))
        loop.close()
    except Exception as e:
        print(f"An error occurred during the scan: {str(e)}")

if __name__ == "__main__":
    main()
