#!/bin/zsh
sleep 20

# TWS Auto-login
xdotool search --name "Trader Workstation" windowactivate --sync   key Tab key Tab type '' key Tab   type '' key Return

# STT Auto-login
xdotool search --name "StocksToTrade" windowactivate --sync   key Tab type '' key Tab   type '' key Return
