###PIR

| Field     | Type    | Null | Key | Default | Extra |
|-----------|---------|------|-----|---------|-------|
| timestamp | int(11) | NO   | PRI | 0       |       |
| node_id   | int(11) | NO   | PRI | 0       |       |

###Light_temp

| Field     | Type    | Null | Key | Default | Extra |
|-----------|---------|------|-----|---------|-------|
| timestamp | int(11) | NO   | PRI | 0       |       |
| node_id   | int(11) | NO   | PRI | 0       |       |
| light     | int(11) | YES  |     | NULL    |       |
| temp      | int(11) | YES  |     | NULL    |       |

### MySQL Commands

    create table light_temp (timestamp INT, node_id INT, light INT, temp INT, primary key (timestamp, node_id));

    create table pir (timestamp INT, node_id INT ,primary key (timestamp, node_id));

