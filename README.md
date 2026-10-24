# IIoT Machinery Monitoring (Варіант 4)

🔗 **Демонстраційне відео роботи системи:** [Посилання на YouTube / Google Drive (додати перед здачею)](...)

---

## 1. Загальний опис системи та варіанта
Цей проєкт реалізує систему моніторингу промислового обладнання (**IIoT — Industrial Internet of Things**) за **Варіантом 4**. 
Система призначена для збору телеметричних даних з віртуального промислового станка (`Machine 01`), передачі їх через легковісний брокер повідомлень за протоколом MQTT, обробки на сервери автоматизації та відображення в реальному часі на інтерактивному дашборді з реалізацією правил аварійної зупинки.

### Технологічний стек:
* **Оркестрація:** Docker Compose (Mosquitto + openHAB)
* **Брокер повідомлень:** Eclipse Mosquitto
* **Сервер автоматизації та UI:** openHAB (з файловою конфігурацією `.things`, `.items`, `.rules`)
* **Симулятор обладнання:** Python (`paho-mqtt`, `json`)

---

## 2. Архітектура системи (Mermaid) та таблиця пристроїв

Архітектура побудована за чотирьохрівневою схемою IIoT:

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
