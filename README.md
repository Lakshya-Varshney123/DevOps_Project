# QuickBite — Microservices-Based Food Ordering System

A runnable coursework project using five independent Flask services, Docker, and Docker Compose.

## Services
- **API Gateway + Web UI (5000):** browser entry point and request routing.
- **Catalog (5001):** restaurant menu.
- **Order (5002):** validates and stores orders in SQLite.
- **Payment (5003):** mock payment authorization only.
- **Notification (5004):** records simulated order confirmations.

The browser communicates with the gateway. The gateway calls Catalog and Order; Order calls Catalog, Payment, and Notification. Each service has its own container. Order data persists in the `order_data` Docker volume.

## Run
Install Docker Desktop, open a terminal in this folder, then run:

```bash
docker compose up --build -d
```

Open **http://localhost:5000**.

Useful commands:
```bash
docker compose ps
docker compose logs -f
docker compose down
docker compose down -v   # also deletes saved order data
```

## API examples
```bash
curl http://localhost:5000/api/menu
curl -X POST http://localhost:5000/api/orders -H "Content-Type: application/json" -d "{\"customer\":\"Krishna\",\"address\":\"Greater Noida\",\"items\":[{\"id\":1,\"quantity\":2}]}"
curl http://localhost:5000/api/orders
curl http://localhost:5000/health
```

## Order workflow
1. Customer chooses menu items and enters name/address.
2. Gateway forwards the order request to Order Service.
3. Order Service validates menu items with Catalog.
4. Payment Service returns a mock authorization.
5. Order Service saves the confirmed order in SQLite.
6. Notification Service records a confirmation message.

**Important:** Payment is simulated; no real money or card information is handled. Notifications are logged/recorded; no SMS or email is sent.

## DevOps concepts
Microservices, REST communication, Docker containerization, Docker Compose orchestration, persistent Docker volume, health endpoints, and GitHub Actions CI (Compose validation and image builds).

## Future improvements
For production: Kubernetes/Amazon EKS, managed database, message broker, authentication, HTTPS, secrets management, centralized logging, Prometheus/Grafana, automated tests, and a real PCI-compliant payment provider.

## Structure
```text
Food_Ordering_Microservices/
├── docker-compose.yml
├── gateway/ (Flask API gateway and web UI)
├── catalog/ (menu service)
├── orders/ (order API and SQLite persistence)
├── payments/ (mock payment API)
├── notifications/ (confirmation API)
└── .github/workflows/ci.yml
```
