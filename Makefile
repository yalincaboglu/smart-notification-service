.PHONY: help build up down logs restart clean test build-no-cache ps stop

# Default target
help:
	@echo "========================================"
	@echo "Smart Notification - Docker Commands"
	@echo "========================================"
	@echo ""
	@echo "Build & Run:"
	@echo "  make build              - Dockerfile'ı build et (cache ile)"
	@echo "  make build-no-cache     - Dockerfile'ı fresh olarak build et"
	@echo "  make up                 - Servisler ayağa kalk (background)"
	@echo "  make down               - Servisler durdur ve kaldır"
	@echo ""
	@echo "Logs & Monitoring:"
	@echo "  make logs               - Tüm servis loglarını göster (live)"
	@echo "  make logs-app           - Sadece app loglarını göster"
	@echo "  make logs-db            - Sadece PostgreSQL loglarını göster"
	@echo "  make logs-redis         - Sadece Redis loglarını göster"
	@echo ""
	@echo "Management:"
	@echo "  make ps                 - Running container'ları listele"
	@echo "  make restart            - Servisler restart et"
	@echo "  make restart-app        - Sadece app restart et"
	@echo "  make stop               - Servisler durdur (kaldırma)"
	@echo "  make clean              - Containers ve volumes sil (⚠️ DATA KAYBI)"
	@echo ""
	@echo "Testing & Validation:"
	@echo "  make test               - Unit testleri çalıştır"
	@echo "  make test-coverage      - Coverage raporu oluştur"
	@echo "  make lint               - Code style kontrol et"
	@echo ""
	@echo "Shell & Debug:"
	@echo "  make shell-app          - App container'a bağlan (bash)"
	@echo "  make shell-db           - PostgreSQL container'a bağlan"
	@echo "  make shell-redis        - Redis container'a bağlan"
	@echo ""
	@echo "========================================"
	@echo ""

# ============ BUILD COMMANDS ============

build:
	@echo "🐳 Building Docker image..."
	docker-compose build

build-no-cache:
	@echo "🐳 Building Docker image (no cache)..."
	docker-compose build --no-cache


# ============ UP & DOWN COMMANDS ============

up:
	@echo "🚀 Starting services (background)..."
	docker-compose --env-file=.env.docker up -d
	@echo "✅ Services started!"
	@echo ""
	@echo "📊 Açık Portlar:"
	@echo "  App          : http://localhost:8000"
	@echo "  PostgreSQL   : localhost:5432"
	@echo "  Redis        : localhost:6379"
	@echo "  pgAdmin      : http://localhost:5050 (admin@example.com / pgadmin_pass)"
	@echo "  Redis Cmder  : http://localhost:8081"
	@echo ""

down:
	@echo "⛔ Stopping and removing services..."
	docker-compose down
	@echo "✅ Services stopped!"

stop:
	@echo "⏹️  Pausing services..."
	docker-compose stop
	@echo "✅ Services paused!"


# ============ LOGS COMMANDS ============

logs:
	@echo "📋 Showing ALL service logs (live)..."
	docker-compose logs -f

logs-app:
	@echo "📋 Showing app logs (live)..."
	docker-compose logs -f app

logs-db:
	@echo "📋 Showing PostgreSQL logs (live)..."
	docker-compose logs -f postgres

logs-redis:
	@echo "📋 Showing Redis logs (live)..."
	docker-compose logs -f redis


# ============ MANAGEMENT COMMANDS ============

ps:
	@echo "📊 Running containers:"
	docker-compose ps

restart:
	@echo "🔄 Restarting all services..."
	docker-compose restart
	@echo "✅ Services restarted!"

restart-app:
	@echo "🔄 Restarting app service..."
	docker-compose restart app
	@echo "✅ App restarted!"

clean:
	@echo "🗑️  Removing containers and volumes..."
	docker-compose down -v
	@echo "✅ Cleanup complete!"
	@echo "⚠️  All volumes deleted!"


# ============ TESTING COMMANDS ============

test:
	@echo "🧪 Running unit tests..."
	docker-compose exec app pytest tests/ -v

test-coverage:
	@echo "📊 Generating coverage report..."
	docker-compose exec app pytest tests/ --cov=src --cov-report=html
	@echo "✅ Coverage HTML generated in htmlcov/"

lint:
	@echo "🔍 Checking code style..."
	docker-compose exec app python -m pylint src/ || true


# ============ SHELL/DEBUG COMMANDS ============

shell-app:
	@echo "🐚 Opening app shell..."
	docker-compose exec app bash

shell-db:
	@echo "🐚 Connecting to PostgreSQL..."
	docker-compose exec postgres psql -U notification_user -d notifications_db

shell-redis:
	@echo "🐚 Connecting to Redis..."
	docker-compose exec redis redis-cli -a redis_secure_pass


# ============ UTILITY COMMANDS ============

inspect-app:
	@echo "🔍 Inspecting app container..."
	docker inspect $$(docker-compose ps -q app)

prune:
	@echo "🧹 Pruning unused Docker resources..."
	docker system prune -f
	@echo "✅ Prune complete!"
