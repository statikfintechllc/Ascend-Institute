import json
import os
import uuid
from datetime import datetime

SIM_LOG = "./logs/simulated_trades.json"
REAL_QUEUE = "./dashboard/trade_queue/"
MERGE_LOG = "./logs/phantom_merge.log"
THRESHOLD_PROFIT = 0.015  # 1.5% minimum gain before real trade is proposed


def load_sim_trades():
    if not os.path.exists(SIM_LOG):
        return []
    with open(SIM_LOG, "r") as f:
        return json.load(f)


def evaluate_trades():
    proposals = []
    trades = load_sim_trades()
    for trade in trades:
        if trade.get("status") == "closed":
            entry = trade["entry_price"]
            exit_ = trade["exit_price"]
            gain = (exit_ - entry) / entry
            if gain >= THRESHOLD_PROFIT:
                proposals.append(
                    {
                        "uuid": str(uuid.uuid4()),
                        "symbol": trade["symbol"],
                        "entry": entry,
                        "exit": exit_,
                        "gain": round(gain, 4),
                        "reason": trade.get("strategy"),
                        "timestamp": datetime.utcnow().isoformat(),
                        "status": "pending_real_execution",
                    }
                )
    return proposals


def queue_trades(proposals):
    for trade in proposals:
        out_file = os.path.join(REAL_QUEUE, f"{trade['uuid']}.json")
        with open(out_file, "w") as f:
            json.dump(trade, f, indent=4)
        with open(MERGE_LOG, "a") as log:
            log.write(
                f"[{trade['timestamp']}] Queued for merge: {trade['symbol']} at {trade['gain'] * 100}%\n"
            )


if __name__ == "__main__":
    print("[MERGE] Evaluating paper trades...")
    proposals = evaluate_trades()
    queue_trades(proposals)
