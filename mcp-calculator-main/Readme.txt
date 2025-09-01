步驟一:
在資料匣上方(位址)輸入cmd

步驟二:
貼入:
set MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQxMTE1OSwiYWdlbnRJZCI6NTAxNzc3LCJlbmRwb2ludElkIjoiYWdlbnRfNTAxNzc3IiwicHVycG9zZSI6Im1jcC1lbmRwb2ludCIsImlhdCI6MTc1NjcyMjg3OX0.LmIa8kcYUDudXE3-4Tx3TvwD2eTdl6zV1u0G9J5yopO3NC2lMpOKYka_oBwlwsc6Vv5Wb3cwgXv7600nuWCNyA
步驟三:
貼入:
python mcp_pipe.py calculator.py

看到:
Processing request of type ListToolsRequest
表示完成,程式等待指令。

如出現錯誤(AI亂回答/程式出現error):
按Ctrl+C > 取消程式後
按上鍵重新跑步驟三



Home Assitance token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2MmFmMDY4ZmQ3ZWM0YzZlODY3NzJhODQ4Zjc4ZWVhNSIsImlhdCI6MTc1NjcyNDMwMSwiZXhwIjoyMDcyMDg0MzAxfQ.0p4AkrDeKnA3x2Qwm0Ib8gE0m2GwHF_Lwglp01yjS0s
