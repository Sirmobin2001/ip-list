import urllib.parse
import socket
import os

# لیست دامنه‌های هدف
DOMAINS = ["nima.nscl.ir", "bpb.yousef.isegaro.com"]

# پورت‌های مورد نظر
PORTS = [443]

# کانفیگ پایه (الگو)
BASE_CONFIG = "vless://4cff3b20-52e7-4bc1-83a4-3576392a4d70@hell.mobinshahidiclash.workers.dev:443?encryption=none&security=tls&sni=hell.mobinshahidiclash.workers.dev&fp=qq&insecure=1&allowInsecure=1&type=ws&host=hell.mobinshahidiclash.workers.dev&path=%2F%3Fed%3D2048#%E5%8E%9F%E7%94%9F%E5%9C%B0%E5%9D%80-443-WS-TLS"

def get_ips(domain):
    """تبدیل دامنه به لیست آی‌پی‌های فعال"""
    try:
        # دریافت اطلاعات آدرس (IPv4)
        data = socket.getaddrinfo(domain, 80, socket.AF_INET)
        # استخراج آی‌پی‌های منحصر به فرد
        return list(set([item[4][0] for item in data]))
    except Exception as e:
        print(f"خطا در یافتن آی‌پی برای دامنه {domain}: {e}")
        return []

def main():
    parsed_url = urllib.parse.urlparse(BASE_CONFIG)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    for domain in DOMAINS:
        domain_configs = []
        ips = get_ips(domain)
        
        print(f"تعداد {len(ips)} آی‌پی برای دامنه {domain} پیدا شد.")
        
        for ip in ips:
            for port in PORTS:
                # ساخت بخش netloc جدید (user@ip:port)
                netloc = f"{parsed_url.username}@{ip}:{port}"
                
                # نام‌گذاری نود بر اساس دامنه و آی‌پی
                node_name = f"{domain}-{ip}-{port}"
                
                # بازسازی کامل لینک vless
                new_config = urllib.parse.urlunparse((
                    parsed_url.scheme,
                    netloc,
                    parsed_url.path,
                    parsed_url.params,
                    urllib.parse.urlencode(query_params, doseq=True),
                    node_name
                ))
                domain_configs.append(new_config)
        
        # ذخیره کانفیگ‌های هر دامنه در فایل جداگانه
        if domain_configs:
            file_name = f"{domain}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write("\n".join(domain_configs))
            print(f"فایل {file_name} با {len(domain_configs)} کانفیگ ساخته شد.")
        else:
            print(f"برای دامنه {domain} هیچ کانفیگی ساخته نشد.")

if __name__ == "__main__":
    main()
