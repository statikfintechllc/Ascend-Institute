<link rel="stylesheet" type="text/css" href="docs/custom.css">
<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/FAIR%20USE-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Fair Use License"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/LICENSE">
    <img src="https://img.shields.io/badge/GREMLINGPT%20v1.0.3-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT License"/>
  </a>
</div>

<div align="center">
  <a
href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/Why-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Why"/>
  </a>
  <a href="https://github.com/statikfintechllc/AscendAI/blob/master/About Us/WHY_GREMLINGPT.md">
    <img src="https://img.shields.io/badge/GremlinGPT-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="GremlinGPT"/>
  </a>
</div>

  <div align="center">
  <a href="https://ko-fi.com/statikfintech_llc">
    <img src="https://img.shields.io/badge/Support-black?style=for-the-badge&logo=dragon&logoColor=gold" alt="Support"/>
  </a>
  <a href="https://patreon.com/StatikFinTech_LLC?utm_medium=unknown&utm_source=join_link&utm_campaign=creatorshare_creator&utm_content=copyLink">
    <img src="https://img.shields.io/badge/SFTi-darkred?style=for-the-badge&logo=dragon&logoColor=gold" alt="SFTi"/>
  </a>
</div>

# GremlinGPT v1.0.3 Linux Service (Systemd)

This unit file installs GremlinGPT as a **persistent autonomous Linux service** that runs without user intervention.

## Features

- ✅ **No user interaction required** - Runs completely autonomously
- ✅ **Proper conda environment activation** - Uses bash with conda profile sourcing
- ✅ **Comprehensive environment setup** - All necessary env vars configured
- ✅ **Robust restart handling** - Graceful shutdown with 30s timeout
- ✅ **Journal logging** - Logs to systemd journal for easy monitoring
- ✅ **Network dependency** - Waits for network before starting

## Setup Path

```bash
GremlinGPT/systemd/gremlin.service
```

⸻

## Install the Service

**Option 1: Automatic (Recommended)**
Run the install script which will configure everything automatically:
```bash
./install.sh
```

**Option 2: Manual Installation**

1. Copy service file to systemd:
```bash
sudo cp systemd/gremlin.service /etc/systemd/system/
```

2. Edit the service file to match your paths:
```bash
sudo nano /etc/systemd/system/gremlin.service
# Update WorkingDirectory, User, Group, and paths to match your setup
```

3. Reload systemd and enable on boot:
```bash
sudo systemctl daemon-reexec && \
sudo systemctl daemon-reload && \
sudo systemctl enable gremlin
```

4. Start the service:
```bash
sudo systemctl start gremlin
```

⸻

## Service Management

**Check Runtime Status**
```bash
sudo systemctl status gremlin
```

**View Logs**
```bash
# Recent logs
journalctl -u gremlin -n 50 --no-pager

# Follow logs in real-time
journalctl -u gremlin -f

# Logs since last boot
journalctl -u gremlin -b --no-pager
```

**Restart the Service**
```bash
sudo systemctl restart gremlin
```

**Stop the Service**
```bash
sudo systemctl stop gremlin
```

**Disable Auto-start**
```bash
sudo systemctl disable gremlin
```

⸻

## Troubleshooting

**Service fails to start:**
1. Check conda installation: `which conda`
2. Verify environment exists: `conda env list | grep gremlin-orchestrator`
3. Check file permissions: `ls -la /path/to/GremlinGPT/core/loop.py`
4. View detailed logs: `journalctl -u gremlin -n 100 --no-pager`

**Service starts but crashes:**
1. Test manual start: `cd /path/to/GremlinGPT && conda activate gremlin-orchestrator && python3 core/loop.py`
2. Check Python dependencies: `conda list` (while in gremlin-orchestrator env)
3. Verify all paths in service file are correct

**No network access:**
- Service waits for network-online.target, but some networks may take longer
- Check logs for network-related errors

⸻

## Recovery After Reboot

GremlinGPT automatically runs on system boot and executes:
```bash
python3 core/loop.py
```

Which provides:
- ✅ **Autonomous FSM agent loop** - Main control system
- ✅ **Retrain trigger monitoring** - Self-improvement cycles  
- ✅ **Code diff watching** - Mutation detection
- ✅ **Event logging** - Full audit trail with reward scores
- ✅ **Network service restoration** - API endpoints and dashboard
- ✅ **Memory system recovery** - Vector store and embeddings

⸻

## Configuration Notes

**Environment Variables:**
- `PYTHONPATH`: Set to GremlinGPT directory for proper imports
- `CONDA_DEFAULT_ENV`: Ensures correct conda environment
- `HOME`: Required for conda profile sourcing
- `PATH`: Includes conda environment binaries

**Security:**
- Service runs as specified user (not root)
- No sudo privileges required during runtime
- All operations contained within user's permissions

**Logging:**
- `StandardOutput=journal` - Stdout goes to systemd journal
- `StandardError=journal` - Stderr goes to systemd journal  
- Use `journalctl -u gremlin` to view all logs

**Process Management:**
- `KillMode=mixed` - Graceful shutdown with SIGTERM, then SIGKILL
- `TimeoutStopSec=30` - 30 second grace period for shutdown
- `Restart=always` - Automatic restart on any exit

⸻

## Advanced Configuration

**Custom Conda Path:**
If conda is installed in a non-standard location, update the ExecStart path:
```bash
ExecStart=/bin/bash -c 'source /path/to/conda/etc/profile.d/conda.sh && conda activate gremlin-orchestrator && python3 core/loop.py'
```

**Resource Limits:**
Add resource constraints if needed:
```ini
[Service]
MemoryLimit=2G
CPUQuota=50%
```

**Custom Working Directory:**
Update `WorkingDirectory` if GremlinGPT is installed elsewhere:
```ini
WorkingDirectory=/custom/path/to/GremlinGPT
```
