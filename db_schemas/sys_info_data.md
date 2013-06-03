| Field       | Type        | Null | Key | Default | Extra |
|-------------|-------------|------|-----|---------|-------|
| cpu_usage   | int(11)     | YES  |     | NULL    |       |
| mem_free    | int(11)     | YES  |     | NULL    |       |
| disk_free   | int(11)     | YES  |     | NULL    |       |
| client_time | int(11)     | NO   | PRI | 0       |       |
| client_type | varchar(20) | YES  |     | NULL    |       |
| client_id   | int(11)     | NO   | PRI | 0       |       |
| server_time | int(11)     | YES  |     | NULL    |       |
| avg_ping    | int(11)     | YES  |     | NULL    |       |
| packet_loss | int(11)     | YES  |     | NULL    |       |

