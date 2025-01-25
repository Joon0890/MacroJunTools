from modules.utiles.scripts.env_utils import load_env, save_env
from modules.utiles.scripts.config_utils import load_config, save_config
from modules.utiles.scripts.env_utils import load_env
from modules.utiles.scripts.config_utils import load_config

def interactive_config():
    # 공통 설정
    services = {
        "1": "instagram",
        "2": "sugang",
        "3": "everytime"
    }

    print("\n=== Service Selection ===")
    for number, service in services.items():
        print(f"{number}. {service.capitalize()}")

    selected_service = input("\nSelect a service to configure (1-3): ").strip()
    if selected_service not in services:
        print("[ERROR] Invalid selection. Please choose a valid option.")
        return

    service = services[selected_service]
    print(f"\nConfiguring {service.capitalize()}...")

    # .env 파일 처리 (민감 정보)
    env_values = load_env()
    username_key = f"{service.upper()}_USERNAME"
    password_key = f"{service.upper()}_PASSWORD"

    username = input(f"Enter {service.capitalize()} username [{env_values.get(username_key, '')}]: ") or env_values.get(username_key, "")
    password = input(f"Enter {service.capitalize()} password [{env_values.get(password_key, '')}]: ") or env_values.get(password_key, "")

    save_env(username_key, username)
    save_env(password_key, password)

    # YAML 파일 처리 (기본 옵션)
    config = load_config()

    if service == "instagram":
        headless = input(f"Enable headless mode (true/false) [{config.get(service, {}).get('headless', True)}]: ") or config.get(service, {}).get('headless', True)
        chrome_close = input(f"Close Chrome after operation (true/false) [{config.get(service, {}).get('chrome_close', True)}]: ") or config.get(service, {}).get('chrome_close', True)
        scrape_limit = input(f"Number of posts to scrape [{config.get(service, {}).get('scrape_limit', 5)}]: ") or config.get(service, {}).get('scrape_limit', 5)
        scrape_limit = int(scrape_limit)
        
        headless = headless.lower() == "true" if isinstance(headless, str) else bool(headless)
        chrome_close = chrome_close.lower() == "true" if isinstance(chrome_close, str) else bool(chrome_close)
        
        config[service] = {"headless": headless, "scrape_limit": scrape_limit, "chrome_close":chrome_close}
    
    elif service == "sugang":
        confidence = input(f"Image detection confidence (0.0 - 1.0) [{config.get(service, {}).get('confidence', 0.95)}]: ") or config.get(service, {}).get('confidence', 0.95)
        
        config[service] = {"confidence": float(confidence)}
    
    elif service == "everytime":
        headless = input(f"Enable headless mode (true/false) [{config.get(service, {}).get('headless', True)}]: ") or config.get(service, {}).get('headless', True)
        chrome_close = input(f"Close Chrome after operation (true/false) [{config.get(service, {}).get('chrome_close', True)}]: ") or config.get(service, {}).get('chrome_close', True)
        
        headless = headless.lower() == "true" if isinstance(headless, str) else bool(headless)
        chrome_close = chrome_close.lower() == "true" if isinstance(chrome_close, str) else bool(chrome_close)

        config[service] = {"headless": headless.lower() == "true", "chrome_close":chrome_close}

    # YAML 저장
    save_config(config)
    print("\n[INFO] Configuration saved successfully!")

def load_settings(service: str):
    # .env 값 불러오기
    env_values = load_env()

    # YAML 값 불러오기
    config = load_config()

    # 각 서비스별 설정값 반환
    settings = {}

    username_key = f"{service.upper()}_USERNAME"
    password_key = f"{service.upper()}_PASSWORD"

    service_config = config.get(service, {})
    settings[service] = {
        "username": env_values.get(username_key),
        "password": env_values.get(password_key),
        **service_config
    }

    return settings

if __name__=="__main__":
    print(load_settings("instagram"))
    #interactive_config()