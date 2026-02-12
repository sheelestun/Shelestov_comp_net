import csv

from icmplib import ping


domains = ["google.com", "yandex.ru", "github.com", "rutracker-net.ru",
           "vk.com", "mail.ru", "youtube.com", "nsu.ru", "nstu.ru"]
results = []
for domain in domains:
    try:
        host = ping(domain, count=3, timeout=2, privileged=True)
        results.append({
            "Host": domain,
            "RTT": host.avg_rtt,
            "Jitter": host.jitter,
            "Packet Loss%": int(host.packet_loss * 100),
            "Packets Received": host.packets_received
        })
        print(f"Checked: {domain}")
    except Exception as e:
        results.append({
            "Host": domain,
            "RTT": "-",
            "Jitter": "-",
            "Packet Loss%": 100,
            "Packets Received": 0
        })
        print(f"Error during checking domain: {domain}!\n"
              f"Error: {e}")

with open("ping_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Host", "RTT", "Jitter",
                                           "Packet Loss%", "Packets Received"],
                            delimiter=";")
    writer.writeheader()
    writer.writerows(results)
print("\nResults saved in ping_results.csv")
