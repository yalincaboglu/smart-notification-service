# 🐳 Docker Setup - Adım Adım Kılavuz

## Ön Hazırlık (İlk Kez)

### 1️⃣ Docker Desktop'ı İndir ve Kur
- **Windows**: https://docs.docker.com/desktop/install/windows-install/
- **macOS**: https://docs.docker.com/desktop/install/mac-install/
- **Linux**: https://docs.docker.com/desktop/install/linux-install/

### 2️⃣ Docker'ın Çalıştığını Doğrula
```powershell
docker --version
docker run hello-world
```

---

## 🚀 İLK KALIŞ (Initial Setup)

### Adım 1: Proje Dizinine Git
```powershell
cd "c:\Users\ylnca\OneDrive\Masaüstü\smart-notification"
```

### Adım 2: Docker Image Build Et
```powershell
docker-compose build
```

**Çıktı örneği:**
```
[+] Building 45.3s (15/15) FINISHED
 => [app 1/8] FROM python:3.11-slim
 => [app 2/8] RUN apt-get update && apt-get install -y ...
 => [app 3/8] RUN python -m venv /opt/venv
 => [app 4/8] COPY requirements.txt .
 => [app 5/8] RUN pip install --no-cache-dir -r requirements.txt
 ...
```

**Ne yapıyor?**
- Multi-stage build: builder ve runtime stage'ler
- Python 3.11-slim base image'dan başlar (~150MB)
- requirements.txt bağımlılıklarını yükler
- Non-root user (appuser) oluşturur
- Final image ~200-250MB

### Adım 3: Servisleri Ayağa Kaldır
```powershell
docker-compose --env-file=.env.docker up -d
```

**Bayraklar açıklaması:**
- `--env-file=.env.docker` : Environment variables dosyası
- `up` : Servisleri başlat
- `-d` : Detached mode (background'da çalış)

**Çıktı örneği:**
```
[+] Running 5/5
 ✔ Container smart-notification-cache      Created
 ✔ Container smart-notification-db         Created
 ✔ Container smart-notification-pgadmin    Created
 ✔ Container smart-notification-app        Created
 ✔ Container smart-notification-redis-commander Created
```

### Adım 4: Çalışan Container'ları Kontrol Et
```powershell
docker-compose ps
```

**Beklenen çıktı:**
```
NAME                                STATUS                 PORTS
smart-notification-app              Up 2 seconds           0.0.0.0:8000->8000/tcp
smart-notification-db               Up 2 seconds           0.0.0.0:5432->5432/tcp
smart-notification-cache            Up 2 seconds           0.0.0.0:6379->6379/tcp
smart-notification-pgadmin          Up 2 seconds           0.0.0.0:5050->80/tcp
smart-notification-redis-commander  Up 2 seconds           0.0.0.0:8081->8081/tcp
```

---

## 📋 LOG TAKIP (Monitoring)

### 📊 Tüm Servislerin Loglarını Canlı Olarak İzle
```powershell
docker-compose logs -f
```

**Neler göreceksin?**
```
smart-notification-db  | The files belonging to this database system will be owned by user "postgres".
smart-notification-cache | Ready to accept connections
smart-notification-app | 2026-07-10 22:11:40 - SmartNotification - INFO - Smart Notification Sistemi Başlatıldı
```

**Çıkış:** `Ctrl+C`

### 📊 Sadece App Loglarını İzle
```powershell
docker-compose logs -f app
```

### 📊 Sadece Database (PostgreSQL) Loglarını İzle
```powershell
docker-compose logs -f postgres
```

### 📊 Sadece Redis Loglarını İzle
```powershell
docker-compose logs -f redis
```

### 📊 Son 50 Satırı Göster (Canlı Değil)
```powershell
docker-compose logs --tail=50 app
```

### 📊 Timestamp ile Logları Göster
```powershell
docker-compose logs -f --timestamps app
```

---

## 🌐 ADMIN PANELS'A ERIŞIM

Tarayıcı aç ve şu adreslere git:

### 1. pgAdmin (PostgreSQL Management)
```
🌐 http://localhost:5050
📧 Email: admin@example.com
🔑 Password: pgadmin_pass
```

**Nasıl kullanılır?**
- Left panel → Add New Server → Fill database config
- Credentials: `notification_user` / `notification_pass`
- Database: `notifications_db`

### 2. Redis Commander
```
🌐 http://localhost:8081
```

**Neler yapabilirsin?**
- Redis keys görüntle
- Data inspect et
- Manual key operations

---

## 🔧 TEMEL DOCKER KOMUTLARI

### Container'a Shell Erişim

**Python App Shell'e Gir**
```powershell
docker-compose exec app bash
```

**Örnek komutlar:**
```bash
ls -la
python src/main.py
pytest tests/ -v
pip list
```

**Çıkış:** `exit`

**PostgreSQL'e Bağlan**
```powershell
docker-compose exec postgres psql -U notification_user -d notifications_db
```

**PostgreSQL sorguları:**
```sql
\dt                              -- Tabloları listele
SELECT * FROM information_schema.roles;  -- Kullanıcıları listele
\q                               -- Çık
```

**Redis'e Bağlan**
```powershell
docker-compose exec redis redis-cli -a redis_secure_pass
```

**Redis komutları:**
```redis
PING                             -- Bağlantıyı test et
SET key "value"                  -- Key set et
GET key                          -- Key oku
KEYS *                           -- Tüm keys listele
FLUSHDB                          -- Tüm keys sil
EXIT                             -- Çık
```

---

## 🧪 TESTLERI CONTAINER'DA ÇALIŞTIR

### Tüm Testleri Çalıştır
```powershell
docker-compose exec app pytest tests/ -v
```

**Beklenen çıktı:**
```
tests/test_notifications.py::TestTelegramNotification::test_valid_chat_id PASSED
tests/test_notifications.py::TestTelegramNotification::test_invalid_chat_id PASSED
...
======================== 12 passed in 0.15s =========================
```

### Coverage Raporu Oluştur
```powershell
docker-compose exec app pytest tests/ --cov=src --cov-report=html
```

Rapor: `htmlcov/index.html` (tarayıcıda aç)

### Belirli Test Dosyasını Çalıştır
```powershell
docker-compose exec app pytest tests/test_notifications.py -v
```

### Belirli Test Class'ını Çalıştır
```powershell
docker-compose exec app pytest tests/test_notifications.py::TestTelegramNotification -v
```

---

## 🔄 SERVIS YÖNETİMİ

### Servisleri Yeniden Başlat
```powershell
# Tüm servisleri
docker-compose restart

# Sadece app'ı
docker-compose restart app

# Sadece PostgreSQL'i
docker-compose restart postgres
```

### Servisleri Durdur (Çalışmayı Durdur Ama Silinmez)
```powershell
docker-compose stop
```

Tekrar başlatmak için:
```powershell
docker-compose start
```

### Servisleri Tamamen Kaldır
```powershell
# Servisleri durdur, containers kaldır (volumes kalır = DATA GÜVENLİ)
docker-compose down

# Servisleri durdur, containers VE volumes kaldır (⚠️ DATA KAYBI)
docker-compose down -v
```

---

## 📊 İLERI KOMUTLAR

### Logs'u Dosyaya Kaydet
```powershell
docker-compose logs > app_logs.txt
```

### Docker Image Bilgilerini İnceleme
```powershell
# Image history görüntüle
docker history smart-notification-app

# Image inspect et
docker image inspect smart-notification-app
```

### Container'ı Inspect Et
```powershell
docker-compose exec app docker inspect $(docker-compose ps -q app)
```

### Network Bilgilerini Göster
```powershell
docker network ls
docker network inspect smart-notification_smart-notification-network
```

### Disk Kullanımını Kontrol Et
```powershell
docker system df
```

### Docker'ı Temizle
```powershell
# Unused containers, images, networks sil
docker system prune

# Volumes da sil
docker system prune -a --volumes
```

---

## 🚨 TROUBLESHOOTING

### Port Already in Use (Port Zaten Kullanılıyor)

**Problem:** `Error response from daemon: Ports are not available`

**Çözüm:**

**Windows PowerShell'de:**
```powershell
# Hangi process 8000 portunu kullanıyor?
netstat -ano | findstr 8000

# Sonuç örneği: "LISTENING     5428"
# 5428 process ID'si

# Process'i kapat
taskkill /PID 5428 /F

# Veya docker-compose'u different name ile çalıştır
docker-compose -p myapp up -d
```

**macOS/Linux'te:**
```bash
lsof -i :8000
kill -9 <PID>
```

### Container Crash (Konteyner Kapandı)

**Problem:** Container'lar açılıyor ama hemen kapanıyor

**Çözüm:**
```powershell
# Detaylı hataları görüntüle
docker-compose logs app

# Specific error'ı ara
docker-compose logs app | findstr ERROR
```

### No PostgreSQL Connection

**Problem:** `psql: could not connect to server`

**Çözüm:**
```powershell
# PostgreSQL container'ı yeniden başlat
docker-compose restart postgres

# Logs'u kontrol et
docker-compose logs postgres

# Container'ın health'ini kontrol et
docker-compose ps
```

### Out of Disk Space

```powershell
# Docker disk kullanımını kontrol et
docker system df

# Unused resources sil
docker system prune -a
docker volume prune
```

---

## 📚 DOCKER-COMPOSE.YML MODÜLÜ

### Struct Açıklaması

```yaml
version: "3.8"                    # Docker Compose versiyonu

volumes:                          # Shared volumes tanımla
  postgres_data:                  # PostgreSQL data volume
  redis_data:                     # Redis data volume
  app_logs:                       # App logs volume

networks:                         # Custom networks
  smart-notification-network:     # Services arası iletişim

services:                         # Container'lar
  app:                            # Python app service
  postgres:                       # Database service
  redis:                          # Cache service
  pgadmin:                        # DB admin panel
  redis-commander:                # Redis admin panel
```

### Service Config Açıklaması

```yaml
services:
  app:
    build:                        # Build configuration
      context: .                  # Dockerfile'ın olduğu dizin
      dockerfile: Dockerfile      # Dockerfile adı
    
    container_name:               # Container adı
    restart: unless-stopped       # Otomatik restart
    
    environment:                  # Environment variables
      - KEY=value
      - DATABASE_URL=...
    
    volumes:                      # Volume mapping
      - ./src:/app/src           # Host:Container
    
    ports:                        # Port mapping
      - "8000:8000"              # Host:Container
    
    networks:                     # Hangi network'e bağlı
      - smart-notification-network
    
    depends_on:                   # Başka servislere bağımlılık
      redis:
        condition: service_healthy
    
    healthcheck:                  # Servis sağlığını kontrol et
      test: [...]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

## 💡 BEST PRACTICES

### Local Development için Tips

**1. Volume mapping kullan (kod sıcak yükleme)**
```yaml
volumes:
  - ./src:/app/src    # Dosyaları değiştirir instance restarts
```

**2. Environment variables'ı ayır**
- Development: `.env.docker`
- Production: secrets management (Vault, AWS Secrets)

**3. Non-root user kullan (security)**
```dockerfile
RUN useradd -r appuser
USER appuser
```

**4. Multi-stage build (image optimize)**
- Development dependencies builder stage'de
- Runtime stage'de sadece gerekli bileşenler

**5. Health checks ekle**
```yaml
healthcheck:
  test: ["CMD", ...]
  interval: 30s
  timeout: 10s
```

---

## 🎯 ÖZET - 3 ADIMDA BAŞLAT

```powershell
# 1. Build
docker-compose build

# 2. Up (background)
docker-compose --env-file=.env.docker up -d

# 3. Logları izle
docker-compose logs -f app
```

Bitince: `Ctrl+C` → `docker-compose down`

---

**Başarılar! 🚀 Docker ile microservices yolculuğuna hoşgeldin!**
