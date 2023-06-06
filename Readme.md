```
CREATE TABLE IF NOT EXISTS personInfo (
  person_id INT PRIMARY KEY,
  cn VARCHAR(255),
  qq VARCHAR(255),
  UNIQUE KEY unique_cn_qq (cn, qq)
);

```

```
CREATE TABLE IF NOT EXISTS cardInfo (
  card_id INT PRIMARY KEY,
  card_name VARCHAR(255),
  card_character VARCHAR(255),
  card_type VARCHAR(255),
  card_condition VARCHAR(255),
  other VARCHAR(255)
)
```

```
CREATE TABLE IF NOT EXISTS cardIndex (
  person_id INT,
  card_ids VARCHAR(1024),
  FOREIGN KEY (person_id) REFERENCES personInfo(person_id)
)
```

```
CREATE TABLE cardNo{} (
  person_id INT,
  card_name VARCHAR(255),
  card_num INT,
  FOREIGN KEY (person_id) REFERENCES personInfo(person_id)
);
```