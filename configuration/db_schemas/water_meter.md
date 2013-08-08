###water_meter_data

| Field     | Type    | Null | Key | Default | Extra |
|-----------|---------|------|-----|---------|-------|
| meter_id  | int(11) | NO   | PRI | 0       |       |
| timestamp | decimal(14,2) | NO   | PRI | 0       |       |
| event   | int(11) | NO   |  | 0       |       |

### MySQL Commands

    create table water_meter_data (meter_id INT, timestamp decimal(14,2), event INT, primary key (timestamp, meter_id));
