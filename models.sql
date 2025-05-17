-- 创建用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    hashed_password VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    recently_used_styles JSON  -- 修改字段名以反映最近使用的styles
);

-- 创建风格分类表
CREATE TABLE style_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_style_category_name (name)
);

-- 创建风格表
CREATE TABLE styles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    description TEXT,
    prompt_template TEXT NOT NULL,
    preview_image VARCHAR(256),
    category_id INT, -- Changed to category_id
    is_popular BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_category_id (category_id),
    FOREIGN KEY (category_id) REFERENCES style_categories(id) -- Foreign key to style_categories
);

-- 创建任务表
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    style_id INT NOT NULL,
    input_image VARCHAR(256) NOT NULL,
    output_image VARCHAR(256),
    custom_prompt TEXT,
    status VARCHAR(32) NOT NULL,
    progress FLOAT DEFAULT 0.0,
    error TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    INDEX idx_user_id (user_id),
    INDEX idx_style_id (style_id),
    INDEX idx_status (status),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (style_id) REFERENCES styles(id)
);

-- 创建积分表
CREATE TABLE credits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount INT DEFAULT 0,
    is_vip BOOLEAN DEFAULT FALSE,
    last_vip_credit_date DATETIME,
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);