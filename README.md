# Smart Notification

## 🚀 Project Overview / Proje Özeti

`Smart Notification` is a polished Python microservice for notifications and logging. / `Smart Notification`, bildirim ve loglama için profesyonel bir Python mikroservistir.

This repository combines:
- **SOLID architecture**
- **Factory Design Pattern**
- **FastAPI REST API**
- **Celery + Redis async queueing**
- **Docker Compose orchestration**
- **Terraform infrastructure automation**

Bu depo, aşağıdaki özellikleri bir araya getirir:
- **SOLID mimarisi**
- **Factory Tasarım Deseni**
- **FastAPI REST API**
- **Celery + Redis asenkron kuyruklama**
- **Docker Compose orkestrasyonu**
- **Terraform altyapı otomasyonu**

---

## 🧩 Architecture / Mimarimiz

### SOLID Principles / SOLID Prensipleri
- **Single Responsibility**: Each component has one clear role. / Her bileşenin net bir sorumluluğu vardır.
- **Open/Closed**: Add new notification channels without changing existing logic. / Yeni bildirim kanalları eklemek için mevcut mantık değiştirilmez.
- **Liskov Substitution**: All notification implementations can be swapped safely. / Tüm bildirim uygulamaları güvenle birbirinin yerine kullanılabilir.
- **Interface Segregation**: Interfaces remain minimal and focused. / Arayüzler minimal ve odaklı tutulur.
- **Dependency Inversion**: High-level logic depends on abstractions, not concrete classes. / Üst düzey mantık somut sınıflar yerine soyutlamalara bağlıdır.

### Factory Design Pattern / Factory Tasarım Deseni
`NotificationFactory` centralizes creation of notification services, making the system:
- easier to extend,
- easier to test,
- more maintainable,
- and decoupled from concrete implementations.

`NotificationFactory`, bildirim servislerinin oluşturulmasını merkezileştirir. Bu sayede sistem:
- genişletmesi daha kolay olur,
- test edilmesi daha kolay olur,
- bakım yapılması daha kolay olur,
- somut uygulamalardan ayrılır.

### Core Modules / Temel Modüller
- `src/notifications/` → notification interfaces and concrete channels / bildirim arabirimleri ve somut kanallar
- `src/logger/` → centralized logging management / merkezi loglama yönetimi
- `src/api/` → FastAPI endpoints and request validation / FastAPI uç noktaları ve istek doğrulama
- `src/tasks.py` → Celery task definitions / Celery görev tanımları
- `src/celery_config.py` → Celery broker/result backend configuration / Celery broker/sonuç altyapısı konfigürasyonu

---

## 🐳 Docker Deployment / Docker ile Çalıştırma

### Quick Start / Hızlı Başlangıç

```bash
docker-compose build
docker-compose --env-file .env.docker up -d
docker-compose logs -f app
```

### Included Services / İçerilen Servisler
- `app` → Python FastAPI application / Python FastAPI uygulaması
- `postgres` → PostgreSQL database / PostgreSQL veritabanı
- `redis` → Redis broker + cache / Redis broker + önbellek
- `pgadmin` → PostgreSQL administration UI / PostgreSQL yönetim arayüzü
- `redis-commander` → Redis management UI / Redis yönetim arayüzü

### Default Ports / Varsayılan Portlar
- `http://localhost:8000` → FastAPI
- `http://localhost:5050` → pgAdmin
- `http://localhost:8081` → Redis Commander
- `localhost:5432` → PostgreSQL
- `localhost:6379` → Redis

### Useful Commands / Faydalı Komutlar

```bash
docker-compose ps
docker-compose exec app bash
docker-compose exec app pytest tests/ -v
docker-compose down -v
```

---

## ⚡ Celery Queue / Celery Kuyruk Yapısı

Celery and Redis are used to process notification jobs asynchronously, keeping the API responsive and scalable. / Celery ve Redis, bildirim işleri asenkron olarak işlemeye yardımcı olur; API tepkisel ve ölçeklenebilir kalır.

### Why this architecture? / Neden bu mimari?
- Non-blocking request handling / Bloklamayan istek işleme
- Background worker scaling / Arka plan işçi ölçeklendirmesi
- Reliable task queue management / Güvenilir görev kuyruğu yönetimi
- Clean separation between API and processing logic / API ile işleme mantığı arasında temiz ayrım

### Flow / Akış
1. API request arrives in FastAPI / API isteği FastAPI’ye gelir
2. Notification payload is validated / Bildirim verisi doğrulanır
3. Task is enqueued to Celery / Görev Celery kuyruğuna eklenir
4. Worker consumes the task and sends notification / İşçi görev teslim alır ve bildirimi gönderir

### Key files / Temel Dosyalar
- `src/api/routes/notifications.py`
- `src/tasks.py`
- `src/celery_worker.py`
- `src/celery_config.py`

---

## ☁️ Terraform Infrastructure / Terraform Mimarisi

Terraform files are included to provision a cloud-ready environment on AWS. / Terraform dosyaları, AWS üzerinde buluta hazır bir ortam sağlamak için eklenmiştir.

### Provided resources / Sağlanan kaynaklar
- `main.tf` → AWS provider, EC2 instance, security group, SSH key pair / AWS sağlayıcısı, EC2 örneği, güvenlik grubu, SSH anahtar çifti
- `variables.tf` → reusable deployment variables / yeniden kullanılabilir dağıtım değişkenleri
- `outputs.tf` → public IP, app URL, SSH command / genel IP, uygulama URL’si, SSH komutu
- `aws_user_data.sh.tpl` → EC2 bootstrap script for Docker, Git, and Docker Compose / Docker, Git ve Docker Compose için EC2 bootstrap betiği
- `terraform.tfvars.example` → sample variable configuration / örnek değişken yapılandırması

### What happens on deploy? / Dağıtımda neler olur?
- Create an AWS EC2 instance on Amazon Linux 2 / Amazon Linux 2 üzerinde bir AWS EC2 örneği oluşturulur
- Install Docker, Docker Compose, Git / Docker, Docker Compose, Git yüklenir
- Clone this repository / Bu depo klonlanır
- Start the Docker Compose stack automatically / Docker Compose ortamı otomatik olarak başlatılır

### Deployment steps / Dağıtım adımları

```bash
copy terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

After apply you will get: / Uygulama sonrası alırsınız:
- EC2 public IP / EC2 genel IP
- Application URL / Uygulama URL’si
- SSH command template / SSH komut şablonu

---

## 🧪 Testing / Testler

Run unit tests: / Birim testlerini çalıştır:

```bash
pytest tests/ -v
```

Generate coverage report: / Kapsam raporu oluştur:

```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 📁 Repository Structure / Proje Dosya Yapısı

```
smart-notification/
├── src/
│   ├── api/
│   ├── notifications/
│   ├── logger/
│   ├── celery_config.py
│   ├── tasks.py
│   ├── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .env.docker
├── requirements.txt
├── main.tf
├── variables.tf
├── outputs.tf
├── aws_user_data.sh.tpl
├── terraform.tfvars.example
└── README.md
```

---

## 💡 Why this project? / Neden bu proje?
- Clean, enterprise-ready architecture / Temiz, kurumsal düzeyde mimari
- SOLID + Factory design for maintainability / Bakım kolaylığı için SOLID + Factory tasarım
- Docker Compose for reliable development workflows / Güvenilir geliştirme iş akışları için Docker Compose
- Celery + Redis for production-grade async processing / Üretim seviyesinde asenkron işleme için Celery + Redis
- Terraform for repeatable cloud deployment / Tekrarlanabilir bulut dağıtımı için Terraform

---

## 🤝 Contribution / Katkıda Bulunma

1. Fork the repository / Repoyu forkla
2. Create a new branch / Yeni branch oluştur: `feature/your-feature`
3. Make your changes / Değişiklik yap
4. Open a pull request / Pull request aç

---

## 📬 Contact / İletişim

If you'd like to collaborate or discuss improvements, open an issue or message me on GitHub. / İş birliği yapmak veya geliştirmeleri tartışmak isterseniz, GitHub üzerinde issue açın veya bana mesaj gönderin.
