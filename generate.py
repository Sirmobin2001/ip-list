import urllib.parse

# لیست دامنه‌های فعال تو
NEW_DOMAINS = ["nima.nscl.ir", "bpb.yousef.isegaro.com"]

# کانفیگ پایه (ورکر)
BASE_CONFIG = "vless://6bf0872b-892d-4052-9ecf-fe2ad8a42e3f@hell.mobinshahidiclash.workers.dev:443?encryption=none&security=tls&sni=hell.mobinshahidiclash.workers.dev&fp=randomized&insecure=1&allowInsecure=1&type=ws&host=hell.mobinshahidiclash.workers.dev&path=%2F%3Fed%3D2048"

def main():
    configs = []
    parsed_url = urllib.parse.urlparse(BASE_CONFIG)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    for i, domain in enumerate(NEW_DOMAINS):
        # تغییر آدرس به دامنه جدید
        netloc = f"{parsed_url.username}@{domain}:{parsed_url.port}"
        
        # ساخت لینک جدید با نام متفاوت برای هر کدام
        new_config = urllib.parse.urlunparse((
            parsed_url.scheme,
            netloc,
            parsed_url.path,
            parsed_url.params,
            urllib.parse.urlencode(query_params, doseq=True),
            f"Config_{i+1}"
        ))
        configs.append(new_config)
    
    # ذخیره در فایل خروجی
    with open("sub.txt", "w") as f:
        f.write("\n".join(configs))

if __name__ == "__main__":
    main()
