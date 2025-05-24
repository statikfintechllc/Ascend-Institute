<div align="center">
  <img src="https://img.shields.io/badge/Fair%20Use-GremlinGPT%20v1.0-black?style=for-the-badge&labelColor=black&color=red&logo=ghost&logoColor=red" alt="GremlinGPT Fair Use">
</div>

# GremlinGPT Linux Service (Systemd)

This unit file installs GremlinGPT as a **persistent autonomous Linux service**.

## Setup Path

```bash
GremlinGPT/systemd/gremlin.service
```

⸻

Install the Service
	1.	Copy service file to systemd:
```bash
sudo cp GremlinGPT/systemd/gremlin.service /etc/systemd/system/
```

2.	Reload systemd and enable on boot:
```bash
sudo systemctl daemon-reexec && \
sudo systemctl daemon-reload && \
sudo systemctl enable gremlin
```

3.	Start the service:
```bash
sudo systemctl start gremlin
```

⸻

Check Runtime Status
```bash
sudo systemctl status gremlin
```

View Logs
```bash
journalctl -u gremlin -n 50 --no-pager
```

Restart the Kernel Manually
```bash
sudo systemctl restart gremlin
```

⸻

Recovery After Reboot

Gremlin automatically runs:
```bash
python3 core/loop.py
```

⸻

Which:
	•	Resumes FSM agent loop
	•	Watches for retrain triggers
	•	Monitors code diffs
	•	Logs events + reward scores

⸻

Notes
	•	Be sure to set the correct User and WorkingDirectory in gremlin.service
	•	It is recommended to run reboot_recover.sh inside the loop for full restore mode
