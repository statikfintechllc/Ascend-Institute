#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────
# ⚠️ GremlinGPT Fair Use Only | Commercial Use Requires License
# Built under the GremlinGPT Dual License v1.0
# © 2025 StatikFintechLLC / AscendAI Project
# Contact: ascend.gremlin@gmail.com
# ─────────────────────────────────────────────────────────────

# GremlinGPT v1.0.3 :: Module Integrity Directive
# This script is a component of the GremlinGPT system, under Alpha expansion.

import json
from datetime import datetime
from pathlib import Path
from utils.logging_config import setup_module_logger

# Initialize module-specific logger
logger = setup_module_logger("scraper")

WATERMARK = "source:GremlinGPT"
ORIGIN = "tws_scraper"

HEADERS = {
    "User-Agent": "GremlinGPT/5.0 (+https://gremlingpt.ai/bot)",
    "Accept": "text/html,python,javascript,java,markdown,jupyter,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}


MODULE = "tws_scraper"
DEFAULT_SIMULATION = {
    "symbol": "SIMTWS",
    "price": 0.87,
    "volume": 1000000,
    "ema": 0.83,
    "vwap": 0.84,
    "timestamp": datetime.utcnow().isoformat(),
}


def locate_tws_files():
    """
    Scan for known TWS output, export, or log files dynamically.
    Enhanced to find actual TWS installations and data files.
    """
    try:
        home = Path.home()
        candidates = []
        
        logger.info(f"[{MODULE}] Scanning for TWS files in {home}")

        # Enhanced search patterns for TWS/IBKR installations
        search_patterns = [
            # Traditional TWS patterns
            "**/tws*/logs/*.json",
            "**/tws*/data/*.csv",
            "**/TWS*/logs/*.json",
            "**/TWS*/data/*.csv",
            "**/TWS*/DailyReports/*.csv",
            
            # Interactive Brokers patterns
            "**/IBKR*/export/*.json",
            "**/IBKR*/reports/*.csv",
            "**/InteractiveBrokers*/output/*.log",
            "**/InteractiveBrokers*/reports/*.csv",
            "**/InteractiveBrokers*/DailyReports/*.csv",
            
            # Trader Workstation patterns
            "**/Trader*Workstation*/logs/*.json",
            "**/Trader*Workstation*/reports/*.csv",
            "**/TraderWorkstation*/logs/*.json",
            "**/TraderWorkstation*/reports/*.csv",
            
            # Common TWS API and data directories
            "**/TWS API*/logs/*.csv",
            "**/TWS API*/data/*.json",
            "**/twsapi*/logs/*.csv",
            "**/tws_api*/data/*.json",
            
            # IB Gateway patterns
            "**/IBGateway*/logs/*.json",
            "**/IBGateway*/reports/*.csv",
            
            # Documents and Downloads folders (where users often save reports)
            "Documents/**/TWS*.csv",
            "Documents/**/IBKR*.csv",
            "Documents/**/position*.csv",
            "Documents/**/trade*.csv",
            "Downloads/**/TWS*.csv",
            "Downloads/**/IBKR*.csv",
            "Downloads/**/position*.csv",
            "Downloads/**/trade*.csv",
            
            # Hidden directories that TWS might use
            ".tws*/data/*.json",
            ".ibkr*/export/*.csv",
            ".trader*/logs/*.json",
        ]


        # Add explicit search in /home/statiksmoke8/Jts for TWS data
        tws_dir = Path("/home/statiksmoke8/Jts")
        if tws_dir.exists():
            logger.info(f"[{MODULE}] Scanning explicit TWS directory: {tws_dir}")
            for ext in ["*.csv", "*.json", "*.log"]:
                for file in tws_dir.rglob(ext):
                    logger.info(f"[{MODULE}] Found TWS file in Jts: {file}")
                    candidates.append(file)
        for pattern in search_patterns:
            try:
                matches = list(home.glob(pattern))
                if matches:
                    logger.info(f"[{MODULE}] Found {len(matches)} files matching pattern: {pattern}")
                    for match in matches:
                        logger.debug(f"[{MODULE}] Found file: {match}")
                candidates += matches
            except Exception as pattern_error:
                logger.warning(f"[{MODULE}] Error with pattern {pattern}: {pattern_error}")

        # System-wide paths (common Linux installations)
        system_patterns = [
            "/opt/tws*/logs/*.json",
            "/opt/TWS*/data/*.csv",
            "/opt/InteractiveBrokers*/reports/*.csv",
            "/usr/local/tws*/logs/*.json",
            "/var/log/**/ib*.log",
            "/var/log/**/tws*.log",
            "/tmp/tws*.json",
            "/tmp/TWS*.csv",
            "/tmp/IBKR*.json",
        ]
        
        for pattern in system_patterns:
            try:
                matches = list(Path("/").glob(pattern.lstrip("/")))
                if matches:
                    logger.info(f"[{MODULE}] Found {len(matches)} system files matching pattern: {pattern}")
                candidates += matches
            except Exception as sys_error:
                logger.warning(f"[{MODULE}] Error with system pattern {pattern}: {sys_error}")

        # Look for running TWS processes and their working directories
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cwd']):
                try:
                    if proc.info['name'] and 'tws' in proc.info['name'].lower():
                        cwd = proc.info['cwd']
                        if cwd:
                            logger.info(f"[{MODULE}] Found TWS process: {proc.info['name']} in {cwd}")
                            # Look for data files in the process working directory
                            cwd_path = Path(cwd)
                            for data_file in cwd_path.rglob("*.csv"):
                                candidates.append(data_file)
                            for data_file in cwd_path.rglob("*.json"):
                                candidates.append(data_file)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except ImportError:
            logger.warning(f"[{MODULE}] psutil not available, skipping process detection")

        # Remove duplicates and filter existing files
        unique_candidates = []
        seen = set()
        for candidate in candidates:
            if candidate.exists() and candidate not in seen:
                unique_candidates.append(candidate)
                seen.add(candidate)
        
        logger.info(f"[{MODULE}] Total candidates found: {len(unique_candidates)}")
        for candidate in unique_candidates:
            logger.info(f"[{MODULE}] Candidate file: {candidate} (size: {candidate.stat().st_size} bytes)")
        
        return unique_candidates
        
    except Exception as e:
        logger.error(f"[{MODULE}] File scan failed: {e}")
        return []


def try_parse_file(file_path):
    try:
        with open(file_path, "r") as f:
            raw = f.read()

            if file_path.suffix == ".json":
                data = json.loads(raw)
                return parse_tws_json(data)

            elif file_path.suffix == ".csv":
                lines = raw.splitlines()
                if len(lines) > 1:
                    values = lines[1].split(",")
                    return [
                        {
                            "symbol": values[0],
                            "price": float(values[1]),
                            "volume": int(values[2]),
                            "ema": float(values[3]),
                            "vwap": float(values[4]),
                            "timestamp": datetime.utcnow().isoformat(),
                        }
                    ]
    except Exception as e:
        logger.warning(f"[{MODULE}] Could not parse {file_path}: {e}")
    return []


def parse_tws_json(data):
    try:
        if isinstance(data, dict):
            return [
                {
                    "symbol": data.get("symbol", "TWS"),
                    "price": data.get("price", 1.0),
                    "volume": data.get("volume", 100000),
                    "ema": data.get("ema", 1.0),
                    "vwap": data.get("vwap", 1.0),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ]
        elif isinstance(data, list) and data:
            return [parse_tws_json(data[0])[0]]
    except Exception as e:
        logger.warning(f"[{MODULE}] JSON parsing error: {e}")
    return []


def safe_scrape_tws():
    try:
        files = locate_tws_files()
        logger.debug(f"[{MODULE}] Found {len(files)} candidate files.")

        for file in files:
            result = try_parse_file(file)
            if result:
                logger.success(f"[{MODULE}] Parsed TWS data from: {file}")
                return result

        logger.info(f"[{MODULE}] No valid files found — using fallback simulation.")
        return [DEFAULT_SIMULATION]

    except Exception as e:
        logger.error(f"[{MODULE}] Scrape failed: {e}")
        return [DEFAULT_SIMULATION]


# CLI test mode
if __name__ == "__main__":
    print(safe_scrape_tws())
