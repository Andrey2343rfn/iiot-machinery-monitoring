```mermaid
graph TD
    subgraph sub1 ["Рівень 1: Пристрої та Сенсори (Edge)"]
        A["Python Simulator: devices.py"] -->|MQTT Publish| B["Mosquitto Broker"]
    end

    subgraph sub2 ["Рівень 2: Мережевий транспорт (Fog / Gateway)"]
        B -->|MQTT Subscribe / TCP 1883| C["openHAB MQTT Binding"]
    end

    subgraph sub3 ["Рівень 3: Обробка та Логіка (Server / Core)"]
        C -->|JSONPath Transformation| D["openHAB Things & Items"]
        D --> E["openHAB Rules Engine: machinery.rules"]
    end

    subgraph sub4 ["Рівень 4: Візуалізація та Керування (Presentation)"]
        D --> F["openHAB Overview UI / Dashboard"]
        E -->|Command / Stop| B
    end
