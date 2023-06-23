%flink.ssql

CREATE TABLE `user_data` (
  `name` STRING,
  `address` STRING,
  `email` STRING
)
WITH (
  'connector' = 'kinesis',
  'stream' = 'Stream-97c9a098',
  'aws.region' = 'us-east-1', 
  'scan.stream.initpos' = 'LATEST',
  'format' = 'json' 
);

-- Flink Stream Data Update
%flink.ssql(type=update)
SELECT * FROM user_data;


-- Flink Stream Data Append
%flink.ssql(type=append)
SELECT * FROM user_data;

-- Flink to count
%flink.ssql(type=update)
SELECT COUNT(*) FROM user_data;
