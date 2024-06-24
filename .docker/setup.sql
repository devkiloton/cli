CREATE DATABASE IF NOT EXISTS broken_db;

USE broken_db;

-- Create the tables
CREATE TABLE feeds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE instagram_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fan_count INT NOT NULL,
    feed_id INT,
    FOREIGN KEY (feed_id) REFERENCES feeds(id)
);

CREATE TABLE tiktok_sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fan_count INT NOT NULL,
    feed_id INT,
    FOREIGN KEY (feed_id) REFERENCES feeds(id)
);

CREATE TABLE posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    feed_id INT,
    FOREIGN KEY (feed_id) REFERENCES feeds(id)
);

-- Insert data into feeds table
INSERT INTO feeds (name) VALUES ('Influencer A');
INSERT INTO feeds (name) VALUES ('Influencer B');
INSERT INTO feeds (name) VALUES ('Influencer C');

-- Insert data into instagram_sources table
INSERT INTO instagram_sources (name, fan_count, feed_id) VALUES ('insta_a', 1000, 1);
INSERT INTO instagram_sources (name, fan_count, feed_id) VALUES ('insta_b', 2000, 2);

-- Insert data into tiktok_sources table
INSERT INTO tiktok_sources (name, fan_count, feed_id) VALUES ('tiktok_a', 1500, 1);
INSERT INTO tiktok_sources (name, fan_count, feed_id) VALUES ('tiktok_b', 2500, 3);

-- Insert data into posts table
INSERT INTO posts (url, feed_id) VALUES ('http://example.com/post1', 1);
INSERT INTO posts (url, feed_id) VALUES ('http://example.com/post2', 1);
INSERT INTO posts (url, feed_id) VALUES ('http://example.com/post3', 2);
INSERT INTO posts (url, feed_id) VALUES ('http://example.com/post4', 3);
INSERT INTO posts (url, feed_id) VALUES ('http://example.com/post5', 3);
