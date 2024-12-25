CREATE TABLE Users ( 
    user_id SERIAL PRIMARY KEY,         -- Auto-incrementing ID for each user
    full_name VARCHAR(100) NOT NULL,    -- Full name with a reasonable length limit
    email VARCHAR(150) UNIQUE NOT NULL, -- Email must be unique and non-null
    password TEXT NOT NULL,             -- Password stored as a hashed string
    score INT DEFAULT 0                 -- Score initialized to 0 by default
);

CREATE TABLE UploadedFiles (
    file_id SERIAL PRIMARY KEY,         -- Auto-incrementing ID for each file
    field VARCHAR(50) NOT NULL,         -- Field of study or category
    module VARCHAR(100) NOT NULL,       -- Module or subject related to the file
    user_id INT NOT NULL,               -- Foreign key referencing the uploader
    file_name VARCHAR(255) NOT NULL,    -- Name of the file
    description TEXT,                   -- Optional description of the file
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date of upload
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);
