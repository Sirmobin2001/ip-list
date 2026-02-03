import urllib.parse
import socket

# لیست دامنه‌های مورد نظر شما
DOMAINS = ["nima.nscl.ir", "bpb.yousef.isegaro.com"]

# کانفیگ اصلی (Base)
BASE_CONFIG = "vless://6bf0872b-892d-4052-9ecf-fe2ad8a42e3f@hell.mobinshahidiclash.workers.dev:443?encryption=none&security=tls&sni=hell.mobinshahidiclash.workers.dev&fp=randomized&insecure=1&allowInsecure=1&type=ws&host=hell.mobinshahidiclash.workers.dev&path=%2F%3Fed%3D2048"

def get_ips(domain):
    """استخراج تمامی IPv4 های متصل به دامنه"""
    try:
        # فقط IPv4 ها را فیلتر می‌کنیم (AF_INET)
        data = socket.getaddrinfo(domain, 80, socket.AF_INET)
        ips = list(set([item[4][0] for item in data]))
        return ips
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
            # ایجاد بخش آدرس: uuid@IP:PORT
            netloc = f"{parsed_url.username}@{ip}:{parsed_url.port}"
            
            # بازسازی لینک با IP جدید
            new_config = urllib.parse.urlunparse((
                parsed_url.scheme,
                netloc,
                parsed_url.path,
                parsed_url.params,
                urllib.parse.urlencode(query_params, doseq=True),
                f"IP-{ip}-from-{domain}" # نام کانفیگ
            ))
            final_configs.append(new_config)
    
    # ذخیره در فایل خروجی
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_configs))
    
    print(f"Done! {len(final_configs)} configs saved to sub.txt")

if __name__ == "__main__":
    main()
