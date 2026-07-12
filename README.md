# AI Text Summarizer 🐳

A lightweight Flask web app that summarizes any text into 3 lines using the Anthropic (Claude) API — containerized with Docker and deployed on AWS EC2.

Built as part of my [#90DaysDevOpsChallenge](https://www.linkedin.com/in/abhisheksali55) — learning DevOps in public.

---

## 🚀 Live Demo

> Deployed on AWS EC2 (Docker container)

```
http://<ec2-public-ip>:5000
```

## ✨ Features

- Paste any text and get an instant 3-line summary
- Powered by Anthropic's Claude API
- `/health` endpoint for uptime checks
- Fully containerized — runs identically on any machine with Docker

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python, Flask |
| AI | Anthropic Claude API |
| Server | Gunicorn (production WSGI server) |
| Containerization | Docker |
| Hosting | AWS EC2 |

## 📁 Project Structure

```
ai-text-summarizer-tool/
├── app.py                # Flask app + Claude API integration
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Frontend UI
├── Dockerfile
├── .env.example           # Sample env file (no real keys)
└── .gitignore
```

## ⚙️ Setup — Run Locally (without Docker)

```bash
git clone https://github.com/abhisheksali55/Ai-text-summarizer-tool.git
cd Ai-text-summarizer-tool

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env          # then add your real ANTHROPIC_API_KEY inside

python app.py
```

Visit `http://localhost:5000`

## 🐳 Setup — Run with Docker

```bash
# Build the image
docker build -t ai-summarizer:v1 .

# Run the container
docker run -d -p 5000:5000 --env-file .env --name ai-summarizer-app ai-summarizer:v1
```

Visit `http://localhost:5000`

## ☁️ Deploying on AWS EC2

1. Launch an EC2 instance (Ubuntu) and SSH into it
2. Install Docker:
   ```bash
   sudo apt update && sudo apt install docker.io -y
   sudo systemctl enable --now docker
   sudo usermod -aG docker $USER
   ```
3. Clone the repo and build/run the container (same commands as above)
4. **Open the port in the EC2 Security Group** — Inbound rule: Custom TCP, port `5000`, source `0.0.0.0/0`
5. Access via `http://<ec2-public-ip>:5000`

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key ([get one here](https://console.anthropic.com)) |
| `PORT` | Port the app runs on (default: `5000`) |

⚠️ Never commit your real `.env` file — it's excluded via `.gitignore`. Only `.env.example` (with placeholder values) is tracked.

---

## 🐛 Errors I Hit & How I Fixed Them

Documenting this because I learned more from debugging this than from anything that worked on the first try.

### Error: `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`

**Where it happened:** Right after deploying to EC2, the container kept crashing on startup. `docker logs` showed:

```
File "/app/app.py", line 7, in <module>
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

**Root cause:** `requirements.txt` had `anthropic` pinned to an older version, but its dependency `httpx` was **not pinned**. When the Docker image was built, the latest `httpx` got installed — and that latest version removed a `proxies` argument that the older `anthropic` SDK was still passing internally. Two libraries, two different assumptions, one crash.

**Fix:**
1. Upgraded the `anthropic` package in `requirements.txt` to a version compatible with the latest `httpx`
2. Rebuilt the image with `--no-cache` to make sure nothing stale was cached:
   ```bash
   docker build --no-cache -t ai-summarizer:v1 .
   ```
3. Container booted clean after that.

**Lesson:** Pin your direct dependencies, but don't assume their sub-dependencies will stay compatible forever. When a library crash mentions an argument you never wrote yourself, check the dependency chain, not just your own code.

### Issue: App running fine in container, but browser said "connection refused"

**Root cause:** Docker container was healthy, but the **EC2 Security Group** didn't have the app's port open — so traffic never reached the EC2 instance in the first place.

**Fix:** Added an inbound rule for the port (Custom TCP, `0.0.0.0/0`) in the Security Group.

**Lesson:** A working container ≠ a reachable app. Docker networking, host firewall/security groups, and port mapping are three separate layers — all three need to be right.

---

## 📌 What's Next

- [ ] Multi-stage Docker build to shrink image size
- [ ] CI/CD pipeline (GitHub Actions → auto-build → auto-deploy to EC2)
- [ ] Add basic rate limiting

## 👤 Author

**Abhishek Sali**
Building in public as part of #90DaysDevOpsChallenge
[LinkedIn](https://www.linkedin.com/in/abhisheksali55) ·  

## 📄 License

This project is open source and available for learning purposes.
