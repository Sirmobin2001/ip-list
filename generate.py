import urllib.parse
import socket

# دامنه‌های هدف
DOMAINS = ["nima.nscl.ir", "bpb.yousef.isegaro.com"]

# پورت‌های مورد نظر
PORTS = [443, 2087, 2096, 8443, 2053]

# کانفیگ پایه
BASE_CONFIG = "vless://4cff3b20-52e7-4bc1-83a4-3576392a4d70@hell.mobinshahidiclash.workers.dev:443?encryption=none&security=tls&sni=hell.mobinshahidiclash.workers.dev&fp=qq&insecure=1&allowInsecure=1&type=ws&host=hell.mobinshahidiclash.workers.dev&path=%2F%3Fed%3D2048#%E5%8E%9F%E7%94%9F%E5%9C%B0%E5%9D%80-443-WS-TLS
"

def get_ips(domain):
    try:
        data = socket.getaddrinfo(domain, 80, socket.AF_INET)
        return list(set([item[4][0] for item in data]))
    except Exception as e:
        print(f"Error resolving {domain}: {e}")
        return []

def main():
    final_configs = []
    parsed_url = urllib.parse.urlparse(BASE_CONFIG)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    for domain in DOMAINS:
        ips = get_ips(domain)
        print(f"Found {len(ips)} IPs for {domain}")
        
        for ip in ips:
            for port in PORTS:
                # جایگزینی IP و پورت جدید در ساختار آدرس
                netloc = f"{parsed_url.username}@{ip}:{port}"
                
                # بازسازی لینک
                new_config = urllib.parse.urlunparse((
                    parsed_url.scheme,
                    netloc,
                    parsed_url.path,
                    parsed_url.params,
                    urllib.parse.urlencode(query_params, doseq=True),
                    f"IP-{ip}-Port-{port}" # نام کانفیگ شامل پورت
                ))
                final_configs.append(new_config)
    
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs))
    
    print(f"Successfully generated {len(final_configs)} configs.")

if __name__ == "__main__":
    main()
