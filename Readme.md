```
CREATE TABLE main_table (
  id INT PRIMARY KEY,
  cn VARCHAR(255),
  qq VARCHAR(255),
  UNIQUE KEY unique_cn_qq (cn, qq)
);

```

```
CREATE TABLE content_table (
  id INT PRIMARY KEY,
  main_id INT,
  key_name VARCHAR(255),
  value VARCHAR(255),
  FOREIGN KEY (main_id) REFERENCES main_table(id)
);
```

```
SELECT key_name, value
FROM content_table
INNER JOIN main_table ON content_table.main_id = main_table.id
WHERE main_table.qq = '2185229059';
```