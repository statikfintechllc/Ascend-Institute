#!/bin/zsh
# Launch all GremlinGPT bridge daemons at once
echo '[+] Spawning all GremlinGPT bridges...'
echo '[+] ai-core on port 5101'
conda run -n ai-core nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5101.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5101.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5101_err.log &
echo '[+] starcoder-wrapper on port 5102'
conda run -n starcoder-wrapper nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5102.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5102.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5102_err.log &
echo '[+] nanogpt-wrapper on port 5103'
conda run -n nanogpt-wrapper nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5103.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5103.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5103_err.log &
echo '[+] ai-agents on port 5104'
conda run -n ai-agents nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5104.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5104.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5104_err.log &
echo '[+] vector-db on port 5105'
conda run -n vector-db nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5105.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5105.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5105_err.log &
echo '[+] dashboard-ui on port 5106'
conda run -n dashboard-ui nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5106.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5106.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5106_err.log &
echo '[+] quantum-research on port 5107'
conda run -n quantum-research nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5107.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5107.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5107_err.log &
echo '[+] finops on port 5108'
conda run -n finops nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5108.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5108.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5108_err.log &
echo '[+] stealth-core on port 5109'
conda run -n stealth-core nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5109.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5109.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5109_err.log &
echo '[+] surveillance-stack on port 5110'
conda run -n surveillance-stack nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5110.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5110.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5110_err.log &
echo '[+] ml-ops-deploy on port 5111'
conda run -n ml-ops-deploy nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5111.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5111.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5111_err.log &
echo '[+] netsec-tools on port 5112'
conda run -n netsec-tools nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5112.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5112.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5112_err.log &
echo '[+] telemetry-ops on port 5113'
conda run -n telemetry-ops nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5113.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5113.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5113_err.log &
echo '[+] intel-recon on port 5114'
conda run -n intel-recon nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5114.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5114.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5114_err.log &
echo '[+] darknet-interface on port 5115'
conda run -n darknet-interface nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5115.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5115.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5115_err.log &
echo '[+] ai-eval on port 5116'
conda run -n ai-eval nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5116.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5116.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5116_err.log &
echo '[+] code-fuzz on port 5117'
conda run -n code-fuzz nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5117.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5117.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5117_err.log &
echo '[+] base-dev on port 5118'
conda run -n base-dev nohup python $HOME/AscendNet/GremlinGPT/Networking/bridge_runner_5118.py > $HOME/AscendNet/GremlinGPT/Logs/bridge_5118.log 2> $HOME/AscendNet/GremlinGPT/Logs/bridge_5118_err.log &
echo '[✓] All bridge daemons launched.'
