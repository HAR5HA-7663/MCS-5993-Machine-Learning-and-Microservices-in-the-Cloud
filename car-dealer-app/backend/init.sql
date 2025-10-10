-- Initialize the car dealership database
-- This script runs automatically when the PostgreSQL container starts

-- Create the cars table with proper indexes
CREATE TABLE IF NOT EXISTS cars (
    vin VARCHAR(20) PRIMARY KEY,
    year INTEGER NOT NULL CHECK (year >= 1900 AND year <= 2030),
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    mileage INTEGER NOT NULL CHECK (mileage >= 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_cars_brand ON cars(brand);
CREATE INDEX IF NOT EXISTS idx_cars_model ON cars(model);
CREATE INDEX IF NOT EXISTS idx_cars_year ON cars(year);
CREATE INDEX IF NOT EXISTS idx_cars_price ON cars(price);
CREATE INDEX IF NOT EXISTS idx_cars_mileage ON cars(mileage);
CREATE INDEX IF NOT EXISTS idx_cars_added_at ON cars(added_at);

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_cars_updated_at ON cars;
CREATE TRIGGER update_cars_updated_at
    BEFORE UPDATE ON cars
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Create views for analytics
CREATE OR REPLACE VIEW car_analytics AS
SELECT 
    COUNT(*) as total_cars,
    AVG(price) as average_price,
    AVG(mileage) as average_mileage,
    MIN(year) as oldest_year,
    MAX(year) as newest_year,
    COUNT(DISTINCT brand) as unique_brands,
    COUNT(DISTINCT model) as unique_models
FROM cars;

CREATE OR REPLACE VIEW brand_summary AS
SELECT 
    brand,
    COUNT(*) as car_count,
    AVG(price)::DECIMAL(10,2) as avg_price,
    AVG(mileage)::INTEGER as avg_mileage,
    MIN(year) as oldest_year,
    MAX(year) as newest_year
FROM cars 
GROUP BY brand 
ORDER BY car_count DESC;

CREATE OR REPLACE VIEW year_summary AS
SELECT 
    year,
    COUNT(*) as car_count,
    AVG(price)::DECIMAL(10,2) as avg_price,
    AVG(mileage)::INTEGER as avg_mileage,
    string_agg(DISTINCT brand, ', ' ORDER BY brand) as brands
FROM cars 
GROUP BY year 
ORDER BY year DESC;

-- Grant permissions (if needed)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO caruser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO caruser;

-- Log initialization completion
DO $$
BEGIN
    RAISE NOTICE 'Car dealership database initialized successfully!';
    RAISE NOTICE 'Tables created: cars';
    RAISE NOTICE 'Views created: car_analytics, brand_summary, year_summary';
    RAISE NOTICE 'Indexes and triggers configured for optimal performance';
END $$;