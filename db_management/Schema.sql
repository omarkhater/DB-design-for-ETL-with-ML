DROP TABLE IF EXISTS DatasetToTraining, ETLScriptToTraining, EngineerModel, DatasetModel, Training, ETLParameters, ETLScript, Model, Metrics2, Metrics1, Customers, Engineer, Dataset CASCADE;
CREATE TABLE IF NOT EXISTS Engineer(
    EngineerID INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Email VARCHAR(255),
    Phone VARCHAR(255),
    Role VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Customers(
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(255),
    Contact VARCHAR(255),
    Priority INT
);

CREATE TABLE IF NOT EXISTS ETLScript (
    ScriptName VARCHAR(255),
    ScriptVersion VARCHAR(255),
    Description TEXT,
    PRIMARY KEY (ScriptName, ScriptVersion)
);
CREATE TABLE IF NOT EXISTS Dataset (
    DatasetID INT PRIMARY KEY,
    Material VARCHAR(255), 
    CollectionDate DATE,
    DataDescription TEXT
);


CREATE TABLE IF NOT EXISTS Model (
    ModelID SERIAL PRIMARY KEY,
    DatasetID INT,
    EngineerID INT,
    CustomerID INT,
    Description TEXT,
    FOREIGN KEY (DatasetID) REFERENCES Dataset(DatasetID),
    FOREIGN KEY (EngineerID) REFERENCES Engineer(EngineerID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE IF NOT EXISTS Metrics1 (
    MetricID INT PRIMARY KEY,
    ModelID INT,
    MetricName VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Metrics2 (
    ModelID INT,
    MetricName VARCHAR(255),
    MetricValue FLOAT
);


CREATE TABLE IF NOT EXISTS ETLParameters (
    ParameterID INT,
    ParameterName VARCHAR(255),
    ScriptName VARCHAR(255),
    ScriptVersion VARCHAR(255),
    ParameterValue VARCHAR(255),
    PRIMARY KEY (ParameterID, ParameterName),
    FOREIGN KEY (ScriptName, ScriptVersion) REFERENCES ETLScript(ScriptName, ScriptVersion)
);

CREATE TABLE IF NOT EXISTS Training (
    TrainingID INT PRIMARY KEY,
    ModelID INT,
    X_Preprocessing TEXT,
    Y_preprocessing TEXT,
    Algorithm VARCHAR(255),
    FOREIGN KEY (ModelID) REFERENCES Model(ModelID)
);

CREATE TABLE IF NOT EXISTS DatasetModel (
    DatasetID INT,
    ModelID INT,
    PRIMARY KEY (DatasetID, ModelID),
    FOREIGN KEY (DatasetID) REFERENCES Dataset(DatasetID),
    FOREIGN KEY (ModelID) REFERENCES Model(ModelID)
);

CREATE TABLE IF NOT EXISTS EngineerModel (
    EngineerID INT,
    ModelID INT,
    PRIMARY KEY (EngineerID, ModelID),
    FOREIGN KEY (EngineerID) REFERENCES Engineer(EngineerID),
    FOREIGN KEY (ModelID) REFERENCES Model(ModelID)
);

CREATE TABLE IF NOT EXISTS ETLScriptToTraining (
    ScriptName VARCHAR(255),
    ScriptVersion VARCHAR(255),
    TrainingID INT,
    PRIMARY KEY (ScriptName, ScriptVersion, TrainingID),
    FOREIGN KEY (ScriptName, ScriptVersion) REFERENCES ETLScript(ScriptName, ScriptVersion),
    FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID)
);

CREATE TABLE IF NOT EXISTS DatasetToTraining (
    DatasetID INT,
    TrainingID INT,
    PRIMARY KEY (DatasetID, TrainingID),
    FOREIGN KEY (DatasetID) REFERENCES Dataset(DatasetID),
    FOREIGN KEY (TrainingID) REFERENCES Training(TrainingID)
);

