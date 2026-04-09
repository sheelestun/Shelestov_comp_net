import socket
import subprocess
import csv


domains = [
    "google.com",
    "ozon.ru",
    "wikipedia.org"
]

results = []

for domain in domains:
    print(f"\n[1/2] DNS try for: {domain}... ")
    try:
        ip = socket.gethostbyname(domain)
        print(f"{ip}")
    except Exception as e:
        print(f"DNS error: {e}")
        results.append([domain, "DNS_ERROR", str(e)])
        continue

    print(f"[2/2] Traceroute for {ip}...")
    try:
        proc = subprocess.run(
            ["tracert", "-d", ip],
            capture_output=True,
            encoding="cp866",
        )
        trace_output = proc.stdout
        print("Done")
    except subprocess.TimeoutExpired:
        trace_output = "TIMEOUT!"
        print("Error! Timeout!")
    except Exception as e:
        trace_output = f"ERROR: {e}"
        print(f"Error! Traceroute: {e}")

    results.append({"Domain": domain,
                    "IP": ip,
                    "Traceroute_Output": trace_output})

csv_file = "dns_trace_results.csv"
with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f,
                            fieldnames=["Domain", "IP", "Traceroute_Output"],
                            delimiter=";")
    writer.writeheader()
    writer.writerows(results)

print(f"\nSuccess! Saved: {csv_file}")


"""
То же самое, но ручками:

======================================
DNS req:
nslookup google.com
nslookup ozon.ru
nslookup wikipedia.org

Example out:
C:/Users/mrlog>nslookup ozon.ru
╤хЁтхЁ:  UnKnown
Address:  8.8.8.4

Не заслуживающий доверия ответ:
╚ь :     ozon.ru
Addresses:  185.73.194.82
          185.73.193.68
======================================
Traceroute:
tracert -d 142.250.185.46
tracert -d 185.73.194.82
tracert -d 208.80.154.224

Example out:
C:/Users/mrlog>tracert -d 185.73.194.82

Трассировка маршрута к 185.73.194.82 с максимальным числом прыжков 30

  1    26 ms     5 ms     6 ms  8.8.8.4
  2     5 ms     4 ms     4 ms  80.89.192.222
  3     8 ms     5 ms     5 ms  10.255.154.189
  4    51 ms    12 ms    83 ms  10.255.154.69
  5     6 ms     5 ms     8 ms  10.255.154.30
  6    10 ms     7 ms     7 ms  193.238.128.150
  7     9 ms     6 ms     7 ms  193.238.128.149
  8     6 ms     7 ms     6 ms  89.189.190.235
  9     7 ms    14 ms     7 ms  89.189.190.246
 10     9 ms     7 ms    70 ms  193.238.131.161
 11     6 ms     5 ms     5 ms  79.104.31.217
 12    52 ms    57 ms    63 ms  79.104.225.219
 13    53 ms   135 ms   101 ms  62.141.90.37
 14     *        *        *     Превышен интервал ожидания для запроса.
 15    67 ms   155 ms    51 ms  10.11.0.253
 16    54 ms    60 ms    92 ms  10.10.0.214
 17     *        *        *     Превышен интервал ожидания для запроса.
 18     *        *        *     Превышен интервал ожидания для запроса.
 19    55 ms    75 ms    51 ms  185.73.194.82
 20    89 ms   100 ms   100 ms  185.73.194.82

Трассировка завершена.
======================================
"""